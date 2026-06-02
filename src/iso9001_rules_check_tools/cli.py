import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="iso9001-rules-check")
    parser.add_argument("pdf_path", nargs="?", help="Path to a selectable-text PDF")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    parser.parse_args(argv)
    return 0
