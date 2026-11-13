from typing import Literal

from pydantic import BaseModel, Field

Status = Literal["belegt", "abgeleitet"]
MoneyLever = Literal["volume", "price", "unit_cost", "risk"]


class Source(BaseModel):
    title: str
    url: str
    snippet: str = ""


class JobPosting(BaseModel):
    title: str
    url: str
    text: str = ""


EVIDENCE_HELP = "Source id such as 'S3' for 'belegt'. 'industry' for 'abgeleitet'."


class Claim(BaseModel):
    text: str
    status: Status
    evidence: str = Field(description=EVIDENCE_HELP)


class ProcessStep(BaseModel):
    name: str = Field(description="Observable work at this company, e.g. 'Dealers place reorders by email'")
    data_input: str = Field(description="What enters the step")
    data_output: str = Field(description="What leaves the step")
    likely_system: str = Field(
        description="Observable channel or light system guess: email, dealer portal, shop cart, ERP, WMS, "
        "spreadsheets, unknown. Prefer the channel people actually use when sources show it."
    )
    status: Status
    evidence: str = Field(description=EVIDENCE_HELP)


class BusinessModel(BaseModel):
    company_type: str = Field(description="One line: what kind of company this is")
    business_model: list[Claim] = Field(description="Who pays, for what, through which channel; at most 4 items")
    unit_economics: list[Claim] = Field(description="The earning unit and what drives its margin; at most 4 items")
    process_map: list[ProcessStep] = Field(
        description="As few steps as needed for this company's operating chain; typically 6 to 8, never pad"
    )
    open_numbers: list[str] = Field(description="Numbers that matter for the unit economics but were not found")


class StepRating(BaseModel):
    step: str
    error_cost: Literal["low", "high"]
    knowledge: Literal["explicit", "tacit"]
    opportunity: Literal["repetitive", "bottleneck", "ambiguity", "none"]
    money_lever: MoneyLever | Literal["none"]
    process_quality: Literal["automate as-is", "redesign then automate", "leave it"]
    score: int = Field(ge=0, le=10, description="Overall AI potential for this company")
    reasoning: str


class StepRatings(BaseModel):
    ratings: list[StepRating]


HbrZone = Literal["No regrets", "Creative catalyst", "Quality control", "Human first"]


class UseCase(BaseModel):
    title: str
    process_step: str = Field(
        description="Name of the process step, in plain language a non-specialist can follow"
    )
    approach: Literal["quick win", "redesign then automate", "strategic bet"]
    hbr_zone: HbrZone = Field(description="From error cost and type of knowledge; must match the human's role")
    what_changes: str = Field(
        description="How AI supports today's process: what triggers it, what AI does, what people still do. "
        "When AI lets people do something they could not do before (new speed, coverage, insight, or offer), "
        "say that briefly in the same paragraph — do not invent a separate heading. "
        "Do not require a process redesign here; that belongs in section 3."
    )
    money_lever: MoneyLever
    money_effect: str = Field(
        description="Concrete unit-economics effect with rough volumes or times. Mark unknown figures as assumptions, "
        "e.g. 'At ~80 dealer emails/day and ~4 minutes sorting (assumption), this frees ~5 hours/day'."
    )
    source_card: str = Field(description="The id of the library card this is adapted from")
    framework_reasoning: str = Field(description="Two or three sentences applying the rubric to this step at this company")
    prerequisites: list[str] = Field(description="Statements of what must exist, not questions")
    pilot: str = Field(description="Baseline to record, success measure, accountable owner, and the condition for scaling")


class SpeculativeAugmentation(BaseModel):
    title: str = Field(description="Short name of the speculative redesigned process")
    process_today: str = Field(description="How the work roughly runs today at this company")
    redesigned_with_ai: str = Field(
        description="How the process would be redesigned so AI and people work as complements, not as a job replacement"
    )
    new_capability: str = Field(
        description="What people could do afterward that they could not do before (new product, service, decision, or reach)"
    )
    business_value: str = Field(description="Concrete unit-economics upside if the speculation holds")


class UseCasePicks(BaseModel):
    ai_approach: str = Field(
        description="Three to four sentences: wave-one AI supports existing processes; deeper redesign is later. "
        "Tie to business model, unit economics, and current situation in the news"
    )
    leave_alone: list[str] = Field(description="Steps not worth automating now, each with a short reason")
    use_cases: list[UseCase]
    meeting_questions: list[str] = Field(
        description="Exactly 4 questions for the three use cases, ordered by: without an answer there is no pilot. "
        "Mix assumptions to test, 'do you have X?', and the volumes or times needed for the money estimates."
    )
    numbers_to_ask: list[str] = Field(
        description="At most 6 unknown volumes, times, costs, or rates used as assumptions in the money_effect texts"
    )
    speculative_augmentation: SpeculativeAugmentation = Field(
        description="One speculative Option-B case: redesign a process with AI so humans gain a capability they did not have, "
        "not a case that only replaces existing labor"
    )


class RunState(BaseModel):
    company_name: str
    company_url: str
    site_pages: list[Source] = []
    job_postings: list[JobPosting] = []
    news: list[Source] = []
    register_hits: list[Source] = []
    model: BusinessModel | None = None
    ratings: list[StepRating] = []
    candidates: dict[str, list[dict]] = {}
    picks: UseCasePicks | None = None
    notes: list[str] = []
    report_path: str = ""
