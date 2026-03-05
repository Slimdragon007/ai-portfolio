from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime


class PipelineStatus(str, Enum):
    intake = "intake"
    qualifying = "qualifying"
    qualified = "qualified"
    disqualified = "disqualified"
    proposing = "proposing"
    reviewing = "reviewing"
    pending_approval = "pending_approval"
    approved = "approved"
    rejected = "rejected"
    error = "error"


class LeadInput(BaseModel):
    name: str = Field(..., description="Contact name")
    company: str = Field(..., description="Company name")
    industry: str = Field(..., description="Industry vertical")
    budget: str = Field(..., description="Budget range or description")
    timeline: str = Field(..., description="Desired timeline")
    need: str = Field(..., description="What they need built")


class ICPMatch(BaseModel):
    mid_market: bool = Field(..., description="Is this a mid-market company?")
    clear_use_case: bool = Field(..., description="Clear AI use case identified?")
    reasonable_budget: bool = Field(..., description="Budget is reasonable for scope?")
    timeline_fit: bool = Field(..., description="Timeline is 3-6 months?")
    notes: str = Field(default="", description="Additional ICP notes")


class QualificationResult(BaseModel):
    lead_id: str
    fit_score: int = Field(..., ge=0, le=100)
    qualified: bool
    reasoning: str
    icp_match: ICPMatch


class ProposalSection(BaseModel):
    title: str
    content: str


class ProposalDraft(BaseModel):
    lead_id: str
    proposal_version: int = 1
    sections: list[ProposalSection]
    customizations_applied: list[str]


class ReviewIssue(BaseModel):
    severity: str = Field(..., description="critical, warning, or suggestion")
    section: str
    detail: str


class ReviewResult(BaseModel):
    lead_id: str
    approved: bool
    issues: list[ReviewIssue] = []
    suggestions: list[str] = []
    revision_required: bool = False


class AgentLog(BaseModel):
    agent_name: str
    lead_id: str
    started_at: datetime
    completed_at: datetime
    duration_ms: int
    tokens_in: int = 0
    tokens_out: int = 0
    cost_usd: float = 0.0
    status: str = "success"
    error: Optional[str] = None


class PipelineState(BaseModel):
    lead_id: str
    lead_input: LeadInput
    status: PipelineStatus = PipelineStatus.intake
    qualification: Optional[QualificationResult] = None
    proposal: Optional[ProposalDraft] = None
    review: Optional[ReviewResult] = None
    agent_logs: list[AgentLog] = []
    retries: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    total_duration_ms: int = 0
    total_cost_usd: float = 0.0
