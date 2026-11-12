import re

import httpx
from pydantic import BaseModel, Field

from app.config import llm
from app.state import JobPosting, RunState, Source
from app.tools import search
from app.tools.fetch import (
    ABOUT_HINTS,
    CAREER_HINTS,
    collect_job_links,
    find_link,
    get_html,
    page_text,
    page_title,
)

# Job posts must signal real operating work, not internships or pure recruiting fluff.
PROCESS_JOB = re.compile(
    r"erp|crm|wms|mes|plm|warehouse|lager|logistik|fulfillment|dealer|händler|order|"
    r"bestell|einkauf|purchas|production|fertigung|montage|assembl|qualität|quality|"
    r"customer.?service|kundenservice|support|warranty|garantie|after.?sales|"
    r"marketing|content|e-?commerce|shop|invoice|rechnung|dispatch|versand",
    re.I,
)
WEAK_JOB = re.compile(r"schüler|praktikum|internship|werkstudent|working student|aushilfe", re.I)
WEAK_SOURCE = re.compile(r"tavily\.com|wikipedia\.org|wiki/", re.I)
REGISTER_HOST = re.compile(
    r"unternehmensregister|northdata|handelsregister|companyhouse|companies.?house|"
    r"bundesanzeiger|creditreform|kompany|opencorporates",
    re.I,
)


def read_site(state: RunState) -> dict:
    notes = list(state.notes)
    pages: list[Source] = []
    jobs: list[JobPosting] = []

    try:
        home_url, home_html = get_html(state.company_url)
    except httpx.HTTPError as exc:
        notes.append(f"Homepage could not be read ({exc.__class__.__name__}). Research relies on search only.")
        return {"notes": notes}

    pages.append(Source(title=page_title(home_html) or "Homepage", url=home_url, snippet=page_text(home_html, 5000)))

    about_url = find_link(home_html, home_url, ABOUT_HINTS)
    if about_url:
        try:
            final_url, html = get_html(about_url)
            pages.append(Source(title=page_title(html) or "About", url=final_url, snippet=page_text(html, 5000)))
        except httpx.HTTPError:
            notes.append(f"About page {about_url} could not be read.")

    career_url = find_link(home_html, home_url, CAREER_HINTS)
    if career_url:
        try:
            final_url, career_html = get_html(career_url)
            pages.append(Source(title=page_title(career_html) or "Careers", url=final_url, snippet=page_text(career_html, 2000)))
            for label, href in collect_job_links(career_html, final_url):
                try:
                    _, job_html = get_html(href)
                    jobs.append(JobPosting(title=label, url=href, text=page_text(job_html, 2500)))
                except httpx.HTTPError:
                    jobs.append(JobPosting(title=label, url=href))
        except httpx.HTTPError:
            notes.append(f"Careers page {career_url} could not be read.")
    else:
        notes.append("No careers page linked from the homepage.")

    return {"site_pages": pages, "job_postings": jobs, "notes": notes}


class Relevant(BaseModel):
    keep: list[int] = Field(description="Numbers of the results that are about this exact company")


def _relevant(state: RunState, hits: list[Source]) -> list[Source]:
    """Drop search hits about a different company, product, or person with the same name."""
    if not hits:
        return hits
    company = f"{state.company_name}, website {state.company_url}"
    if state.site_pages:
        company += f', homepage title "{state.site_pages[0].title}"'
    listing = "\n".join(f"{i}. {h.title} ({h.url}): {h.snippet[:200]}" for i, h in enumerate(hits))
    try:
        result = llm(temperature=0).with_structured_output(Relevant).invoke(
            [
                ("system", "Return the numbers of the search results that are about this exact company. "
                 "Drop results about other companies, products, places, or people that share the name."),
                ("human", f"Company: {company}\n\nResults:\n{listing}"),
            ]
        )
    except Exception:
        return hits
    return [h for i, h in enumerate(hits) if i in set(result.keep)]


def _mentions_company(state: RunState, hit: Source) -> bool:
    text = f"{hit.title} {hit.snippet} {hit.url}".lower()
    tokens = [t for t in re.split(r"[^a-z0-9äöüß&]+", state.company_name.lower()) if len(t) > 2]
    return any(t in text for t in tokens) if tokens else state.company_name.lower() in text


def _process_job(job: JobPosting) -> bool:
    title = job.title or ""
    blob = f"{title} {job.text}"
    # Internships and student roles pollute the process map even when the page mentions a warehouse.
    if WEAK_JOB.search(title):
        return False
    return bool(PROCESS_JOB.search(blob))


def _clean_news(hits: list[Source]) -> list[Source]:
    return [h for h in hits if not WEAK_SOURCE.search(h.url)]


def _clean_register(state: RunState, hits: list[Source]) -> list[Source]:
    cleaned = []
    for hit in hits:
        if WEAK_SOURCE.search(hit.url):
            continue
        if not _mentions_company(state, hit):
            continue
        if not REGISTER_HOST.search(hit.url):
            # Keep non-register profiles only when they clearly name the company; label later in model.
            if "profile" not in hit.title.lower() and "gmbh" not in f"{hit.title} {hit.snippet}".lower():
                continue
        cleaned.append(hit)
    return cleaned


def search_news_register(state: RunState) -> dict:
    notes = list(state.notes)
    news: list[Source] = []
    register: list[Source] = []
    jobs = [j for j in state.job_postings if _process_job(j)]
    dropped_jobs = len(state.job_postings) - len(jobs)
    if dropped_jobs:
        notes.append(f"Dropped {dropped_jobs} job posting(s) without a clear process signal.")

    try:
        news = search.search_news(state.company_name)
    except Exception as exc:
        notes.append(f"News search failed ({exc.__class__.__name__}).")
    try:
        register = search.search_register(state.company_name)
    except Exception as exc:
        notes.append(f"Register search failed ({exc.__class__.__name__}).")
    job_hits: list[Source] = []
    if not jobs:
        try:
            job_hits = search.search_jobs(state.company_name)
        except Exception as exc:
            notes.append(f"Job search failed ({exc.__class__.__name__}).")

    kept = _relevant(state, news + register + job_hits)
    news = _clean_news([h for h in news if h in kept])
    register = _clean_register(state, [h for h in register if h in kept])
    for hit in job_hits:
        if hit in kept and not WEAK_SOURCE.search(hit.url):
            candidate = JobPosting(title=hit.title, url=hit.url, text=hit.snippet)
            if _process_job(candidate):
                jobs.append(candidate)
    if job_hits and jobs:
        notes.append("Job postings come from web search, not from the company's own careers page.")

    if not news:
        notes.append("No recent news found.")
    if not register:
        notes.append("No register or size information found.")
    return {"news": news, "register_hits": register, "job_postings": jobs, "notes": notes}
