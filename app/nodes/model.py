from app.config import llm
from app.state import BusinessModel, RunState

SYSTEM = """You are a senior operations and AI consultant preparing a first meeting with a company.
From public research only, describe how the company works and how it makes money.

Status rules, applied to every claim and every process step:
- "belegt": directly supported by the research below. Evidence is the exact source URL.
- "abgeleitet": what companies of this kind usually do. Evidence is "typical industry knowledge".
Never mark something "belegt" without a URL from the research. When in doubt, use "abgeleitet".

Business model: who pays, for what, through which channels.
Unit economics: name the unit that earns money (a product sold, an order, a project, a contract)
and what drives its margin: price, volume, cost per unit, risk. Use numbers only when a source states them.
List the numbers that would matter but were not found under open_numbers.

Process map: as many operational steps as the business really has, usually 6 to 12.
Concrete steps, not department names ("Dealer places reorder via B2B portal", not "Sales").
Each step has a data input, a data output, and the system it most likely runs in.
Job postings are strong evidence for which steps and systems exist.
Write in English."""


def _research_digest(state: RunState) -> str:
    parts = [f"Company: {state.company_name} ({state.company_url})", state.site_text or "(website not readable)"]
    if state.job_postings:
        parts.append("Job postings:")
        parts += [f"- {j.title} ({j.url})\n  {j.text[:1500]}" for j in state.job_postings]
    if state.news:
        parts.append("News:")
        parts += [f"- {n.title} ({n.url}): {n.snippet}" for n in state.news]
    if state.register_hits:
        parts.append("Register and size snippets:")
        parts += [f"- {r.title} ({r.url}): {r.snippet}" for r in state.register_hits]
    return "\n".join(parts)


def model_business(state: RunState) -> dict:
    result = llm().with_structured_output(BusinessModel).invoke(
        [("system", SYSTEM), ("human", _research_digest(state))]
    )
    return {"model": result}
