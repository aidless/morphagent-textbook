#!/usr/bin/env python3
"""
Rebuild the combined Book.txt from all chapter markdown files.

Reads chapters/*.md in sorted filename order, strips YAML frontmatter,
and concatenates them into a single Book.txt file at the project root.

Usage:
    python scripts/build_book.py
    python scripts/build_book.py --output Manuscript/Book.txt
"""

import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHAPTERS_DIR = PROJECT_ROOT / "chapters"
DEFAULT_OUTPUT = PROJECT_ROOT / "Book.txt"

BOOK_HEADER = """\
# 操作形态学：自修改 LLM 智能体的具身认知

> **Operational Morphology: The Embodied Cognition of Self-Modifying LLM Agents**

一本关于自修改 LLM 智能体的操作形态学的开源教科书。

---
"""

PART_HEADER_PATTERN = re.compile(r"^part:\s*(.+)$", re.MULTILINE)


def strip_frontmatter(text: str) -> str:
    """Remove YAML frontmatter block from markdown text."""
    if not text.startswith("---"):
        return text
    end = text.find("---", 3)
    if end == -1:
        return text
    return text[end + 3 :].strip() + "\n"


def get_part_from_frontmatter(filepath: Path) -> str | None:
    """Extract the 'part' field from YAML frontmatter."""
    text = filepath.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.find("---", 3)
    if end == -1:
        return None
    yaml_str = text[3:end]
    match = PART_HEADER_PATTERN.search(yaml_str)
    if match:
        return match.group(1).strip()
    return None


PART_NAMES = {
    "I": "Part I . 基础：LLM 智能体",
    "II": "Part II . 理论：4E 认知",
    "III": "Part III . 核心：操作形态学",
    "IV": "Part IV . 高级主题",
    "V": "Part V . 应用与社会",
    "VI": "Part VI . 附录",
}


def build_book(output_path: Path) -> None:
    """Build the combined Book.txt from all chapter files."""
    if not CHAPTERS_DIR.exists():
        print(f"ERROR: Chapters directory not found: {CHAPTERS_DIR}")
        sys.exit(1)

    chapter_files = sorted(CHAPTERS_DIR.glob("*.md"))
    if not chapter_files:
        print(f"ERROR: No .md files found in {CHAPTERS_DIR}")
        sys.exit(1)

    print(f"Building Book.txt from {len(chapter_files)} chapters ...")

    sections: list[str] = []
    sections.append(BOOK_HEADER)

    current_part = None
    chapter_count = 0

    for fpath in chapter_files:
        part = get_part_from_frontmatter(fpath)
        if part and part != current_part:
            current_part = part
            part_title = PART_NAMES.get(part, f"Part {part}")
            sections.append(f"# {part_title}\n")

        body = strip_frontmatter(fpath.read_text(encoding="utf-8"))
        sections.append(body)
        chapter_count += 1

    combined = "\n".join(sections)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(combined, encoding="utf-8")

    size_kb = output_path.stat().st_size / 1024
    print(f"Written: {output_path} ({chapter_count} chapters, {size_kb:.1f} KB)")


def main() -> None:
    output = DEFAULT_OUTPUT
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output = Path(sys.argv[idx + 1])
        else:
            print("ERROR: --output requires a path argument")
            sys.exit(1)

    build_book(output)


if __name__ == "__main__":
    main()
