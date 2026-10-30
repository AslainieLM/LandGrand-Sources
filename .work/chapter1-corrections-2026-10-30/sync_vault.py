from pathlib import Path
import json,re,shutil

ROOT=Path(__file__).resolve().parent
VAULT=ROOT.parent.parent/'LandGrand'
QA=json.loads((ROOT/'final-verification.json').read_text())
assert QA['pages']==9 and QA['comments']==7

def read(name): return (VAULT/name).read_text(encoding='utf-8')
def write(name,text):
    text=re.sub(r'(?m)^updated: .*$', 'updated: 2026-10-30',text,count=1)
    (VAULT/name).write_text(text,encoding='utf-8')
def replace_line(text,prefix,new):
    lines=text.splitlines()
    matches=[i for i,line in enumerate(lines) if line.startswith(prefix)]
    assert len(matches)==1,(prefix,matches)
    lines[matches[0]]=new
    return '\n'.join(lines)+'\n'

observation='Sources/Researcher Observation - Rock and Mineral Samples 2026-10-30'
draft='Manuscript/Drafts/Land Grand - Chapter I - Revised - v9.docx'

# The two decisions separate editing authorization from the new reported source.
name='Decisions/Decision Register.md'
text=read(name)
assert '| D-020 |' not in text and '| D-021 |' not in text
rows='''| D-020 | 2026-10-30 | Apply the reviewed Chapter I corrections using the supplied final-named Word file as the base. Preserve the school format and original, add the verified bibliography, restore scope details, clarify survey wording and make unresolved factual/game-rule dependencies reviewable in local comments. Prospective validation and one-level checks are plans, not completed results. | [[Manuscript/Chapter I Revision Notes#Revision and status|Direct correction request and resulting revision]]. | [[Manuscript/Drafts/Chapter I Introduction|Revision 9]], [[Manuscript/Drafting Dashboard|Dashboard]], [[Manuscript/Chapter I Final Review 2026-10-30|Prior review]] |
| D-021 | 2026-10-30 | Record personal observation as the user's stated source for the rock/mineral-sample concern. Attribute problem 4 to the researcher rather than the survey. The actual observation date, setting and sample details remain open; the separate city-wide scarcity perception is not a verified inventory. | [[Sources/Researcher Observation - Rock and Mineral Samples 2026-10-30|Direct reply and evidence limits]]. | [[Manuscript/Evidence Register|E-13]], [[Questions/Open Questions|Q-12]], [[Project/Research and Evaluation|Research context]], [[Manuscript/Drafts/Chapter I Introduction|Revision 9]] |'''
needle='\n\nThe imported proposal is an initial documentary baseline.'
assert needle in text
write(name,text.replace(needle,'\n'+rows+needle,1))

name='Questions/Open Questions.md'
text=replace_line(read(name),'| Q-12 |','| Q-12 | Before formalizing the material observation | D-021 identifies the researcher\'s personal observation as the source. What actual observation date, setting, available/missing specimens and extent document the reported limitation? No city-wide inventory has been supplied. | [[Sources/Researcher Observation - Rock and Mineral Samples 2026-10-30|Observation record]] and [[Manuscript/Chapter I Revision Notes#Pending confirmations|Current revision]] | Partly clarified: source type confirmed; observation date and sample details remain open |')
write(name,text)

name='Manuscript/Evidence Register.md'
text=read(name)
text=replace_line(text,'| E-13 |','| E-13 | Researcher-reported limited rock/mineral samples for demonstrations | [[Sources/Researcher Observation - Rock and Mineral Samples 2026-10-30|Personal-observation clarification]] under D-021 | Source identified by the user; date, setting and extent remain undocumented | Revision 9 attributes the observation to the researcher. It is not a survey finding, teacher report or independently verified inventory. Q-12 retains the missing details; no city-wide scarcity claim is made. Digital illustrations remain supplementary. |')
lines=text.splitlines()
for i,line in enumerate(lines):
    if line.startswith('| E-03 |') or line.startswith('| E-11 |'):lines[i]=line.replace('Revision 8','Revision 9')
write(name,'\n'.join(lines)+'\n')

