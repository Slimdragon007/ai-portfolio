"""SQLite storage for benchmark results."""

import json
import uuid
from datetime import datetime
from pathlib import Path

import aiosqlite

from schemas import BenchmarkRun, TestResult

DB_PATH = Path(__file__).parent / "benchmark_results.db"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS runs (
                id TEXT PRIMARY KEY,
                suite TEXT NOT NULL,
                version TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                total_tests INTEGER,
                passed INTEGER,
                failed INTEGER,
                pass_rate REAL,
                avg_score REAL,
                total_cost REAL
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id TEXT PRIMARY KEY,
                run_id TEXT NOT NULL,
                test_name TEXT NOT NULL,
                passed INTEGER NOT NULL,
                score REAL NOT NULL,
                response TEXT,
                details_json TEXT,
                latency_ms INTEGER,
                tokens_in INTEGER,
                tokens_out INTEGER,
                cost_usd REAL,
                FOREIGN KEY (run_id) REFERENCES runs(id)
            )
        """)
        await db.commit()


async def save_run(run: BenchmarkRun) -> str:
    run_id = run.id or str(uuid.uuid4())[:8]
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO runs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (run_id, run.suite_name, run.version, run.timestamp.isoformat(),
             run.total_tests, run.passed, run.failed,
             run.pass_rate, run.avg_score, run.total_cost_usd)
        )
        for r in run.results:
            await db.execute(
                "INSERT INTO results VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (str(uuid.uuid4())[:8], run_id, r.test_name,
                 1 if r.passed else 0, r.score, r.response,
                 json.dumps([d.model_dump() for d in r.details]),
                 r.latency_ms, r.tokens_in, r.tokens_out, r.cost_usd)
            )
        await db.commit()
    return run_id


async def get_runs(suite: str = None) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        if suite:
            cursor = await db.execute(
                "SELECT * FROM runs WHERE suite = ? ORDER BY timestamp DESC", (suite,))
        else:
            cursor = await db.execute("SELECT * FROM runs ORDER BY timestamp DESC")
        rows = await cursor.fetchall()
        cols = ["id", "suite", "version", "timestamp", "total_tests", "passed",
                "failed", "pass_rate", "avg_score", "total_cost"]
        return [dict(zip(cols, row)) for row in rows]


async def get_results(run_id: str) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT * FROM results WHERE run_id = ? ORDER BY test_name", (run_id,))
        rows = await cursor.fetchall()
        cols = ["id", "run_id", "test_name", "passed", "score", "response",
                "details_json", "latency_ms", "tokens_in", "tokens_out", "cost_usd"]
        return [dict(zip(cols, row)) for row in rows]


async def compare_versions(suite: str, v1: str, v2: str) -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        r1 = await db.execute(
            "SELECT * FROM runs WHERE suite = ? AND version = ? ORDER BY timestamp DESC LIMIT 1",
            (suite, v1))
        r2 = await db.execute(
            "SELECT * FROM runs WHERE suite = ? AND version = ? ORDER BY timestamp DESC LIMIT 1",
            (suite, v2))
        row1 = await r1.fetchone()
        row2 = await r2.fetchone()

        if not row1 or not row2:
            return {"error": "One or both versions not found"}

        return {
            "v1": {"version": v1, "pass_rate": row1[7], "avg_score": row1[8], "cost": row1[9]},
            "v2": {"version": v2, "pass_rate": row2[7], "avg_score": row2[8], "cost": row2[9]},
            "delta_pass_rate": round(row2[7] - row1[7], 1),
            "delta_cost": round(row2[9] - row1[9], 4),
        }
