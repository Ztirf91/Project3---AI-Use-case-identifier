import argparse
import json
import os
import sys
import time

from app.config import CHROMA_DIR, OUTPUTS_DIR
from app.graph import build_graph
from app.nodes.report import slugify
from app.state import RunState


def main() -> None:
    parser = argparse.ArgumentParser(description="Research a company and write an AI use case brief.")
    parser.add_argument("--company", required=True, help="Company name, e.g. 'Riese & Müller'")
    parser.add_argument("--url", required=True, help="Company homepage, e.g. https://www.r-m.de")
    parser.add_argument("--contact-name")
    parser.add_argument("--contact-email")
    parser.add_argument("--city")
    args = parser.parse_args()

    missing = [k for k in ("OPENAI_API_KEY", "TAVILY_API_KEY") if not os.getenv(k)]
    if missing:
        sys.exit(f"Missing in .env: {', '.join(missing)}")
    if not CHROMA_DIR.exists():
        sys.exit("Use-case index not found. Run: python -m app.library")

    start = time.time()
    graph = build_graph()
    state = RunState(company_name=args.company, company_url=args.url)
    for update in graph.stream(state, stream_mode="updates"):
        for node in update:
            print(f"[{time.time() - start:5.1f}s] {node} done")

    if args.contact_email or args.contact_name:
        lead_dir = OUTPUTS_DIR / slugify(args.company)
        lead_dir.mkdir(parents=True, exist_ok=True)
        lead = {"name": args.contact_name, "email": args.contact_email, "city": args.city, "company": args.company}
        (lead_dir / "lead.json").write_text(json.dumps(lead, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Report: {OUTPUTS_DIR / slugify(args.company) / 'report.md'}")


if __name__ == "__main__":
    main()