name='Project/Research and Evaluation.md'
text=read(name)
heading='## Researcher-reported material observation'
assert heading not in text
addition='''## Researcher-reported material observation

On 2026-10-30, the user identified personal observation as the source of the concern about limited rock and mineral samples for classroom demonstrations. [[Sources/Researcher Observation - Rock and Mineral Samples 2026-10-30|The source record]] retains the exact reply and its limits. D-021 supports researcher attribution in Chapter I; it does not establish an independently checked materials inventory. The actual observation date, setting and sample details remain open under Q-12. The user's additional city-wide scarcity perception is not generalized in the manuscript.

Revision 9 describes scientific/curriculum review and a complete-level content/device check as prospective development work. No validation, prototype, device test or evaluation result is claimed. Q-02–Q-05 retain the detailed decisions needed for later development and research.

'''
assert '## What remains undocumented' in text
write(name,text.replace('## What remains undocumented',addition+'## What remains undocumented',1))

# Current working manuscript is already synchronized from the verified Word body.
notes='''---
type: revision-review
status: reviewed
updated: 2026-10-30
sources:
  - "[[Sources/Chapter I Final User Draft 2026-10-30]]"
  - "[[Sources/Researcher Observation - Rock and Mineral Samples 2026-10-30]]"
  - "[[Sources/Baluan Survey CSV Records]]"
  - "[[Manuscript/Chapter 1-3 Writing Guide]]"
  - "[[Project/Scope and Requirements]]"
---

# Chapter I Revision Notes

## Revision and status

**Revision 9, corrected review copy, 2026-10-30.** [[Manuscript/Drafts/Land Grand - Chapter I - Revised - v9.docx|Open the current Word copy]] or [[Manuscript/Drafts/Chapter I Introduction|the synchronized Markdown]]. The user requested: “Implement and fix those bottlenecks, use the existing word pasted.” D-020 records this authorization. The base is the unchanged [[Sources/Chapter I Final User Draft 2026-10-30|user-supplied final-named chapter]], not a blank document or redesign.

The corrected copy has **nine rendered pages**, including **BIBLIOGRAPHY on page 9**. Context spans **pages 1–4**. All six Chapter I introductions begin **This section** and are separate from details. The bibliography also has a short This section opening. The numbered problem and objective lists each run 1–4.

Problem 4 is now **The researcher observed limited rock and mineral samples for classroom demonstrations.** D-021 records the user's identification of personal observation as its source. This is an attributed qualitative report, separate from survey findings. The observation date, exact setting and sample details remain pending under Q-12. No city-wide scarcity claim or independent inventory result is asserted.

This is a reviewable correction, not adviser approval, completed curriculum validation or demonstrated learning effectiveness. Seven Word comments identify changes and remaining dependencies at their relevant passages.

## Scope and Limitations wording follow-up

The shorter wording saved in [[Sessions/2026-10-28 - Chapter I Scope and Limitations|the earlier session]] is integrated through the user's newer chapter and this correction. Revision 9 keeps the single-player sentence, separates Scope's introduction, restores Unity/C#/Piskel/Clip Studio Paint, restores the LG-23 exclusions and device-testing qualification, and clarifies overall versus Grade 5 survey findings. Planned-action wording is consistent, while historical survey expectations retain could. The abbreviation is 2D.

Scientific/curriculum review is described as prospective work. A complete-level content/device check precedes expansion to 60 levels as a proposed production sequence. No star threshold, unlock condition, validated competency list or completed test was invented.

## Problem and objective alignment

| No. | Current reported problem | Matching specific objective | Evidence and scope |
| --- | --- | --- | --- |
| 1 | Parents reported difficulty explaining lessons in printed modules. | Provide short Science lessons before each level to help parents explain the selected topics during home study. | Overall parent question 3. Module difficulty is general; the game supports only the selected Science content. |
| 2 | Teacher responses raised concerns about the effectiveness of modular learning. | Add interactive exploration and reviews after each level to support learning alongside printed Science modules. | Overall teacher question 2. Views are mixed, not universal agreement or measured ineffectiveness. |
| 3 | Survey responses identified landforms, rocks, and minerals as difficult Science topics. | Develop four episodes covering Mountains, Hills, Plains, and Plateaus, with selected rock and mineral content. | Parent/teacher topic mentions, not pupil test scores or a claim of the most prevalent difficulty. |
| 4 | The researcher observed limited rock and mineral samples for classroom demonstrations. | Present digital illustrations of selected rocks and minerals with names and short descriptions. | User-reported personal observation under D-021; date and sample details pending. Illustrations provide supplementary visual examples, not physical specimens. |

The game audience remains Grade 5. The survey covers parents of Grades 4–6 learners and teachers handling Kindergarten and Grades 3–6. Correctly labeled Grade 5 subgroup analysis remains separate. Dates, sample size and the selected 85% finding are stated once in Context.

## Writing and page checks

| Heading | Heading page | Introductory paragraph page |
| --- | ---: | ---: |
| Project Context | 1 | 1 |
| Purpose and Description of the Project | 4 | 4 |
| Objectives of the Project | 5 | 5 |
| Scope and Limitations of the Project | 6 | 6 |
| Scope | 6 | 6 |
| Limitations | 8 | 8 |
| BIBLIOGRAPHY | 9 | 9 |

Native Word word count is **1,712**, including bibliography text. The body contains 68 paragraphs. The section geometry, existing typography and double spacing are preserved. The final limitation stays with the other limitations on page 8; no nearly empty continuation page remains.

## Verification

- Native Word opened the file read-only and exported document content without printing comments. The packaged render_docx.py adapter produced all nine final page PNGs; every page was inspected.
- XML body text matches native Word paragraph text, accounting for manual line breaks in bibliography entries. Both PDF lists display 1–4. All three official URLs are live hyperlinks in Word and are preserved as PDF URI targets.
- Seven comments have matching start/end/reference anchors, a comments relationship and the required content type. Comments are verified structurally because page rendering does not show them reliably.
- Only body XML, the necessary hyperlink/comment relationships, the comments content type and refreshed app statistics changed; comments.xml was added. All source styles, numbering definitions, section XML, original relationships, core metadata and opaque parts are preserved.
- The packaged source/final image and text diff records expected body changes and the added bibliography page. No source, prior Word version or raw survey CSV was edited. Pre-update note backups are retained.
- Internal contract, reference evidence, builder, native audit, comparison and final verification: D:\\Projects\\LandGrand-Sources\\.work\\chapter1-corrections-2026-10-30. PDF/PNG files are internal QA, not requested deliverables.

## Reference and source mapping

The three already verified official sources now have matching bibliography entries in the corrected Word file. Each entry has the institutional author, year/date, exact work title and official link. The user retains ownership of final citation style and margins. The standalone bibliography can be moved into the full manuscript's back matter when assembling the complete capstone.

| Source | Supported use |
| --- | --- |
| [[Sources/UNESCO GEM 2023 Technology|UNESCO 2023 report recommendations]] | Context-appropriate technology, inclusion, evidence and sustainability; not a Land Grand effectiveness result. |
| [[Sources/DepEd Distance Learning Strategies 2020|DepEd memorandum DM-CI-2020-00162]] | Historical printed/digital modular arrangements, supplementary resources and household support. |
| [[Sources/PHIVOLCS Sarangani Earthquake 2026|DOST-PHIVOLCS advisory]] | June 8, 2026 magnitude 7.8 offshore Sarangani earthquake; not a Baluan closure or modality order. |
| [[Sources/Baluan Survey CSV Records|Survey CSVs]] | Adult responses, actual grade coverage, mixed views and the 17/20 parent-explanation result. |
| [[Sources/Researcher Observation - Rock and Mineral Samples 2026-10-30|Researcher observation clarification]] | Source of the fourth concern, with date/setting/sample details still pending. |
| [[Sources/Project Clarifications 2026-10-26|User clarifications]] | Survey dates, school context, Android range, school format and planned completion window. |

## Pending confirmations

- **Q-12 / E-13:** Actual observation date, setting and available/missing sample details. Personal observation is the supplied source; a city-wide inventory is not established.
- **Q-02–Q-03 and Q-06–Q-07:** Detailed scoring, completion, progression and save behavior. Revision 9 retains proposed features without inventing rules.
- **Q-04–Q-05:** Exact curriculum/content mapping, validation responsibility and research evaluation method. Planned checks are not completed validation or measured gains.
- **Q-09–Q-10:** Actual selection/recruitment procedure, administration records, topic coding and the unrelated mathematics-table discrepancy.
- **Q-11:** Exact approved deadline, explicit year confirmation and full schedule. November–December is user-supplied; 2026 remains the recorded contextual year assumption under D-015.
- **Q-08 / MW-03:** Adviser approval and any local novelty claim remain separate evidence matters. MW-01's minimum-four requirement and MW-02's school-format ownership remain settled.

## Revision 8 historical record

[[Manuscript/Drafts/Land Grand - Chapter I - Revised - v8.docx|Revision 8]] remains unchanged, with eight inspected pages and Context on pages 1–4. D-019 integrated the broader-survey short statements and conditional fourth concern. The user then supplied the newer final-named chapter for review. The review findings remain available in [[Manuscript/Chapter I Final Review 2026-10-30|the pre-correction review]], and full earlier notes are preserved in the task-local backups.

## Four problem statements in revision 7

This stable historical anchor preserves earlier source/decision links. [[Manuscript/Drafts/Land Grand - Chapter I - Revised - v7.docx|Revision 7]] used separate landform and rock/mineral concerns with labeled Grade 5 subgroup evidence. D-019 replaced that structure with broader-survey statements and a conditional material concern. D-021 now supplies researcher-observation attribution for that fourth concern; the source details remain qualified.
'''
write('Manuscript/Chapter I Revision Notes.md',notes)

