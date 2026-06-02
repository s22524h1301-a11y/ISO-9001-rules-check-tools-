import json
import subprocess
import sys
from pathlib import Path

from reportlab.pdfgen import canvas


def _write_text_pdf(path: Path, text: str) -> None:
    c = canvas.Canvas(str(path))
    text_object = c.beginText(72, 720)
    for line in text.splitlines():
        text_object.textLine(line)
    c.drawText(text_object)
    c.save()


def test_cli_json_outputs_section_matches(tmp_path: Path):
    pdf_path = tmp_path / "policy.pdf"
    _write_text_pdf(
        pdf_path,
        "1. Quality policy\nThe organization shall establish a quality policy and communicate it.",
    )

    result = subprocess.run(
        [sys.executable, "-m", "iso9001_rules_check_tools", "--json", str(pdf_path)],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["format"] == "json"
    assert len(payload["sections"]) == 1
    section = payload["sections"][0]
    assert section["section_id"] == "1"
    assert section["heading"] == "1. Quality policy"
    assert section["matches"][0]["clause_id"] == "5.2"
