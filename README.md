# ISO 9001 Rules Check Tools

Current version: `v0.7.0`

Language / 語言: [English](#english) | [中文](#中文)

---

<a id="english"></a>
## English

ISO 9001 Rules Check Tools is a small CLI utility for analyzing selectable-text PDFs and suggesting which ISO 9001 clauses may apply to each section of the document.

It is designed as an MVP first: extract text from PDF, split it into sections, and return likely clause matches with text or JSON output.

### What it does

- Reads text from selectable-text PDF files
- Splits the document into sections or subsections
- Suggests possible ISO 9001 clause matches for each section
- Exports results as plain text or JSON

### Scope

- Input: PDF
- PDF type: selectable-text electronic PDFs
- Output: likely ISO 9001 clause matches per section
- Current focus: support for a stable, explainable MVP

### Installation

Requires Python 3.12 or later.

```bash
pip install -e .
```

If you want to run tests:

```bash
pip install -e ".[dev]"
```

### Usage

Show CLI help:

```bash
python -m iso9001_rules_check_tools --help
```

Analyze a PDF with text output:

```bash
python -m iso9001_rules_check_tools path/to/document.pdf
```

Analyze a PDF with JSON output:

```bash
python -m iso9001_rules_check_tools --json path/to/document.pdf
```

The CLI prints section headings, matched clause IDs, and section bodies by default. Use `--json` to emit structured JSON output instead.

### Expected output

For each section, the tool returns:

- Section heading
- Section body or summary
- Possible ISO 9001 clause matches
- Matching reasons

### Current progress

- [x] Project scaffold
- [x] CLI entry point
- [x] Clause data model
- [x] Initial clause matcher
- [x] Basic tests
- [x] PDF text extraction
- [x] Section and subsection splitting
- [x] Section-level clause reporting
- [x] JSON export
- [x] ISO 9001:2015 clause catalog expanded through chapters 4 to 10
- [ ] Deeper document structure recognition
- [ ] Ongoing matching accuracy improvements

### Open issues

- Clause matching still needs tuning to reduce false positives
- PDF layouts vary a lot, so structure parsing will need continued refinement
- This is still a CLI tool, not a web UI
- If the project grows, the output format and documentation can be expanded further

### Roadmap

1. Improve PDF text extraction
2. Improve section and subsection splitting
3. Connect matching and reporting more tightly
4. Add richer export formats if needed
5. Consider a web UI later

### Testing

```bash
pytest tests/test_cli.py tests/test_matcher.py -v
```

### Project status

This is an MVP in active development.

The main goal is to keep the "PDF text analysis + ISO 9001 clause mapping" pipeline stable and explainable, then expand capability gradually.

For development and version rules, see [docs/VERSIONING.md](/C:/Users/qc00/Documents/codex/iso9001-rules-check-tools/docs/VERSIONING.md)

### Release status

- `v0.7.0` expands the ISO 9001 clause catalog through chapters 4 to 10.
- The pipeline now goes from PDF text extraction to section parsing to clause association and broader clause coverage.

---

<a id="中文"></a>
## 中文

ISO 9001 Rules Check Tools 是一個用來分析可選取文字 PDF 文件，並找出文件中每個段落或小節可能對應哪些 ISO 9001 條文的小工具。

這個專案先以 MVP 為目標：完成 PDF 文字擷取、段落切分、條文對應建議，並提供文字或 JSON 輸出。

### 這個工具會做什麼

- 讀取可選取文字的 PDF
- 將文件切成段落或小節
- 對每個段落或小節列出可能對應的 ISO 9001 條文
- 輸出純文字報表或 JSON

### 支援範圍

- 輸入格式：PDF
- PDF 類型：可選取文字的電子檔
- 輸出方向：每個段落或小節對應可能相關的 ISO 9001 條文
- 目前重點：先把流程做穩、做得容易理解

### 安裝

需要 Python 3.12 或以上。

```bash
pip install -e .
```

如果你要執行測試：

```bash
pip install -e ".[dev]"
```

### 使用方式

先看看 CLI 說明：

```bash
python -m iso9001_rules_check_tools --help
```

分析 PDF 並輸出文字報表：

```bash
python -m iso9001_rules_check_tools path/to/document.pdf
```

分析 PDF 並輸出 JSON：

```bash
python -m iso9001_rules_check_tools --json path/to/document.pdf
```

CLI 預設會輸出段落標題、條文命中結果和段落內容；如果加上 `--json`，就會輸出結構化 JSON。

### 預期輸出

對每個段落或小節，工具會回傳：

- 段落或小節標題
- 內容摘要或正文
- 可能對應的 ISO 9001 條文
- 條文對應理由

### 目前進度

- [x] 專案骨架
- [x] CLI 入口
- [x] 初版條文資料結構
- [x] 初版條文比對器
- [x] 基礎測試
- [x] PDF 文字擷取
- [x] 文件段落 / 小節切分
- [x] Section 級條文對應輸出
- [x] JSON 匯出
- [x] ISO 9001:2015 條文 catalog 擴充到第 4 到第 10 章
- [ ] 更進一步的文件結構辨識
- [ ] 比對準確度持續調整

### 待解決問題

- 條文對應邏輯還需要持續調整，避免誤判
- 不同 PDF 排版差異很大，文件結構辨識還需要持續補強
- 目前是 CLI 工具，尚未加入視覺化介面或網頁版
- 若要對外使用，還可以再補更完整的輸出格式與使用說明

### 路線圖

1. 完成 PDF 文字擷取
2. 完成段落 / 小節切分
3. 串接條文比對與輸出
4. 提供 JSON 或報表輸出
5. 視需求加入 Web UI

### 測試

```bash
pytest tests/test_cli.py tests/test_matcher.py -v
```

### 專案狀態

這是一個持續開發中的 MVP。

目前的重點是先把「PDF 文字分析 + ISO 9001 條文對應」這條主流程穩定下來，再逐步擴充功能。

開發與版本規則請見 [docs/VERSIONING.md](/C:/Users/qc00/Documents/codex/iso9001-rules-check-tools/docs/VERSIONING.md)

### Release Status

- `v0.7.0` 擴充了 ISO 9001 條文 catalog，涵蓋第 4 到第 10 章。
- 現在的流程已經從 PDF 文字擷取，串到段落切分，再到條文對應與更完整的覆蓋範圍。
