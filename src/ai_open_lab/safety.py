"""Rule-based prompt and agent safety scanner."""

from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class SafetyRule:
    """A rule used by the prompt safety scanner."""

    rule_id: str
    category: str
    severity: str
    pattern: re.Pattern[str]
    message: str


@dataclass(frozen=True)
class Finding:
    """One safety scanner finding."""

    rule_id: str
    category: str
    severity: str
    message: str
    match: str


RULES: tuple[SafetyRule, ...] = (
    SafetyRule(
        "override-instructions",
        "prompt-injection",
        "high",
        re.compile(r"\b(ignore|forget|bypass|override)\b.{0,40}\b(instruction|policy|rule|system)\b", re.I),
        "Text appears to request overriding higher-priority instructions.",
    ),
    SafetyRule(
        "secret-exfiltration",
        "data-exfiltration",
        "high",
        re.compile(r"\b(api[_ -]?key|token|password|secret|credential|private key)\b", re.I),
        "Text asks for or references sensitive credentials.",
    ),
    SafetyRule(
        "system-prompt-request",
        "prompt-injection",
        "medium",
        re.compile(r"\b(system prompt|developer message|hidden instruction|internal instruction)\b", re.I),
        "Text asks for hidden or internal instructions.",
    ),
    SafetyRule(
        "tool-misuse",
        "tool-safety",
        "medium",
        re.compile(r"\b(run|execute|download|upload|curl|powershell|cmd\.exe)\b.{0,60}\b(silent|without asking|no approval|background)\b", re.I),
        "Text may be attempting unsafe tool execution.",
    ),
    SafetyRule(
        "url-exfiltration",
        "data-exfiltration",
        "medium",
        re.compile(r"\b(send|post|upload|exfiltrate)\b.{0,80}\b(http://|https://|webhook|pastebin)\b", re.I),
        "Text may be attempting to send data to an external URL.",
    ),
)


def scan_text(text: str) -> list[Finding]:
    """Scan text and return ordered findings."""

    findings: list[Finding] = []
    for rule in RULES:
        for match in rule.pattern.finditer(text):
            findings.append(
                Finding(
                    rule_id=rule.rule_id,
                    category=rule.category,
                    severity=rule.severity,
                    message=rule.message,
                    match=match.group(0),
                )
            )
    return findings


def risk_level(findings: list[Finding]) -> str:
    """Summarize findings into a coarse risk level."""

    severities = {finding.severity for finding in findings}
    if "high" in severities:
        return "high"
    if "medium" in severities:
        return "medium"
    if findings:
        return "low"
    return "none"
