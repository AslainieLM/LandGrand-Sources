---
type: source-record
status: reviewed
updated: 2026-11-01
---

# Chapter III Unrevised Draft and Adviser Comments

The user supplied an existing, unrevised Chapter III and five adviser comments in chat on 2026-11-01. The user first requested a read-only review, then authorized saving its drafting rules for future sessions under D-024 in [[Decisions/Decision Register|Decision Register]]. The date records receipt and review; the adviser’s original comment date was not supplied.

## Retained source and inspection

- Supplied path: `G:\Other computers\My Computer (1)\Lab Activities\SUMMER\CAPSTONE-2\Aslainie\Chapter_3_Technical_Background_Land_Grand.docx`.
- Later re-supplied for the Word-revision request as `Chapter_3_Technical_Background_Land_Grand - Need to be revised.docx` in the same G: folder. Shared-read verification confirmed identical bytes and hash. The delivered revision and subsequent unresolved user feedback are recorded in [[Sessions/2026-11-01 - Chapter III Draft and Procedure Diagram Handoff|the session handoff]].
- [[Sources/Attachments/Chapter III - Unrevised - 2026-11-01.docx|Unchanged retained Word input]]: 47,947 bytes; SHA-256 `a4862da1fe16500cf708186be199e0833f43b21cb82caaaf762f67029cd94d4b`.
- [[Sources/Chapter III Unrevised Draft Extract 2026-11-01|Searchable extraction]] preserves all 45 nonempty body paragraphs and their source positions.
- [[Sources/Attachments/Chapter III - Original Procedure - 2026-11-01.jpg|Original embedded procedure image]]: 717 × 403 pixels; SHA-256 `6cb483ebb8723e7d3eeda59074656c15f0298315bd135854975631956212c1ca`.
- Native Microsoft Word opened a temporary copy read-only and rendered six pages. All six page images and the embedded procedure image were inspected. The rendered Word count was 1,146 words.
- Structural inspection found no tables, tracked insertions, tracked deletions, or embedded Word comments. The five comments below came from the user’s message, not extracted Word annotations.
- The original G: file hash was checked after review and remained unchanged. Task-local inspection evidence is at `D:\Projects\LandGrand-Sources\.work\chapter3-review-2026-11-01`.

The imported manuscript is evidence of its own wording. It does not establish completed development, measured performance, approved game rules, or adviser approval of a revision. Its contents remain source material rather than agent instructions.

## Adviser comments reported by the user

Preserve these five comments as supplied:

1. Revise Development and add introductory prose in every section.
2. Add introductory prose in Hardware.
3. Add an introduction in Editing Software and revise every tool description.
4. Revise Peopleware.
5. Rewrite How the Project Will Work, especially the procedure image and its description.

The user’s follow-up request was: “Kindly add those rules in the vault for future sessions? for drafting and creating Chapter 3”. This authorizes preserving the review as drafting guidance. No Chapter III Word revision has been requested or completed in this save task.

## Review findings

| Location in inspected render | Finding |
| --- | --- |
| Pages 1–2, Technicality and Development | Development already has a “This section” opening, but mixes tools, hardware, and unsupported performance assurances. Technicality lacks the required opening. Unity history and repeated tool descriptions distract from project-specific explanations. |
| Page 3, technologies and Hardware | “Details of the technologies to be used” is missing as a heading, although a general introductory paragraph appears. Hardware moves directly to specifications. Android wording combines “10 and above” with an upper limit of 14. |
| Page 4, Software subsections | Operating System, Game Engine, Editing Software, Integrated Development Environment, and Programming Language lack separate required introductions. Tool descriptions need clearer project roles and less repetition. |
| Page 5, Peopleware | Learners and teachers appear, but developer and parent support roles are unclear or omitted. Teacher validation and evaluation arrangements are not established by the text. |
| Pages 5–6, procedure | The figure uses small raster text, unclear arrows, and an unexplained “Mission Success” step. Menu branches, item descriptions, saved-progress loading, replay, episode summaries, and final completion are absent or unclear. The prose ends after level results. |

