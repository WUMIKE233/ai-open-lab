"""Tiny TF-IDF retrieval for Markdown and text notes."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import math
from pathlib import Path
import re


TOKEN_PATTERN = re.compile(r"[A-Za-z0-9_]+")


@dataclass(frozen=True)
class Document:
    """A source document loaded from disk."""

    path: Path
    text: str


@dataclass(frozen=True)
class SearchResult:
    """A ranked retrieval hit."""

    path: str
    score: float
    snippet: str


def tokenize(text: str) -> list[str]:
    """Return normalized word tokens."""

    return [match.group(0).lower() for match in TOKEN_PATTERN.finditer(text)]


def load_documents(root: str | Path) -> list[Document]:
    """Load Markdown and text files from a file or directory."""

    root_path = Path(root)
    if root_path.is_file():
        candidates = [root_path]
    else:
        candidates = [
            path for path in root_path.rglob("*")
            if path.is_file() and path.suffix.lower() in {".md", ".txt"}
        ]
    return [Document(path=path, text=path.read_text(encoding="utf-8")) for path in candidates]


def _idf(document_tokens: list[list[str]]) -> dict[str, float]:
    document_count = len(document_tokens)
    document_frequency: Counter[str] = Counter()
    for tokens in document_tokens:
        document_frequency.update(set(tokens))
    return {
        token: math.log((1 + document_count) / (1 + count)) + 1
        for token, count in document_frequency.items()
    }


def _tfidf(tokens: list[str], idf: dict[str, float]) -> dict[str, float]:
    counts = Counter(tokens)
    total = sum(counts.values()) or 1
    return {token: (count / total) * idf.get(token, 0.0) for token, count in counts.items()}


def _cosine(left: dict[str, float], right: dict[str, float]) -> float:
    shared = set(left) & set(right)
    numerator = sum(left[token] * right[token] for token in shared)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    return numerator / (left_norm * right_norm)


def _snippet(text: str, query_tokens: list[str], width: int = 220) -> str:
    lowered = text.lower()
    positions = [lowered.find(token) for token in query_tokens if lowered.find(token) >= 0]
    center = min(positions) if positions else 0
    start = max(0, center - width // 3)
    end = min(len(text), start + width)
    snippet = " ".join(text[start:end].split())
    if start > 0:
        snippet = "..." + snippet
    if end < len(text):
        snippet += "..."
    return snippet


def search(root: str | Path, query: str, top_k: int = 3) -> list[SearchResult]:
    """Search documents under root and return top ranked snippets."""

    documents = load_documents(root)
    if not documents:
        return []

    tokenized_documents = [tokenize(document.text) for document in documents]
    idf = _idf(tokenized_documents + [tokenize(query)])
    document_vectors = [_tfidf(tokens, idf) for tokens in tokenized_documents]
    query_tokens = tokenize(query)
    query_vector = _tfidf(query_tokens, idf)

    ranked: list[SearchResult] = []
    for document, vector in zip(documents, document_vectors):
        score = _cosine(vector, query_vector)
        if score > 0:
            ranked.append(
                SearchResult(
                    path=str(document.path),
                    score=round(score, 4),
                    snippet=_snippet(document.text, query_tokens),
                )
            )

    ranked.sort(key=lambda item: item.score, reverse=True)
    return ranked[:top_k]
