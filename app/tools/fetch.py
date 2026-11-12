import re
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/130.0 Safari/537.36"
    ),
    "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
}

CAREER_HINTS = re.compile(r"karriere|career|jobs|stellen|join-us|arbeiten-bei|work-with-us", re.I)
ABOUT_HINTS = re.compile(r"ueber-uns|uber-uns|über uns|about|unternehmen|company|wir-sind", re.I)
POSTING_URL = re.compile(r"/job/|/jobs/\d|/stellenangebot|/position/|/vacanc|/o/|personio\.(de|com)/job|join\.com/companies/.+/\d", re.I)
POSTING_TITLE = re.compile(r"\((m/w/d|w/m/d|m/f/d|f/m/d|all genders?|d/m/w)\)|\bm/w/d\b", re.I)
SKIP_LINK = re.compile(r"initiativ|locale=|login|anmelden|cookie|alert|newsletter|datenschutz|privacy|impressum", re.I)


@retry(
    stop=stop_after_attempt(2),
    wait=wait_exponential(min=1, max=4),
    retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError)),
    reraise=True,
)
def get_html(url: str) -> tuple[str, str]:
    with httpx.Client(headers=HEADERS, timeout=10, follow_redirects=True) as client:
        response = client.get(url)
        response.raise_for_status()
        return str(response.url), response.text


def page_text(html: str, limit: int = 6000) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg", "iframe"]):
        tag.decompose()
    text = re.sub(r"\s+", " ", soup.get_text(" ")).strip()
    return text[:limit]


def page_title(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    return soup.title.get_text(strip=True) if soup.title else ""


def links(html: str, base_url: str) -> list[tuple[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    found = []
    for a in soup.find_all("a", href=True):
        href = urljoin(base_url, a["href"]).split("#")[0]
        if href.startswith("http"):
            found.append((a.get_text(" ", strip=True), href))
    return found


def find_link(html: str, base_url: str, pattern: re.Pattern) -> str | None:
    for label, href in links(html, base_url):
        if SKIP_LINK.search(href):
            continue
        if pattern.search(urlparse(href).path) or pattern.search(label):
            return href
    return None


def _is_posting(label: str, href: str) -> bool:
    return bool(POSTING_URL.search(href) or POSTING_TITLE.search(label))


def collect_job_links(career_html: str, career_url: str, limit: int = 5, max_listing_pages: int = 3) -> list[tuple[str, str]]:
    """Job posting links from a career page, following up to a few listing sub-pages."""
    postings: dict[str, str] = {}
    listing_pages: list[str] = []
    site_host = urlparse(career_url).netloc.removeprefix("www.").split(".")[-2]

    def scan(html: str, base: str, allow_listings: bool) -> None:
        for label, href in links(html, base):
            if SKIP_LINK.search(href) or SKIP_LINK.search(label) or href.rstrip("/") == base.rstrip("/"):
                continue
            if _is_posting(label, href):
                postings.setdefault(href, label)
            elif allow_listings and CAREER_HINTS.search(href) and site_host in urlparse(href).netloc:
                if href not in listing_pages:
                    listing_pages.append(href)

    scan(career_html, career_url, allow_listings=True)
    for page in listing_pages[:max_listing_pages]:
        if len(postings) >= limit:
            break
        try:
            final_url, html = get_html(page)
            scan(html, final_url, allow_listings=False)
        except httpx.HTTPError:
            continue
    return [(label, href) for href, label in list(postings.items())[:limit]]
