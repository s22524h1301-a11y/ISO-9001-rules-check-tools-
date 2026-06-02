# Changelog

All notable changes to this project will be documented in this file.

## [v0.6.0] - 2026-06-02

### Changed

- Improved section splitting to recognize nested numbering like `1`, `1.1`, and `1.1.1`
- Kept the whole-document fallback for unstructured text
- Preserved the existing flat `Section` output model

### Notes

- This release makes the parser more reliable for real-world ISO-style documents

## [v0.5.0] - 2026-06-02

### Added

- JSON output for section-level analysis
- `--json` CLI flag for machine-readable stdout
- Shared report builder for text and JSON output

### Notes

- This release makes the analysis results easy to consume programmatically

## [v0.4.0] - 2026-06-02

### Added

- Section-level clause matching in the CLI report
- Clause IDs and reasons shown under each section
- Report output that combines parsing and matching

### Notes

- This release connects the analysis pipeline end to end up to clause association

## [v0.3.0] - 2026-06-02

### Added

- Section splitting for extracted PDF text
- CLI output that prints section IDs, headings, and bodies
- Whole-document fallback when no structure is detected

### Notes

- This release adds the second analysis layer in the pipeline

## [v0.2.0] - 2026-06-02

### Added

- PDF text extraction for selectable-text PDFs
- CLI wiring that prints extracted text directly
- Hard failure when no extractable text is available

### Notes

- This release adds the first working PDF analysis layer

## [v0.1.2] - 2026-06-02

### Fixed

- Allow single clear keyword matches to be kept in the matcher
- Remove the hard cap that truncated positive matches to three results

### Notes

- This release updates the patch version after the matcher fix

## [v0.1.1] - 2026-06-02

### Changed

- Reworked the README into a more formal project landing page
- Added an explicit version section to the README
- Added a changelog to track future releases
- Bumped the project version to `0.1.1`

### Notes

- This release is documentation-focused and does not change the core analysis flow

## [v0.1.0] - 2026-06-02

### Added

- Initial Python project scaffold
- CLI entry point
- Initial ISO 9001 clause catalog
- Initial matching logic
- Basic tests
