# Chapter III Word revision contract

Reference: `chapter3-source.docx` in this directory, an unchanged copy of the newly supplied G: file. SHA-256 `a4862da1fe16500cf708186be199e0833f43b21cb82caaaf762f67029cd94d4b`; 47,947 bytes; one section; six native Word pages. All six rendered source pages were inspected. See source-inventory.json, source-word-audit.json, source-style-audit.json, source.pdf and source-pages.

The user requests a revised/improved draft using the existing source and vault rules. All body content is an authorized edit region. The original manuscript and canonical vault files remain unchanged in this deliverable pass. The school structure and established project facts take precedence over generic document/academic presets.

## Source page and style system

- Letter portrait, 8.5 × 11 inches. Left margin 1.5 inches; right/top/bottom 1 inch. Header/footer distances 709 twips. One continuous source section with its exact sectPr retained. No new section, page furniture, or TOC.
- Source first two paragraphs: centered, bold Cambria 14-point title runs, double line spacing. Retain their visual pattern and CHAPTER III / TECHNICAL BACKGROUND text. The separate bibliography uses the same title pattern once.
- Body paragraphs: source paragraph 2; 12-point inherited Times New Roman, double spacing (480 twips auto), justified, half-inch first-line indent, 200 twips after. Reuse this pattern.
- Main sections: source paragraph 3, Heading1; secondary: paragraph 5, Heading2; minor software headings: source paragraph 26, with the semantic Heading3 style added while retaining its 12-point text pattern. Black text, source heading spacing, keep with next. Title case follows the vault wording.
- Hardware lists: source paragraph 16, literal bullet, 1080-twip left / 360-twip hanging, 12-point, double spacing, 100-twip after. Convert the two Markdown specification tables to source-derived bullet lists to preserve the supplied Word treatment.
- Figure: original anchored drawing in paragraph 41 is replaced with inline drawings to keep the revised panels within the text area. Its caption source paragraph 42 provides centered bold caption treatment. Use 11-point caption text and single spacing for readable multi-line captions, recorded as intentional changes. Keep image/caption pairs together.

## Editable slots and flow

- `word/document.xml/w:document/w:body`: preserve source title paragraphs and final section properties; replace remaining content with the vault Chapter III draft, polished for this Word pass.
- Three main sections remain Technicality of the project; Details of the technologies to be used; How the project will work. Every section/subsection gets an introductory paragraph beginning This section. No new research methodology chapter.
- Replace the source's single low-resolution procedure image with two readable connected panels, Figure 4A and 4B. Retain 4 as the source's working figure number; note that manuscript assembly must confirm it. A joins the two panels; B returns to the Landform Map. Use only documented flow, with abstract completion guards.
- Rendered figure A: 587 × 497 layout pixels; 4.5-inch Word width. Figure B: 939 × 1048; 6-inch Word width. Both are rasterized at twice the source layout resolution. Panel B's effective label size is about 10.1 points. Full figure preview and all final Word pages require inspection.
- Keep the chapter free from review comments, editorial reminders, verification lists, and citation-year debates. Put unresolved scoring/unlock/failure/save decisions in the separate revision notes.
- Matching four-entry bibliography is separate back matter. Use source body/title patterns, half-inch hanging entries and working APA author-date format. Align entries left and place each live URL on a new line within its entry to avoid stretched justified lines. Preserve links and provide live URL relationships.

## Package preservation

The complete package inventory, sizes and hashes are in source-inventory.json. Preserve every source part byte-for-byte except word/document.xml, its document relationships and [Content_Types].xml as needed for added PNG files. Keep styles, theme, numbering, metadata, settings, existing image, and all other opaque parts unchanged. Add only two new image parts to the revised chapter and four URL relationships to the bibliography. The unused original image part/relationship may remain preserved.

No source tables, tracked changes, embedded comments, rich content controls, or manuscript notes were found. Native Word exports operate on read-only copies and close only the automation-owned instance.

## Verification

Compare exact section XML and every preserve-only package part; check original/source hashes; match all four citations/references and 2020–2026 dates; check all 15 introductions and game scope. Use the packaged renderer with native Word PDF/PDFium adapters, inspect all latest page PNGs, and produce the packaged render-and-diff fidelity check. No Word/Obsidian approval is assumed.
