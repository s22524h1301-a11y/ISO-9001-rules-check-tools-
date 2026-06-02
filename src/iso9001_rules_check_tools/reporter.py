from __future__ import annotations

import json
from typing import cast

from iso9001_rules_check_tools.clause_catalog import default_clause_catalog
from iso9001_rules_check_tools.matcher import match_section
from iso9001_rules_check_tools.models import Section


def build_section_report(sections: tuple[Section, ...]) -> dict[str, object]:
    catalog = default_clause_catalog()
    section_entries: list[dict[str, object]] = []
    for section in sections:
        matches = match_section(section, catalog)
        section_entries.append(
            {
                "section_id": section.section_id,
                "heading": section.heading,
                "body": section.body,
                "matches": [
                    {
                        "clause_id": match.clause_id,
                        "clause_title": match.clause_title,
                        "score": match.score,
                        "reason": match.reason,
                    }
                    for match in matches
                ],
            }
        )
    return {"format": "report", "sections": section_entries}


def render_section_report(sections: tuple[Section, ...]) -> str:
    report = build_section_report(sections)
    section_entries = cast(list[dict[str, object]], report["sections"])
    lines: list[str] = []
    for section in section_entries:
        lines.append(f"[{section['section_id']}] {section['heading']}")
        if section["body"]:
            lines.append(cast(str, section["body"]))
        matches = cast(list[dict[str, object]], section["matches"])
        if matches:
            lines.append("Matches:")
            for match in matches:
                lines.append(f"- {match['clause_id']} {match['clause_title']}")
                lines.append(f"  {match['reason']}")
        else:
            lines.append("Matches: none")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_section_report_json(sections: tuple[Section, ...]) -> str:
    report = build_section_report(sections)
    report["format"] = "json"
    return json.dumps(report, ensure_ascii=False, indent=2)
