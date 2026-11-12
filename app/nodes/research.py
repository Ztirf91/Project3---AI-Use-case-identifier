import httpx

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


def read_site(state: RunState) -> dict:
    notes = list(state.notes)
    pages: list[Source] = []
    texts: list[str] = []
    jobs: list[JobPosting] = []

    try:
        home_url, home_html = get_html(state.company_url)
    except httpx.HTTPError as exc:
        notes.append(f"Homepage could not be read ({exc.__class__.__name__}). Research relies on search only.")
        return {"notes": notes}

    pages.append(Source(title=page_title(home_html) or "Homepage", url=home_url))
    texts.append(f"[Homepage {home_url}]\n{page_text(home_html, 5000)}")

    about_url = find_link(home_html, home_url, ABOUT_HINTS)
    if about_url:
        try:
            final_url, html = get_html(about_url)
            pages.append(Source(title=page_title(html) or "About", url=final_url))
            texts.append(f"[About page {final_url}]\n{page_text(html, 4000)}")
        except httpx.HTTPError:
            notes.append(f"About page {about_url} could not be read.")

    career_url = find_link(home_html, home_url, CAREER_HINTS)
    if career_url:
        try:
            final_url, career_html = get_html(career_url)
            pages.append(Source(title=page_title(career_html) or "Careers", url=final_url))
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

    return {"site_text": "\n\n".join(texts), "site_pages": pages, "job_postings": jobs, "notes": notes}


def search_news_register(state: RunState) -> dict:
    notes = list(state.notes)
    news: list[Source] = []
    register: list[Source] = []
    jobs = list(state.job_postings)

    try:
        news = search.search_news(state.company_name)
    except Exception as exc:
        notes.append(f"News search failed ({exc.__class__.__name__}).")
    try:
        register = search.search_register(state.company_name)
    except Exception as exc:
        notes.append(f"Register search failed ({exc.__class__.__name__}).")
    if not jobs:
        try:
            for hit in search.search_jobs(state.company_name):
                jobs.append(JobPosting(title=hit.title, url=hit.url, text=hit.snippet))
            if jobs:
                notes.append("Job postings come from web search, not from the company's own careers page.")
        except Exception as exc:
            notes.append(f"Job search failed ({exc.__class__.__name__}).")

    if not news:
        notes.append("No recent news found.")
    if not register:
        notes.append("No register or size information found.")
    return {"news": news, "register_hits": register, "job_postings": jobs, "notes": notes}
