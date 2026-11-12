import os
import re
import unicodedata

from tavily import TavilyClient

from app.state import Source

LEGAL_FORMS = {"gmbh", "ag", "kg", "co", "se", "ug", "mbh", "inc", "ltd", "llc", "gbr", "ohg", "e.k", "und", "and"}

REGISTER_DOMAINS = [
    "unternehmensregister.de",
    "bundesanzeiger.de",
    "handelsregister.de",
    "northdata.de",
    "northdata.com",
    "de.wikipedia.org",
    "en.wikipedia.org",
]


def _client() -> TavilyClient:
    return TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


def _fold(text: str) -> str:
    text = text.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()


def _name_tokens(company: str) -> list[str]:
    words = re.findall(r"[\w.]+", _fold(company))
    return [w for w in words if len(w) > 1 and w not in LEGAL_FORMS]


def _mentions(company: str, source: Source) -> bool:
    haystack = _fold(f"{source.title} {source.url} {source.snippet}")
    haystack_loose = haystack.replace("ue", "u").replace("ae", "a").replace("oe", "o")
    tokens = _name_tokens(company)
    return all(t in haystack or t.replace("ue", "u").replace("ae", "a").replace("oe", "o") in haystack_loose for t in tokens)


def _search(company: str, query: str, max_results: int, **kwargs) -> list[Source]:
    response = _client().search(query, max_results=max_results, **kwargs)
    hits = [
        Source(title=r.get("title", ""), url=r.get("url", ""), snippet=(r.get("content") or "")[:600])
        for r in response.get("results", [])
    ]
    return [h for h in hits if _mentions(company, h)]


def search_news(company: str, max_results: int = 6) -> list[Source]:
    return _search(company, f'"{company}"', max_results, topic="news", days=365)


def search_jobs(company: str, max_results: int = 5) -> list[Source]:
    return _search(company, f'"{company}" Stellenangebot OR Stellenanzeige OR job (m/w/d)', max_results)


def search_register(company: str, max_results: int = 5) -> list[Source]:
    hits = _search(company, f"{company} Mitarbeiter Umsatz Gründung Sitz", max_results, include_domains=REGISTER_DOMAINS)
    if not hits:
        hits = _search(company, f'"{company}" employees revenue founded headquarters', max_results)
    return hits
