---
type: writing-guide
status: active
updated: 2026-11-01
sources:
  - "[[Sources/Chapter III Unrevised Draft 2026-11-01]]"
  - "[[Manuscript/Table of Contents]]"
  - "[[Manuscript/Chapter 1-3 Writing Guide]]"
---

# Chapter III Drafting Guide

Use this guide whenever creating, drafting, revising, or reviewing Land Grand Chapter III. It implements the user-authorized save under D-024 in [[Decisions/Decision Register|Decision Register]]. [[Sources/Chapter III Unrevised Draft 2026-11-01|The source and review record]] preserves the five adviser comments separately from the agent’s recommendations. Saving these rules does not mark the comments addressed or approve new game behavior.

Under D-025, [[Manuscript/Drafts/Chapter III Technical Background|working Markdown revision 1]] now implements the initial prose and diagram corrections in the vault. Read [[Manuscript/Chapter III Revision Notes|its coverage and verification notes]] for what is implemented and what remains open; the original Word input is unchanged.

For the next revision, first read [[Sessions/2026-11-01 - Chapter III Draft and Procedure Diagram Handoff|the latest handoff]] and [[Manuscript/Drafts/Land Grand - Chapter III - Revised - v1.docx|delivered Word v1]]. The user reports remaining bottlenecks and prioritizes the procedure diagram under D-026. The earlier Markdown overview and Word panels are working proposals, not accepted flows. Completed render and citation checks do not resolve this feedback.

## Read before drafting

