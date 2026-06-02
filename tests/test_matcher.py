from iso9001_rules_check_tools.clause_catalog import default_clause_catalog
from iso9001_rules_check_tools.matcher import match_section
from iso9001_rules_check_tools.models import Section


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
