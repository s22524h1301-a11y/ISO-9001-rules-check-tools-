# ISO 9001 Section Splitting Design

Date: 2026-06-02

## Goal

Add a lightweight section splitting layer that turns extracted PDF text into one or more `Section` objects. When the document does not contain obvious headings or numbering, the entire document should be treated as a single section.

## Problem Statement

The user wants the tool to analyze a whole document but still report results at the section or subsection level when possible. The first version should:

- accept extracted document text
- split it into meaningful sections when headings or numbering are present
- keep section titles separate from section bodies when possible
- fall back to one whole-document section when no structure is detected

This feature is only for basic text parsing. It does not need machine learning or layout analysis.

## First Version Scope

Included in the MVP:

- a dedicated section splitting module
- rule-based detection of headings and numbered sections
- fallback to a single whole-document section
- preservation of section order
- tests for structured and unstructured text inputs

Excluded from the MVP:

- OCR
- semantic topic detection
- page layout analysis
- automatic summary generation
- advanced nested outline reconstruction

## Recommended Approach

Use a simple rule-based parser with a safe fallback.

Why this approach:

- it is easy to understand and debug
- it keeps behavior deterministic
- it works well for office-style documents with headings and numbering
- it satisfies the user's requirement to treat unstructured documents as one section

## Architecture

The parser should sit between PDF text extraction and clause matching:

1. Input layer
   - receives the extracted document text

2. Section parsing layer
   - scans for heading-like lines and numbering patterns
   - groups lines into ordered sections
   - creates one `Section` object per detected block
   - falls back to a single section if nothing useful is detected

3. Downstream analysis layer
   - passes each section to the clause matcher
   - can later feed reporting or JSON output

## Data Flow

1. The CLI obtains extracted text from the PDF reader.
2. The parser inspects the text line by line.
3. If headings or numbered blocks are found, the parser emits multiple sections.
4. If no clear structure is found, the parser emits one whole-document section.
5. Each section is then passed to the clause matcher.

## Section Model

The parser should reuse the existing `Section` dataclass:

- `section_id`
- `heading`
- `body`

The parser should not introduce a new data structure unless it is required later for nested outlines. For this MVP, a flat `Section` list is enough.

## Parsing Rules

The parser should use simple and transparent rules:

- treat a line as a heading when it looks like a numbered item or a short title
- start a new section when a new heading is detected
- accumulate following lines as the body until the next heading
- trim empty lines around headings and bodies
- preserve the original order of sections

Fallback rule:

- if no heading or numbering pattern is detected, return one section with:
  - `section_id="1"`
  - `heading="Document"`
  - `body=<full extracted text>`

## Error Handling

The parser should not fail just because the document is messy.

It should only fail if:

- the input text is empty after trimming
- the input cannot be parsed at all for a technical reason

Otherwise it should return the best available result, including the single-section fallback.

## Testing Strategy

We should test from the outside in:

- structured text with headings yields multiple sections
- unstructured text yields a single whole-document section
- section order is preserved
- section headings and bodies are separated correctly when headings are present

The tests should use short inline text samples so the behavior is easy to read.

## Success Criteria

The feature is successful if:

- extracted PDF text can be split into ordered `Section` objects
- documents with obvious structure produce multiple sections
- documents without structure produce one whole-document section
- the parser stays simple enough for later debugging and reporting

