# ISO 9001 Section Splitting Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Split extracted PDF text into ordered `Section` objects, while falling back to one whole-document section when no structure is detected.

**Architecture:** Add a small `section_parser.py` module between PDF extraction and clause matching. The parser will scan extracted text line by line, detect heading-like or numbered section starts, and build a flat ordered list of `Section` objects. If it cannot detect meaningful structure, it will emit a single fallback section for the whole document. The CLI will then print sectionized output so the feature is visible end to end before clause matching uses it.

**Tech Stack:** Python 3.12, standard library string parsing and `re`, `pytest` for tests, existing `Section` dataclass from `models.py`

---

### Task 1: Add the section parser

**Files:**
- Create: `src/iso9001_rules_check_tools/section_parser.py`
- Create: `tests/test_section_parser.py`

- [ ] **Step 1: Write the failing parser tests**

```python
from iso9001_rules_check_tools.section_parser import split_into_sections


def test_split_into_sections_detects_numbered_headings():
    text = (
        "1. Introduction\n"
        "This is the intro.\n\n"
        "2. Quality policy\n"
        "The organization shall establish a quality policy.\n"
    )

    sections = split_into_sections(text)

    assert [section.section_id for section in sections] == ["1", "2"]
    assert sections[0].heading == "1. Introduction"
    assert "This is the intro." in sections[0].body
    assert sections[1].heading == "2. Quality policy"
    assert "quality policy" in sections[1].body.lower()


def test_split_into_sections_falls_back_to_one_whole_document_section():
    text = "This document has no obvious heading structure.\nIt is just body text."

    sections = split_into_sections(text)

    assert len(sections) == 1
    assert sections[0].section_id == "1"
    assert sections[0].heading == "Document"
    assert "no obvious heading structure" in sections[0].body
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -m pytest tests/test_section_parser.py -v`
Expected: fail because `section_parser.py` does not exist yet.

- [ ] **Step 3: Add the minimal parser implementation**

```python
from __future__ import annotations

import re

from iso9001_rules_check_tools.models import Section

_NUMBERED_HEADING_RE = re.compile(r"^\s*\d+(?:\.\d+)*[.)]?\s+\S+")
_SHORT_HEADING_RE = re.compile(r"^[A-Z][A-Za-z0-9 ,:/&()\-]{0,80}$")


def split_into_sections(text: str) -> tuple[Section, ...]:
    lines = [line.rstrip() for line in text.splitlines()]
    sections: list[Section] = []
    current_heading: str | None = None
    current_body: list[str] = []
    current_section_id = 1

    def flush_section() -> None:
        nonlocal current_heading, current_body, current_section_id
        if current_heading is None and not any(part.strip() for part in current_body):
            return
        heading = current_heading or "Document"
        body = "\n".join(part for part in current_body if part.strip()).strip()
        sections.append(
            Section(
                section_id=str(current_section_id),
                heading=heading,
                body=body,
            )
        )
        current_section_id += 1
        current_heading = None
        current_body = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current_body:
                current_body.append("")
            continue
        if _is_heading(stripped):
            flush_section()
            current_heading = stripped
            current_body = []
            continue
        current_body.append(stripped)

    flush_section()
    if not sections and text.strip():
        return (
            Section(
                section_id="1",
                heading="Document",
                body=text.strip(),
            ),
        )
    if not sections:
        return ()
    if len(sections) == 1 and sections[0].heading == "Document":
        return sections
    return tuple(sections)


def _is_heading(line: str) -> bool:
    return bool(_NUMBERED_HEADING_RE.match(line) or _SHORT_HEADING_RE.match(line))
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python -m pytest tests/test_section_parser.py -v`
Expected: PASS for both structured and fallback cases.

- [ ] **Step 5: Commit the parser**

```bash
git add src/iso9001_rules_check_tools/section_parser.py tests/test_section_parser.py
git commit -m "feat: add section parser"
```

### Task 2: Connect section parsing to the CLI output

**Files:**
- Modify: `src/iso9001_rules_check_tools/cli.py`
- Create: `tests/test_cli_section_parser.py`

- [ ] **Step 1: Write the failing CLI test**

```python
import subprocess
import sys
from pathlib import Path

from reportlab.pdfgen import canvas


def _write_text_pdf(path: Path, text: str) -> None:
    c = canvas.Canvas(str(path))
    c.drawString(72, 720, text)
    c.save()


def test_cli_prints_section_headings_and_bodies(tmp_path: Path):
    pdf_path = tmp_path / "sample.pdf"
    _write_text_pdf(
        pdf_path,
        "1. Introduction\nThis is the intro.\n\n2. Quality policy\nThe organization shall establish a quality policy.",
    )

    result = subprocess.run(
        [sys.executable, "-m", "iso9001_rules_check_tools", str(pdf_path)],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "1. Introduction" in result.stdout
    assert "2. Quality policy" in result.stdout
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -m pytest tests/test_cli.py tests/test_cli_pdf_reader.py tests/test_cli_section_parser.py -v`
Expected: fail because the CLI still only prints raw extracted text.

- [ ] **Step 3: Update the CLI to print sectionized output**

```python
import argparse
import sys

from iso9001_rules_check_tools.pdf_reader import PdfTextExtractionError, extract_pdf_text
from iso9001_rules_check_tools.section_parser import split_into_sections


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="iso9001-rules-check")
    parser.add_argument("pdf_path", help="Path to a selectable-text PDF")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        text = extract_pdf_text(args.pdf_path)
    except PdfTextExtractionError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    sections = split_into_sections(text)
    for section in sections:
        print(f"[{section.section_id}] {section.heading}")
        if section.body:
            print(section.body)
        print()
    return 0
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python -m pytest tests/test_cli.py tests/test_cli_pdf_reader.py tests/test_cli_section_parser.py tests/test_section_parser.py -v`
Expected: PASS.

- [ ] **Step 5: Commit the CLI integration**

```bash
git add src/iso9001_rules_check_tools/cli.py tests/test_cli_section_parser.py
git commit -m "feat: print parsed sections in cli"
```

### Task 3: Verify the whole task and update docs if needed

**Files:**
- Modify: `README.md` only if the usage example needs to mention sectionized output

- [ ] **Step 1: Run the full relevant test set**

Run: `python -m pytest tests/test_cli.py tests/test_cli_pdf_reader.py tests/test_cli_section_parser.py tests/test_section_parser.py tests/test_pdf_reader.py tests/test_matcher.py -v`
Expected: PASS.

- [ ] **Step 2: Update docs only if needed**

If the CLI output format changes in a meaningful way, update `README.md` to mention that the tool now prints section headings and bodies instead of raw PDF text.

- [ ] **Step 3: Commit the release-ready patch**

```bash
git add README.md
git commit -m "docs: describe section parsing output"
```

