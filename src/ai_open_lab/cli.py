"""Command-line interface for AI Open Lab."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from ai_open_lab.prompt_eval import evaluate_cases, load_cases
from ai_open_lab.rag import search
from ai_open_lab.safety import risk_level, scan_text


def _eval_prompts(args: argparse.Namespace) -> int:
    report = evaluate_cases(load_cases(args.cases))
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["failed"] == 0 else 1


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
