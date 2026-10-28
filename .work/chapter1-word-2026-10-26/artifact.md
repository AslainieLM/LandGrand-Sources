# Chapter I Word revision contract

Author: Aslainie L. Maruhom. Audience: capstone author, adviser, and panel. Purpose: revised Chapter I for author/adviser review, not a claim of approval or measured effectiveness.

## Design authority and evidence

Reference: `reference.docx`, copied read-only from the user-designated school-format file and identical to the retained vault original. SHA-256 `8701feed03dc35bf065cba7b20911eb7251335b14eee6e0ab58d3317962b72d7`. All six native Word reference pages were rendered and inspected. Structural evidence is in `reference-evidence.json`; native export audit is in `reference-render/word-audit.json`.

Reference has 41 nonblank paragraphs, one section, no tables, images, headers, footers, fields, notes, comments, or tracked revisions requiring migration. Its entire body is editable manuscript content; original remains unchanged.

## Preserved layout and styles

- Letter portrait 8.5 by 11 inches; left margin 1.5 inches, other margins 1 inch. Preserve section XML exactly, including header/footer distances and document grid.
- Centered CHAPTER I and INTRODUCTION: Cambria 14, bold, double spaced, matching reference paragraphs 1 and 2.
- Body: Times New Roman 12, justified, double spaced. Preserve role-specific paragraph indents/spacing from reference.
- Main headings: reference regular 12-point styles, not generic title presets. Project Context/objectives use paragraphs 4/17; purpose/scope main headings use 15/23. Scope subheading uses Cambria 12 from paragraph 25; Limitations uses paragraph 33.
- Main narrative pattern: paragraph 5; introductory chapter paragraph: 3; purpose: 16; objectives introduction: 18. Nested scope/limitation prose: 26/34.
- Context and objective bullets: paragraph 11, existing numId 1, level 0. Scope bullets: paragraph 28, numId 3, level 1. Limitation bullets: paragraph 36, numId 2, level 0. Preserve numbering definitions unchanged.
- Add keepNext only to headings/lead-ins and keepLines to bullets to prevent stranding. These are content-flow adjustments, not margin/font changes. No forced blank pages or manual page breaks.

## Body slot map and content rules

1–2: preserve titles. 3: replace introduction. 4–14: replace/expand Context with global, national, regional/local rationale, honest survey evidence and four concerns/design needs. 15–16: purpose heading and revised prose. 17–22: general objective plus four deliverable bullets. 23–32: scope heading, intro, Scope and updated bullets. 33–41: Limitations and updated bullets. All slots accounted for, including obsolete feature-label objectives and redundant list lead-ins.

Use PDF-selected four section names. Context must span at least two rendered pages. Four problem bullets include two observed concerns and two design needs; do not invent four empirical findings. No unresolved internal IDs, callouts, wikilinks, placeholders, or CSV-processing commentary in delivered Word prose.

Planned completion window: November–December 2026. User supplied months, year inferred and explicitly disclosed from the 2026 project context; no exact date or approved full study schedule claimed. Survey July 7, 2026 is separate. Grade 5 subgroup summaries, if used, must have denominators and retained calculation provenance. Android 10+ is a target; RAM/storage targets remain untested.

## Package preservation and verification

Only `word/document.xml` may change; optionally app.xml statistics may be refreshed after rendering. Preserve all other ZIP entries byte-for-byte, especially styles, numbering, relationships, theme, fonts, settings and author metadata. Retain section XML canonical identity.

Create a separate `Land Grand - Chapter I - Revised.docx` in vault Manuscript/Drafts. Use native Word read-only PDF export, packaged render_docx.py through the existing native Word/PDFium adapter, and inspect every final page PNG. Verify headings, four objectives, context page span, source hashes, untouched package parts, Word text and PDF text. The final Markdown mirror must match the Word body. All PDF/PNG/build scripts are internal QA, not requested deliverables.
