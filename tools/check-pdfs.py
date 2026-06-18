#!/usr/bin/env python3
"""Lightweight PDF anonymity checks for reviewer-facing files."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PDFS = [ROOT / "static/pdfs/paper.pdf", ROOT / "static/pdfs/supplementary.pdf"]
TERM_FILE = ROOT / "tools/anonymity_terms.txt"

PATTERNS = [
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    re.compile(r"/Users/[A-Za-z0-9._-]+"),
    re.compile(r"/home/[A-Za-z0-9._-]+"),
    re.compile(r"github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", re.I),
    re.compile(r"overleaf\.com/project/[A-Za-z0-9]+", re.I),
]


def load_terms() -> list[str]:
    if not TERM_FILE.exists():
        return []
    terms: list[str] = []
    for raw in TERM_FILE.read_text(encoding="utf-8").splitlines():
        term = raw.strip()
        if term and not term.startswith("#"):
            terms.append(term.lower())
    return terms


def main() -> int:
    try:
        from pypdf import PdfReader
    except Exception as exc:  # pragma: no cover - environment guard
        print(f"warning: could not import pypdf; skipped PDF text checks: {exc}", file=sys.stderr)
        return 0

    terms = load_terms()
    status = 0

    for pdf in PDFS:
        if not pdf.exists():
            continue
        reader = PdfReader(str(pdf))
        metadata = reader.metadata or {}
        metadata_text = "\n".join(f"{key}: {value}" for key, value in metadata.items() if value)
        page_text = "\n".join((page.extract_text() or "") for page in reader.pages)
        combined = f"{metadata_text}\n{page_text}"
        lower = combined.lower()

        for pattern in PATTERNS:
            if pattern.search(combined):
                print(f"{pdf}: leak pattern matched: {pattern.pattern}", file=sys.stderr)
                status = 1

        for term in terms:
            if term in lower:
                print(f"{pdf}: sensitive term matched: {term}", file=sys.stderr)
                status = 1

        for key in ("/Author", "/Creator", "/Producer"):
            value = metadata.get(key)
            if value and key == "/Author":
                print(f"{pdf}: non-empty author metadata: {value}", file=sys.stderr)
                status = 1

    return status


if __name__ == "__main__":
    raise SystemExit(main())
