import asyncio
import json
import time
from datetime import datetime

from .schemas import (
    ProposalDraft, ReviewResult, ReviewIssue, AgentLog
)

SYSTEM_PROMPT = """You are a proposal review agent for FlowstateAI, an AI automation consultancy.

Review the given proposal for quality, completeness, and accuracy:

Check for:
1. Missing sections (Overview, Scope, Timeline, Pricing, Terms are all required)
2. Vague scope items (deliverables should be specific and measurable)
3. Pricing that doesn't match the stated budget range
4. Timeline gaps or unrealistic milestones
5. Missing compliance or legal terms for regulated industries
6. Tone: professional but not corporate. Direct, practical.

Return JSON with:
- approved: true if no critical issues
- issues: array of { severity (critical/warning/suggestion), section, detail }
- suggestions: array of improvement suggestions
- revision_required: true if any critical issues found

Be thorough but fair. Minor issues are suggestions, not blockers."""

DEMO_REVIEWS = {
    "Coastal Kitchen": ReviewResult(
        lead_id="",
        approved=True,
        issues=[
            ReviewIssue(
                severity="suggestion",
                section="Pricing",
                detail="Consider adding a monthly retainer option for ongoing model retraining after the initial 3-month support period."
            ),
            ReviewIssue(
                severity="suggestion",
                section="Scope",
                detail="Specify which POS systems are supported in Phase 1 vs. future phases."
            ),
        ],
        suggestions=[
            "Add a case study reference from a similar restaurant deployment",
            "Include expected ROI timeline (when they'll see the 15-25% waste reduction)",
        ],
        revision_required=False,
    ),
    "Smith & Associates Law": ReviewResult(
        lead_id="",
        approved=True,
        issues=[
            ReviewIssue(
                severity="warning",
                section="Terms",
                detail="Add explicit data retention and deletion policy. Law firms require this for compliance."
            ),
            ReviewIssue(
                severity="suggestion",
                section="Timeline",
                detail="12 weeks is tight for legal document AI. Consider adding a 2-week buffer for attorney feedback cycles."
            ),
        ],
        suggestions=[
            "Reference ABA guidelines on AI-assisted legal work",
            "Add a section on model accuracy expectations and human oversight requirements",
        ],
        revision_required=False,
    ),
}


async def review_proposal(
    proposal: ProposalDraft,
    lead_id: str,
    api_key: str | None = None,
    company_name: str = "",
) -> tuple[ReviewResult, AgentLog]:
    started = datetime.utcnow()
    t0 = time.time()

    if api_key:
        result = await _call_claude(proposal, lead_id, api_key)
    else:
        result = await _demo_response(lead_id, company_name)

    elapsed = int((time.time() - t0) * 1000)
    log = AgentLog(
        agent_name="reviewer",
        lead_id=lead_id,
        started_at=started,
        completed_at=datetime.utcnow(),
        duration_ms=elapsed,
        tokens_in=500 if api_key else 0,
        tokens_out=300 if api_key else 0,
        cost_usd=round(0.003 * (800 / 1000), 4) if api_key else 0.0,
    )
    return result, log


async def _demo_response(lead_id: str, company_name: str) -> ReviewResult:
    await asyncio.sleep(1.8)
    if company_name in DEMO_REVIEWS:
        result = DEMO_REVIEWS[company_name].model_copy(deep=True)
        result.lead_id = lead_id
        return result
    return ReviewResult(
        lead_id=lead_id,
        approved=True,
        issues=[],
        suggestions=["Demo mode: full review requires live API connection."],
        revision_required=False,
    )


async def _call_claude(
    proposal: ProposalDraft,
    lead_id: str,
    api_key: str,
) -> ReviewResult:
    import anthropic

    client = anthropic.AsyncAnthropic(api_key=api_key)

    sections_text = "\n\n".join(
        f"## {s.title}\n{s.content}" for s in proposal.sections
    )

    user_msg = f"""Review this proposal (version {proposal.proposal_version}):

{sections_text}

Customizations applied: {', '.join(proposal.customizations_applied)}

Return valid JSON with approved (bool), issues array, suggestions array, and revision_required (bool)."""

    response = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )

    text = response.content[0].text
    start = text.find("{")
    end = text.rfind("}") + 1
    data = json.loads(text[start:end])
    data["lead_id"] = lead_id

    return ReviewResult(**data)
