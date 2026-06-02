# ISO 9001 Nested Section Splitting Design

Date: 2026-06-02

## Goal

Improve the section parser so it can recognize nested numbered headings like `1`, `1.1`, and `1.1.1`, while still returning a flat list of `Section` objects. If no useful structure is found, the parser should continue to fall back to one whole-document section.

## Problem Statement

The user wants better section splitting for common office-style documents that use nested numbering. The current parser can handle only a limited set of heading patterns, which makes it less reliable for real ISO-related documents. The first version of this improvement should:

- detect nested numbered headings
- preserve section order
- keep the `Section` dataclass unchanged
- keep the whole-document fallback for unstructured text

This feature is only about better rule-based parsing. It does not need a tree model yet.

## First Version Scope

Included in the MVP:

- recognition of `1`, `1.1`, `1.1.1`, and similar nested numbering
- recognition of common heading lines that start with nested numbering
- flat output as a tuple of `Section` objects
- fallback to one whole-document section when no structure is detected
- tests that cover nested headings and unstructured documents

Excluded from the MVP:

- true parent-child section trees
- outline reconstruction across pages
- OCR
- bullet list interpretation as headings
- table parsing
- semantic topic clustering

## Recommended Approach

Use a rule-based parser with a stronger numbered-heading detector, but keep the output flat.

Why this approach:

- it improves the parser where the documents are most structured
- it avoids refactoring the whole data model
- it keeps the CLI and matcher unchanged
- it is a good intermediate step before any tree-based model

## Architecture

The parser should continue to sit between PDF extraction and clause matching:

1. Input layer
   - receives extracted document text

2. Section parsing layer
   - recognizes nested numbered headings
   - starts a new section when a heading-like line is detected
   - groups following body lines until the next heading
   - returns a flat list of `Section` objects

3. Downstream analysis layer
   - consumes the returned sections without knowing how they were detected

## Data Flow

1. The CLI obtains extracted text from the PDF reader.
2. The parser scans the text line by line.
3. Numbered headings such as `1`, `1.1`, and `1.1.1` are recognized as section starts.
4. If no meaningful structure is detected, one fallback section is returned.
5. The section list is passed unchanged to the reporting layer.

## Parsing Rules

The parser should recognize:

- numbered headings with one level, such as `1. Introduction`
- nested numbered headings, such as `1.1 Scope` and `1.1.1 Purpose`
- optional trailing punctuation after the numbering, such as `1.2.` or `1.2)`
- heading text that follows the numbering on the same line

The parser should still:

- preserve order
- trim whitespace around headings and bodies
- keep empty lines out of the body unless they help preserve paragraph boundaries
- use the whole-document fallback if no structure is detected

Fallback rule:

- if no heading-like line is found, return one section with:
  - `section_id="1"`
  - `heading="Document"`
  - `body=<full extracted text>`

## Error Handling

The parser should not fail just because the document is messy.

It should only fail if:

- the input text is empty after trimming
- the input cannot be parsed for a technical reason

Otherwise it should return the best available result.

## Testing Strategy

We should test from the outside in:

- nested numbering like `1`, `1.1`, `1.1.1` yields separate sections
- section order is preserved
- unstructured text still falls back to one section
- the CLI still prints section and match output without changes to the downstream reporting format

The tests should use small inline text samples so the behavior is easy to inspect.

## Success Criteria

The feature is successful if:

- nested numbered headings are detected reliably
- the parser still returns a flat `Section` list
- unstructured documents still become a single section
- the downstream matcher/reporting code continues to work without changes