name='Current Focus.md'
text=read(name)
text=replace_line(text,'- Distinguish [[Sources/Chapter1 Discussion Notes', '- Distinguish [[Sources/Chapter1 Discussion Notes|discussion notes]] from [[Sources/Chapter I Unrevised Draft|the original school-format manuscript]]. [[Manuscript/Drafts/Land Grand - Chapter I - Revised - v9.docx|Revision 9]] and its synchronized Markdown apply the authorized corrections under D-020. Nine pages were inspected; Context spans pages 1–4 and the three-entry bibliography is on page 9. Problem 4 is attributed to the researcher under D-021; Q-12 retains its missing observation details.')
text=replace_line(text,'- Latest review input:', '- Latest source and correction: [[Sources/Chapter I Final User Draft 2026-10-30|the user-supplied final-named chapter]] is preserved unchanged. The [[Manuscript/Chapter I Final Review 2026-10-30|prior review]] led to revision 9, which adds verified bibliography entries, restores scope details and clarifies survey wording. [[Manuscript/Chapter I Revision Notes|Current revision notes]] own the seven local comments and remaining decisions.')
text=replace_line(text,'- Earlier [[Sessions/', '- Earlier [[Sessions/2026-10-28 - Chapter I Scope and Limitations|Scope wording work]] is retained for history. Its principal wording/format corrections now appear in revision 9. The next work is to document the remaining observation, content, game-rule and method details identified in the comments, then continue Chapters II–III in the order requested.')
write(name,text)

