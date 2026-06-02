from iso9001_rules_check_tools.clause_catalog import default_clause_catalog
from iso9001_rules_check_tools.matcher import match_section
from iso9001_rules_check_tools.models import Section


def test_match_section_returns_quality_policy_for_section():
    section = Section(
        section_id="2",
        heading="Quality policy",
        body="The organization shall establish a quality policy and communicate it.",
    )

    matches = match_section(section, default_clause_catalog())

    assert matches[0].clause_id == "5.2"
