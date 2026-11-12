import re

from app.config import llm
from app.state import BusinessModel, RunState

INDUSTRY = "typical industry knowledge"
AGGREGATORS = re.compile(r"leadiq|tracxn|zoominfo|crunchbase|rocketreach|apollo\.io|dnb\.com|growjo|tavily\.com", re.I)

SYSTEM = """You are a senior operations and AI consultant preparing a first meeting with a company.
From the numbered public sources below, describe how the company works and how it makes money.

Evidence rules, applied to every claim and every process step:
- "belegt": the sources state or clearly show it. evidence is the source id, e.g. "S3".
- "abgeleitet": what companies of this kind usually do. evidence is "industry".
Prefer "belegt" whenever a source supports the claim, even partially. Never invent a source id.
Do not contradict the sources. If a source shows sales through dealers, do not claim direct sales unless a source shows it.
Sources marked [estimate] come from data aggregators. Quote their figures only as estimates, e.g. "around 300 employees (aggregator estimate)".
Use the news: market exits, new plants, product launches, and restructuring change the business model and priorities.

Business model: who pays, for what, through which channels, in which markets.
Unit economics: name the unit that earns money and what drives its margin: price, volume, cost per unit, risk.
Use numbers only when a source states them. List the numbers that matter but were not found under open_numbers.

Process map: the operational value chain, as many steps as the business really has (usually 8 to 12), one line each.
Cover the whole chain where it applies: product development, procurement, production or service delivery,
sales and channel management, order handling, logistics, after-sales and warranty, marketing, and support functions.
Concrete steps, not department names: "Dealer places reorder via B2B portal", not "Sales".
Each step has a data input, a data output, and the system it most likely runs in.
For every step, go through the sources and check whether one shows that this step exists at this company.
A job posting for a warehouse, assembly, marketing, or service role proves the matching step. A website statement
such as "we assemble in Germany" proves production. In those cases the step is "belegt" with that source id.
Only steps that no source mentions are "abgeleitet".
Write in English."""


def _sources(state: RunState) -> list[tuple[str, str, str, str]]:
    """(id, url, label, text) for every piece of research, in a stable order."""
    items = []
    for page in state.site_pages:
        items.append((page.url, f"Company website: {page.title}", page.snippet))
    for job in state.job_postings:
        items.append((job.url, f"Job posting: {job.title}", job.text[:1500]))
    for hit in state.news:
        items.append((hit.url, f"News: {hit.title}", hit.snippet))
    for hit in state.register_hits:
        label = f"Register or company profile: {hit.title}"
        if AGGREGATORS.search(hit.url):
            label += " [estimate]"
        items.append((hit.url, label, hit.snippet))
    return [(f"S{i}", url, label, text) for i, (url, label, text) in enumerate(items, start=1)]


def _digest(state: RunState, sources: list[tuple[str, str, str, str]]) -> str:
    lines = [f"Company: {state.company_name} ({state.company_url})", ""]
    for sid, url, label, text in sources:
        lines.append(f"[{sid}] {label} ({url})\n{text}\n")
    return "\n".join(lines)


def _resolve(item, urls: dict[str, str]) -> None:
    """Replace source ids with URLs. Anything 'belegt' without a valid id is downgraded."""
    ids = [i for i in re.findall(r"S\d+", item.evidence) if i in urls]
    if item.status == "belegt" and ids:
        item.evidence = urls[ids[0]]
    else:
        item.status = "abgeleitet"
        item.evidence = INDUSTRY


def model_business(state: RunState) -> dict:
    sources = _sources(state)
    if not sources:
        return {"notes": state.notes + ["No research material, so the business could not be modeled."]}
    try:
        result = llm().with_structured_output(BusinessModel).invoke(
            [("system", SYSTEM), ("human", _digest(state, sources))]
        )
    except Exception as exc:
        return {"notes": state.notes + [f"Business modeling failed ({exc.__class__.__name__}: {exc})."]}

    urls = {sid: url for sid, url, _, _ in sources}
    for item in [*result.business_model, *result.unit_economics, *result.process_map]:
        _resolve(item, urls)
    return {"model": result}