name='Home.md'
text=read(name).replace('Manuscript/Drafts/Land Grand - Chapter I - Revised - v8.docx|current revised Word copy','Manuscript/Drafts/Land Grand - Chapter I - Revised - v9.docx|current revised Word copy')
text=text.replace('This source has not silently replaced the agent-generated revision 8 pair or closed its evidence questions.','The user subsequently authorized correction into revision 9; [[Manuscript/Chapter I Revision Notes|current revision notes]] distinguish implemented edits from open evidence and game-rule questions.')
write(name,text)

name='Manuscript/Drafting Dashboard.md'
text=read(name)
text=text.replace('## Now\n','## Now\n\n- [x] Produce [[Manuscript/Drafts/Land Grand - Chapter I - Revised - v9.docx|revision 9]] from the supplied Word base, with synchronized Markdown, bibliography, restored scope details and seven local comments. All nine pages passed visual review.\n- [ ] Document the remaining observation date/sample details, content validation, game rules and methodology points in [[Manuscript/Chapter I Revision Notes#Pending confirmations|pending confirmations]].\n',1)
text=replace_line(text,'- [ ] Address the latest review', '- [x] Apply the latest review\'s bibliography, Scope, paragraph-separation and survey-wording corrections. D-021 now supplies personal-observation attribution for problem 4; its remaining details and other factual/game-rule decisions are identified in comments.')
rows={
'| I — Project Context |':'| I — Project Context | [[Manuscript/Drafts/Chapter I Introduction#Project Context|Current section]] | Corrected review copy; revision 9, 2026-10-30 | Context spans pages 1–4. Researcher attribution for problem 4 is supplied; observation and sampling records remain qualified. |',
'| I — Purpose and Description |':'| I — Purpose and Description | [[Manuscript/Drafts/Chapter I Introduction#Purpose and Description of the Project|Current section]] | Corrected review copy; revision 9, 2026-10-30 | Retains supplementary lessons, exploration, collection and review. No effectiveness or local-novelty result is claimed. |',
'| I — Objectives |':'| I — Objectives | [[Manuscript/Drafts/Chapter I Introduction#Objectives of the Project|Current section]] | Corrected review copy; revision 9, 2026-10-30 | Four objectives match the four attributed concerns. Digital examples remain supplementary to physical specimens. |',
'| I — Scope and Limitations |':'| I — Scope and Limitations | [[Manuscript/Drafts/Chapter I Introduction#Scope and Limitations of the Project|Current section]] | Corrected review copy; revision 9, 2026-10-30 | Restored tools, LG-23 exclusions and device-testing qualification; added prospective validation/first-level checks. Detailed game rules remain open. |'}
for prefix,new in rows.items():text=replace_line(text,prefix,new)
text=text.replace('- Word revision 8 preserves the supplied Chapter I format and has passed layout verification.','- Word revision 9 preserves the supplied Chapter I format and has passed nine-page layout verification; its added bibliography is included for the standalone chapter.')
write(name,text)

