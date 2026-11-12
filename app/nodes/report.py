import os
import re
from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from app import library
from app.config import DISCOVERY_PATH, OUTPUTS_DIR, PROCESS_REDESIGN_PATH
from app.process_map import PROCESS_MAP_IMAGE, generate_process_map_image
from app.state import RunState

TEMPLATES = Path(__file__).resolve().parent.parent / "templates"

LEVERS = {
    "volume": "more units sold",
    "price": "better price",
    "unit_cost": "lower cost per unit",
    "risk": "less risk per unit",
}

FRAMEWORKS = [
    {"name": "APQC, How Can Organizations Identify And Prioritize Valuable AI Use Cases?", "url": "https://www.apqc.org/How-Can-Organizations-Identify-And-Prioritize-Valuable-AI-Use-Cases"},
    {"name": "AWS, Taxonomy of agentic primitives in Amazon Quick (2026)", "url": "https://aws.amazon.com/blogs/machine-learning/taxonomy-of-agentic-primitives-in-amazon-quick/"},
    {"name": "Anand and Wu, The Gen AI Playbook for Organizations, HBR (2025)", "url": "https://hbr.org/2025/11/the-gen-ai-playbook-for-organizations"},
    {"name": "OpenAI, Identifying and scaling AI use cases", "url": "https://openai.com/business/learn/identifying-and-scaling-ai-use-cases/"},
    {"name": "appliedAI, How to find and prioritize AI use cases (2020)", "url": "https://www.appliedai.de/uploads/files/Whitepapers/appliedAI-Whitepaper-Applying-AI-How-to-find-and-prioritize-AI-use-cases-2020-EN.pdf"},
    {"name": "MIT Sloan, How to find the right business use cases for generative AI (2025)", "url": "https://mitsloan.mit.edu/ideas-made-to-matter/how-to-find-right-business-use-cases-generative-ai"},
    {"name": "Taylor Radey, Finding AI use cases: one helpful framework to try (2025)", "url": "https://www.taylorradey.com/post/finding-ai-use-cases-framework"},
    {"name": "MIT Sloan, Want AI-Driven Productivity? Redesign Work", "url": "https://sloanreview.mit.edu/article/want-ai-driven-productivity-redesign-work/"},
    {"name": "MIT Sloan, Don’t Let Artificial Intelligence Supercharge Bad Processes", "url": "https://sloanreview.mit.edu/article/dont-let-artificial-intelligence-supercharge-bad-processes/"},
    {"name": "HBR, The Secret to Successful AI-Driven Process Redesign (2025)", "url": "https://hbr.org/2025/01/the-secret-to-successful-ai-driven-process-redesign"},
    {"name": "HBR, Stop Automating Old Processes. Design New Ones Instead. (2026)", "url": "https://hbr.org/2026/09/stop-automating-old-processes-design-new-ones-instead"},
    {"name": "Randstad, Before you automate, AI-vate or agent-icate", "url": "https://www.randstadenterprise.com/insights/randstad-enterprise-insights/before-you-automate-ai-vate-or-agent-icate/"},
    {"name": "Brynjolfsson, The Turing Trap, Stanford Digital Economy Lab (2022)", "url": "https://digitaleconomy.stanford.edu/news/the-turing-trap-the-promise-peril-of-human-like-artificial-intelligence/"},
]


# Distilled for the brief from corpus/frameworks/process_redesign.md (not stored as paragraphs there).
REDESIGN_PARAGRAPHS = [
    "Do not automate the process as found — redesign it first. AI on yesterday’s workflow usually speeds up waste: "
    "retyping, handoffs, and approvals that should not exist. Break the work into tasks, cut or relocate what nobody "
    "needs, then decide what AI drafts or proposes and what a named person still owns. Ask which process to clean up "
    "first, and which human capabilities should get stronger afterward — not merely what can be automated.",
    "Redesign pays when it moves unit economics, not when it saves a few clicks. Remove double entry and cycle time "
    "falls; standardize intake and errors fall; give specialists AI-prepared options and they spend time on judgment "
    "and customers. People stay accountable for money, legal, and customer outcomes; AI removes low-value motion "
    "around them. That is how AI becomes a complement instead of a faster broken process.",
]

AI_PATHS = {
    "a_title": "Option A — Automate / substitute",
    "a_text": (
        "AI copies what people already do and takes over those tasks. Machines become substitutes for labor. "
        "Output can get cheaper, but people become more replaceable and more of the upside goes to whoever owns the system."
    ),
    "b_title": "Option B — Augment / complement",
    "b_text": (
        "AI enables people to do things they could not do before. Humans and machines are complements. "
        "Augmentation also tends to create new products, services, and tasks — not only cheaper versions of old ones."
    ),
}


