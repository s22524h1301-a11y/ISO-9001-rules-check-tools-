from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Section:
    section_id: str
    heading: str
    body: str


@dataclass(frozen=True)
class Clause:
    clause_id: str
    clause_title: str
    clause_title_zh: str
    keywords: Tuple[str, ...]
    description: str


@dataclass(frozen=True)
class ClauseMatch:
    clause_id: str
    clause_title: str
    score: int
    reason: str


@dataclass(frozen=True)
class AnalysisResult:
    source_path: str
    sections: tuple[Section, ...]
    matches_by_section: tuple[tuple[ClauseMatch, ...], ...]
