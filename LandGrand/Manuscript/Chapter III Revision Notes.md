---
type: manuscript-review
status: active
updated: 2026-11-01
sources:
  - "[[Sources/Chapter III Unrevised Draft 2026-11-01]]"
  - "[[Manuscript/Chapter III Drafting Guide]]"
---

# Chapter III Revision Notes

## Current revision and authorization

The user requested: “Kindly implement and fix those bottlenecks in the vault for the chapter 3”. D-025 in [[Decisions/Decision Register|Decision Register]] records authorization to implement the vault draft and drafting support. This follows the earlier read-only review and D-024 rules save.

The earlier [[Manuscript/Drafts/Chapter III Technical Background|Markdown revision 1]] contains a substantive draft and one Mermaid overview. A later explicit Word-revision request produced [[Manuscript/Drafts/Land Grand - Chapter III - Revised - v1.docx|Word v1]] and [[Manuscript/Drafts/Land Grand - Chapter III - References - v1.docx|its separate reference list]]. The Word pass further shortened the procedure prose, defined abbreviations, retained source-style specification bullets, and split the diagram into panels 4A/4B. It is not an exact mirror of the earlier Markdown draft. The [[Sources/Chapter III Unrevised Draft 2026-11-01|original Word input and embedded image]] remain unchanged.

## Latest Word delivery and user feedback

**Needs revision; procedure diagram first next session.** After receiving the draft, the user reported many remaining Chapter III bottlenecks, especially its procedure diagram. They asked to finish for today, fix it later, and save progress. [[Sessions/2026-11-01 - Chapter III Draft and Procedure Diagram Handoff|The handoff]] owns the verbatim feedback, delivered-file locations/hashes, and next-session plan. D-026 records the save and deferred priority. Specific remaining defects have not all been supplied, so do not label the issue resolved or invent the user's intended redesign.

The Word chapter has 10 pages; its references have one page. All 11 final pages were visually inspected, all 15 section introductions checked, and all four citations matched to dated references and live links. Source page geometry and opaque package parts were preserved. These technical checks passed, but user/adviser acceptance and flow completeness remain separate. Preserve the version 1 Word snapshots and create a new version for subsequent changes.

The corresponding [Word-pass revision notes](<D:/Projects/LandGrand-Sources/Deliverables/Chapter III Revision 2026-11-01/Land Grand - Chapter III - Revision Notes.md>) retain the editing/terminology details and outstanding game-rule decisions. Native Word counted 1,698 chapter words; no sentence exceeded 30 words in the final prose check. No technical performance, learning-effectiveness, or Unity implementation result is established.

The actual corrected Chapter I was read from `D:\Projects\LandGrand-Sources\Deliverables\Chapters I-II Corrections 2026-11-01\Land Grand - Chapter I - Corrected.docx` before drafting. SHA-256 at this pass: `8c877353238d7940924997b23539b1562cf42f683dc712179af9a6b281e014ed`. The original Chapter III text, PPT Slide 32, selected manuscript outline, current requirements, decisions, and open questions supplied the other project context. Current user-designated documents take precedence over older in-vault Chapter I–II status rows.

## Adviser comment coverage

This table records the earlier Markdown implementation. Word v1 subsequently applied those initial corrections and passed page checks; the user's later feedback above keeps overall Chapter III revision open.

