# Case Study 08: Prompt Benchmark Suite
## Systematic Prompt Testing, Scoring, and Version Comparison

---

## Problem

Prompt engineering is trial and error for most teams. You tweak a system prompt, test it manually on 2-3 inputs, and ship it. When something breaks in production, you have no idea which version caused the regression, no baseline to compare against, and no scoring data to back up your decisions.

The question: can you build a repeatable testing framework for prompts the same way engineers test code?

---

## Architecture

```
YAML Test Suite (cases + expected criteria)
    -> CLI Runner: loads suite, executes each case (demo or live Claude API)
    -> Scorer: 5-dimension evaluation (contains, length, blocklist, intent, tone)
    -> SQLite Storage: persists every run with full detail
    -> Dashboard: Chart.js visualization, filterable results, version comparison
```

### Key Components

1. **YAML Test Suites**: declarative test cases with business context, expected criteria, and scoring rules. Human-readable, version-controllable.

2. **Multi-Dimension Scorer**: five independent checks (contains_check, length_check, must_not_contain, intent_match, tone_check) each returning pass/fail with weighted contribution to an overall 0-100 score.

3. **Version Comparison**: run the same suite against different prompt versions. Compare pass rates, average scores, and cost deltas. Detect regressions before they hit production.

4. **Pydantic Data Contracts**: TestCase, TestResult, BenchmarkRun, ScoreDetail models enforce typed data flow from test definition through scoring to storage.

5. **Dual Mode**: demo mode generates realistic responses locally (no API key needed). Live mode calls Claude API and tracks token usage and cost.

---

## Build Details

**Stack**: Python (Pydantic, aiosqlite, PyYAML, Anthropic SDK) + HTML/JS dashboard (Chart.js)

### What Makes It Different

- **Declarative test suites**: tests are data, not code. A YAML file defines 12 test cases across 5 intent categories (pricing, availability, complaint, info, deflect). Adding a test takes 10 lines of YAML.
- **Weighted scoring**: each dimension contributes to the overall score with configurable weights. Contains check (30%), length check (15%), blocklist (20%), intent match (20%), tone match (15%). A response can partially pass.
- **Regression detection**: the dashboard highlights version-over-version changes. v1.1 improved pass rate from 67% to 83% but introduced a tone regression on complaint handling. v2.0 fixed the regression and cut cost by 50%.
- **Three visualization modes**: pass rate comparison, average score trends, and cost tracking across versions. Toggle between views with one click.
- **CLI + dashboard**: engineers use the CLI for CI/CD integration. Stakeholders use the dashboard for visual analysis. Same data, different interfaces.

---

## Result

- 12 test cases across 5 intent categories (pricing, availability, complaint, info, edge cases)
- 3 prompt versions benchmarked: v1.0 (67% pass), v1.1 (83% pass), v2.0 (92% pass, recommended)
- Caught a tone regression in v1.1 (complaint responses lost empathetic tone)
- Dashboard shows pass rate, score distribution, and cost trends in interactive charts
- Full CLI with run, compare, and export commands

---

## Proof

The live dashboard is running at the portfolio site with pre-loaded demo data for all 3 versions. The Python CLI, scorer, storage layer, and YAML test suite are open source in the repo under `projects/prompt-benchmark/`.

---

[Back to Portfolio](../README.md)
