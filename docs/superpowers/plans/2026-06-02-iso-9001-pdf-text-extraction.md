# ISO 9001 PDF Text Extraction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a PDF text extraction layer for selectable-text PDFs and fail clearly when a document has no extractable text.

**Architecture:** Keep the PDF layer isolated from clause matching. A new `pdf_reader.py` module will read each page, combine text into a single document string, and raise a dedicated error when the document is textless. The CLI will then call this extractor directly so the feature can be exercised from the command line before section splitting exists.

**Tech Stack:** Python 3.12, `pypdf` for PDF reading, `reportlab` for test fixture PDFs, `pytest` for tests, standard library `pathlib` and `argparse`

---

### Task 1: Add the PDF extraction module

**Files:**
- Create: `src/iso9001_rules_check_tools/pdf_reader.py`
- Create: `tests/test_pdf_reader.py`

- [ ] **Step 1: Write the failing extraction tests**

```python
from pathlib import Path

import pytest
from reportlab.pdfgen import canvas

from iso9001_rules_check_tools.pdf_reader import PdfTextExtractionError, extract_pdf_text


def _write_text_pdf(path: Path, text: str) -> None:
    c = canvas.Canvas(str(path))
    c.drawString(72, 720, text)
    c.save()


def _write_blank_pdf(path: Path) -> None:
    c = canvas.Canvas(str(path))
    c.showPage()
    c.save()


def test_extract_pdf_text_returns_combined_text(tmp_path: Path):
    pdf_path = tmp_path / "sample.pdf"
    _write_text_pdf(pdf_path, "Hello ISO 9001")

    result = extract_pdf_text(pdf_path)

    assert "Hello ISO 9001" in result


def test_extract_pdf_text_raises_when_no_text_is_available(tmp_path: Path):
    pdf_path = tmp_path / "blank.pdf"
    _write_blank_pdf(pdf_path)

    with pytest.raises(PdfTextExtractionError, match="no extractable text"):
        extract_pdf_text(pdf_path)
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -m pytest tests/test_pdf_reader.py -v`
Expected: fail because `pdf_reader.py` does not exist yet.

- [ ] **Step 3: Add the minimal extraction implementation**

```python
from pathlib import Path

from pypdf import PdfReader


class PdfTextExtractionError(RuntimeError):
    pass


def extract_pdf_text(pdf_path: str | Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages: list[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        text = text.strip()
        if text:
            pages.append(text)
    combined = "\n\n".join(pages).strip()
    if not combined:
        raise PdfTextExtractionError("PDF has no extractable text")
    return combined
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python -m pytest tests/test_pdf_reader.py -v`
Expected: PASS for both extraction cases.

- [ ] **Step 5: Commit the extraction module**

```bash
git add src/iso9001_rules_check_tools/pdf_reader.py tests/test_pdf_reader.py
git commit -m "feat: add pdf text extraction"
```

### Task 2: Wire the CLI to the extractor

**Files:**
- Modify: `src/iso9001_rules_check_tools/cli.py`
- Modify: `tests/test_cli.py`
- Create: `tests/test_cli_pdf_reader.py`

- [ ] **Step 1: Write the failing CLI tests**

```python
import subprocess
import sys
from pathlib import Path

from reportlab.pdfgen import canvas


def _write_text_pdf(path: Path, text: str) -> None:
    c = canvas.Canvas(str(path))
    c.drawString(72, 720, text)
    c.save()


def _write_blank_pdf(path: Path) -> None:
    c = canvas.Canvas(str(path))
    c.showPage()
    c.save()


def test_cli_prints_extracted_text(tmp_path: Path):
    pdf_path = tmp_path / "sample.pdf"
    _write_text_pdf(pdf_path, "Hello from CLI")

    result = subprocess.run(
        [sys.executable, "-m", "iso9001_rules_check_tools", str(pdf_path)],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Hello from CLI" in result.stdout


def test_cli_fails_on_blank_pdf(tmp_path: Path):
    pdf_path = tmp_path / "blank.pdf"
    _write_blank_pdf(pdf_path)

    result = subprocess.run(
        [sys.executable, "-m", "iso9001_rules_check_tools", str(pdf_path)],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "no extractable text" in result.stderr.lower()
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -m pytest tests/test_cli.py tests/test_cli_pdf_reader.py -v`
Expected: fail because the CLI still only parses arguments and does not call the extractor.

- [ ] **Step 3: Update the CLI to call the extractor**

```python
import argparse
import sys

from iso9001_rules_check_tools.pdf_reader import PdfTextExtractionError, extract_pdf_text


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
    print(text)
    return 0
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python -m pytest tests/test_cli.py tests/test_cli_pdf_reader.py -v`
Expected: PASS, including the blank-PDF failure case.

- [ ] **Step 5: Commit the CLI integration**

```bash
git add src/iso9001_rules_check_tools/cli.py tests/test_cli.py tests/test_cli_pdf_reader.py
git commit -m "feat: wire cli to pdf extraction"
```

### Task 3: Verify the whole task and prepare the next step

**Files:**
- Modify: `README.md` only if the usage section needs to mention the new CLI behavior

- [ ] **Step 1: Run the full relevant test set**

Run: `python -m pytest tests/test_cli.py tests/test_cli_pdf_reader.py tests/test_pdf_reader.py tests/test_matcher.py -v`
Expected: PASS.

- [ ] **Step 2: Update docs only if needed**

If the CLI usage text changes in a meaningful way, update `README.md` to show that the tool now prints extracted text and fails clearly on blank PDFs.

- [ ] **Step 3: Commit the release-ready patch**

```bash
git add README.md
git commit -m "docs: document pdf extraction behavior"
```

