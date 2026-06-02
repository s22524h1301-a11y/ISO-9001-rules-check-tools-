from __future__ import annotations

from iso9001_rules_check_tools.clause_catalog import default_clause_catalog
from iso9001_rules_check_tools.matcher import match_section
from iso9001_rules_check_tools.models import Section


def render_section_report(sections: tuple[Section, ...]) -> str:
    lines: list[str] = []
    catalog = default_clause_catalog()
    for section in sections:
        lines.append(f"[{section.section_id}] {section.heading}")
        if section.body:
            lines.append(section.body)
        matches = match_section(section, catalog)
        if matches:
            lines.append("Matches:")
            for match in matches:
                lines.append(f"- {match.clause_id} {match.clause_title}")
                lines.append(f"  {match.reason}")
        else:
            lines.append("Matches: none")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
