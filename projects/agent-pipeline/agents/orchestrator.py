import uuid
from datetime import datetime

from .schemas import (
    LeadInput, PipelineState, PipelineStatus
)
from .qualifier import qualify_lead
from .proposal import draft_proposal
from .reviewer import review_proposal

MAX_RETRIES = 2


async def run_pipeline(
    lead: LeadInput,
    api_key: str | None = None,
    on_stage: callable = None,
) -> PipelineState:
    """Run the full agent pipeline for a lead.

    on_stage: optional async callback(state, stage_name, detail_dict)
    called at each stage transition for real-time UI updates.
    """
    lead_id = str(uuid.uuid4())[:8]
    state = PipelineState(lead_id=lead_id, lead_input=lead)

    async def notify(stage: str, detail: dict = None):
        if on_stage:
            await on_stage(state, stage, detail or {})

    # Stage 1: Qualify
    state.status = PipelineStatus.qualifying
    state.updated_at = datetime.utcnow()
    await notify("qualifying", {"agent": "qualifier", "input": lead.model_dump()})

    try:
        qual_result, qual_log = await qualify_lead(lead, lead_id, api_key)
        state.qualification = qual_result
        state.agent_logs.append(qual_log)
        state.total_cost_usd += qual_log.cost_usd
    except Exception as e:
        state.status = PipelineStatus.error
        state.updated_at = datetime.utcnow()
        await notify("error", {"agent": "qualifier", "error": str(e)})
        return state

    await notify("qualified", {
        "agent": "qualifier",
        "output": qual_result.model_dump(),
    })

    if not qual_result.qualified:
        state.status = PipelineStatus.disqualified
        state.updated_at = datetime.utcnow()
        state.total_duration_ms = sum(l.duration_ms for l in state.agent_logs)
        await notify("disqualified", {"reason": qual_result.reasoning})
        return state

    state.status = PipelineStatus.qualified
    state.updated_at = datetime.utcnow()

    # Stage 2: Propose (with retry loop)
    revision_feedback = None
    version = 1

    for attempt in range(1 + MAX_RETRIES):
        state.status = PipelineStatus.proposing
        state.updated_at = datetime.utcnow()
        await notify("proposing", {
            "agent": "proposal",
            "version": version,
            "retry": attempt > 0,
        })

        try:
            proposal, prop_log = await draft_proposal(
                lead, qual_result, lead_id, api_key,
                revision_feedback=revision_feedback,
                version=version,
            )
            state.proposal = proposal
            state.agent_logs.append(prop_log)
            state.total_cost_usd += prop_log.cost_usd
        except Exception as e:
            state.status = PipelineStatus.error
            state.updated_at = datetime.utcnow()
            await notify("error", {"agent": "proposal", "error": str(e)})
            return state

        await notify("proposed", {
            "agent": "proposal",
            "output": {"version": version, "sections": len(proposal.sections)},
        })

        # Stage 3: Review
        state.status = PipelineStatus.reviewing
        state.updated_at = datetime.utcnow()
        await notify("reviewing", {"agent": "reviewer"})

        try:
            review, rev_log = await review_proposal(
                proposal, lead_id, api_key,
                company_name=lead.company,
            )
            state.review = review
            state.agent_logs.append(rev_log)
            state.total_cost_usd += rev_log.cost_usd
        except Exception as e:
            state.status = PipelineStatus.error
            state.updated_at = datetime.utcnow()
            await notify("error", {"agent": "reviewer", "error": str(e)})
            return state

        await notify("reviewed", {
            "agent": "reviewer",
            "output": review.model_dump(),
        })

        if not review.revision_required:
            break

        # Revision needed
        state.retries += 1
        version += 1
        issues_text = "; ".join(
            f"[{i.severity}] {i.section}: {i.detail}"
            for i in review.issues
        )
        revision_feedback = f"Issues found: {issues_text}"
        await notify("revision_needed", {
            "attempt": attempt + 1,
            "feedback": revision_feedback,
        })

    # Final status
    state.status = PipelineStatus.pending_approval
    state.updated_at = datetime.utcnow()
    state.total_duration_ms = sum(l.duration_ms for l in state.agent_logs)
    state.total_cost_usd = round(state.total_cost_usd, 4)
    await notify("pending_approval", {
        "total_duration_ms": state.total_duration_ms,
        "total_cost_usd": state.total_cost_usd,
    })

    return state
