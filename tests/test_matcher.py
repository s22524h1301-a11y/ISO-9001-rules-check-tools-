from iso9001_rules_check_tools.clause_catalog import default_clause_catalog
from iso9001_rules_check_tools.matcher import match_section
from iso9001_rules_check_tools.models import Section


def _pick_catalog(*clause_ids: str):
    catalog = default_clause_catalog()
    return tuple(clause for clause in catalog if clause.clause_id in clause_ids)


def test_quality_policy_section_prefers_clause_5_2():
    section = Section(
        section_id="2.1",
        heading="Quality policy",
        body="The organization shall establish a quality policy and communicate it to employees.",
    )

    matches = match_section(section, default_clause_catalog())

    assert matches[0].clause_id == "5.2"


def test_empty_catalog_returns_no_matches():
    section = Section(
        section_id="9.9",
        heading="Anything",
        body="No clause keywords here.",
    )

    matches = match_section(section, ())

    assert matches == ()


def test_policing_words_do_not_create_false_matches():
    section = Section(
        section_id="4.2",
        heading="Process note",
        body="Our policymaking process and document records are kept internally.",
    )

    matches = match_section(section, default_clause_catalog())

    assert [match.clause_id for match in matches] == ["7.5"]


def test_single_clear_keyword_match_is_kept_without_title_hit():
    section = Section(
        section_id="5.2.1",
        heading="Internal memo",
        body="policy",
    )

    matches = match_section(section, default_clause_catalog())

    assert matches[0].clause_id == "5.2"


def test_matcher_returns_all_positive_matches_without_truncation():
    section = Section(
        section_id="x",
        heading="Quality policy documented information objective background context",
        body="organization quality policy communicate quality objectives planning documented information records context internal issues external issues",
    )
    catalog = _pick_catalog("4.1", "5.2", "6.2", "7.5")

    matches = match_section(section, catalog)

    assert {match.clause_id for match in matches} == {"4.1", "5.2", "6.2", "7.5"}


def test_internal_audit_section_matches_clause_9_2():
    section = Section(
        section_id="9.2.1",
        heading="Internal audit",
        body="The organization shall conduct internal audits and report the results.",
    )

    matches = match_section(section, default_clause_catalog())

    assert matches[0].clause_id == "9.2"


def test_management_review_section_matches_clause_9_3():
    section = Section(
        section_id="9.3.1",
        heading="Management review",
        body="Top management shall review the quality management system.",
    )

    matches = match_section(section, default_clause_catalog())

    assert matches[0].clause_id == "9.3"


def test_corrective_action_section_matches_clause_10_2():
    section = Section(
        section_id="10.2.1",
        heading="Corrective action",
        body="The organization shall react to nonconformity and take corrective action.",
    )

    matches = match_section(section, default_clause_catalog())

    assert matches[0].clause_id == "10.2"


def test_continual_improvement_section_matches_clause_10_3():
    section = Section(
        section_id="10.3.1",
        heading="Continual improvement",
        body="The organization shall continually improve the suitability, adequacy and effectiveness of the QMS.",
    )

    matches = match_section(section, default_clause_catalog())

    assert matches[0].clause_id == "10.3"
