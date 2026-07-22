#!/usr/bin/env python3
"""
Count words, lines, and estimate page count for the entire textbook.

Scans all chapter markdown files, strips YAML frontmatter and code blocks,
then counts CJK characters and English words separately.

Usage:
    python scripts/word_count.py
    python scripts/word_count.py --json
"""

import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHAPTERS_DIR = PROJECT_ROOT / "chapters"

# Match CJK Unified Ideographs and common CJK punctuation
CJK_CHAR_PATTERN = re.compile(
    r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff\u2e80-\u2eff\u3000-\u303f\uff00-\uffef]"
)

# Match English words (sequences of ASCII letters)
EN_WORD_PATTERN = re.compile(r"[a-zA-Z]+")

# Match fenced code blocks to optionally exclude
CODE_BLOCK_PATTERN = re.compile(r"```[\s\S]*?```", re.MULTILINE)

# Words per page estimation (mixed CJK + English, typical textbook density)
WORDS_PER_PAGE = 350
CHARS_PER_PAGE = 700


def strip_frontmatter(text: str) -> str:
    """Remove YAML frontmatter block."""
    if not text.startswith("---"):
        return text
    end = text.find("---", 3)
    if end == -1:
        return text
    return text[end + 3 :]


def strip_code_blocks(text: str) -> str:
    """Remove fenced code blocks (optional, for body-text-only counts)."""
    return CODE_BLOCK_PATTERN.sub("", text)


def count_text(text: str, exclude_code: bool = True) -> dict:
    """Count CJK characters and English words in text."""
    cleaned = strip_frontmatter(text)
    if exclude_code:
        cleaned = strip_code_blocks(cleaned)

    cjk_chars = len(CJK_CHAR_PATTERN.findall(cleaned))
    en_words = len(EN_WORD_PATTERN.findall(cleaned))
    lines = cleaned.count("\n") + 1

    return {
        "cjk_chars": cjk_chars,
        "en_words": en_words,
        "lines": lines,
        "total_words_equiv": cjk_chars + en_words,
    }


def main() -> None:
    as_json = "--json" in sys.argv

    if not CHAPTERS_DIR.exists():
        print(f"ERROR: Chapters directory not found: {CHAPTERS_DIR}")
        sys.exit(1)

    chapter_files = sorted(CHAPTERS_DIR.glob("*.md"))

    total_cjk = 0
    total_en = 0
    total_lines = 0
    per_chapter: list[dict] = []

    for fpath in chapter_files:
        stats = count_text(fpath.read_text(encoding="utf-8"), exclude_code=True)
        total_cjk += stats["cjk_chars"]
        total_en += stats["en_words"]
        total_lines += stats["lines"]
        per_chapter.append({"file": fpath.name, **stats})

    total_equiv = total_cjk + total_en
    est_pages_body = total_equiv / WORDS_PER_PAGE
    est_pages_cjk = total_cjk / CHARS_PER_PAGE
    # Weighted average: CJK chars take more space than English words
    est_pages = est_pages_cjk * 0.6 + est_pages_body * 0.4

    if as_json:
        result = {
            "total_cjk_chars": total_cjk,
            "total_en_words": total_en,
            "total_lines": total_lines,
            "total_word_equivalent": total_equiv,
            "estimated_pages": round(est_pages, 1),
            "chapters": per_chapter,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("## Textbook Word Count")
        print()
        print(f"| Metric | Value |")
        print(f"|---|---|")
        print(f"| Total chapters | {len(chapter_files)} |")
        print(f"| CJK characters | {total_cjk:,} |")
        print(f"| English words | {total_en:,} |")
        print(f"| Word equivalent (CJK + EN) | {total_equiv:,} |")
        print(f"| Total lines | {total_lines:,} |")
        print(f"| Estimated pages | ~{est_pages:.0f} |")
        print()

        # Per-chapter breakdown
        print("### Per-Chapter Breakdown")
        print()
        print("| Chapter | CJK Chars | EN Words | Word Equiv |")
        print("|---|---|---|---|")
        for ch in per_chapter:
            print(
                f"| {ch['file']} | {ch['cjk_chars']:,} | {ch['en_words']:,} | {ch['total_words_equiv']:,} |"
            )


if __name__ == "__main__":
    main()