1. Read [[Manuscript/Drafting Dashboard|Dashboard]] for the current Chapter III status and [[Sources/Chapter III Unrevised Draft 2026-11-01|the retained input and comments]] completely.
2. Apply [[Manuscript/Chapter 1-3 Writing Guide#Readability and subsection openings|the shared readability and introduction rules]] and [[Manuscript/Chapter 1-3 Writing Guide#Reference publication years|the 2020–2026 reference rule]]. Manuscript prose uses basic academic English; concise chat style does not apply to the chapter.
3. Read the latest user-designated Chapter I and relevant [[Project/Scope and Requirements|requirements]], [[Project/Game Flow|game flow]], [[Project/Technical Baseline|technical baseline]], [[Decisions/Decision Register|decisions]], and [[Questions/Open Questions|open questions]]. As of this review, the latest corrected Chapter I copy is at `D:\LandGrand\LandGrand-Sources\Deliverables\Chapters I-II Corrections 2026-11-01\Land Grand - Chapter I - Corrected.docx`. Read the actual file before using its content; its existence does not indicate adviser approval. A later user-designated version takes precedence.
4. Classify statements as proposed behavior, reported equipment, verified configuration, or tested results. Recheck technical configuration when claiming current implementation. Draft independent explanations while leaving affected unresolved rules visible in a separate review list.

## Required structure

Use **CHAPTER III — TECHNICAL BACKGROUND**, with the three main sections from [[Manuscript/Table of Contents#Chapter III – Technical Background|the selected BSIT outline]]:

1. **Technicality of the project** — explain the technical approach in paragraphs.
2. **Details of the technologies to be used** — explain hardware, software, peopleware, and the applicable offline/network boundary.
3. **How the project will work** — explain the proposed learner flow and local progress handling.

Restore the missing second main heading in the unrevised input. Use consistent subordinate heading levels. Retain Development, Hardware, Editing Software, and Peopleware in appropriate places so each adviser comment can be checked. Development explains the technical work and how components fit together; research methodology and detailed SDLC documentation remain in Chapter IV under the selected outline.

Every retained section and subsection needs its own separate introduction immediately below its heading. Begin its first sentence with the exact words **“This section”** before descriptions, lists, tables, or figures. The chapter-level introduction may begin **“This chapter.”** A heading followed by “The following are…” does not meet the introduction rule. A tool formatted as a subsection needs an introduction; a tool discussed within an already introduced subsection can use connected prose without becoming another heading.

## Development and technology descriptions

- Explain how Unity, C#, graphical assets, touch interaction, Android packaging, and local progress storage will support the documented learning activities. Describe proposed functions with consistent planned wording. Use completed wording only for evidenced work.
- Explain each tool once in its appropriate subsection: what it does, its specific proposed task in Land Grand, and the output or component it contributes. Earlier overview paragraphs should connect components without repeating every definition.
- Replace company/founder histories, popularity claims, blanket statements about free software, and unsupported assurances of speed or compatibility with relevant project roles. Describe licensing only when necessary and verified.
- Explain C# as the scripting language for documented game functions. Describe Visual Studio Code accurately as the code editor and explain relevant C#/Unity extensions when discussing code completion or debugging. Identify installed extensions or editor settings only after verification. If the generic IDE heading is retained, clarify the editor’s role in its prose.
- Introduce Editing Software, then distinguish the proposed tasks for Piskel and Clip Studio Paint. Piskel can support pixel-art sprites and frame animation exported for Unity; Clip Studio Paint can support illustrations and other artwork. Confirm the actual asset workflow before claiming particular assets or animations were produced.
- Include Android Build Support, SDK, NDK, and JDK/OpenJDK when explaining the build environment if relevant to the actual setup. Verify supported versions against the recorded Unity version before describing an installed toolchain.

## Existing setting and continuity

PPT Slide 32 calls for existing as well as proposed technologies. Introduce the recorded learning setting before the proposed setup. Use [[Sources/Project Clarifications 2026-10-26|the school-context account]] and [[Sources/Baluan Survey CSV Records|qualified adult device-access reports]] where relevant. Do not turn general access to phones, tablets, or computers into verified Android compatibility or invent a school hardware/network inventory. Missing inventory details qualify affected statements; they do not prevent drafting the proposed technical approach.

Keep hardware, software, peopleware, and network discussion connected to the three main headings. The selected manuscript outline owns the structure, Slide 32 owns these discussion topics and continuity guidance, adviser comments own their reported corrections, and D-016/D-023 own the exact introduction wording and reference-year restriction. Do not attribute the user's additional rules to the PPT.

## Hardware and offline operation

- Introduce developer equipment and learner-device targets as separate groups. Explain their purposes before presenting specifications. Treat proposal-listed computer specifications as declared equipment until checked.
- Use **Android 10 and above**, following D-012. Remove the unrevised input’s upper limit of Android 14. Treat 2 GB RAM and 300 MB free storage as proposed minimum targets subject to device testing, not proven requirements that guarantee performance.
- Keep current file-level configuration evidence in [[Project/Technical Baseline#Configuration inspection, 2026-11-01|Technical Baseline]]. Reconcile its recorded minimum-API conflict under Q-01 before claiming an aligned build; saving this guide does not authorize changing Unity settings.
- Explain offline use through lessons, graphics, audio, and progress available on the device. Separate obtaining/installing an application package from playing the installed game. Avoid requiring an internet download unless that distribution method is actually chosen.
- Explain the network topic in terms of the documented offline scope. Preserve its exclusions rather than introducing servers, online accounts, cloud storage, websites, multiplayer, or an administrator panel. APK packaging alone is not evidence of offline behavior.
- Describe automatic local saving as support for later continuation. Use LG-19 for the saved fields; keep save format, timing, reset, replay aggregation, and profile-count decisions under Q-07 until confirmed. Gameplay records do not establish learning gains or central teacher monitoring.

## Peopleware

Introduce the people and distinguish their proposed roles:

- **Developer/researcher:** prepares the application and coordinates documented development and testing work.
- **Grade 5 learners at Baluan Elementary School:** intended players of the supplementary learning game.
- **Teachers:** provide instructional guidance and may review Science content if that arrangement is confirmed. Keep proposed review separate from completed validation or formal evaluation participation.
- **Parents or guardians:** may assist with home study and device use. This support does not imply an in-game account or assigned evaluation role.

Identify actual responsibilities and participants from evidence. The existing parent/teacher survey is cross-grade adult evidence, not a Grade 5 learner test. Keep beneficiary, user, content reviewer, and evaluation participant distinct. Follow [[Project/Research and Evaluation|Research and Evaluation]] for study design rather than inventing recruitment, consent, or approval details here.

## Procedure figure and explanation

Rewrite the proposed flow figure and its explanation together. Use the [[Project/Game Flow|canonical flow]] and confirmed requirements as the baseline. Cover:

1. Launching the installed application and restoring available local progress; exact first-use/name-entry behavior remains a decision if undocumented.
2. The Main Menu’s Play, Settings, Tutorial, and Exit paths. Show only confirmed details for those branches.
3. Play leading to the Landform Map, an unlocked episode, and an available level. Explain Easy, Normal, and Hard availability without making every mode freely selectable.
4. A short lesson before each level.
5. Exploration, movement, jumping, and collection, with item names, illustrations, and descriptions. Connect the item-information step back to gameplay.
6. Level results showing collected items, the review, and up to three gameplay stars under rules still to be defined.
7. Replay or continuation to available content; episode summaries and unlocking after the required completion conditions.
8. Final completion after the four episodes, with local progress available for later play.

Use readable text, consistent symbols, clear arrow direction, and labelled decision branches. Distinguish learner action, game screens, and local device storage. Show save/load connections without inventing a database or online service. Explain each figure step in the same order in the prose. Replace the unexplained “Mission Success” label with a documented completion step or decision. Check figure readability at its final Word size; prefer a clear vector or sufficiently high-resolution replacement.

Use a descriptive caption, such as **“Proposed Gameplay and Local Progress Flow of Land Grand.”** Confirm the number during full-manuscript assembly; the source’s “Figure 4” alone cannot establish its correct position. Keep the figure and caption together where possible and introduce the figure before displaying it.

Q-02, Q-03, Q-06, and Q-07 own the unresolved star/completion conditions, episode order and initial unlock, failure/retry/pause behavior, and save policies. Preserve uncertainty in the separate verification list. Do not invent exact thresholds or make all independent drafting wait for those answers.

## Before delivery

- [ ] All three main sections are present in the required order, with correct subordinate heading levels.
- [ ] Every section/subsection has a separate “This section” introduction before its details.
- [ ] All five adviser comments are mapped to actual changed passages or figure elements. Saving a rule alone is not an implemented correction.
- [ ] Tool descriptions are concise, project-specific, supported, and free from duplicated history or unsupported performance claims.
- [ ] Hardware targets, Android range, local saving, peopleware roles, and exclusions agree with the latest Chapter I and confirmed requirements.
- [ ] Proposed work, configuration findings, and tested results remain distinct; current technical claims were rechecked.
- [ ] Figure paths and prose agree, labels are readable, and the caption/numbering is checked. Remaining decisions are listed separately.
- [ ] Cited technical sources have verified 2020–2026 dates and matching bibliography entries. An undated product page may help verification but is not automatically a compliant reference.
- [ ] A revised Word deliverable is a separate copy preserving the source and school format. Render and inspect every final page, including the complete procedure figure and caption. Report any check that cannot be completed.
- [ ] Update [[Manuscript/Drafting Dashboard|Dashboard]] and the review record only to the state actually achieved. Adviser approval requires separate evidence.
