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
    name: str
    data_input: str
    data_output: str
    likely_system: str = Field(description="System the step most likely runs in, or 'unknown'")
    status: Status
    evidence: str = Field(description=EVIDENCE_HELP)


class BusinessModel(BaseModel):
    company_type: str = Field(description="One line: what kind of company this is")
    business_model: list[Claim] = Field(description="Who pays, for what, through which channel")
    unit_economics: list[Claim] = Field(description="The earning unit and what drives its margin")
    process_map: list[ProcessStep]
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
    process_step: str
    approach: Literal["quick win", "redesign then automate", "strategic bet"]
    hbr_zone: HbrZone = Field(description="From error cost and type of knowledge; must match the human's role")
    process_change: str = Field(description="What to change, remove, or standardize in the process itself, before or alongside AI")
    what_changes: str = Field(description="How the work runs afterwards: trigger, what AI does, what people do")
    money_lever: MoneyLever
    money_effect: str = Field(description="How it moves this company's unit economics")
    source_card: str = Field(description="The id of the library card this is adapted from")
    framework_reasoning: str = Field(description="Two or three sentences applying the rubric to this step at this company")
    prerequisites: list[str] = Field(description="Statements of what must exist, not questions")
    pilot: str = Field(description="Baseline to record, success measure, accountable owner, and the condition for scaling")
    questions_assumptions: list[str] = Field(description="Assumptions to test, riskiest first")
    questions_prerequisites: list[str] = Field(description="'Do you have ...?' questions specific to this company")
    questions_decision: list[str] = Field(description="What to learn to decide if this is the right use case")


class UseCasePicks(BaseModel):
    ai_approach: str = Field(
        description="Four to six sentences: the right AI approach for this company now, tied to its business model, "
        "unit economics, and current situation in the news"
    )
    leave_alone: list[str] = Field(description="Steps not worth automating now, each with a short reason")
    use_cases: list[UseCase]


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