# Historical review is left intact and receives a dated implementation pointer.
name='Manuscript/Chapter I Final Review 2026-10-30.md'
text=read(name)
text+='\n\n## Authorized correction follow-up\n\nThe user authorized implementation under D-020. [[Manuscript/Drafts/Land Grand - Chapter I - Revised - v9.docx|Revision 9]] applies the document corrections and includes a verified bibliography. D-021 supplies the researcher\'s personal-observation attribution for problem 4. [[Manuscript/Chapter I Revision Notes|Current revision notes]] identify remaining observation details, content validation, game rules and methodology points. The original reviewed file is preserved; the findings above describe that original version.\n'
write(name,text)

name='Sources/Chapter I Final User Draft 2026-10-30.md'
backup=ROOT/'vault-before-corrections'/name
backup.parent.mkdir(parents=True,exist_ok=True)
assert not backup.exists()
shutil.copy2(VAULT/name,backup)
text=read(name).replace('The last agent-generated full Word copy remains revision 8; neither that copy nor its mirrored Markdown was rewritten during this read-only review.','At the initial read-only review, the last agent-generated full Word copy was revision 8. The subsequent authorized correction produced [[Manuscript/Drafts/Land Grand - Chapter I - Revised - v9.docx|revision 9]] and updated the working Markdown; the retained source and earlier Word copies remain unchanged.')
write(name,text)

name='Maintenance/Change Log.md'
text=read(name)
text+='''

### Chapter I correction implemented in revision 9, 2026-10-30

- Recorded D-020 and edited a copy of the user's supplied Word chapter, preserving its school geometry, typography, styles, numbering and original files. Added three verified bibliography entries with live official links on page 9.
- Restored development tools, excluded quiz/GPS/scanning functions and device-testing qualification. Separated Scope's opening, clarified mixed-grade survey interpretation, corrected 2D and proposal tense, and preserved historical survey expectations.
- Recorded the user's personal-observation clarification under D-021 in [[Sources/Researcher Observation - Rock and Mineral Samples 2026-10-30|its source record]]. Attributed problem 4 to the researcher, retained date/setting/sample details under Q-12 and kept the unsupported city-wide inventory claim out of the manuscript.
- Made content/curriculum review and a complete-level content/device check prospective. Kept seven local Word comments for the remaining evidence, method and game-rule dependencies; no thresholds, completed validations or research results were invented.
- Rendered and inspected every final page. The copy has nine pages, Context on pages 1–4, restarted 1–4 lists and Bibliography on page 9. Verified native text, hyperlinks, PDF URI targets, comment wiring, preserve-only parts and the packaged source/final diff.
- Synchronized Markdown, current pointers, dashboard, revision notes, evidence status and research context. Earlier review history, Word copies, source documents and both raw survey CSVs remain unchanged. Backups and final checks are in the task-local correction folder.
'''
write(name,text)
print(json.dumps({'revision':9,'vault_synced':True,'decisions':['D-020','D-021'],'observation_record':observation,'open_items_preserved':['Q-01','Q-02','Q-03','Q-04','Q-05','Q-09','Q-10','Q-11','Q-12']},indent=2))
