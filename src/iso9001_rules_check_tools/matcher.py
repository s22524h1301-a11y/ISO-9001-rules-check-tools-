from __future__ import annotations

import re

from iso9001_rules_check_tools.clause_catalog import default_clause_catalog
from iso9001_rules_check_tools.models import Clause, ClauseMatch, Section

_WHITESPACE_RE = re.compile(r"\s+")
_ASCII_KEYWORD_RE_TEMPLATE = r"(?<!\w){keyword}(?!\w)"


def _normalize(text: str) -> str:
    return _WHITESPACE_RE.sub(" ", text.lower()).strip()


def _score_section_against_clause(section: Section, clause: Clause) -> ClauseMatch:
    section_text = _normalize(f"{section.heading} {section.body}")
    title_hits = tuple(
        keyword
        for keyword in (clause.clause_title, clause.clause_title_zh)
        if _phrase_matches(_normalize(keyword), section_text)
    )
    matched_keywords = tuple(
        keyword
        for keyword in clause.keywords
        if _keyword_matches(_normalize(keyword), section_text)
    )
    score = len(matched_keywords) + (2 if title_hits else 0)
    if not title_hits and len(matched_keywords) < 2:
        score = 0
    reason_parts = []
    if title_hits:
        reason_parts.append("title hit: " + ", ".join(title_hits))
    if matched_keywords:
        reason_parts.append("matched keywords: " + ", ".join(matched_keywords))
    reason = "; ".join(reason_parts) if reason_parts else "No keyword overlap"
    return ClauseMatch(
        clause_id=clause.clause_id,
        clause_title=clause.clause_title,
        score=score,
        reason=reason,
    )


def _phrase_matches(keyword: str, section_text: str) -> bool:
    if not keyword:
        return False
    if re.search(r"[a-z0-9]", keyword):
        pattern = _ASCII_KEYWORD_RE_TEMPLATE.format(keyword=re.escape(keyword).replace(r"\ ", r"\s+"))
        return re.search(pattern, section_text) is not None
    return keyword in section_text


def _keyword_matches(keyword: str, section_text: str) -> bool:
    if not keyword:
        return False
    if re.search(r"[a-z0-9]", keyword):
        pattern = _ASCII_KEYWORD_RE_TEMPLATE.format(keyword=re.escape(keyword).replace(r"\ ", r"\s+"))
        return re.search(pattern, section_text) is not None
    return keyword in section_text


def match_section(
    section: Section,
    catalog: tuple[Clause, ...] | None = None,
) -> tuple[ClauseMatch, ...]:
    if catalog is None:
        catalog = default_clause_catalog()
    ranked = tuple(_score_section_against_clause(section, clause) for clause in catalog)
    positive_matches = tuple(match for match in ranked if match.score > 0)
    return tuple(sorted(positive_matches, key=lambda match: -match.score))[:3]
