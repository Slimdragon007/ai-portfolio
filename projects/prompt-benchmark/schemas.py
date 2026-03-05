"""Pydantic models for prompt benchmark test cases and results."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class BusinessContext(BaseModel):
    name: str
    services: str = ""
    pricing: str = ""
    tone: str = "professional"
    hours: str = ""
    location: str = ""


class TestInput(BaseModel):
    message: str
    business_context: BusinessContext


class ExpectedCriteria(BaseModel):
    contains_any: list[str] = []
    contains_all: list[str] = []
    must_not_contain: list[str] = []
    intent: str = ""
    tone: str = ""
    max_words: int = 0
    min_words: int = 0


class TestCase(BaseModel):
    name: str
    input: TestInput
    expected: ExpectedCriteria


class ScoreDetail(BaseModel):
    check: str
    passed: bool
    score: float = 0.0
    detail: str = ""


class TestResult(BaseModel):
    test_name: str
    passed: bool
    score: float = Field(..., ge=0, le=100)
    response: str = ""
    details: list[ScoreDetail] = []
    latency_ms: int = 0
    tokens_in: int = 0
    tokens_out: int = 0
    cost_usd: float = 0.0


class BenchmarkRun(BaseModel):
    id: Optional[str] = None
    suite_name: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    results: list[TestResult] = []
    total_tests: int = 0
    passed: int = 0
    failed: int = 0
    pass_rate: float = 0.0
    avg_score: float = 0.0
    total_cost_usd: float = 0.0
    total_latency_ms: int = 0
