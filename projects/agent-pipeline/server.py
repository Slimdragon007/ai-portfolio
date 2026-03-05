"""
FlowstateAI Agent Pipeline - FastAPI Server
Endpoints for running multi-agent lead qualification, proposal, and review.
"""

import asyncio
import json
import os
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

import aiosqlite
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from agents.schemas import LeadInput, PipelineState, PipelineStatus
from agents.orchestrator import run_pipeline

DB_PATH = Path(__file__).parent / "db" / "pipeline.db"


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

async def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS pipeline_runs (
                lead_id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                lead_input TEXT NOT NULL,
                state_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        await db.commit()


async def save_state(state: PipelineState):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO pipeline_runs (lead_id, status, lead_input, state_json, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(lead_id) DO UPDATE SET
                status = excluded.status,
                state_json = excluded.state_json,
                updated_at = excluded.updated_at
        """, (
            state.lead_id,
            state.status.value,
            state.lead_input.model_dump_json(),
            state.model_dump_json(),
            state.created_at.isoformat(),
            state.updated_at.isoformat(),
        ))
        await db.commit()


async def load_state(lead_id: str) -> PipelineState | None:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT state_json FROM pipeline_runs WHERE lead_id = ?",
            (lead_id,)
        )
        row = await cursor.fetchone()
        if row:
            return PipelineState.model_validate_json(row[0])
        return None


async def load_all_runs() -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT lead_id, status, lead_input, created_at, updated_at FROM pipeline_runs ORDER BY created_at DESC"
        )
        rows = await cursor.fetchall()
        results = []
        for row in rows:
            results.append({
                "lead_id": row[0],
                "status": row[1],
                "lead_input": json.loads(row[2]),
                "created_at": row[3],
                "updated_at": row[4],
            })
        return results


async def get_stats() -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM pipeline_runs")
        total = (await cursor.fetchone())[0]

        cursor = await db.execute(
            "SELECT COUNT(*) FROM pipeline_runs WHERE status = ?",
            (PipelineStatus.pending_approval.value,)
        )
        approved = (await cursor.fetchone())[0]

        cursor = await db.execute(
            "SELECT COUNT(*) FROM pipeline_runs WHERE status = ?",
            (PipelineStatus.disqualified.value,)
        )
        disqualified = (await cursor.fetchone())[0]

        cursor = await db.execute(
            "SELECT COUNT(*) FROM pipeline_runs WHERE status = ?",
            (PipelineStatus.error.value,)
        )
        errors = (await cursor.fetchone())[0]

        cursor = await db.execute("SELECT state_json FROM pipeline_runs")
        rows = await cursor.fetchall()
        total_cost = 0.0
        total_duration = 0
        for row in rows:
            s = json.loads(row[0])
            total_cost += s.get("total_cost_usd", 0)
            total_duration += s.get("total_duration_ms", 0)

        return {
            "total_runs": total,
            "pending_approval": approved,
            "disqualified": disqualified,
            "errors": errors,
            "total_cost_usd": round(total_cost, 4),
            "avg_duration_ms": round(total_duration / max(total, 1)),
        }


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="FlowstateAI Agent Pipeline", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------

class RunRequest(BaseModel):
    lead: LeadInput
    api_key: str | None = None


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.post("/pipeline/run")
async def pipeline_run(req: RunRequest):
    """Run pipeline and stream stage events via SSE."""
    queue: asyncio.Queue = asyncio.Queue()

    async def on_stage(state: PipelineState, stage: str, detail: dict):
        await save_state(state)
        await queue.put({
            "stage": stage,
            "status": state.status.value,
            "detail": detail,
            "lead_id": state.lead_id,
            "timestamp": datetime.utcnow().isoformat(),
        })

    async def run_and_finish():
        try:
            final_state = await run_pipeline(
                lead=req.lead,
                api_key=req.api_key,
                on_stage=on_stage,
            )
            await save_state(final_state)
            await queue.put({
                "stage": "complete",
                "status": final_state.status.value,
                "detail": final_state.model_dump(mode="json"),
                "lead_id": final_state.lead_id,
                "timestamp": datetime.utcnow().isoformat(),
            })
        except Exception as e:
            await queue.put({
                "stage": "error",
                "status": "error",
                "detail": {"error": str(e)},
                "lead_id": "unknown",
                "timestamp": datetime.utcnow().isoformat(),
            })
        finally:
            await queue.put(None)

    task = asyncio.create_task(run_and_finish())

    async def event_stream():
        while True:
            event = await queue.get()
            if event is None:
                break
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/pipeline/status/{lead_id}")
async def pipeline_status(lead_id: str):
    state = await load_state(lead_id)
    if not state:
        raise HTTPException(status_code=404, detail="Lead not found")
    return state.model_dump(mode="json")


@app.get("/pipeline/leads")
async def pipeline_leads():
    return await load_all_runs()


@app.get("/pipeline/stats")
async def pipeline_stats():
    return await get_stats()


@app.get("/health")
async def health():
    return {"status": "ok", "service": "flowstateai-agent-pipeline"}