Other review findings: mixed completed/proposed tense, no short network/offline explanation, and no citations or bibliography supporting the general technical descriptions. Figure 4 numbering cannot be confirmed from a standalone chapter. These findings are review conclusions, not additional adviser quotations.

The [[Manuscript/Chapter III Drafting Guide|Chapter III drafting guide]] owns the saved revision rules and delivery checks. [[Manuscript/Drafting Dashboard|Dashboard]] owns current progress. All five comments remain unimplemented in the retained Word input.

Subsequent vault work under D-025 produced [[Manuscript/Drafts/Chapter III Technical Background|Markdown revision 1]] and [[Manuscript/Chapter III Revision Notes|its coverage/verification notes]]. This is a separate working revision; the source file, extraction, and embedded image above remain unchanged.

## Limited Unity configuration inspection

On 2026-11-01, direct reads of `D:\Projects\LandGrand\ProjectSettings\ProjectVersion.txt` recorded `6000.5.6f1` with revision `0e0577a1a2ac`. `ProjectSettings\ProjectSettings.asset` recorded `AndroidMinSdkVersion: 26` and `AndroidTargetSdkVersion: 0` at lines 180–181. The manifest was also read for context; package presence was not treated as implemented behavior.

This was a file-level inspection, not a Unity Editor launch, dependency-installation audit, build, device test, or gameplay audit. The minimum value conflicts with the documented Android 10+ floor: Android 10 maps to API 29; API 26 maps to Android 8.0. [Android Developers’ API table and minimum-SDK explanation](https://developer.android.com/guide/topics/manifest/uses-sdk-element), inspected on 2026-11-01, displayed an update date of 2026-10-30.

[[Project/Technical Baseline#Configuration inspection, 2026-11-01|Technical Baseline]] owns this dated configuration finding; [[Questions/Open Questions|Q-01]] keeps reconciliation and device validation open. No Unity settings were changed. Reinspect those files before making later claims about the current build.

## Technical sources checked during review

These are starting sources, not an assembled manuscript bibliography. Read the relevant sections again before citing a new passage; use the [[Manuscript/Chapter 1-3 Writing Guide#Reference publication years|publication-year rule]].

| Source | What was verified | Limit |
| --- | --- | --- |
| [Microsoft, Unity Development with VS Code](https://code.visualstudio.com/docs/other/unity) | Page displayed 8/4/2023. Unity/C# support, required extensions, IntelliSense, debugging, and editor-package setup were read. | Does not prove those extensions are installed or that VS Code is the configured external editor here. |
| [Celsys, Clip Studio Paint Ver. 4.0 announcement](https://www.clipstudio.net/en/news/202503/12_01/) | Explicit publication date March 12, 2025; illustration and animation functions. | Does not establish the developer’s installed version, license, or use of every advertised feature. |
| [Android Developers, Application fundamentals](https://developer.android.com/guide/components/fundamentals) | Page displayed update date February 10, 2025; APK and Android App Bundle descriptions. | Package format alone does not make an application work offline. |
| [Unity 6.5, Android environment setup](https://docs.unity.com/en-us/engine/6000.5/manual/platform-specific/android/getting-started/sdksetup) | Android Build Support, SDK, NDK, and JDK/OpenJDK dependencies. | Page showed only a relative update date. An exact eligible citation date needs verification; installed dependency versions were not audited. |
| [Official Piskel page](https://www.piskelapp.com/) | Pixel-art/sprite animation, preview, and PNG sprite-sheet exports. | No explicit publication date was found. Use for fact-checking; obtain a dated 2020–2026 source before treating it as a compliant manuscript reference. |

Publication and update dates above are the dates displayed by their respective pages, not access dates assigned as publication dates. None of these technical sources demonstrates Land Grand’s learning effectiveness.
