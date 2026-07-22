#!/usr/bin/env python3
"""
Validate all chapter files in the MorphAgent textbook.

Checks:
1. YAML frontmatter format is correct and parseable
2. chapter number matches the filename prefix
3. Required sections exist (learning objectives, exercises, references)
4. No TODO/FIXME markers left in the text
5. Status is one of: outline, draft, final

Usage:
    python scripts/validate_chapters.py
    python scripts/validate_chapters.py --strict   # fail on warnings too
"""

import re
import sys
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHAPTERS_DIR = PROJECT_ROOT / "chapters"

REQUIRED_FRONTMATTER_KEYS = [
    "chapter",
    "title_cn",
    "title_en",
    "part",
    "pages_planned",
    "status",
    "last_updated",
    "keywords",
    "learning_objectives",
    "prerequisites",
]

VALID_STATUSES = {"outline", "draft", "final"}
VALID_PARTS = {"I", "II", "III", "IV", "V", "VI"}

REQUIRED_SECTIONS = ["学习目标", "练习题", "参考文献（本章内）"]

TODO_PATTERN = re.compile(r"\b(TODO|FIXME|XXX|HACK)\b", re.IGNORECASE)

passed = []
failed = []
warnings = []


def parse_frontmatter(filepath: Path) -> dict | None:
    """Extract and parse YAML frontmatter from a markdown file."""
    text = filepath.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.find("---", 3)
    if end == -1:
        return None
    yaml_str = text[3:end].strip()
    try:
        return yaml.safe_load(yaml_str)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML frontmatter: {e}")


def check_filename_match(frontmatter: dict, filepath: Path) -> list[str]:
    """Verify that the chapter number in frontmatter matches the filename."""
    errors = []
    chapter_num = frontmatter.get("chapter")
    if chapter_num is None:
        errors.append("Missing 'chapter' field in frontmatter")
        return errors

    # Extract numeric prefix from filename: "01-llm-agent-era.md" -> 1
    match = re.match(r"^(\d+)-", filepath.name)
    if not match:
        errors.append(f"Filename does not start with a numeric prefix: {filepath.name}")
        return errors

    file_num = int(match.group(1))
    if file_num != int(chapter_num):
        errors.append(
            f"Chapter number mismatch: frontmatter says {chapter_num}, "
            f"filename says {file_num}"
        )
    return errors


def check_required_keys(frontmatter: dict) -> list[str]:
    """Check that all required frontmatter keys are present."""
    errors = []
    for key in REQUIRED_FRONTMATTER_KEYS:
        if key not in frontmatter:
            errors.append(f"Missing required frontmatter key: '{key}'")
    return errors


def check_valid_values(frontmatter: dict, filepath: Path) -> list[str]:
    """Validate enum-style fields."""
    errors = []
    status = frontmatter.get("status")
    if status and status not in VALID_STATUSES:
        errors.append(f"Invalid status '{status}', must be one of {VALID_STATUSES}")

    part = frontmatter.get("part")
    if part and part not in VALID_PARTS:
        errors.append(f"Invalid part '{part}', must be one of {VALID_PARTS}")

    lo = frontmatter.get("learning_objectives")
    if lo is not None and not isinstance(lo, list):
        errors.append("'learning_objectives' must be a list")

    kw = frontmatter.get("keywords")
    if kw is not None and not isinstance(kw, list):
        errors.append("'keywords' must be a list")

    prereq = frontmatter.get("prerequisites")
    if prereq is not None and not isinstance(prereq, list):
        errors.append("'prerequisites' must be a list")

    return errors


def check_required_sections(filepath: Path) -> list[str]:
    """Check that required section headings exist in the file body."""
    errors = []
    text = filepath.read_text(encoding="utf-8")

    # Skip frontmatter
    body_start = 0
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            body_start = end + 3

    body = text[body_start:]

    for section in REQUIRED_SECTIONS:
        if f"## {section}" not in body:
            errors.append(f"Missing required section: '## {section}'")

    return errors


def check_todo_markers(filepath: Path) -> list[str]:
    """Check for leftover TODO/FIXME markers."""
    text = filepath.read_text(encoding="utf-8")
    matches = TODO_PATTERN.finditer(text)

    found = []
    for m in matches:
        line_no = text[: m.start()].count("\n") + 1
        found.append(f"  Line {line_no}: '{m.group()}' in context: {text[m.start():m.end()+20].strip()}")

    return found


def validate_chapter(filepath: Path, strict: bool = False) -> bool:
    """Run all validation checks on a single chapter file. Returns True if all pass."""
    chapter_errors = []
    chapter_warnings = []

    # 1. Frontmatter parsing
    try:
        fm = parse_frontmatter(filepath)
    except ValueError as e:
        chapter_errors.append(str(e))
        _report(filepath, chapter_errors, chapter_warnings)
        return False

    if fm is None:
        chapter_errors.append("No YAML frontmatter found (must start with ---)")
        _report(filepath, chapter_errors, chapter_warnings)
        return False

    # 2. Required keys
    chapter_errors.extend(check_required_keys(fm))

    # 3. Filename match
    chapter_errors.extend(check_filename_match(fm, filepath))

    # 4. Valid values
    chapter_errors.extend(check_valid_values(fm, filepath))

    # 5. Required sections
    chapter_errors.extend(check_required_sections(filepath))

    # 6. TODO/FIXME markers
    todos = check_todo_markers(filepath)
    if todos:
        chapter_warnings.extend(todos)

    # 7. Status warning for non-final chapters
    status = fm.get("status")
    if status != "final" and status:
        chapter_warnings.append(f"Chapter status is '{status}', not 'final'")

    _report(filepath, chapter_errors, chapter_warnings)
    return len(chapter_errors) == 0


def _report(filepath: Path, errors: list[str], warns: list[str]) -> None:
    """Append results to global lists."""
    if not errors:
        passed.append(filepath.name)
    else:
        failed.append((filepath.name, errors))

    if warns:
        warnings.append((filepath.name, warns))


def main() -> None:
    strict = "--strict" in sys.argv[1:]

    if not CHAPTERS_DIR.exists():
        print(f"ERROR: Chapters directory not found: {CHAPTERS_DIR}")
        sys.exit(1)

    chapter_files = sorted(CHAPTERS_DIR.glob("*.md"))
    if not chapter_files:
        print(f"ERROR: No .md files found in {CHAPTERS_DIR}")
        sys.exit(1)

    print(f"Validating {len(chapter_files)} chapters in {CHAPTERS_DIR} ...\n")

    all_ok = True
    for f in chapter_files:
        ok = validate_chapter(f, strict=strict)
        if not ok:
            all_ok = False

    # Print summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)

    if passed:
        print(f"\nPASSED ({len(passed)}/{len(chapter_files)}):")
        for name in passed:
            print(f"  [PASS] {name}")

    if failed:
        print(f"\nFAILED ({len(failed)}/{len(chapter_files)}):")
        for name, errors in failed:
            print(f"  [FAIL] {name}")
            for err in errors:
                print(f"         - {err}")

    if warnings:
        print(f"\nWARNINGS ({len(warnings)} files):")
        for name, warns in warnings:
            print(f"  [WARN] {name}")
            for w in warns:
                print(f"         - {w}")

    if strict and warnings:
        all_ok = False
        print("\n(--strict mode: treating warnings as failures)")

    print()
    if all_ok:
        print("All chapters passed validation.")
        sys.exit(0)
    else:
        print("Some chapters failed validation. See details above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
