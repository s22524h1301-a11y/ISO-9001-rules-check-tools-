from iso9001_rules_check_tools.section_parser import split_into_sections


def test_split_into_sections_detects_numbered_headings():
    text = (
        "1. Introduction\n"
        "This is the intro.\n\n"
        "2. Quality policy\n"
        "The organization shall establish a quality policy.\n"
    )

    sections = split_into_sections(text)

    assert [section.section_id for section in sections] == ["1", "2"]
    assert sections[0].heading == "1. Introduction"
    assert "This is the intro." in sections[0].body
    assert sections[1].heading == "2. Quality policy"
    assert "quality policy" in sections[1].body.lower()


def test_split_into_sections_falls_back_to_one_whole_document_section():
    text = "This document has no obvious heading structure.\nIt is just body text."

    sections = split_into_sections(text)

    assert len(sections) == 1
    assert sections[0].section_id == "1"
    assert sections[0].heading == "Document"
    assert "no obvious heading structure" in sections[0].body
