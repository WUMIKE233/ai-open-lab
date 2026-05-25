"""Small JSONL prompt evaluation helpers."""

from __future__ import annotations

from dataclasses import dataclass
import json
import re
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class PromptCase:
    """A single prompt evaluation fixture."""

    case_id: str
    prompt: str
    response: str
    expected_keywords: tuple[str, ...] = ()
    forbidden_keywords: tuple[str, ...] = ()
    expected_regex: tuple[str, ...] = ()


@dataclass(frozen=True)
class PromptResult:
    """Result for one prompt case."""

    case_id: str
    passed: bool
    score: float
    missing_keywords: tuple[str, ...]
    forbidden_hits: tuple[str, ...]
    missing_regex: tuple[str, ...]


def _as_tuple(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    if isinstance(value, Iterable):
        return tuple(str(item) for item in value)
    raise TypeError(f"Expected string or list of strings, got {type(value).__name__}")


def load_cases(path: str | Path) -> list[PromptCase]:
    """Load prompt cases from a JSONL file."""

    cases: list[PromptCase] = []
    source = Path(path)
    for line_number, raw_line in enumerate(source.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        data = json.loads(line)
        case_id = str(data.get("id") or f"case-{line_number}")
        cases.append(
            PromptCase(
                case_id=case_id,
                prompt=str(data.get("prompt", "")),
                response=str(data.get("response", "")),
                expected_keywords=_as_tuple(data.get("expected_keywords")),
                forbidden_keywords=_as_tuple(data.get("forbidden_keywords")),
                expected_regex=_as_tuple(data.get("expected_regex")),
            )
        )
    return cases


def evaluate_case(case: PromptCase) -> PromptResult:
    """Evaluate one case with deterministic keyword and regex checks."""

    response_lower = case.response.lower()
    missing_keywords = tuple(
        keyword for keyword in case.expected_keywords if keyword.lower() not in response_lower
    )
    forbidden_hits = tuple(
        keyword for keyword in case.forbidden_keywords if keyword.lower() in response_lower
    )
    missing_regex = tuple(
        pattern for pattern in case.expected_regex if re.search(pattern, case.response, re.IGNORECASE) is None
    )

    total_checks = (
        len(case.expected_keywords)
        + len(case.forbidden_keywords)
        + len(case.expected_regex)
    )
    failures = len(missing_keywords) + len(forbidden_hits) + len(missing_regex)
    score = 1.0 if total_checks == 0 else max(0.0, (total_checks - failures) / total_checks)

    return PromptResult(
        case_id=case.case_id,
        passed=failures == 0,
        score=round(score, 4),
        missing_keywords=missing_keywords,
        forbidden_hits=forbidden_hits,
        missing_regex=missing_regex,
    )


def evaluate_cases(cases: Iterable[PromptCase]) -> dict[str, Any]:
    """Evaluate many cases and return a JSON-serializable report."""

    results = [evaluate_case(case) for case in cases]
    passed = sum(1 for result in results if result.passed)
    total = len(results)
    average_score = 0.0 if total == 0 else sum(result.score for result in results) / total

    return {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "average_score": round(average_score, 4),
        "results": [
            {
                "id": result.case_id,
                "passed": result.passed,
                "score": result.score,
                "missing_keywords": list(result.missing_keywords),
                "forbidden_hits": list(result.forbidden_hits),
                "missing_regex": list(result.missing_regex),
            }
            for result in results
        ],
    }
