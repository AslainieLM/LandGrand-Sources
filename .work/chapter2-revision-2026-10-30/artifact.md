# Chapter II revision contract

## Authority and scope

This is a separate Land Grand review draft, not DisasterSafetyGame. No canonical vault note, original Word file, earlier draft or survey data may be changed. Outputs belong outside the Obsidian vault in Deliverables/Chapter II Revision 2026-10-30. The supplied Chapter I controls the four objectives. Current vault decisions qualify its older sampling and specimen-observation wording. No Chapter I revision is requested here.

## References and inspected patterns

- Format authority: chapter1-reference.docx in this task directory, SHA256 6ad898c79899c91d506b625b992959af921c53fee88167390d2151f581ada3ad. Eight pages, one section. All eight reference-render PNGs inspected.
- Revision input: chapter2-original.docx, SHA256 168781620da2b47b7390cce5a3182656610f60d34ece8c91a28d5114f9b85180. Seven pages; all original-render PNGs and complete body text inspected, including screenshots and bibliography.
- Section audit and style-evidence.json supply measurements. Both inputs remain unchanged. No fields, content controls, headers, footers, tables or footnotes exist in the format authority.

## Page and typography system

Letter portrait, 8.5 by 11 inches, left margin 1.5 inches, other margins 1 inch. Header/footer distance 709 twips; one column. Preserve section XML byte for byte. No new running header, footer, page numbering or decorative rules.

- Two-line chapter title: clone body paragraphs 1 and 2, centered Cambria 14 bold, double spacing. Replace text with CHAPTER II and REVIEW OF RELATED LITERATURE. Use Title semantics on the second line with explicit source appearance.
- Opening: clone paragraph 3, Times New Roman 12, justified, double spacing, first line 540 twips, before 240 twips.
- Main sections: clone paragraph 4, Times New Roman 12, left aligned, before 160 and after 120 twips, double spacing, keep with next/keep lines. Assign Heading 1 semantics; direct formatting retains source appearance, not default theme appearance.
- Subsections: same source heading, Heading 2 semantics. No per-objective or per-project headings.
- Introductions: clone paragraph 5, first-line 720 twips, keep lines. Exact This section opening after each section and subsection.
- Body: clone paragraph 6, Times New Roman 12, justified, double spacing, first-line 720 twips. Keep widow control; ordinary paragraphs may split across pages.
- Separate bibliography: source-derived centered Cambria 14 title, This section opening, alphabetized APA references in Times New Roman 12, double spaced, left aligned, 0.5-inch hanging indent. Italicize journal and volume or standalone work title. DOI/URL text is a live hyperlink. APA 7 is the working edition; not a newly confirmed institutional policy.

## Slot and package map

- word/document.xml/body: replace Chapter I content in two copied output packages. Preserve and append the original sectPr. This is an intentional full body replacement, using cloned source paragraph roles and clear hierarchy.
- Manuscript slots: chapter opening; Related Literature / Theoretical Background with proposed CTML first; Related Studies in objective order 1–4; Related Projects and Synopsis nested under Related Studies.
- Bibliography slots: separate back-matter document, 15 cited sources, no editorial comments.
- Do not reproduce source Chapter II screenshots. Their capture source/credit and Figure 3 identity are unverified. Originals retain them. Replace weakly verified Rock Collect with The Open University's attributable collection description. Explain in companion notes.
- Preserve-only: all original parts and relationships except document.xml, necessary new hyperlink relationships, and refreshed app statistics. Preserve styles, numbering, settings, theme, fonts, web settings, core metadata, existing relationships and sectPr. Record inventories before authoring. Do not use generic style presets or erase metadata.
- No document comments, tracked changes, review instructions, alignment table, or verification list in the manuscript. Those belong in the companion Markdown file outside the vault.

## Fidelity and delivery gates

Read both files completely, preserve originals and vault hashes, match all 15 citations/references, inspect objective order and all four This section openings. Check scope against Land Grand (four landforms, 60 planned levels, Grade 5 audience, cross-grade adult survey, offline Android 10+). Study and product claims must remain within inspected source access. Render with hidden read-only native Word export and the packaged render_docx.py adapter; inspect every final page. Run packaged render_and_diff.py against the reference and compare preserve-only package parts. No full manuscript TOC is requested; heading semantics support later assembly.
