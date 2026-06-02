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
