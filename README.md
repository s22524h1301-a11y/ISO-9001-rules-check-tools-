# ISO 9001 Rules Check Tools

Current version: `v0.7.0`

一個用來分析 PDF 文件內容，並找出文件段落或小節可能對應哪些 ISO 9001 條文的小工具。

目前專案以可選取文字的 PDF 為目標，先完成最小可用版本，讓你可以快速檢查一份文件大致落在哪些條文範圍。

## 專案目標

- 讀取 PDF 文件中的文字內容
- 將文件切成段落或小節
- 針對每個段落或小節，列出可能對應的 ISO 9001 條文
- 先不做「符合 / 不符合」判定，專注在條文對應建議

## 目前功能

- 建立 Python 專案骨架
- 提供基本 CLI 入口
- 內建初版 ISO 9001 條文 catalog
- 具備初版條文比對邏輯
- 已建立單元測試

## 支援範圍

- 輸入格式：PDF
- PDF 類型：可選取文字的電子檔
- 輸出方向：每個段落或小節對應可能相關的 ISO 9001 條文

## 安裝

需要 Python 3.12 或以上。

```bash
pip install -e .
```

如果你要執行測試：

```bash
pip install -e ".[dev]"
```

## 使用方式

先看看 CLI 說明：

```bash
python -m iso9001_rules_check_tools --help
```

```bash
python -m iso9001_rules_check_tools path/to/document.pdf
```

```bash
python -m iso9001_rules_check_tools --json path/to/document.pdf
```

The CLI now prints section headings, matched clause IDs, and bodies by default, and you can pass `--json` to emit structured JSON output instead. It still exits with a non-zero code if the PDF has no extractable text.

目前專案還在第一階段，完整的 PDF 分析流程會在後續版本持續補上。

## 輸出預期

未來完成後，這個工具會針對 PDF 中的每個段落或小節，輸出類似下面的結果：

- 段落或小節標題
- 內容摘要
- 可能對應的 ISO 9001 條文
- 條文對應理由

## 目前進度

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

## 待解決問題

- 條文對應邏輯還需要持續調整，避免誤判
- 不同 PDF 排版差異很大，文件結構辨識還需要持續補強
- 目前是 CLI 工具，尚未加入視覺化介面或網頁版
- 若要對外使用，還可以再補更完整的輸出格式與使用說明

## 路線圖

1. 完成 PDF 文字擷取
2. 完成段落 / 小節切分
3. 串接條文比對與輸出
4. 提供 JSON 或報表輸出
5. 視需求加入 Web UI

## 測試

```bash
pytest tests/test_cli.py tests/test_matcher.py -v
```

## 專案狀態

這是一個持續開發中的 MVP。

目前的重點是先把「PDF 文字分析 + ISO 9001 條文對應」這條主流程穩定下來，再逐步擴充功能。

開發與版本規則請見 [docs/VERSIONING.md](/C:/Users/qc00/Documents/codex/iso9001-rules-check-tools/docs/VERSIONING.md)

## Release Status

- v0.7.0 expands the ISO 9001 clause catalog through chapters 4 to 10.
- The pipeline now goes from PDF text extraction to section parsing to clause association and broader clause coverage.
