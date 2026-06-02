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
