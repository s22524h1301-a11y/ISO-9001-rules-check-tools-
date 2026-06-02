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
