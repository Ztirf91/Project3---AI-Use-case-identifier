import json
from typing import Literal

from pydantic import BaseModel, Field, create_model

from app import library
from app.config import MODEL, REASONING_MODEL, RUBRIC_PATH, llm
from app.state import RunState, StepRatings, UseCase, UseCasePicks

TOP_STEPS = 5
RAG_TOP_K = 8
CARDS_PER_STEP = 3
FIT_WEIGHT = 0.70
SIM_WEIGHT = 0.30

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
- Select distinct business tasks. task_scope explains boundaries between related cards; a different tool or source
  does not make the same task a new use case.
- Each use case adapts one candidate card. source_card must be that card's id, exactly as given.
- approach normally follows the card's approach. You may label a "redesign then automate" card as a "quick win" only
  if you scope it down to a narrow first step, and process_change must say what that narrow step is.
  A "strategic bet" card is never a quick win. Among the three, at least one "quick win" and at least one
  "redesign then automate".
- Among the three hbr_zone values, at least one must be "Creative catalyst" or "Human first".
  Do not label all three "Quality control" unless the rubric truly forces that; usually at least one step is
  proposal work (Creative catalyst) or expert-led work with AI assist (Human first).
- Prefer use cases that move different unit-economics levers, when the company's situation justifies it.
- Fit the company's current situation from the news (for example a market exit, cost pressure, or a product launch).

Rules for each use case:
- hbr_zone follows from error cost and type of knowledge for this step at this company, and must match the human's role:
  No regrets = AI runs it; Creative catalyst = AI proposes, a person chooses; Quality control = AI produces, a person
  verifies; Human first = a person leads, AI assists with parts. Never propose end-to-end automation in Human first.
- process_change says what to change in the process itself before AI: eliminate waste, standardize intake, name an
  owner. Sequence: purpose → eliminate → standardize → then let AI draft/classify/propose. Never automate a broken
  process as-is; redesign so AI creates unit-economics value (cost, volume, price, or risk), not just fewer clicks.
- what_changes describes how the work runs afterwards: what triggers it, what the AI does, what people still do.
- money_effect must be concrete. Include a rough volume or time math for THIS company.
  If the figure is not in the sources, mark it clearly as an assumption, for example:
  "At ~80 dealer emails/day and ~4 minutes sorting each (assumption), this frees ~5 hours/day."
  Put every such unknown figure into numbers_to_ask.
- framework_reasoning applies two or three rubric checks to this step at this company in plain sentences. No generic phrases.
- prerequisites are statements of what must exist ("A product catalog with current dealer prices"), not questions.
- pilot names the baseline to record, the success measure from the card's pilot_metrics, the accountable owner, and the
  condition for scaling.
- source_type distinguishes customer case studies, documented solutions, and workflow templates. Templates do not prove
  customer results. Publisher-reported effects are not promised outcomes for this company.
- Workflow guides and demonstrators also do not prove a customer deployment or ROI. Respect verification_scope and
  limitations; additional_sources are supporting references or implementation alternatives for the same task.
- If the use case touches personal data, add a prerequisite about GDPR and, where relevant, the EU AI Act.

Rules for the meeting section:
- meeting_questions: exactly 4 questions total for the three use cases (not per use case).
  Order them by "without an answer there is no pilot". First the riskiest assumptions and missing owners/data,
  then the volumes or times needed to validate the money estimates.
  Make them specific to this company. Avoid questions that could be asked of any company.
- numbers_to_ask: at most 6 unknown volumes, times, costs, or rates used as assumptions in the money_effect texts.
- leave_alone must not contain a step that one of the three use cases sits on.

Overall:
- ai_approach: the right AI approach for this company now, in three to four sentences, tied to its business model,
  unit economics, and current situation.
- leave_alone: at most three steps that should not be automated now, each with a short reason.
- speculative_augmentation: ONE speculative case (not one of the three library use cases) that redesigns a process
  with AI as Option B — augmentation / complement. Humans must gain a capability they did not have before
  (new insight, new offer, new reach, better decisions). Do NOT propose pure labor substitution. Mark it clearly
  as speculation for the meeting. Tie it to this company's model and situation.
- Keep every field concise. Prefer short paragraphs over lists of caveats.
Write in English.

