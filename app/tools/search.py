import os

from tavily import TavilyClient

from app.state import Source


def _client() -> TavilyClient:
    return TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


def _to_sources(response: dict) -> list[Source]:
    return [
        Source(title=r.get("title", ""), url=r.get("url", ""), snippet=(r.get("content") or "")[:600])
        for r in response.get("results", [])
    ]


def search_news(company: str, max_results: int = 5) -> list[Source]:
    response = _client().search(f'"{company}"', topic="news", days=365, max_results=max_results)
    return _to_sources(response)


def search_jobs(company: str, max_results: int = 5) -> list[Source]:
    response = _client().search(f'"{company}" Stellenangebot OR Stellenanzeige OR job (m/w/d)', max_results=max_results)
    return _to_sources(response)


def search_register(company: str, max_results: int = 5) -> list[Source]:
    query = f'"{company}" Handelsregister OR Unternehmensregister OR Bundesanzeiger OR northdata Mitarbeiter Umsatz'
    response = _client().search(query, max_results=max_results)
    return _to_sources(response)
