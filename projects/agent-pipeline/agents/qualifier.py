import asyncio
import json
import time
import uuid
from datetime import datetime

from .schemas import (
    LeadInput, QualificationResult, ICPMatch, AgentLog
)

SYSTEM_PROMPT = """You are a lead qualification agent for FlowstateAI, an AI automation consultancy.

Score incoming leads against the FlowstateAI Ideal Customer Profile (ICP):
- Mid-market company (10-500 employees, or revenue $1M-$100M)
- Clear AI/automation use case (not vague "we want AI")
- Reasonable budget ($5K-$100K for initial engagement)
- Timeline of 3-6 months for implementation
- Industry where AI automation has proven ROI (restaurants, law, healthcare, real estate, e-commerce)

Return a JSON object with:
- fit_score: 0-100 integer
- qualified: true if score >= 60
- reasoning: 2-3 sentences explaining your assessment
- icp_match: object with mid_market, clear_use_case, reasonable_budget, timeline_fit (all boolean), and notes

Be direct. No fluff. Score honestly."""

DEMO_RESPONSES = {
    "Coastal Kitchen": QualificationResult(
        lead_id="",
        fit_score=85,
        qualified=True,
        reasoning="Strong ICP fit. Restaurant industry has proven AI ROI for order management and inventory. Budget is reasonable for a phased rollout. Timeline aligns with a 4-month implementation.",
        icp_match=ICPMatch(
            mid_market=True,
            clear_use_case=True,
            reasonable_budget=True,
            timeline_fit=True,
            notes="Multi-location restaurant group. AI order management + inventory forecasting is a well-defined scope with measurable outcomes."
        )
    ),
    "Smith & Associates Law": QualificationResult(
        lead_id="",
        fit_score=72,
        qualified=True,
        reasoning="Good fit with some caveats. Document automation for a mid-size law firm is a proven use case. Budget is on the lower end but workable for an initial pilot. Timeline is tight at 3 months but feasible for a focused scope.",
        icp_match=ICPMatch(
            mid_market=True,
            clear_use_case=True,
            reasonable_budget=True,
            timeline_fit=True,
            notes="15-attorney firm. Document review and contract drafting automation. May need to scope down to a single practice area for the pilot."
        )
    ),
    "Jake's Garage": QualificationResult(
        lead_id="",
        fit_score=31,
        qualified=False,
        reasoning="Poor ICP fit. Single-location auto shop with no defined budget and vague requirements ('make things easier with AI'). No clear use case that would justify AI investment at this stage. Would recommend revisiting when they have a specific operational bottleneck and allocated budget.",
        icp_match=ICPMatch(
            mid_market=False,
            clear_use_case=False,
            reasonable_budget=False,
            timeline_fit=False,
            notes="Small business, 3 employees. No budget allocated. Need is undefined. Not ready for AI automation engagement."
        )
    ),
}


async def qualify_lead(
    lead: LeadInput,
    lead_id: str,
    api_key: str | None = None,
) -> tuple[QualificationResult, AgentLog]:
    started = datetime.utcnow()
    t0 = time.time()

    if api_key:
        result = await _call_claude(lead, lead_id, api_key)
    else:
        result = await _demo_response(lead, lead_id)

    elapsed = int((time.time() - t0) * 1000)
    log = AgentLog(
        agent_name="qualifier",
        lead_id=lead_id,
        started_at=started,
        completed_at=datetime.utcnow(),
        duration_ms=elapsed,
        tokens_in=200 if api_key else 0,
        tokens_out=150 if api_key else 0,
        cost_usd=round(0.003 * (350 / 1000), 4) if api_key else 0.0,
    )
    return result, log


async def _demo_response(lead: LeadInput, lead_id: str) -> QualificationResult:
    await asyncio.sleep(1.5)
    if lead.company in DEMO_RESPONSES:
        result = DEMO_RESPONSES[lead.company].model_copy()
        result.lead_id = lead_id
        return result
    # Generic fallback for custom leads in demo mode
    return QualificationResult(
        lead_id=lead_id,
        fit_score=55,
        qualified=False,
        reasoning="Demo mode: lead not in sample dataset. In live mode, this would be scored by Claude against FlowstateAI ICP criteria.",
        icp_match=ICPMatch(
            mid_market=False,
            clear_use_case=False,
            reasonable_budget=False,
            timeline_fit=False,
            notes="Demo fallback response."
        )
    )


async def _call_claude(lead: LeadInput, lead_id: str, api_key: str) -> QualificationResult:
    import anthropic

    client = anthropic.AsyncAnthropic(api_key=api_key)
    user_msg = f"""Score this lead:
Name: {lead.name}
Company: {lead.company}
Industry: {lead.industry}
Budget: {lead.budget}
Timeline: {lead.timeline}
Need: {lead.need}

Return valid JSON matching the QualificationResult schema."""

    response = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )

    text = response.content[0].text
    # Extract JSON from response
    start = text.find("{")
    end = text.rfind("}") + 1
    data = json.loads(text[start:end])
    data["lead_id"] = lead_id

    return QualificationResult(**data)
