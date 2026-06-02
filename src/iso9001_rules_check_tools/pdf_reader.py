from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader
from pypdf.errors import PdfReadError


class PdfTextExtractionError(RuntimeError):
    pass


def extract_pdf_text(pdf_path: str | Path) -> str:
    path = Path(pdf_path)
    try:
        reader = PdfReader(str(path))
    except (FileNotFoundError, PdfReadError, OSError) as exc:
        raise PdfTextExtractionError(f"Unable to read PDF: {path}") from exc

    pages: list[str] = []
    for page in reader.pages:
        text = (page.extract_text() or "").strip()
        if text:
            pages.append(text)

    combined = "\n\n".join(pages).strip()
    if not combined:
        raise PdfTextExtractionError("PDF has no extractable text")
    return combined