def load_process_redesign_proposal() -> str:
    """Load the redesign-with-AI proposal block from the framework file."""
    text = PROCESS_REDESIGN_PATH.read_text(encoding="utf-8")
    if "## Proposal:" not in text:
        return ""
    block = text.split("## Proposal:", 1)[1].strip()
    # Drop the heading remainder on the first line if present; keep body from first blank or table.
    lines = block.splitlines()
    if lines and lines[0].strip() and not lines[0].startswith("|") and not lines[0].startswith("**"):
        lines = lines[1:]
    return "\n".join(lines).strip()


def load_discovery() -> tuple[str, list[str]]:
    """Approach paragraph + general discovery questions from discovery.md."""
    text = DISCOVERY_PATH.read_text(encoding="utf-8")
    stance = text.split("## Stance", 1)[-1].split("## Questions", 1)[0]
    paras = [p.strip() for p in stance.strip().split("\n\n") if p.strip() and not p.startswith("#")]
    q_block = text.split("## Questions", 1)[-1]
    questions = []
    for line in q_block.splitlines():
        line = line.strip()
        if line[:1].isdigit() and ". " in line:
            questions.append(line.split(". ", 1)[1].strip())
        elif line.startswith("- "):
            questions.append(line[2:].strip())
    return paras[0] if paras else "", questions


ZONES = {
    "No regrets": "AI runs it",
    "Creative catalyst": "AI proposes, a person chooses",
    "Quality control": "AI produces, a person verifies",
    "Human first": "a person leads, AI assists",
}

def slugify(name: str) -> str:
    folded = name.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    return re.sub(r"[^a-z0-9]+", "-", folded).strip("-")


def _tag(item) -> str:
    if item.status == "belegt" and item.evidence.startswith("http"):
        return f"*([documented]({item.evidence}))*"
    if item.status == "belegt":
        return "*(documented)*"
    return "*(assumption)*"


def _cell(text: str) -> str:
    return (text or "").replace("|", "/").replace("\n", " ")


def render_report(state: RunState) -> dict:
    notes = list(state.notes)
    out_dir = OUTPUTS_DIR / slugify(state.company_name)
    out_dir.mkdir(parents=True, exist_ok=True)

    process_image = None
    image_path = out_dir / PROCESS_MAP_IMAGE
    if state.model and state.model.process_map:
        if image_path.exists() and not os.getenv("FORCE_PROCESS_MAP"):
            process_image = PROCESS_MAP_IMAGE
        else:
            try:
                process_image = generate_process_map_image(
                    state.company_name,
                    state.model.process_map,
                    image_path,
                )
            except Exception as exc:
                notes.append(
                    "Process map image could not be generated "
                    f"({exc.__class__.__name__}). Check OPENAI_KEY2, IMAGE_MODEL and image-model access."
                )

    updated = state.model_copy(update={"notes": notes})
    env = Environment(loader=FileSystemLoader(TEMPLATES), trim_blocks=False, lstrip_blocks=False)
    env.globals.update(tag=_tag, cell=_cell)
    numbers = []
    if state.model:
        numbers.extend(state.model.open_numbers)
    if state.picks:
        for item in state.picks.numbers_to_ask:
            if item not in numbers:
                numbers.append(item)
    numbers = numbers[:6]
    discovery_intro, discovery_questions = load_discovery()
    markdown = env.get_template("report.md.j2").render(
        s=updated,
        m=state.model,
        picks=state.picks,
        cards={c["id"]: c for c in library.load_cards()},
        levers=LEVERS,
        zones=ZONES,
        frameworks=FRAMEWORKS,
        date=date.today().strftime("%d %B %Y"),
        process_image=process_image,
        numbers=numbers,
        redesign_paragraphs=REDESIGN_PARAGRAPHS,
        redesign_proposal=load_process_redesign_proposal(),
        ai_paths=AI_PATHS,
        discovery_intro=discovery_intro,
        discovery_questions=discovery_questions,
    )
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)

    report_path = out_dir / "report.md"
    report_path.write_text(markdown, encoding="utf-8")
    (out_dir / "state.json").write_text(updated.model_dump_json(indent=2), encoding="utf-8")
    return {"report_path": str(report_path), "notes": notes}
