# ISO 9001 PDF Text Extraction Design

Date: 2026-06-02

## Goal

Add a small, reliable PDF text extraction layer for selectable-text PDFs. The tool should extract text from each page, combine it into document text, and fail clearly when the PDF does not contain any extractable text.

## Problem Statement

The user wants the project to support the first step of document analysis: reading text from a PDF before any section splitting or clause matching happens. The first version should:

- accept a PDF path
- extract selectable text page by page
- return the combined text for the document
- raise a clear error when no selectable text is available

This feature is only for text-based PDFs. It does not need OCR or image recognition.

## First Version Scope

Included in the MVP:

- a dedicated PDF text extraction module
- per-page extraction using the current PDF library
- a custom error for PDFs with no extractable text
- basic CLI integration so the pipeline can call the extractor
- tests for successful extraction and empty-text failure cases

Excluded from the MVP:

- OCR for scanned PDFs
- section splitting
- clause matching changes
- page layout analysis
- confidence scoring or recovery heuristics for image-only PDFs

## Recommended Approach

Use a direct extraction-first approach with a hard failure on empty output.

Why this approach:

- it is the simplest behavior to understand
- it matches the user requirement for a clear error
- it keeps the PDF layer isolated from section parsing and clause matching
- it is easy to test with small fixture PDFs

## Architecture

The system should add one new layer between the CLI and the existing analysis pipeline:

1. Input validation layer
   - accepts a PDF file path
   - verifies the file exists and can be opened

2. PDF extraction layer
   - opens the PDF
   - extracts text from each page
   - strips empty page outputs
   - combines page text into one document string
   - raises a dedicated error if no text is found

3. Downstream analysis layer
   - receives the extracted text once PDF reading succeeds
   - can later feed section parsing and clause matching

## Data Flow

1. The user runs the tool with a PDF path.
2. The CLI passes the path to the PDF extraction function.
3. The extractor reads each page and collects text.
4. If at least one page contains text, the extractor returns the combined document text.
5. If no page contains text, the extractor raises a clear extraction error.

## Module Design

Add a new module, `pdf_reader.py`, with a small surface area:

- `extract_pdf_text(pdf_path: str) -> str`
- `PdfTextExtractionError`

The extractor should depend only on the PDF library and the standard library.
It should not know anything about clause catalog logic or section matching.

## Error Handling

The tool should fail clearly when:

- the file does not exist
- the file is not a PDF
- the PDF cannot be opened
- the PDF has no extractable text

For this MVP, "no extractable text" should be a hard failure, not a silent empty result.
This keeps the user from assuming the document was analyzed successfully when it was not.

## Testing Strategy

We should test from the outside in:

- a fixture PDF with selectable text returns the expected combined string
- a PDF with no selectable text raises `PdfTextExtractionError`
- the CLI path can be extended later without changing the extraction contract

The test fixture should be small and deterministic so the behavior stays stable.

## Success Criteria

The feature is successful if:

- a selectable-text PDF can be read into a combined string
- the tool fails clearly when no text can be extracted
- the extraction behavior is isolated and testable
- the next stage can build section splitting on top of the extracted text

