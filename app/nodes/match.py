import json

from app import library
from app.config import RUBRIC_PATH, llm
from app.state import RunState, StepRatings, UseCasePicks

TOP_STEPS = 5
CARDS_PER_STEP = 3

RATE_SYSTEM = """You are a senior AI consultant. Rate every process step of this company with the rubric below.
Be strict. A step without a money lever, or with high error cost and tacit knowledge, gets a low score.
A step marked "abgeleitet" is an assumption; you may rate it, but say so in the reasoning.

RUBRIC
{rubric}"""

PICK_SYSTEM = """You are a senior AI consultant preparing a first meeting with an SME.
Using the rubric, the company model, the step ratings, and ONLY the candidate library cards listed,
choose exactly three use cases for this company.

Rules:
- Three use cases on three different process steps.
- Each use case adapts one candidate card. source_card must be that card's id, exactly as given.
- Each names the unit-economics lever it moves and explains how, in this company's terms.
- At least one is a "quick win". At least one is "redesign then automate": say what changes in the process first.
- If a step relies on an "abgeleitet" assumption, the questions_assumptions must test it.
- questions_prerequisites are concrete "Do you have ...?" questions taken from the card's needs and this company's context.
- questions_decision help decide whether this use case is the right one (volumes, owners, current pain, error cost).
- framework_reasoning uses rubric terms (e.g. No regrets, Quality control, repetitive task, skill bottleneck) and says why they apply here.
- If the use case touches personal data, add a prerequisite about GDPR and, where relevant, the EU AI Act.
- ai_approach: the right overall approach for this company in three to five sentences, given its business model and maturity.
- leave_alone: steps that should not be automated now, each with a short reason.
Write in English. Be concrete to this company; avoid generic AI language.

RUBRIC
{rubric}"""


def _model_json(state: RunState) -> str:
    return state.model.model_dump_json(indent=1) if state.model else "{}"


def _card_view(card: dict) -> dict:
    keys = ("id", "title", "source_name", "pattern", "ai_does", "needs", "sme_fit", "money_lever", "approach", "similarity")
    return {k: card.get(k) for k in keys}


def _check(picks: UseCasePicks, allowed_ids: set[str]) -> list[str]:
    problems = []
    if len(picks.use_cases) != 3:
        problems.append(f"Expected 3 use cases, got {len(picks.use_cases)}.")
    steps = [u.process_step for u in picks.use_cases]
    if len(set(steps)) != len(steps):
        problems.append("Two use cases sit on the same process step.")
    for u in picks.use_cases:
        if u.source_card not in allowed_ids:
            problems.append(f"'{u.title}' uses source_card '{u.source_card}', which is not among the candidate cards.")
    approaches = {u.approach for u in picks.use_cases}
    if "quick win" not in approaches:
        problems.append("No quick win among the three.")
    if "redesign then automate" not in approaches:
        problems.append("No 'redesign then automate' use case among the three.")
    return problems


def match_use_cases(state: RunState) -> dict:
    try:
        return _match(state)
    except Exception as exc:
        return {"notes": state.notes + [f"Use-case matching failed ({exc.__class__.__name__}: {exc})."]}


def _match(state: RunState) -> dict:
    notes = list(state.notes)
    rubric = RUBRIC_PATH.read_text(encoding="utf-8")
    model = state.model
    if not model or not model.process_map:
        notes.append("No process map, so no use cases could be matched.")
        return {"notes": notes}

    ratings = llm().with_structured_output(StepRatings).invoke(
        [("system", RATE_SYSTEM.format(rubric=rubric)), ("human", _model_json(state))]
    ).ratings

    steps_by_name = {s.name: s for s in model.process_map}
    ranked = sorted((r for r in ratings if r.process_quality != "leave it"), key=lambda r: r.score, reverse=True)
    candidates: dict[str, list[dict]] = {}
    for rating in ranked[:TOP_STEPS]:
        step = steps_by_name.get(rating.step)
        query = rating.step
        if step:
            query = f"{step.name}. Input: {step.data_input}. Output: {step.data_output}. System: {step.likely_system}"
        candidates[rating.step] = [_card_view(c) for c in library.search(query, n=CARDS_PER_STEP)]

    allowed_ids = {c["id"] for cards in candidates.values() for c in cards}
    context = json.dumps(
        {
            "company": json.loads(_model_json(state)),
            "step_ratings": [r.model_dump() for r in ratings],
            "candidate_cards_by_step": candidates,
        },
        indent=1,
    )
    messages = [("system", PICK_SYSTEM.format(rubric=rubric)), ("human", context)]
    picker = llm(temperature=0.3).with_structured_output(UseCasePicks)
    picks = picker.invoke(messages)

    problems = _check(picks, allowed_ids)
    if problems:
        retry = messages + [("human", "Your answer broke these rules. Fix them:\n- " + "\n- ".join(problems))]
        picks = picker.invoke(retry)
        remaining = _check(picks, allowed_ids)
        if remaining:
            notes.append("Use-case selection still breaks rules after one retry: " + " ".join(remaining))

    return {"ratings": ratings, "candidates": candidates, "picks": picks, "notes": notes}