RUBRIC
{rubric}"""


def _model_json(state: RunState) -> str:
    return state.model.model_dump_json(indent=1) if state.model else "{}"


def _card_view(card: dict) -> dict:
    keys = (
        "id", "title", "source_name", "source_type", "source_summary", "typical_effect", "pattern", "ai_does",
        "needs", "sme_fit", "money_lever", "approach", "pilot_metrics", "human_role", "task_scope",
        "limitations", "verification_scope", "additional_sources", "similarity", "fit_score", "rerank_score",
    )
    return {k: card.get(k) for k in keys}


class CardFit(BaseModel):
    id: str = Field(description="Exact card id")
    fit: float = Field(ge=0, le=1, description="How well this card fits the company and this process step")


class CardFits(BaseModel):
    scores: list[CardFit]


RERANK_SYSTEM = """You are a senior AI consultant reranking retrieved use-case cards for ONE process step at ONE company.
For each card, score fit from 0.0 to 1.0:
- 1.0 = clearly matches this company's channels, systems, data reality, and unit economics for this step
- 0.5 = plausible but needs stretch assumptions
- 0.0 = wrong industry pattern, missing prerequisites the company is unlikely to have, or wrong kind of work
Score THIS company, not generic SMEs. Return one score per card id, using the ids exactly as given."""


def _company_brief(state: RunState) -> dict:
    model = state.model
    return {
        "company": state.company_name,
        "company_type": model.company_type if model else "",
        "business_model": [c.text for c in (model.business_model if model else [])],
        "unit_economics": [c.text for c in (model.unit_economics if model else [])],
        "news": [{"title": n.title, "snippet": n.snippet} for n in state.news[:5]],
    }


def _rerank_for_step(state: RunState, step_query: str, step_name: str, cards: list[dict]) -> list[dict]:
    """Retrieve already done; score company fit and blend with similarity (70/30), keep top 3."""
    if not cards:
        return []
    if len(cards) == 1:
        only = dict(cards[0])
        only["fit_score"] = 1.0
        only["rerank_score"] = round(FIT_WEIGHT * 1.0 + SIM_WEIGHT * float(only.get("similarity") or 0), 3)
        return [only]

    listing = [
        {
            "id": c["id"],
            "title": c.get("title"),
            "pattern": c.get("pattern"),
            "ai_does": c.get("ai_does"),
            "needs": c.get("needs"),
            "sme_fit": c.get("sme_fit"),
            "money_lever": c.get("money_lever"),
            "approach": c.get("approach"),
            "task_scope": c.get("task_scope"),
            "similarity": c.get("similarity"),
        }
        for c in cards
    ]
    payload = {
        "company": _company_brief(state),
        "process_step": step_name,
        "step_query": step_query,
        "cards": listing,
    }
    try:
        result = llm(temperature=0, model=MODEL).with_structured_output(CardFits).invoke(
            [("system", RERANK_SYSTEM), ("human", json.dumps(payload, ensure_ascii=False, indent=1))]
        )
        fit_by_id = {s.id: float(s.fit) for s in result.scores}
    except Exception:
        fit_by_id = {c["id"]: 0.5 for c in cards}

    sims = [float(c.get("similarity") or 0) for c in cards]
    lo, hi = (min(sims), max(sims)) if sims else (0.0, 1.0)

    ranked = []
    for card in cards:
        sim = float(card.get("similarity") or 0)
        sim_norm = 0.5 if hi <= lo else (sim - lo) / (hi - lo)
        fit = max(0.0, min(1.0, fit_by_id.get(card["id"], 0.5)))
        scored = dict(card)
        scored["fit_score"] = round(fit, 3)
        scored["rerank_score"] = round(FIT_WEIGHT * fit + SIM_WEIGHT * sim_norm, 3)
        ranked.append(scored)
    ranked.sort(key=lambda c: c["rerank_score"], reverse=True)
    return ranked[:CARDS_PER_STEP]


def _picks_schema(card_ids: list[str], step_names: list[str]) -> type[UseCasePicks]:
    """UseCasePicks whose source_card and process_step can only take values from this run."""
    if not card_ids:
        raise ValueError("No candidate library cards were retrieved for the top-rated steps.")
    if not step_names:
        raise ValueError("No process steps available to attach use cases to.")
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
    zones = {u.hbr_zone for u in picks.use_cases}
    if zones.isdisjoint({"Creative catalyst", "Human first"}):
        problems.append("At least one use case must be 'Creative catalyst' or 'Human first'.")
    n_questions = len(picks.meeting_questions)
    if n_questions != 4:
        problems.append(f"meeting_questions must have exactly 4 items, got {n_questions}.")
    if not picks.numbers_to_ask:
        problems.append("numbers_to_ask is empty; list the assumptions used in money_effect.")
    if len(picks.numbers_to_ask) > 6:
        problems.append("numbers_to_ask has more than 6 items; keep only the critical ones.")
    if len(picks.leave_alone) > 3:
        problems.append("leave_alone has more than 3 items; keep only the clearest ones.")
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
            query = f"{step.name}. Input: {step.data_input}. Output: {step.data_output}. Channel: {step.likely_system}"
        retrieved = library.search(query, n=RAG_TOP_K)
        shortlist = _rerank_for_step(state, query, rating.step, retrieved)
        candidates[rating.step] = [_card_view(c) for c in shortlist]

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
