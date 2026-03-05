import asyncio
import json
import time
from datetime import datetime

from .schemas import (
    QualificationResult, LeadInput, ProposalDraft, ProposalSection, AgentLog
)

SYSTEM_PROMPT = """You are a proposal drafting agent for FlowstateAI, an AI automation consultancy.

Given a qualified lead and their details, generate a professional proposal with these sections:
1. Overview: 2-3 sentences on what FlowstateAI will build
2. Scope: Bullet list of deliverables
3. Timeline: Phase breakdown with milestones
4. Pricing: Tiered pricing (Starter, Growth, Enterprise) appropriate to the lead's budget
5. Terms: Standard engagement terms

Customize the proposal to the lead's industry, specific need, and budget range.
Return valid JSON with sections array and customizations_applied list.
Be specific and practical. No generic filler."""

DEMO_PROPOSALS = {
    "Coastal Kitchen": ProposalDraft(
        lead_id="",
        proposal_version=1,
        sections=[
            ProposalSection(
                title="Overview",
                content="FlowstateAI will design and deploy an AI-powered order management and inventory forecasting system for Coastal Kitchen's multi-location restaurant operations. The system will integrate with your existing POS to automate order routing, predict ingredient demand, and reduce food waste by 15-25%."
            ),
            ProposalSection(
                title="Scope",
                content="- POS integration layer (Toast/Square API)\n- AI order routing engine (dine-in, takeout, delivery prioritization)\n- Inventory forecasting model trained on 12 months of historical data\n- Real-time waste tracking dashboard\n- Staff notification system for low-stock alerts\n- Manager approval workflows for automated reorders"
            ),
            ProposalSection(
                title="Timeline",
                content="Phase 1 (Weeks 1-4): Discovery, POS integration, data pipeline setup\nPhase 2 (Weeks 5-10): AI model training, order routing engine build\nPhase 3 (Weeks 11-14): Dashboard, alerts, staff training\nPhase 4 (Weeks 15-16): Launch, monitoring, optimization"
            ),
            ProposalSection(
                title="Pricing",
                content="Starter (1 location): $18,000\nGrowth (2-4 locations): $35,000\nEnterprise (5+ locations): $55,000\n\nIncludes: 3 months post-launch support, model retraining, and priority Slack channel."
            ),
            ProposalSection(
                title="Terms",
                content="50% upfront, 25% at Phase 2 completion, 25% at launch. Net 15 payment terms. 90-day post-launch support included. Source code ownership transfers to client at project completion."
            ),
        ],
        customizations_applied=[
            "Restaurant-specific POS integration scope",
            "Food waste reduction KPI (15-25%)",
            "Multi-location tiered pricing",
            "Industry-standard inventory forecasting approach",
        ]
    ),
    "Smith & Associates Law": ProposalDraft(
        lead_id="",
        proposal_version=1,
        sections=[
            ProposalSection(
                title="Overview",
                content="FlowstateAI will build an AI document automation system for Smith & Associates, focused on contract review and drafting for your corporate practice group. The system will reduce first-draft turnaround from 4 hours to 15 minutes while maintaining your firm's established language and clause preferences."
            ),
            ProposalSection(
                title="Scope",
                content="- Document ingestion pipeline (PDF, DOCX, email attachments)\n- AI contract review engine with clause extraction and risk flagging\n- First-draft generation from client intake forms\n- Firm-specific language model fine-tuned on your template library\n- Attorney review and approval workflow\n- Integration with your document management system (iManage/NetDocuments)"
            ),
            ProposalSection(
                title="Timeline",
                content="Phase 1 (Weeks 1-3): Template library audit, DMS integration, data pipeline\nPhase 2 (Weeks 4-8): AI model training on firm templates, clause library build\nPhase 3 (Weeks 9-11): Review workflow, attorney feedback loop\nPhase 4 (Week 12): Launch to corporate practice group, training sessions"
            ),
            ProposalSection(
                title="Pricing",
                content="Pilot (1 practice group): $22,000\nFirm-wide rollout: $45,000\n\nIncludes: Model retraining quarterly, 60-day post-launch support, and compliance documentation."
            ),
            ProposalSection(
                title="Terms",
                content="50% upfront, 50% at launch. Net 30 payment terms. All data remains on-premise or in firm-approved cloud. SOC 2 compliance documentation provided. Attorney-client privilege protections maintained throughout."
            ),
        ],
        customizations_applied=[
            "Legal industry compliance requirements",
            "Attorney-client privilege safeguards",
            "DMS integration (iManage/NetDocuments)",
            "Practice group pilot approach for risk mitigation",
        ]
    ),
}


async def draft_proposal(
    lead: LeadInput,
    qualification: QualificationResult,
    lead_id: str,
    api_key: str | None = None,
    revision_feedback: str | None = None,
    version: int = 1,
) -> tuple[ProposalDraft, AgentLog]:
    started = datetime.utcnow()
    t0 = time.time()

    if api_key:
        result = await _call_claude(lead, qualification, lead_id, api_key, revision_feedback, version)
    else:
        result = await _demo_response(lead, lead_id, version)

    elapsed = int((time.time() - t0) * 1000)
    log = AgentLog(
        agent_name="proposal",
        lead_id=lead_id,
        started_at=started,
        completed_at=datetime.utcnow(),
        duration_ms=elapsed,
        tokens_in=400 if api_key else 0,
        tokens_out=600 if api_key else 0,
        cost_usd=round(0.003 * (1000 / 1000), 4) if api_key else 0.0,
    )
    return result, log


async def _demo_response(lead: LeadInput, lead_id: str, version: int) -> ProposalDraft:
    await asyncio.sleep(2.5)
    if lead.company in DEMO_PROPOSALS:
        result = DEMO_PROPOSALS[lead.company].model_copy(deep=True)
        result.lead_id = lead_id
        result.proposal_version = version
        return result
    return ProposalDraft(
        lead_id=lead_id,
        proposal_version=version,
        sections=[
            ProposalSection(title="Overview", content="Demo mode: proposal generation requires live API connection."),
        ],
        customizations_applied=["demo_fallback"]
    )


async def _call_claude(
    lead: LeadInput,
    qualification: QualificationResult,
    lead_id: str,
    api_key: str,
    revision_feedback: str | None,
    version: int,
) -> ProposalDraft:
    import anthropic

    client = anthropic.AsyncAnthropic(api_key=api_key)

    revision_note = ""
    if revision_feedback:
        revision_note = f"\n\nREVISION REQUIRED. Previous review feedback:\n{revision_feedback}\nAddress all issues in this revision."

    user_msg = f"""Generate a proposal for this qualified lead:

Company: {lead.company}
Industry: {lead.industry}
Need: {lead.need}
Budget: {lead.budget}
Timeline: {lead.timeline}
Fit Score: {qualification.fit_score}
ICP Notes: {qualification.icp_match.notes}
{revision_note}

Return valid JSON with sections array (title + content for each) and customizations_applied list."""

    response = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )

    text = response.content[0].text
    start = text.find("{")
    end = text.rfind("}") + 1
    data = json.loads(text[start:end])
    data["lead_id"] = lead_id
    data["proposal_version"] = version

    return ProposalDraft(**data)