| User-reported adviser comment | Revision 1 implementation | Remaining check |
| --- | --- | --- |
| Revise Development and introduce every section | Rewritten [[Manuscript/Drafts/Chapter III Technical Background#Development|Development]] and separate “This section” introductions under every section/subsection. | Word v1's 15 openings and pagination were checked. Further user feedback and adviser acceptance remain open. |
| Introduce Hardware | [[Manuscript/Drafts/Chapter III Technical Background#Hardware|Hardware]] distinguishes declared development equipment from learner-device targets before the specification tables. | Confirm equipment and test minimum device targets before making performance claims. |
| Introduce Editing Software and revise every tool description | [[Manuscript/Drafts/Chapter III Technical Background#Software|Software]] explains each tool's planned task and output; Editing Software introduces Piskel and Clip Studio Paint. Repeated company history and promotional claims were removed. | Installed versions and the actual asset workflow remain unverified. |
| Revise Peopleware | [[Manuscript/Drafts/Chapter III Technical Background#Peopleware|Peopleware]] distinguishes developer/researcher, Grade 5 players, teachers, and parent/guardian support. | Content-review arrangements and formal evaluation participation remain proposals. |
| Rewrite the procedure image and description | [[Manuscript/Drafts/Chapter III Technical Background#How the project will work|Mermaid overview and matching prose]] cover the initial proposed flow. Word v1 later used two connected panels; their page layout was inspected. | The user still reports diagram bottlenecks. Revisit its logic, explanation, and presentation next session; completion/save guards remain open. |

These are implemented draft responses in Markdown, not confirmation that the adviser has accepted them or that the original Word chapter was corrected.

## PPT and manuscript coverage

| Requirement and origin | What changed |
| --- | --- |
| Three main sections; technicality in paragraph form — [[Sources/Capstone Manuscript BSIT Extract#PDF Page 1|BSIT outline page 1]] | Restored all three headings. Technicality uses explanatory prose. |
| Existing and proposed technologies — [[Sources/Chapter 1-3 Guidelines Extract#Slide 32|PPT Slide 32]] | Added Current learning and technical setting using the researcher's recorded school account and qualified survey access reports. It does not invent a school device/network inventory. |
| Hardware, software, peopleware, network — Slide 32 | All four topics now have their own introductions and project-specific explanations. Network explains the offline boundary. |
| Continuity — Slide 32 | Development connects content, assets, scripts, builds, and planned checks. Tool descriptions and procedure paragraphs follow a consistent order. |
| Introductions and basic academic English — user rules and adviser comments | Every manuscript subsection begins with a separate “This section” paragraph. Chapter opening begins “This chapter.” |
| Verified references dated 2020–2026 — D-023 | Four cited technical sources have matching entries and verified displayed dates. Dates describe the cited pages, not installed software releases. |
| Methodology belongs in Chapter IV — selected outline | Chapter III explains technical intent. It does not invent a study design, Gantt chart, completed testing procedure, or evaluation results. |

## Technical source verification

Sources were opened and their relevant sections read on 2026-11-01. These are primary technical documents, not learning-effectiveness studies.

| Citation | Verified date and locator | Supported use and boundary |
| --- | --- | --- |
| Celsys (2025) | [Official announcement](https://www.clipstudio.net/en/news/202503/12_01/), heading and opening paragraph; March 12, 2025. | Supports illustration/animation capability. Does not prove the developer uses version 4.0 or holds a particular license. |
| Google (2025) | [Application fundamentals](https://developer.android.com/guide/components/fundamentals), opening APK explanation; footer displays last updated February 10, 2025. | Supports installation-package explanation. The update date is used for the page version cited. No APK-to-offline guarantee is inferred. |
| Microsoft (2023) | [Unity Development with VS Code](https://code.visualstudio.com/docs/other/unity), Install, Set up Unity, Editing Evolved, and Debugging; displayed date 8/4/2023. | Supports C#/Unity editing, extensions, code completion, and debugging. Does not prove the extensions or external-editor settings are installed locally. |
| Unity Technologies (2026) | [Unity User Manual 2022.3, Android environment setup](https://docs.unity3d.com/2022.3/Documentation/Manual/android-sdksetup.html), dependency list and explicit footer “Publication Date: 2026-07-02”. | The cited manual edition identifies Android Build Support, SDK, NDK, and JDK/OpenJDK. Its 2026 date is a displayed publication date, not a copyright-only inference or Unity 2022.3 release year. The same dependency categories were checked in the [Unity 6.5 manual](https://docs.unity.com/en-us/engine/6000.5/manual/platform-specific/android/getting-started/sdksetup). No dependency version was selected from the older engine edition. |

The Unity 6.5 page still exposes only a relative update date in the inspected view; it is a corroborating verification source, not a fifth manuscript citation. The Piskel homepage and release index did not expose a verified eligible publication year in the inspected text. The GitHub release API could not be opened through the web tool. Revision 1 therefore describes Piskel's intended project assignment without inserting an undated bibliography entry or claiming a particular release is installed. The original proposal already names Piskel as a selected tool.

APA author-date entries are used consistently. The institutional APA edition and any literal footnote/endnote requirement remain separate confirmation matters; this Markdown revision does not create Word notes. Merge these references into one bibliography when assembling the manuscript, avoiding duplicate entries.

## Figure and game-rule boundaries

The Mermaid figure is the replacement diagram source in the vault. Its solid arrows describe proposed screen/activity flow. Dashed storage connections describe data relationships rather than an exhaustive specification of save triggers or transaction timing. “Episode requirements met?” and “Level completed” retain abstract guards until Q-02–Q-03 are answered. No star threshold, episode starting order, or exact number of levels required for an unlock was invented.

The diagram shows the documented Settings, Tutorial, and Exit destinations. Their detailed controls and return/failure paths remain under Q-06. The replay arrow passes through the lesson, consistent with the lesson-before-each-level requirement. The diagram includes no separate quiz screen, online account, central learner dashboard, GPS, scanning, or multiplayer feature.

The descriptive caption is intentionally unnumbered until full-manuscript assembly establishes figure order. The original raster image remains evidence of the supplied draft. [[Sources/Attachments/Chapter III - Proposed Flow - v1.svg|The generated vector preview]] was produced from exactly the Mermaid source in revision 1. Mermaid 10.9.3 parsed and rendered it in an isolated headless browser; the complete 1433 × 1464 pixel raster preview was visually inspected for readable labels, arrow directions, decision branches, and clipping. The vault retains the scalable SVG, while task-local QA retains the PNG and parser report. This verifies the generated preview, not the live Obsidian view or final Word layout.

## Remaining decisions and evidence

| Item | Owner and effect | Treatment in revision 1 |
| --- | --- | --- |
| Android configuration versus target | [[Questions/Open Questions|Q-01]] and [[Project/Technical Baseline#Configuration inspection, 2026-11-01|dated API setting]] | Uses Android 10+ as the requirement and does not claim a matching or tested build. No Unity settings changed. |
| Star and completion conditions | Q-02 | Says up to three gameplay stars; leaves diagram guards abstract. |
| Episode order, initial unlock, and completion requirements | Q-03 | Names all four landforms without declaring their list order as the unlocking order. |
| Selected items, competencies, and reviewer arrangements | Q-04 | Describes planned scientific/curriculum review, not completed validation. |
| Study evaluation and permissions | Q-05 | Does not assign evaluation participants or claim learning gains. |
| Failure/retry/pause and detailed menu behavior | Q-06 | Does not fabricate transitions or settings controls. |
| Profiles, first-use name entry, replay aggregation, resets, and save timing | Q-07 | Describes required fields and local continuation at a high level. |
| Actual development equipment and installed toolchain | [[Project/Technical Baseline|Technical Baseline]] | Keeps equipment declared and device requirements proposed. Direct reinspection is needed before actual configuration claims. |
| School device/network inventory | [[Sources/Project Clarifications 2026-10-26|recorded school context]] and [[Sources/Baluan Survey CSV Records|adult access reports]] | No school-wide inventory or verified Android availability is asserted. This does not block the initial draft. |

## Checks and next step

The current Chapter III status is **Needs revision**, following the user's session-close feedback. Word revision 1 has been delivered and preserved; the Markdown body below its metadata remains an earlier baseline. The next session begins with the procedure diagram and the user's remaining concerns, followed by affected game-rule clarification and a separately versioned revision when requested. No further redesign is part of today's save.

At the earlier Markdown stage, the maintained validator passed for 61 notes, 659 internal links, eight configurations, and 16 retained-file hashes, with zero errors. Focused checks confirmed the three main headings, all 15 “This section” introductions, and four matching 2020–2026 references. The generated flow passed its parser/render check and complete static-preview visual inspection. Task-local evidence remains at `D:\Projects\LandGrand-Sources\.work\chapter3-vault-revision-2026-11-01\final-checks.json`. Word-pass evidence is separately recorded in `.work\chapter3-word-revision-2026-11-01\final-verification.json`. Current session-save validation is recorded in the change log.

The checks establish the inspected versions' structure, references, previews, page layout, and retained-byte integrity. Live Obsidian rendering, implementation, and user/adviser acceptance remain separate. Successful page rendering does not close the latest reported diagram/content concerns.
