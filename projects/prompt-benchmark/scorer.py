"""Scoring logic for prompt benchmark test results."""

from schemas import ExpectedCriteria, ScoreDetail


def contains_check(response: str, criteria: ExpectedCriteria) -> ScoreDetail:
    """Check if response contains any/all required keywords."""
    response_lower = response.lower()

    if criteria.contains_all:
        missing = [w for w in criteria.contains_all if w.lower() not in response_lower]
        passed = len(missing) == 0
        return ScoreDetail(
            check="contains_all",
            passed=passed,
            score=100.0 if passed else 0.0,
            detail=f"Missing: {', '.join(missing)}" if not passed else "All keywords found",
        )

    if criteria.contains_any:
        found = [w for w in criteria.contains_any if w.lower() in response_lower]
        passed = len(found) > 0
        score = (len(found) / len(criteria.contains_any)) * 100
        return ScoreDetail(
            check="contains_any",
            passed=passed,
            score=score,
            detail=f"Found {len(found)}/{len(criteria.contains_any)}: {', '.join(found)}" if found else "No keywords found",
        )

    return ScoreDetail(check="contains", passed=True, score=100.0, detail="No keyword criteria")


def length_check(response: str, criteria: ExpectedCriteria) -> ScoreDetail:
    """Check word count bounds."""
    words = len(response.split())
    issues = []

    if criteria.max_words and words > criteria.max_words:
        issues.append(f"Too long: {words} words (max {criteria.max_words})")
    if criteria.min_words and words < criteria.min_words:
        issues.append(f"Too short: {words} words (min {criteria.min_words})")

    passed = len(issues) == 0
    score = 100.0 if passed else 50.0
    return ScoreDetail(
        check="length",
        passed=passed,
        score=score,
        detail="; ".join(issues) if issues else f"{words} words (within bounds)",
    )


def must_not_contain_check(response: str, criteria: ExpectedCriteria) -> ScoreDetail:
    """Check that forbidden phrases are absent."""
    if not criteria.must_not_contain:
        return ScoreDetail(check="must_not_contain", passed=True, score=100.0, detail="No forbidden phrases defined")

    response_lower = response.lower()
    found = [p for p in criteria.must_not_contain if p.lower() in response_lower]
    passed = len(found) == 0
    return ScoreDetail(
        check="must_not_contain",
        passed=passed,
        score=100.0 if passed else 0.0,
        detail=f"Found forbidden: {', '.join(found)}" if found else "Clean",
    )


def intent_match(response: str, criteria: ExpectedCriteria) -> ScoreDetail:
    """Simple intent classification based on keywords."""
    if not criteria.intent:
        return ScoreDetail(check="intent", passed=True, score=100.0, detail="No intent criteria")

    intent_keywords = {
        "pricing": ["price", "cost", "$", "rate", "fee", "starting at", "from"],
        "availability": ["hours", "open", "closed", "available", "book", "appointment", "schedule"],
        "complaint": ["sorry", "apologize", "understand", "feedback", "concern", "resolve"],
        "info": ["offer", "provide", "service", "located", "find us", "welcome"],
        "deflect": ["unable", "cannot", "don't", "spam", "inappropriate"],
    }

    response_lower = response.lower()
    expected = criteria.intent.lower()
    keywords = intent_keywords.get(expected, [])

    if not keywords:
        return ScoreDetail(check="intent", passed=True, score=75.0, detail=f"Unknown intent category: {expected}")

    matches = sum(1 for k in keywords if k in response_lower)
    score = min(100.0, (matches / max(len(keywords) * 0.3, 1)) * 100)
    passed = score >= 50

    return ScoreDetail(
        check="intent",
        passed=passed,
        score=score,
        detail=f"Intent '{expected}': {matches} keyword matches, score {score:.0f}",
    )


def tone_check_local(response: str, criteria: ExpectedCriteria) -> ScoreDetail:
    """Local tone estimation (no API call). Rough heuristic."""
    if not criteria.tone:
        return ScoreDetail(check="tone", passed=True, score=100.0, detail="No tone criteria")

    tone = criteria.tone.lower()
    response_lower = response.lower()

    if tone == "friendly":
        friendly_signals = ["!", "happy to", "glad", "welcome", "love", "great", "wonderful", "excited"]
        matches = sum(1 for s in friendly_signals if s in response_lower)
        score = min(100.0, matches * 25)
    elif tone == "professional":
        pro_signals = ["please", "thank", "assist", "happy to help", "regarding"]
        matches = sum(1 for s in pro_signals if s in response_lower)
        score = min(100.0, matches * 30)
    elif tone == "empathetic":
        emp_signals = ["understand", "sorry", "appreciate", "hear", "concern", "frustrat"]
        matches = sum(1 for s in emp_signals if s in response_lower)
        score = min(100.0, matches * 30)
    else:
        score = 75.0

    passed = score >= 50
    return ScoreDetail(
        check="tone",
        passed=passed,
        score=score,
        detail=f"Tone '{tone}': score {score:.0f}/100",
    )


def score_response(response: str, criteria: ExpectedCriteria) -> tuple[float, bool, list[ScoreDetail]]:
    """Run all scoring checks and return (overall_score, passed, details)."""
    checks = [
        contains_check(response, criteria),
        length_check(response, criteria),
        must_not_contain_check(response, criteria),
        intent_match(response, criteria),
        tone_check_local(response, criteria),
    ]

    weights = {
        "contains_any": 25, "contains_all": 25, "contains": 0,
        "length": 15, "must_not_contain": 20,
        "intent": 25, "tone": 15,
    }

    total_weight = 0
    weighted_score = 0
    for c in checks:
        w = weights.get(c.check, 10)
        if c.detail == "No keyword criteria" or c.detail.startswith("No "):
            continue
        weighted_score += c.score * w
        total_weight += w

    overall = weighted_score / max(total_weight, 1)
    passed = overall >= 60 and all(c.passed for c in checks if c.check == "must_not_contain")

    return round(overall, 1), passed, checks
