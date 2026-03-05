#!/usr/bin/env python3
"""
Prompt Benchmark Suite CLI
Run, compare, and export prompt test results.

Usage:
    python benchmark.py run --suite tests/meta-responder.yaml --version v2.0
    python benchmark.py compare --suite meta-responder --v1 v1.0 --v2 v2.0
    python benchmark.py export --format csv --output results.csv
"""

import argparse
import asyncio
import csv
import json
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path

import yaml

from schemas import (
    TestCase, TestInput, BusinessContext, ExpectedCriteria,
    TestResult, BenchmarkRun, ScoreDetail,
)
from scorer import score_response
from storage import init_db, save_run, get_runs, get_results, compare_versions


def load_suite(path: str) -> tuple[str, list[TestCase]]:
    """Load test suite from YAML file."""
    with open(path) as f:
        data = yaml.safe_load(f)

    suite_name = data.get("suite", Path(path).stem)
    tests = []
    for t in data.get("tests", []):
        ctx = t["input"]["business_context"]
        test = TestCase(
            name=t["name"],
            input=TestInput(
                message=t["input"]["message"],
                business_context=BusinessContext(**ctx),
            ),
            expected=ExpectedCriteria(**t["expected"]),
        )
        tests.append(test)
    return suite_name, tests


async def run_suite(suite_path: str, version: str, api_key: str = None):
    """Run a test suite and store results."""
    await init_db()
    suite_name, tests = load_suite(suite_path)

    print(f"Running suite: {suite_name} (version {version})")
    print(f"Tests: {len(tests)}")
    print("-" * 50)

    results = []
    for test in tests:
        t0 = time.time()

        if api_key:
            response = await call_claude(test, api_key)
        else:
            response = generate_demo_response(test)

        latency = int((time.time() - t0) * 1000)
        overall, passed, details = score_response(response, test.expected)

        result = TestResult(
            test_name=test.name,
            passed=passed,
            score=overall,
            response=response,
            details=details,
            latency_ms=latency,
            tokens_in=0,
            tokens_out=0,
            cost_usd=0.0,
        )
        results.append(result)

        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {test.name}: {overall:.0f}/100")

    passed_count = sum(1 for r in results if r.passed)
    run = BenchmarkRun(
        id=str(uuid.uuid4())[:8],
        suite_name=suite_name,
        version=version,
        results=results,
        total_tests=len(results),
        passed=passed_count,
        failed=len(results) - passed_count,
        pass_rate=round(passed_count / len(results) * 100, 1),
        avg_score=round(sum(r.score for r in results) / len(results), 1),
        total_cost_usd=sum(r.cost_usd for r in results),
    )

    run_id = await save_run(run)
    print("-" * 50)
    print(f"Results: {run.passed}/{run.total_tests} passed ({run.pass_rate}%)")
    print(f"Avg score: {run.avg_score}")
    print(f"Run ID: {run_id}")


def generate_demo_response(test: TestCase) -> str:
    """Generate a realistic demo response for testing scoring logic."""
    ctx = test.input.business_context
    intent = test.expected.intent

    if intent == "pricing":
        return f"Thanks for reaching out! At {ctx.name}, {ctx.pricing}. We'd love to help you find the right option. Feel free to call or message us to book!"
    elif intent == "availability":
        hours = ctx.hours or "Please call us for current hours."
        return f"Great question! Our hours are {hours}. We'd be happy to help you schedule a visit. Just let us know what works for you!"
    elif intent == "complaint":
        return f"We're so sorry to hear about your experience. That's not the standard we hold ourselves to at {ctx.name}. We'd love the chance to make this right. Could you send us your contact info so our manager can reach out directly?"
    elif intent == "info":
        loc = f" We're located at {ctx.location}." if ctx.location else ""
        return f"Welcome! At {ctx.name}, we offer {ctx.services}.{loc} Let us know if you have any other questions. We're happy to help!"
    elif intent == "deflect":
        return f"Thanks for your message! If you have questions about our services at {ctx.name}, we're happy to help."
    else:
        return f"Thanks for reaching out to {ctx.name}! We'd be happy to assist. Could you tell us more about what you're looking for?"


async def call_claude(test: TestCase, api_key: str) -> str:
    """Call Claude API with the test case."""
    import anthropic

    client = anthropic.AsyncAnthropic(api_key=api_key)
    ctx = test.input.business_context

    system_prompt = f"""You are a helpful business assistant for {ctx.name}.
Business: {ctx.services}
Pricing: {ctx.pricing}
Hours: {ctx.hours}
Location: {ctx.location}
Tone: {ctx.tone}

Draft a reply to this customer message. Be concise, on-brand, and helpful.
Never reveal you are an AI or language model."""

    response = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=200,
        system=system_prompt,
        messages=[{"role": "user", "content": test.input.message}],
    )
    return response.content[0].text


async def cmd_compare(suite: str, v1: str, v2: str):
    await init_db()
    result = await compare_versions(suite, v1, v2)
    if "error" in result:
        print(f"Error: {result['error']}")
        return
    print(f"Comparison: {v1} vs {v2}")
    print(f"  {v1}: {result['v1']['pass_rate']}% pass, ${result['v1']['cost']:.4f} cost")
    print(f"  {v2}: {result['v2']['pass_rate']}% pass, ${result['v2']['cost']:.4f} cost")
    print(f"  Delta: {result['delta_pass_rate']:+.1f}% pass rate, ${result['delta_cost']:+.4f} cost")


async def cmd_export(fmt: str, output: str):
    await init_db()
    runs = await get_runs()
    if fmt == "csv":
        with open(output, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=runs[0].keys() if runs else [])
            writer.writeheader()
            writer.writerows(runs)
        print(f"Exported {len(runs)} runs to {output}")
    else:
        with open(output, "w") as f:
            json.dump(runs, f, indent=2, default=str)
        print(f"Exported {len(runs)} runs to {output}")


def main():
    parser = argparse.ArgumentParser(description="Prompt Benchmark Suite")
    sub = parser.add_subparsers(dest="command")

    run_p = sub.add_parser("run", help="Run a test suite")
    run_p.add_argument("--suite", required=True, help="Path to YAML test suite")
    run_p.add_argument("--version", required=True, help="Prompt version label")
    run_p.add_argument("--api-key", help="Claude API key (demo mode if omitted)")

    cmp_p = sub.add_parser("compare", help="Compare two versions")
    cmp_p.add_argument("--suite", required=True, help="Suite name")
    cmp_p.add_argument("--v1", required=True, help="First version")
    cmp_p.add_argument("--v2", required=True, help="Second version")

    exp_p = sub.add_parser("export", help="Export results")
    exp_p.add_argument("--format", choices=["csv", "json"], default="csv")
    exp_p.add_argument("--output", required=True, help="Output file path")

    args = parser.parse_args()

    if args.command == "run":
        asyncio.run(run_suite(args.suite, args.version, args.api_key))
    elif args.command == "compare":
        asyncio.run(cmd_compare(args.suite, args.v1, args.v2))
    elif args.command == "export":
        asyncio.run(cmd_export(args.format, args.output))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
