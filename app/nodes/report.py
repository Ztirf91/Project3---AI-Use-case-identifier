import re
from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from app import library
from app.config import OUTPUTS_DIR
from app.state import RunState

TEMPLATES = Path(__file__).resolve().parent.parent / "templates"

LEVERS = {
    "volume": "more units sold",
    "price": "better price",
    "unit_cost": "lower cost per unit",
    "risk": "less risk per unit",
}

FRAMEWORKS = [
    {"name": "Anand and Wu, The Gen AI Playbook for Organizations, HBR (2025)", "url": "https://hbr.org/2025/11/the-gen-ai-playbook-for-organizations"},
    {"name": "OpenAI, Identifying and scaling AI use cases", "url": "https://openai.com/business/learn/identifying-and-scaling-ai-use-cases/"},
    {"name": "appliedAI, How to find and prioritize AI use cases (2020)", "url": "https://www.appliedai.de/uploads/files/Whitepapers/appliedAI-Whitepaper-Applying-AI-How-to-find-and-prioritize-AI-use-cases-2020-EN.pdf"},
    {"name": "MIT Sloan, How to find the right business use cases for generative AI (2025)", "url": "https://mitsloan.mit.edu/ideas-made-to-matter/how-to-find-right-business-use-cases-generative-ai"},
    {"name": "Taylor Radey, Finding AI use cases: one helpful framework to try (2025)", "url": "https://www.taylorradey.com/post/finding-ai-use-cases-framework"},
]


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def _tag(item) -> str:
    if item.status == "belegt" and item.evidence.startswith("http"):
        return f"*([documented]({item.evidence}))*"
    if item.status == "belegt":
        return "*(documented)*"
    return "*(assumption)*"


def _cell(text: str) -> str:
    return (text or "").replace("|", "/").replace("\n", " ")


def render_report(state: RunState) -> dict:
    env = Environment(loader=FileSystemLoader(TEMPLATES), trim_blocks=False, lstrip_blocks=False)
    env.globals.update(tag=_tag, cell=_cell)
    markdown = env.get_template("report.md.j2").render(
        s=state,
        m=state.model,
        picks=state.picks,
        cards={c["id"]: c for c in library.load_cards()},
        levers=LEVERS,
        frameworks=FRAMEWORKS,
        date=date.today().strftime("%d %B %Y"),
    )
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)

    out_dir = OUTPUTS_DIR / slugify(state.company_name)
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / "report.md"
    report_path.write_text(markdown, encoding="utf-8")
    (out_dir / "state.json").write_text(state.model_dump_json(indent=2), encoding="utf-8")
    return {"report_path": str(report_path)}
