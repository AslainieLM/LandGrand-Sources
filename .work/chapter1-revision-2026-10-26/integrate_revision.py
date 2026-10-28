"""Retain an unrevised manuscript and integrate its working revision and sources."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent.parent
VAULT = WORKSPACE / 'LandGrand'
DATE = '2026-10-26'
origin = json.loads((ROOT / 'origin.json').read_text(encoding='utf-8-sig'))
inspection = json.loads((ROOT / 'inspection.json').read_text(encoding='utf-8'))
original = (ROOT / 'source.docx').read_bytes()
assert hashlib.sha256(original).hexdigest() == origin['sha256']
assert not inspection['media']
assert all(b['kind'] in {'paragraph', 'sectPr'} for b in inspection['blocks'])
paragraphs = [b for b in inspection['blocks'] if b['kind'] == 'paragraph' and b['text'].strip()]
assert len(paragraphs) == 41
changes = {}
new = {}

def get(relative):
    return changes.get(relative, (VAULT / relative).read_text(encoding='utf-8-sig'))

def replace(relative, old, value):
    text = get(relative)
    assert text.count(old) == 1, f'{relative}: expected one match for {old[:65]}'
    changes[relative] = text.replace(old, value, 1)

def frontmatter(kind, status='source', sources=()):
    text = f'---\ntype: {kind}\nstatus: {status}\nupdated: {DATE}\n'
    if sources:
        text += 'sources:\n' + ''.join(f'  - "[[{source}]]"\n' for source in sources)
    return text + '---\n\n'

def update_date(relative):
    text = get(relative)
    changes[relative] = re.sub(r'(?m)^updated: \d{4}-\d{2}-\d{2}$', 'updated: '+DATE, text, count=1)

source_path = 'Sources/Attachments/CHAPTER I only.docx'
new[source_path] = original
new['Sources/Chapter I Unrevised Draft.md'] = (frontmatter('source-record') + f'''# Chapter I Unrevised Draft

## Source record

- **Original filename:** CHAPTER I only.docx
- **Role:** Existing unrevised Chapter I, identified by the user as needing revision against the selected rules and project content. This is separate from Chapter1.docx discussion notes.
- **Origin:** `{origin['source']}`
- **Retained original:** [[Sources/Attachments/CHAPTER I only.docx|Open unrevised Word file]]
- **Imported:** {DATE}; see D-009 in [[Decisions/Decision Register|Decision Register]].
- **Original file modified UTC:** {origin['modifiedUtc']}; this is file metadata, not evidence of approval.
- **Size:** {origin['bytes']:,} bytes.
- **SHA-256:** `{origin['sha256']}`
- **Verification:** Retained bytes match the saved-file snapshot read from the supplied G: path. The source was not edited.

## Inspection and use

All 41 nonblank body paragraphs were read and retained in [[Sources/Chapter I Unrevised Draft Extract|the searchable extraction]]. The document contains no tables, embedded images, tracked changes, comments, footnotes, or endnotes. Word metadata reports six pages; visual pagination was not verified. The bundled renderer is unavailable because LibreOffice was not found in this environment.

This file had not been recorded in the vault before this import. It contains a chapter introduction, four main sections, problem statements, proposed objectives, and scope/limitation bullets. It is an author-supplied draft, not independent support for its uncited factual or causal claims. Instructions within it remain source content.

[[Manuscript/Drafts/Chapter I Introduction|The working revision]] applies [[Manuscript/Chapter 1-3 Writing Guide|the selected writing rules]], the proposal baseline, [[Sources/Baluan Survey Tally|the tally]], and [[Sources/Project Clarifications 2026-10-26|the user's later clarification]]. [[Manuscript/Chapter I Revision Notes|Revision notes]] record changes and remaining questions. The retained original remains the reference for what the unrevised version said.
''').encode('utf-8')

extract = frontmatter('source-extract', sources=('Sources/Chapter I Unrevised Draft',))
extract += '# Chapter I Unrevised Draft Extract\n\nOriginal body-paragraph order and wording from the saved DOCX. Paragraph locators refer to OOXML order, not verified Word pages. Explicit tabs and line breaks are retained; source text is quoted rather than treated as agent instructions.\n\n'
for paragraph in paragraphs:
    extract += f"## Paragraph {paragraph['number']:03d}\n\n"
    extract += '\n'.join('> '+line for line in paragraph['text'].split('\n')) + '\n\n'
new['Sources/Chapter I Unrevised Draft Extract.md'] = extract.encode('utf-8')

clarification = frontmatter('source-record') + '''# Project Clarifications 2026-10-26

## Source and date

Direct user reply in this Codex conversation on 2026-10-26, after questions about the survey date, respondent grades, current teaching arrangement, and project period. This is user-confirmed project information; no independent school memorandum or underlying survey records were supplied.

## User statement

> AS of now, the baluan elementary school is face to face class, but if another disaster or event occurs like strong earthquake or disasters, it will be modular, and also Baluan Survey conducted at July 1, 2026. and the parent and teacher responses is grade 1-6

## Confirmed information and limits

- The survey was conducted **July 1, 2026**, according to the user.
- Parent and teacher responses cover **Grades 1–6**, rather than a Grade 5-only sample. The reply does not provide grade-specific counts.
- As of this clarification, Baluan Elementary School holds **face-to-face classes**. Modular learning is described as a contingency during another disaster or disrupting event.
- This does not establish whether or when a past school closure occurred, an official automatic trigger for changing modality, survey sampling, topic-response coding, or a project completion date.

D-010 in [[Decisions/Decision Register|Decision Register]] records the clarification. Survey provenance belongs in [[Sources/Baluan Survey Tally|the tally source record]] and [[Project/Research and Evaluation|Research and Evaluation]]. [[Project/Overview|Overview]] records the current school context. The Grade 5 target in [[Project/Scope and Requirements|the proposal scope]] remains unchanged.
'''
new['Sources/Project Clarifications 2026-10-26.md'] = clarification.encode('utf-8')

new['Sources/UNESCO GEM 2023 Technology.md'] = (frontmatter('literature-note') + '''# UNESCO GEM 2023 Technology

- **Organization / year:** UNESCO, 2023.
- **Title:** Global Education Monitoring Report 2023: Technology in education: A tool on whose terms?
- **Inspected source:** [Official Recommendations page](https://gem-report-2023.unesco.org/recommendations/), especially the introductory premise and four policy questions.
- **Bibliographic verification:** [Official publication record](https://www.unesco.org/gem-report/en/publication/technology).
- **Accessed:** 2026-10-26. The online recommendations and publication record were read; the complete report was not represented as read or retained locally.

## Relevant finding and boundary

The recommendations call for learner-centred, context-appropriate decisions supported by evidence, inclusion, and sustainability. This supports the design rationale in [[Manuscript/Drafts/Chapter I Introduction|Chapter I]], not a claim that Land Grand improves learning or that a particular local group has a measured deficit. Used for E-01 in [[Manuscript/Evidence Register|Evidence Register]].
''').encode('utf-8')

new['Sources/DepEd Distance Learning Strategies 2020.md'] = (frontmatter('literature-note') + '''# DepEd Distance Learning Strategies 2020

- **Organization / date:** Department of Education, Office of the Undersecretary for Curriculum and Instruction, July 21, 2020.
- **Title:** Suggested Strategies in Implementing Distance Learning Delivery Modalities (DLDM) for School Year 2020–2021.
- **Identifier:** DM-CI-2020-00162.
- **Source:** [Official DepEd-hosted PDF](https://region8.deped.gov.ph/wp-content/uploads/2020/07/DM-CI-2020-00162-2.pdf), 32 PDF pages.
- **Inspected locators:** PDF page 1 identifies the memorandum; pages 3–4, Appendix A items 1, 3, 6, and 12; page 6, Appendix B section A.
- **Accessed:** 2026-10-26. Relevant PDF text was read; no complete local copy is claimed.

## Relevant finding and boundary

The memorandum describes printed/digital modular arrangements, contextual selection, supplementary resources, and household learning support. It supplies historical Philippine context for E-02 in [[Manuscript/Evidence Register|Evidence Register]]. Its 2020–2021 scope does not establish Baluan's 2026 modality or current policy. Local circumstances come from [[Sources/Project Clarifications 2026-10-26|the user clarification]].
''').encode('utf-8')

new['Sources/PHIVOLCS Sarangani Earthquake 2026.md'] = (frontmatter('source-record') + '''# PHIVOLCS Sarangani Earthquake 2026

- **Organization:** DOST-PHIVOLCS.
- **Title / date:** Tsunami Information No. 2: Cancellation of Tsunami Warning, June 8, 2026, issued 3:19 PM.
- **Source:** [Official one-page advisory](https://tsunami.phivolcs.dost.gov.ph/Tsunami_Information/2026_Tsunami_Information/Jun/07/20260607_2337z_Advisory2_2.pdf).
- **Locator:** PDF page 1, opening event description.
- **Accessed:** 2026-10-26. Advisory text inspected; no local PDF copy claimed.

## Verified fact and boundary

The advisory confirms a magnitude 7.8 earthquake offshore Sarangani on June 8, 2026. It does not document a Baluan school closure or change of teaching mode. [[Manuscript/Drafts/Chapter I Introduction|The revision]] uses the event as regional background. [[Sources/Project Clarifications 2026-10-26|The user's clarification]] separately establishes the reported present school context.
''').encode('utf-8')

revised = (ROOT / 'revised-chapter.md').read_text(encoding='utf-8')
changes['Manuscript/Drafts/Chapter I Introduction.md'] = revised
def words(text):
    return len(re.findall(r"\b[\w]+(?:['’\-][\w]+)*\b", text))
original_words = words('\n'.join(p['text'] for p in paragraphs))
manuscript = revised.split('This chapter presents', 1)[1]
revised_words = words('This chapter presents' + manuscript)
context = revised.split('## Project Context\n\n', 1)[1].split('\n## Purpose and Description', 1)[0]

notes = frontmatter('revision-review', 'reviewed', ('Sources/Chapter I Unrevised Draft', 'Sources/Project Clarifications 2026-10-26', 'Manuscript/Chapter 1-3 Writing Guide')) + f'''# Chapter I Revision Notes

## Revision and status

Revision 1, {DATE}. [[Manuscript/Drafts/Chapter I Introduction|Open the revised working chapter]]. [[Sources/Chapter I Unrevised Draft|The supplied unrevised chapter]] is retained unchanged. The review changes section logic and claim strength, as well as grammar; it does not establish adviser approval, implemented software, or measured effectiveness.

The deliverable is working Markdown in the vault. No revised Word file or verified two-page Context layout is claimed. The source Word metadata reports six pages; the unavailable bundled renderer prevented a page-layout audit.

## Terminology ledger

| Canonical form | Variants or ambiguity in the original | Applied choice |
| --- | --- | --- |
| Land Grand | Land Grand; workspace name LandGrand | Retain the official academic spelling; workspace naming remains unchanged. |
| Grade 5 learners | Grade Five pupils; Grade Five students | Use Grade 5 learners for the target audience. |
| Grades 1–6 survey respondents | Original wording implied Grade 5-only evidence | Use the user's confirmed cross-grade coverage; no Grade 5 subgroup is inferred. |
| Game progress | Learning achievements; assessment; tracking progress | Describe completed levels, stars, and collected items without treating them as knowledge measures. |
| Episode / difficulty mode / level | Potential interchangeability | Follow [[GLOSSARY]] and retain their distinct meanings. |

## Revision notes

- Replaced generic app lists and unsupported claims about children, parental module completion, phone habits, and disengagement with attributed context and tally findings.
- Preserved the original project's supplementary Science-learning purpose. Added verified global/national context and separated the confirmed earthquake event from unverified school-disruption claims.
- Incorporated the July 1 survey date, Grades 1–6 coverage, present face-to-face teaching, and contingency use of modular learning from the direct user clarification.
- Replaced feature-quality labels under Objectives with a general objective and four proposed deliverables. Kept the completion date visible rather than claiming all SMART requirements are finalized.
- Restored the selected subsection names and proposal boundaries. Qualified stars, game saves, level counts, teacher monitoring, Android support, and the original blanket database exclusion against the canonical proposal.

## Problem and objective alignment

The retained four-bullet format is provisional. P-01–P-02 are reported concerns; P-03–P-04 are design needs, not additional measured local deficits. MW-01 still requires clarification if four independently evidenced problems are expected.

| Concern | Evidence and limits | Corresponding objective | Proposed requirement IDs |
| --- | --- | --- | --- |
| P-01: Difficulty assisting with module explanations | Parent question 3: 17 Yes, 2 No, 1 Maybe; cross-grade perceptions | O-01: Pre-level lessons and item explanations | LG-07, LG-10 |
| P-02: Perceived Science difficulty | Parent and teacher rating distributions; not Grade 5 test results | O-02: Focused landform episodes and selected content | LG-01, LG-03–LG-05; content selection remains Q-04 |
| P-03: Design need for an interactive supplement | Parent question 8 and teacher question 6 report expectations; no finding that current activities are absent | O-03: Exploration, collection, and review | LG-08–LG-10, LG-12 |
| P-04: Continuity and resumption as a design need | User-described contingency, with proposed offline/local-save scope; no local internet-deficit claim | O-04: Offline use with local save/load | LG-02, LG-19, LG-24 |

The objectives specify observable deliverables. Their time-bound element remains incomplete until Q-11 is answered. They do not promise a numerical learning gain or add an evaluation protocol.

## Main-text discipline audit

- **Kept:** Educational purpose, target school/audience, offline exploration, landform episodes, proposed level distribution, and local saves.
- **Replaced:** Uncited generalizations and a claimed current earthquake-related learning shift with bounded source-supported wording.
- **Compressed or removed:** Long app/platform catalogues, repeated promotional benefits, teacher achievement-tracking implications, and statements equating gameplay with assessment.
- **Added:** Source-attributed context, survey denominators and opposing/uncertain responses, cross-grade boundaries, and user-confirmed current context.
- **Statistics retained:** Selected question counts and derived 85% for parental explanation difficulty; subject-rating counts and topic mentions. These are descriptive summaries, not inferential evidence of effectiveness. Complete tables and arithmetic checks remain in [[Sources/Baluan Survey Tally|the source record and extraction]].
- **Word count:** Original extracted chapter {original_words:,}; revised main text approximately {revised_words:,}; revised Project Context approximately {words(context):,}. Counts use a consistent word-token rule, include in-text locators, and are not Word pagination. The increase supplies evidence and qualifications required by the writing rules; it is not presented as compression.

## Verified references and citation mapping

The working text uses provisional author–date citations. MW-02 remains open; no school-required citation style has been assumed.

| Working citation | Reference / actual reading location | Supported use |
| --- | --- | --- |
| UNESCO, 2023 | [[Sources/UNESCO GEM 2023 Technology|Official 2023 GEM recommendations and publication record]] | Context-appropriate, evidence-based educational technology decisions; no game efficacy claim. |
| Department of Education, 2020 | [[Sources/DepEd Distance Learning Strategies 2020|DM-CI-2020-00162, July 21, 2020]], PDF pages 3–4 and 6 | Historical distance-learning and supplementary-resource context. |
| DOST-PHIVOLCS, 2026 | [[Sources/PHIVOLCS Sarangani Earthquake 2026|Tsunami Information No. 2, June 8, 2026]], PDF page 1 | Occurrence, date, location, and magnitude of the earthquake. |
| Tally - Baluan, n.d. | [[Sources/Baluan Survey Tally|Unpublished aggregate tally]], exact group/question and rating/topic tables | Reported local perceptions and counts. Administration date is user-confirmed separately; no publication date or author is invented. |
| Project clarification, 2026 | [[Sources/Project Clarifications 2026-10-26|Direct user statement dated October 26, 2026]] | Survey date/coverage and reported current/contingency class arrangements. Formal treatment as personal communication or project evidence needs the chosen citation style. |

## Pending confirmations

- **Q-11:** Project completion date and development/study period; required for final time-bound objectives and scope wording.
- **Q-01:** Android version range; the unrevised Android 10+ wording does not resolve the pre-proposal's conflicting range.
- **MW-01:** Meaning of at least four problems. Review P-03–P-04 as design needs; do not relabel them as measured problems without evidence.
- **MW-02:** Citation style, page size, margins, font, spacing, and verified Context length in the final Word layout.
- **Q-09–Q-10:** Survey sampling, raw/instrument records, topic attribution/coding, and mathematics topic total of 14 versus sum of 13.
- **Q-04–Q-05:** Final learning competencies/content validation and any method used to claim learning effectiveness.

User confirmation resolves survey date, broad grade coverage, and the reported current class arrangement. Do not ask for those answers again unless new conflicting evidence arises. The final chapter requires author/adviser review of the revised problem framing and supporting records.
'''
new['Manuscript/Chapter I Revision Notes.md'] = notes.encode('utf-8')

# Keep the owning notes consistent with the supplied clarification and actual draft progress.
r = 'Sources/Baluan Survey Tally.md'
replace(r, '## Reported results useful for Chapter I', '''## User-confirmed survey context

On 2026-10-26, [[Sources/Project Clarifications 2026-10-26|the user confirmed]] that the survey was conducted **July 1, 2026**, and parent/teacher responses cover **Grades 1–6**. These details come from the direct clarification, not dates or grade labels printed in the supplied tally. No Grade 5-only counts were supplied. Record D-010 preserves the confirmation.

## Reported results useful for Chapter I''')
replace(r, "The supplied file does not document the survey administration date, grade coverage, selection method, unique respondent identities, complete administration protocol, raw responses, or approvals. Its file date and school label do not establish those details. In particular, the document does not identify the responses as Grade 5-only. Confirm provenance and the source instruments before generalizing beyond these reported responses.",
        'The supplied file itself does not document administration date, grade coverage, selection method, unique respondent identities, complete administration protocol, raw responses, or approvals. The user subsequently confirmed the date and Grades 1–6 coverage above; sampling, instruments, and underlying records remain unconfirmed. Keep the cross-grade findings distinct from the intended Grade 5 project audience.')

r = 'Project/Overview.md'
update_date(r)
replace(r, '## Where to go next', '''## Current school context

As of 2026-10-26, [[Sources/Project Clarifications 2026-10-26|the user reports]] that Baluan Elementary School holds face-to-face classes, with modular learning as a contingency if another strong earthquake or other event disrupts classes. This clarification does not establish a current closure or an independently verified school policy. The proposed at-home supplementary use remains consistent with the proposal baseline.

## Where to go next''')

r = 'Project/Research and Evaluation.md'
replace(r, 'It does not document the collection date, respondent grade coverage, sampling, or a completed evaluation of Land Grand. Do not infer Grade 5 participation, all-school conditions, or learning gains from the filename or project audience.',
        'The file itself omits collection date and grade coverage; [[Sources/Project Clarifications 2026-10-26|the user confirmed]] July 1, 2026 and Grades 1–6 coverage. Sampling and underlying records remain undocumented, as does a completed evaluation of Land Grand. Do not treat these cross-grade perceptions as Grade 5-only results, all-school prevalence, or learning gains.')

r = 'Manuscript/Evidence Register.md'
replace(r,
        '| E-01 | Global context for the relevant Grade 5 learning problem | No specific research source entered | Missing | Chapter I Context: find relevant original studies or authoritative reports; retain population, date, and limitations. |',
        '| E-01 | Global context for the relevant Grade 5 learning problem | [[Sources/UNESCO GEM 2023 Technology|UNESCO 2023 recommendations]] | Context source inspected; population-specific evidence limited | Supports context-appropriate educational technology decisions. Does not establish a global Grade 5 Science deficit or prove game effectiveness. |')
replace(r,
        '| E-02 | Philippine/national context for the same problem | No specific national source entered | Missing | Chapter I Context: find evidence matching the subject and population; do not substitute unrelated performance figures. |',
        '| E-02 | Philippine/national context for the same problem | [[Sources/DepEd Distance Learning Strategies 2020|DepEd 2020 DLDM memorandum]]; [[Sources/PHIVOLCS Sarangani Earthquake 2026|PHIVOLCS event advisory]] for regional background | Historical/context sources inspected | Supports historical home-learning arrangements and the earthquake event separately. Does not establish a current Baluan closure, Grade 5 deficit, or national outcome trend. |')
replace(r,
        '| E-03 | Actual problem at Baluan Elementary School | [[Sources/Baluan Survey Tally|User-supplied parent/teacher tally]], including reported difficulty explaining modules, subject ratings, and science-topic frequencies | Source inspected; provenance incomplete | Chapter I Context: cite the tally as reported perceptions with exact table/question locators. Confirm collection date, grade coverage, sampling, and instruments; resolve Q-09–Q-10. It does not establish pupil test performance or measured learning gains. |',
        '| E-03 | Actual problem at Baluan Elementary School | [[Sources/Baluan Survey Tally|Parent/teacher tally]] and [[Sources/Project Clarifications 2026-10-26|user-confirmed date, grade coverage, and current school context]] | Source inspected; user context confirmed; sampling limited | Survey conducted July 1, 2026 across Grades 1–6; no Grade 5 subgroup supplied. Cite perceptions with exact locators. Current face-to-face classes and contingency modular use are user-reported. Q-09–Q-10 remain partly open. |')

r = 'Questions/Open Questions.md'
replace(r,
        '| Q-09 | Before generalizing survey findings | When was the Baluan survey administered, which grades and respondent groups were included, how were respondents selected, and where are the administered instruments and underlying records? The tally alone does not supply these details. | [[Sources/Baluan Survey Tally|Survey provenance]] | Open |',
        '| Q-09 | Before generalizing survey findings | The user confirmed July 1, 2026 and Grades 1–6 coverage in D-010. How were respondents selected, and where are the administered instruments, raw records, and any grade-specific counts? | [[Sources/Baluan Survey Tally|Survey provenance]] | Partly resolved: date and grade coverage confirmed by user |')
replace(r, '\nNo answers have been inferred from the Unity project.',
        '\n| Q-11 | Before finalizing Chapter I | What project completion date and development/study period should make the objectives time-bound and define the scope? | [[Manuscript/Chapter I Revision Notes#Pending confirmations|Chapter I revision]] | Open |\n\nNo answers have been inferred from the Unity project.')
changes[r] = changes[r].replace('| Open |\n\n| Q-11', '| Open |\n| Q-11')

r = 'Decisions/Decision Register.md'
replace(r, '\nThe imported proposal is an initial documentary baseline.',
        '\n| D-009 | 2026-10-26 | Retain CHAPTER I only.docx as the unrevised manuscript source and revise the working Chapter I against the selected guidance and project evidence. Preserve the original and distinguish it from discussion notes. | User supplied the document, identified it as unrevised, and stated that it needs revision under the Chapter I rules and content. | [[Sources/Chapter I Unrevised Draft|Unrevised chapter]], [[Manuscript/Drafts/Chapter I Introduction|Working revision]], [[Manuscript/Chapter I Revision Notes|Revision notes]] |\n| D-010 | 2026-10-26 | Record the user-confirmed survey date of July 1, 2026, Grades 1–6 parent/teacher coverage, and current face-to-face classes at Baluan with modular learning as a contingency during disruptions. These are user-provided facts, not independent school documentation. | [[Sources/Project Clarifications 2026-10-26|Direct user reply]] during Chapter I revision. | [[Sources/Baluan Survey Tally|Survey provenance]], [[Project/Overview|Overview]], [[Manuscript/Evidence Register|Evidence Register]] |\n\nThe imported proposal is an initial documentary baseline.')
changes[r] = changes[r].replace('|\n\n| D-009', '|\n| D-009')

r = 'Manuscript/Drafting Dashboard.md'
replace(r, '- [ ] Draft the Purpose and Description section from the pre-proposal. This can begin without inventing local problem statistics.',
        '- [x] Revise the four Chapter I sections from the supplied unrevised manuscript (2026-10-26); see [[Manuscript/Chapter I Revision Notes|revision notes]].\n- [ ] Review Chapter I problem framing and confirm the completion date, Android range, and remaining writing requirements.')
replace(r, '- [ ] Assemble evidence for Project Context using [[Manuscript/Evidence Register|Evidence Register]].',
        '- [ ] Complete the remaining evidence and provenance checks in [[Manuscript/Evidence Register|Evidence Register]]; initial global/national sources and the local tally are now linked.')
old_rows = [line for line in get(r).splitlines() if line.startswith('| I — ')]
new_status = [
    ('Needs evidence; revision 1 drafted 2026-10-26', 'Review cross-grade survey limits, P-03–P-04 as design needs, MW-01, and final Word length; use E-01–E-03.'),
    ('Drafting; revision 1 saved 2026-10-26', 'Review the proposed learner experience and wording of educational benefits; no local novelty claim is established.'),
    ('Drafting; revision 1 saved 2026-10-26', 'Confirm Q-11 completion date and review the four problem/objective mappings before finalizing SMART wording.'),
    ('Drafting; revision 1 saved 2026-10-26', 'Confirm Q-01 device range and study period; preserve unresolved detailed game rules.')]
assert len(old_rows) == 4
for old, (status, action) in zip(old_rows, new_status):
    cells = old.split(' | ')
    replace(r, old, cells[0]+' | '+cells[1]+' | '+status+' | '+action+' |')
replace(r, 'The local survey tally is available for attributed perceptions, with provenance and one topic-total discrepancy unresolved.',
        'The user confirmed the survey date and Grades 1–6 coverage. Sampling, topic coding, and one topic-total discrepancy remain unresolved; no Grade 5-only baseline was supplied.')

r = 'Maintenance/Vault Guide.md'
update_date(r)
replace(r, 'Working chapter files live in `Manuscript/Drafts`; their scaffolds are not completed prose.',
        'Working chapter files live in `Manuscript/Drafts`; each file and the dashboard declare its current state. A scaffold or working revision is not an approved manuscript.')

r = 'Current Focus.md'
update_date(r)
replace(r, '- Treat [[Sources/Chapter1 Discussion Notes|Chapter1.docx]] as discussion notes, as identified by the user. Its import does not establish that a finished chapter draft exists.',
        '- Distinguish [[Sources/Chapter1 Discussion Notes|Chapter1.docx discussion notes]] from [[Sources/Chapter I Unrevised Draft|CHAPTER I only.docx, the unrevised manuscript]]. Chapter I revision 1 is saved in the working draft; [[Manuscript/Chapter I Revision Notes|revision notes]] track remaining checks.')

r = 'Home.md'
replace(r, '- [[Sources/Baluan Survey Tally|Baluan survey tally]] — parent/teacher responses, subject difficulty ratings, and data checks for local context',
        '- [[Sources/Baluan Survey Tally|Baluan survey tally]] — parent/teacher responses, subject difficulty ratings, and data checks for local context\n- [[Sources/Chapter I Unrevised Draft|Unrevised Chapter I]] and [[Manuscript/Drafts/Chapter I Introduction|working revision]] — original manuscript, revised prose, and [[Manuscript/Chapter I Revision Notes|review notes]]\n- [[Sources/Project Clarifications 2026-10-26|2026-10-26 project clarification]] — confirmed survey date/coverage and reported school context')

r = 'Maintenance/Change Log.md'
changes[r] = get(r) + '''
### Chapter I source and working revision

- Retained CHAPTER I only.docx unchanged and extracted all 41 nonblank paragraphs. Recorded D-009 and distinguished this manuscript from Chapter1.docx discussion notes.
- Recorded D-010 from the user's reply: July 1, 2026 survey date; Grades 1–6 parent/teacher coverage; present face-to-face classes and contingency modular learning.
- Saved Chapter I revision 1 with the four selected sections, bounded context claims, four provisional problem/objective mappings, and the proposal's feature boundaries.
- Added source records for the UNESCO 2023 recommendations, DepEd's historical 2020 distance-learning memorandum, and the PHIVOLCS earthquake advisory. The event was verified separately from school delivery arrangements.
- Updated survey provenance, research context, evidence status, current focus, and drafting progress. Q-09 is partly resolved; Q-11 retains the unanswered completion date. Original source files and unresolved requirements remain intact.
- Revision notes record terminology, claim changes, citations, word counts, and pending confirmations. No revised DOCX or verified Word pagination is claimed.
'''

# Guard against accidental overwrites and retain local rollback copies.
for relative in new:
    assert not (VAULT / relative).exists(), f'Already exists: {relative}'
backup = ROOT / 'notes-before-revision.zip'
assert not backup.exists()
with ZipFile(backup, 'w', ZIP_DEFLATED) as archive:
    for relative in changes:
        archive.write(VAULT / relative, 'LandGrand/' + relative)
    archive.write(WORKSPACE / 'tools/source-integrity.json', 'tools/source-integrity.json')

manifest_path = WORKSPACE / 'tools/source-integrity.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
assert source_path not in {e['path'] for e in manifest['files']}
manifest['recorded'] = DATE
manifest['files'].append({'path': source_path, 'sha256': origin['sha256'], 'role': 'original'})
for relative, data in new.items():
    path = VAULT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
for relative, text in changes.items():
    (VAULT / relative).write_text(text, encoding='utf-8')
manifest_path.write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
summary = {'new_files': list(new), 'updated_notes': list(changes), 'original_paragraphs': len(paragraphs),
           'original_word_count': original_words, 'revised_word_count': revised_words,
           'context_word_count': words(context), 'retained_sha256': origin['sha256']}
(ROOT / 'integration-report.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
print(json.dumps(summary, indent=2))
