from __future__ import annotations

import re

from iso9001_rules_check_tools.models import Section

_NUMBERED_HEADING_RE = re.compile(r"^\s*\d+(?:\.\d+)*[.)]?\s+\S+")
_SHORT_HEADING_RE = re.compile(r"^[A-Z][A-Za-z0-9 ,:/&()\-]{0,80}$")


def split_into_sections(text: str) -> tuple[Section, ...]:
    stripped_text = text.strip()
    if not stripped_text:
        return ()

    lines = [line.rstrip() for line in stripped_text.splitlines()]
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

    if not sections:
        return (
            Section(
                section_id="1",
                heading="Document",
                body=stripped_text,
            ),
        )

    if len(sections) == 1 and sections[0].heading == "Document":
        return sections

    return tuple(sections)


def _is_heading(line: str) -> bool:
    return bool(_NUMBERED_HEADING_RE.match(line) or _SHORT_HEADING_RE.match(line))
