"""Command-line interface for AI Open Lab."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from ai_open_lab.prompt_eval import (
    apply_average_score_gate,
    evaluate_cases,
    filter_report_results,
    load_cases,
    render_markdown_report,
)
from ai_open_lab.rag import search
from ai_open_lab.safety import risk_level, scan_text


def _eval_prompts(args: argparse.Namespace) -> int:
    report = evaluate_cases(load_cases(args.cases))
    report = apply_average_score_gate(report, min_average_score=args.min_average_score)
    display_report = filter_report_results(report, failures_only=args.failures_only)
    if args.format == "markdown":
        print(render_markdown_report(display_report))
    else:
        print(json.dumps(display_report, indent=2, ensure_ascii=False))
    return 0 if report["failed"] == 0 and report["score_gate_passed"] else 1


def _rag_search(args: argparse.Namespace) -> int:
    results = search(args.path, args.query, top_k=args.top_k)
    print(json.dumps([result.__dict__ for result in results], indent=2, ensure_ascii=False))
    return 0


def _safety_scan(args: argparse.Namespace) -> int:
    text = args.text
    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    findings = scan_text(text)
    report = {
        "risk_level": risk_level(findings),
        "finding_count": len(findings),
        "findings": [finding.__dict__ for finding in findings],
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["risk_level"] in {"none", "low"} else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ai-open-lab", description="Local-first AI utility demos.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    eval_parser = subparsers.add_parser("eval-prompts", help="Evaluate JSONL prompt test cases.")
    eval_parser.add_argument("cases", help="Path to JSONL prompt cases.")
    eval_parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="json",
        help="Output format for the evaluation report.",
    )
    eval_parser.add_argument(
        "--failures-only",
        action="store_true",
        help="Only display failed cases while preserving the full summary counts.",
    )
    eval_parser.add_argument(
        "--min-average-score",
        type=float,
        default=0.0,
        help="Fail when the full report average score is below this 0.0-1.0 threshold.",
    )
    eval_parser.set_defaults(func=_eval_prompts)

    rag_parser = subparsers.add_parser("rag-search", help="Search Markdown/text notes with tiny TF-IDF retrieval.")
    rag_parser.add_argument("path", help="File or directory to search.")
    rag_parser.add_argument("query", help="Search query.")
    rag_parser.add_argument("--top-k", type=int, default=3, help="Number of results to return.")
    rag_parser.set_defaults(func=_rag_search)

    safety_parser = subparsers.add_parser("safety-scan", help="Scan text for prompt and agent safety risks.")
    safety_parser.add_argument("text", nargs="?", default="", help="Text to scan.")
    safety_parser.add_argument("--file", help="Read text from a UTF-8 file.")
    safety_parser.set_defaults(func=_safety_scan)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
