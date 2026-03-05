# Case Study 07: Agent Pipeline
## Multi-Agent Orchestration for Lead Qualification and Proposal Generation

---

## Problem

Most "AI demos" are single-prompt tools. They take one input, call one model, return one output. That's useful, but it doesn't represent how real AI systems work in production.

Real business workflows require multiple specialized agents, structured data handoffs, quality gates, retry logic, and observable state. The question: can you build a multi-agent pipeline that runs a complete business process end-to-end, with each agent doing one job well?

---

## Architecture

```
Lead Input (Pydantic model)
    -> Qualifier Agent: scores lead against ICP criteria (0-100)
    -> Gate: score >= 60 continues, below stops pipeline
    -> Proposal Agent: drafts 5-section proposal customized to industry
    -> Reviewer Agent: QA checks for completeness, compliance, accuracy
    -> Gate: critical issues trigger revision (max 2 retries)
    -> Deliver: final state with full audit trail
```

### Key Components

1. **Pydantic Data Contracts**: every agent receives and returns validated models. No free-text handoffs. LeadInput, QualificationResult, ProposalDraft, ReviewResult, AgentLog, PipelineState.

2. **Orchestrator**: manages the pipeline flow, tracks state transitions, handles retry logic, and fires SSE events for real-time UI updates.

3. **SSE Streaming**: Server-Sent Events push each stage transition to the frontend. The dashboard updates live as agents complete their work.

4. **Dual Mode**: demo mode runs pre-scripted responses with simulated delays (works on GitHub Pages with zero backend). Live mode calls Claude API for real inference.

5. **SQLite Persistence**: every pipeline run is stored with full state, enabling stats, history, and audit.

---

## Build Details

**Stack**: Python (FastAPI, Pydantic, aiosqlite) + HTML/JS dashboard

### What Makes It Different

- **Structured agent handoffs**: agents don't pass prose to each other. They pass validated Pydantic models with typed fields. The qualifier returns a fit_score (int, 0-100), not "this lead seems good."
- **Quality gate with retry**: if the reviewer finds critical issues, the pipeline loops back to the proposal agent with specific revision feedback. Max 2 retries before escalation.
- **Observable state machine**: PipelineStatus enum tracks every transition (intake -> qualifying -> qualified -> proposing -> reviewing -> pending_approval). Every state change is logged with timestamp, duration, and cost.
- **Cost tracking**: each agent logs token usage and cost. The pipeline reports total cost across all agents, useful for production budgeting.
- **Client-side fallback**: the HTML dashboard works standalone on GitHub Pages by simulating the full pipeline in the browser when the server is unavailable.

---

## Result

- 3 demo leads run through the full pipeline: qualified restaurant (score 85), qualified law firm (score 72), disqualified auto shop (score 31)
- Pipeline completes in ~5.8 seconds (demo mode) with 3 agent stages
- Retry loop tested: reviewer feedback triggers proposal revision with specific issue references
- Dashboard shows real-time pipeline visualization, agent log, qualification scores, proposal sections, and review issues
- Zero external dependencies for the demo: works on any static host

---

## Proof

The live demo is running at the portfolio site. Click "Run Pipeline" on any of the 3 sample leads and watch the agents work. The FastAPI backend, all agent modules, and the full dashboard are open source in the repo under `projects/agent-pipeline/`.

---

[Back to Portfolio](../README.md)
