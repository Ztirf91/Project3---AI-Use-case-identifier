import json
from typing import Literal

from pydantic import Field, create_model

from app import library
from app.config import REASONING_MODEL, RUBRIC_PATH, llm
from app.state import RunState, StepRatings, UseCase, UseCasePicks

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

Rules for the selection:
- Three use cases on three different process steps.
- Each use case adapts one candidate card. source_card must be that card's id, exactly as given.
- approach normally follows the card's approach. You may label a "redesign then automate" card as a "quick win" only
  if you scope it down to a narrow first step, and process_change must say what that narrow step is.
  A "strategic bet" card is never a quick win. Among the three, at least one "quick win" and at least one
  "redesign then automate".
- Prefer use cases that move different unit-economics levers, when the company's situation justifies it.
- Fit the company's current situation from the news (for example a market exit, cost pressure, or a product launch).

Rules for each use case:
- hbr_zone follows from error cost and type of knowledge for this step at this company, and must match the human's role:
  No regrets = AI runs it; Creative catalyst = AI proposes, a person chooses; Quality control = AI produces, a person
  verifies; Human first = a person leads, AI assists with parts. Never propose end-to-end automation in Human first.
- process_change says what to change in the process itself (remove a re-typing step, standardize an input, define an
  owner or a rule) before or alongside AI. A poor process is not automated as it is.
- what_changes describes how the work runs afterwards: what triggers it, what the AI does, what people still do.
- framework_reasoning applies two or three rubric checks to this step at this company in plain sentences. No generic phrases.
- prerequisites are statements of what must exist ("A product catalog with current dealer prices"), not questions.
- pilot names the baseline to record, the success measure from the card's pilot_metrics, the accountable owner, and the
  condition for scaling.
- source_type distinguishes customer case studies, documented solutions, and workflow templates. Templates do not prove
  customer results. Publisher-reported effects are not promised outcomes for this company.
- If the use case touches personal data, add a prerequisite about GDPR and, where relevant, the EU AI Act.

Rules for the questions (these drive the first meeting, so make them specific to this company):
- questions_assumptions: statements, not questions. The riskiest assumption first: the one the use case breaks on if
  it is wrong (for example "Dealers still send reorders by email rather than through a B2B portal").
  Include every "abgeleitet" step the use case relies on.
- leave_alone must not contain a step that one of the three use cases sits on.
- questions_prerequisites: "Do you have ...?" questions that name this company's likely systems, data, and roles.
- questions_decision: volumes, current time or error rates, who owns the step, and what hurts most today.
- Three questions per list. Avoid questions that could be asked of any company.

Overall:
- ai_approach: the right AI approach for this company now, in four to six sentences, tied to its business model,
  unit economics, and current situation.
- leave_alone: steps that should not be automated now, each with a short reason.
Write in English.

RUBRIC
{rubric}"""


def _model_json(state: RunState) -> str:
    return state.model.model_dump_json(indent=1) if state.model else "{}"


def _card_view(card: dict) -> dict:
    keys = ("id", "title", "source_name", "source_type", "source_summary", "typical_effect", "pattern", "ai_does", "needs", "sme_fit", "money_lever", "approach", "pilot_metrics", "human_role", "similarity")
    return {k: card.get(k) for k in keys}


def _picks_schema(card_ids: list[str], step_names: list[str]) -> type[UseCasePicks]:
    """UseCasePicks whose source_card and process_step can only take values from this run."""
    use_case = create_model(
        "UseCase",
        __base__=UseCase,
        source_card=(Literal[tuple(card_ids)], Field(description="Id of the candidate card this is adapted from")),
        process_step=(Literal[tuple(step_names)], Field(description="Exact name of the process step")),
    )
    return create_model("UseCasePicks", __base__=UseCasePicks, use_cases=(list[use_case], ...))


def _check(picks: UseCasePicks, allowed_ids: set[str], card_approach: dict[str, str]) -> list[str]:
    problems = []
    if len(picks.use_cases) != 3:
        problems.append(f"Expected 3 use cases, got {len(picks.use_cases)}.")
    steps = [u.process_step for u in picks.use_cases]
    if len(set(steps)) != len(steps):
        problems.append("Two use cases sit on the same process step.")
    for u in picks.use_cases:
        if u.source_card not in allowed_ids:
            problems.append(f"'{u.title}' uses source_card '{u.source_card}', which is not among the candidate cards.")
        elif card_approach.get(u.source_card) == "strategic bet" and u.approach == "quick win":
            problems.append(f"'{u.title}' is labeled 'quick win', but its card is a 'strategic bet'.")
        if any(item.strip().lower().startswith(u.process_step.lower()) for item in picks.leave_alone):
            problems.append(f"'{u.title}' sits on '{u.process_step}', which is also listed under leave_alone.")
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
    card_approach = {c["id"]: c.get("approach") for cards in candidates.values() for c in cards}
    context = json.dumps(
        {
            "company": json.loads(_model_json(state)),
            "current_situation_news": [{"title": n.title, "snippet": n.snippet} for n in state.news],
            "register_and_size": [{"title": r.title, "snippet": r.snippet} for r in state.register_hits],
            "step_ratings": [r.model_dump() for r in ratings],
            "candidate_cards_by_step": candidates,
        },
        indent=1,
        ensure_ascii=False,
    )
    messages = [("system", PICK_SYSTEM.format(rubric=rubric)), ("human", context)]
    schema = _picks_schema(sorted(allowed_ids), [s.name for s in model.process_map])
    picker = llm(temperature=0.3, model=REASONING_MODEL).with_structured_output(schema)

    def pick(msgs) -> UseCasePicks:
        return UseCasePicks.model_validate(picker.invoke(msgs).model_dump())

    picks = pick(messages)
    problems = _check(picks, allowed_ids, card_approach)
    if problems:
        retry = messages + [("human", "Your answer broke these rules. Fix them:\n- " + "\n- ".join(problems))]
        picks = pick(retry)
        remaining = _check(picks, allowed_ids, card_approach)
        if remaining:
            notes.append("Use-case selection still breaks rules after one retry: " + " ".join(remaining))

    return {"ratings": ratings, "candidates": candidates, "picks": picks, "notes": notes}
