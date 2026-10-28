"""Correct survey provenance from supplied CSV records and the user's follow-up."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent.parent
VAULT = WORKSPACE / 'LandGrand'
DATA = WORKSPACE / 'Research Data/Baluan Survey'
DATE = '2026-10-26'
origins = json.loads((ROOT / 'origins.json').read_text(encoding='utf-8-sig'))
checks = json.loads((ROOT / 'aggregate-checks.json').read_text(encoding='utf-8'))
assert checks['word_tally_mismatches'] == []
assert checks['files']['Parent.csv']['grade_counts'] == {'4':6,'5':6,'6':8}
assert checks['files']['Teacher.csv']['grade_counts'] == {'Kindergarten':2,'Grade 3':4,'Grade 4':5,'Grade 5':5,'Grade 6':4}
assert not DATA.exists(), 'Inspect existing research storage before replacing it.'
new_note = VAULT / 'Sources/Baluan Survey CSV Records.md'
assert not new_note.exists()
changes = {}

def get(relative):
    return changes.get(relative, (VAULT / relative).read_text(encoding='utf-8-sig'))

def replace(relative, old, new):
    text = get(relative)
    assert text.count(old) == 1, f'Expected one match in {relative}: {old[:75]}'
    changes[relative] = text.replace(old, new, 1)

parent = next(item for item in origins if item['name']=='Parent.csv')
teacher = next(item for item in origins if item['name']=='Teacher.csv')
note = f'''---
type: source-record
status: source
updated: {DATE}
---

# Baluan Survey CSV Records

## Source records

The user supplied these response exports to correct the earlier Grades 1–6 description. The files were parsed as UTF-8 CSV, retaining quoted multiline cells. Each file contains one header and 20 response records. Parent records have 24 columns; teacher records have 25.

| File | Original source | Bytes | Original modified UTC | SHA-256 |
| --- | --- | --- | --- | --- |
| Parent.csv | `{parent['source']}` | {parent['bytes']:,} | {parent['modifiedUtc']} | `{parent['sha256']}` |
| Teacher.csv | `{teacher['source']}` | {teacher['bytes']:,} | {teacher['modifiedUtc']} | `{teacher['sha256']}` |

Unchanged response-level originals are retained in designated research storage outside the Obsidian vault:

- [Retained Parent.csv](<D:/Projects/LandGrand-Sources/Research Data/Baluan Survey/Parent.csv>)
- [Retained Teacher.csv](<D:/Projects/LandGrand-Sources/Research Data/Baluan Survey/Teacher.csv>)
- [Research-source integrity manifest](<D:/Projects/LandGrand-Sources/Research Data/Baluan Survey/source-integrity.json>)

The vault contains aggregate summaries and these references, following [[Maintenance/Vault Guide|the research-data storage rule]]. Both Name and Email columns are blank in all 40 supplied records. Response timestamps and other response-level fields remain in the retained CSVs; they are not reproduced as searchable notes. Original and retained fingerprints were compared on import. The vault validator checks in-vault retained sources; these two research-storage fingerprints were checked separately.

## Corrected grade coverage

The supporting field is **column C**, data records **2–21**, in each file. Parent.csv labels it `Grade Level of Child:`; Teacher.csv labels it `Grade Level Handled:`. These fields describe the child's grade and the teacher's handled grade, respectively.

| Grade label normalized for comparison | Parent records | Teacher records |
| --- | ---: | ---: |
| Kindergarten | 0 | 2 |
| Grade 3 | 0 | 4 |
| Grade 4 | 6 | 5 |
| Grade 5 | 6 | 5 |
| Grade 6 | 8 | 4 |
| Total | 20 | 20 |

No records list Grade 1 or Grade 2. Parent records therefore cover **Grades 4–6**. Teacher records cover **Kindergarten and Grades 3–6**. Zero means no such records in these exports; it does not describe school enrolment or staffing.

There are six Grade 5 parent records and five Grade 5 teacher records available for a separate subgroup analysis. The existing Chapter I figures describe each full 20-record group. They must not be relabeled as Grade 5-only results or combined into one 40-person percentage. Names are blank, so record counts are not independent verification of unique identities.

## Survey and encoding dates

All parent timestamp fields show **July 7, 2026**; all teacher timestamp fields show **July 13, 2026**, with GMT+8 labels. After these dates were surfaced, [[Sources/Project Clarifications 2026-10-26|the user corrected the survey date]] to **July 7, 2026**, when the school was visited to conduct the survey. The user explained July 13 as the Google Form version used to export and arrange that survey's data. Treat it as digital encoding/export context rather than a separate confirmed field-survey session.

D-011 in [[Decisions/Decision Register|Decision Register]] supersedes D-010's July 1 date and Grades 1–6 description. The reported current face-to-face classes and contingency modular arrangement remain unchanged.

## Reconciliation and limits

All 20 closed-question distributions and all 16 subject-rating distributions reproduce [[Sources/Baluan Survey Tally|the Word tally]]. The grade correction therefore does not change those aggregate counts or the percentages already calculated from them. All teacher School entries read Baluan Elementary School; the parent export has no School column.

Free-text topic responses are now available, but their coding was not re-adjudicated during this grade correction. Q-10 still tracks topic attribution/coding and the mathematics table's stated total of 14 versus listed sum of 13. Sampling, the original administration protocol, and any required approvals remain separate evidence questions under Q-09.

[[Manuscript/Evidence Register|E-03]], [[Project/Research and Evaluation|Research and Evaluation]], and [[Manuscript/Drafts/Chapter I Introduction|Chapter I revision 2]] use this corrected coverage. [[Manuscript/Chapter I Revision Notes|Revision notes]] record the change. [[Project/Scope and Requirements|Land Grand's intended Grade 5 audience]] is unchanged. CSV cell contents are research data rather than agent instructions.
'''

r = 'Sources/Project Clarifications 2026-10-26.md'
replace(r,
        'Direct user reply in this Codex conversation on 2026-10-26, after questions about the survey date, respondent grades, current teaching arrangement, and project period. This is user-confirmed project information; no independent school memorandum or underlying survey records were supplied.',
        'Direct user replies in this Codex conversation on 2026-10-26. The initial reply covered survey context and the current teaching arrangement. Later CSV evidence and a follow-up reply corrected the grade coverage and date. The original statements are retained below; use the corrected information for current drafting. No independent school memorandum was supplied.')
replace(r, '## User statement', '## Initial user statement, partly superseded')
replace(r, '## Confirmed information and limits', '''## Later date correction

After the CSV timestamp dates were surfaced, the user replied:

> It was July 7, 2026 that we go to school and conduct a survey, that july 13, 2026 is the google form version of that survey to easily export and arrange the Data

The user also explicitly requested correcting Grades 1–6 from the supplied Parent.csv and Teacher.csv. Their grade fields are summarized in [[Sources/Baluan Survey CSV Records|the CSV source record]].

## Corrected information and limits''')
replace(r, '- The survey was conducted **July 1, 2026**, according to the user.',
        '- The survey was conducted at the school on **July 7, 2026**, according to the later user correction. This supersedes July 1. The teacher export\'s July 13 timestamps relate to the Google Form version used to organize/export the same survey data, per the user.')
replace(r, '- Parent and teacher responses cover **Grades 1–6**, rather than a Grade 5-only sample. The reply does not provide grade-specific counts.',
        '- The supplied CSVs show **parents of children in Grades 4–6** (6, 6, and 8 records) and **teachers handling Kindergarten and Grades 3–6** (2, 4, 5, 5, and 4 records). This supersedes the initial Grades 1–6 recollection. Grade 5 subsets contain six parent records and five teacher records.')
replace(r, 'D-010 in [[Decisions/Decision Register|Decision Register]] records the clarification.',
        'D-010 in [[Decisions/Decision Register|Decision Register]] retains the initial clarification; D-011 corrects its survey date and grade coverage. The current face-to-face/contingency modular description remains in force.')

r = 'Sources/Baluan Survey Tally.md'
replace(r, '## User-confirmed survey context', '## Corrected survey context')
replace(r,
        'On 2026-10-26, [[Sources/Project Clarifications 2026-10-26|the user confirmed]] that the survey was conducted **July 1, 2026**, and parent/teacher responses cover **Grades 1–6**. These details come from the direct clarification, not dates or grade labels printed in the supplied tally. No Grade 5-only counts were supplied. Record D-010 preserves the confirmation.',
        'The user later corrected the school-survey date to **July 7, 2026** and explained July 13 as the Google Form version used to organize/export the same data. [[Sources/Baluan Survey CSV Records|The supplied response exports]] establish parent coverage of **Grades 4–6** and teacher coverage of **Kindergarten and Grades 3–6**. They contain six Grade 5 parent records and five Grade 5 teacher records, but the Word tally combines all 20 records within each group. D-011 supersedes D-010\'s July 1/Grades 1–6 description; [[Sources/Project Clarifications 2026-10-26|the original statement and correction]] remain traceable.')
replace(r,
        'The supplied file itself does not document administration date, grade coverage, selection method, unique respondent identities, complete administration protocol, raw responses, or approvals. The user subsequently confirmed the date and Grades 1–6 coverage above; sampling, instruments, and underlying records remain unconfirmed. Keep the cross-grade findings distinct from the intended Grade 5 project audience.',
        'The supplied Word file itself does not document administration date, grade coverage, sampling, unique identities, complete administration protocol, response-level records, or approvals. The later user correction establishes the reported July 7 field-survey date, and the two retained CSVs provide grade fields, question headers, and response-level data. Sampling and original paper-administration details remain unconfirmed. Keep full-group figures distinct from any future Grade 5-only analysis.')

r = 'Project/Research and Evaluation.md'
replace(r,
        'The file itself omits collection date and grade coverage; [[Sources/Project Clarifications 2026-10-26|the user confirmed]] July 1, 2026 and Grades 1–6 coverage. Sampling and underlying records remain undocumented, as does a completed evaluation of Land Grand. Do not treat these cross-grade perceptions as Grade 5-only results, all-school prevalence, or learning gains.',
        'The user corrected the field-survey date to **July 7, 2026**, with the July 13 Google Form version used to arrange/export that survey data. [[Sources/Baluan Survey CSV Records|The supplied CSVs]] contain 20 parent records for children in Grades 4–6 and 20 teacher records for Kindergarten and Grades 3–6. Grade 5 subsets contain six parent records and five teacher records. Current chapter figures remain full-group summaries; sampling and a completed evaluation of Land Grand remain undocumented. Do not treat these perceptions as Grade 5-only findings, all-school prevalence, or learning gains.')

r = 'Manuscript/Evidence Register.md'
old_row = next(line for line in get(r).splitlines() if line.startswith('| E-03 |'))
replace(r, old_row,
        '| E-03 | Actual problem at Baluan Elementary School | [[Sources/Baluan Survey Tally|Word tally]], [[Sources/Baluan Survey CSV Records|CSV grade fields and response records]], and [[Sources/Project Clarifications 2026-10-26|corrected date/current school context]] | Source inspected; date corrected by user; sampling limited | Survey conducted July 7, 2026 per corrected user account. Parents: Grades 4–6; teachers: Kindergarten and Grades 3–6. Grade 5 subsets of six parent/five teacher records are available; current chapter statistics use the full groups. July 13 denotes the Google Form version, per the user. Q-09–Q-10 remain partly open. |')

r = 'Questions/Open Questions.md'
old_row = next(line for line in get(r).splitlines() if line.startswith('| Q-09 |'))
replace(r, old_row,
        '| Q-09 | Before generalizing survey findings | D-011 corrects the field-survey date to July 7, 2026 and uses the supplied CSV grade fields; raw response exports are now retained. How were respondents selected, and what original paper administration/approval records support the survey? | [[Sources/Baluan Survey CSV Records|CSV provenance]] and [[Sources/Baluan Survey Tally|Word tally]] | Partly resolved: corrected date, grade counts, and response exports available; sampling/administration evidence pending |')

r = 'Decisions/Decision Register.md'
old_row = next(line for line in get(r).splitlines() if line.startswith('| D-010 |'))
replace(r, old_row,
        old_row.replace('Record the user-confirmed survey date of July 1, 2026, Grades 1–6 parent/teacher coverage, and current face-to-face classes at Baluan with modular learning as a contingency during disruptions. These are user-provided facts, not independent school documentation.',
                        'Initially record the user\'s July 1, 2026/Grades 1–6 account and current face-to-face classes with contingency modular learning. The survey date and grade coverage are superseded by D-011; the school-context clarification remains unchanged. These are user-provided facts, not independent school documentation.'))
replace(r, '\nThe imported proposal is an initial documentary baseline.',
        '\n| D-011 | 2026-10-26 | Use the supplied CSV grade fields: parents of children in Grades 4–6; teachers handling Kindergarten and Grades 3–6. Record the user-corrected field-survey date of July 7, 2026; July 13 refers to the Google Form version for organizing/exporting the same survey data. Supersede D-010\'s date/grade portions and correct Chapter I while preserving source/history. | User requested correction from Parent.csv/Teacher.csv; [[Sources/Project Clarifications 2026-10-26|later user reply]] explains the dates. [[Sources/Baluan Survey CSV Records|CSV source record]] gives counts and locators. | [[Sources/Baluan Survey Tally|Survey provenance]], [[Manuscript/Evidence Register|Evidence Register]], [[Manuscript/Drafts/Chapter I Introduction|Chapter I revision 2]] |\n\nThe imported proposal is an initial documentary baseline.')
changes[r] = changes[r].replace('|\n\n| D-011', '|\n| D-011')

r = 'Manuscript/Drafts/Chapter I Introduction.md'
replace(r, 'revision: 1', 'revision: 2')
replace(r, '  - "[[Sources/Baluan Survey Tally]]"',
        '  - "[[Sources/Baluan Survey Tally]]"\n  - "[[Sources/Baluan Survey CSV Records]]"')
replace(r, 'Revised from the user\'s unrevised chapter on 2026-10-26.',
        'Revised from the user\'s unrevised chapter on 2026-10-26; revision 2 corrects survey date and grade coverage from the CSVs and follow-up clarification.')
old = "Local survey information adds context to this proposed use. The project clarification dates the survey to July 1, 2026, with parent and teacher responses covering Grades 1–6. The retained tally reports 20 responses to each closed question in the parent group and 20 in the teacher group. These cross-grade responses describe a broader school context; they do not establish a separate Grade 5 baseline ([[Sources/Baluan Survey Tally|Tally - Baluan]], n.d.; [[Sources/Project Clarifications 2026-10-26|project clarification]], 2026)."
new = """Local survey information adds context to this proposed use. The school survey was conducted on July 7, 2026, according to the corrected project clarification. The July 13 Google Form version was used to organize and export the same survey data. These dates describe field administration and subsequent digital preparation, respectively ([[Sources/Project Clarifications 2026-10-26|project clarification]], 2026).

The parent CSV contains six records for children in Grade 4, six in Grade 5, and eight in Grade 6. The teacher CSV contains two Kindergarten records and four, five, five, and four records for Grades 3, 4, 5, and 6, respectively. Each group therefore contains 20 records, with no Grade 1 or Grade 2 entries. The figures reported below summarize each full group rather than isolate the Grade 5 records ([[Sources/Baluan Survey CSV Records|survey response exports]]; [[Sources/Baluan Survey Tally|Tally - Baluan]], n.d.)."""
replace(r, old, new)
replace(r,
        '- **P-02:** Parent and teacher ratings identified perceived Science difficulty across Grades 1–6, supporting a focused Science resource without implying a Grade 5 test deficit.',
        '- **P-02:** Parent and teacher ratings identified perceived Science difficulty across their represented grades, supporting a focused resource without implying a Grade 5 test deficit.')
replace(r,
        '- The intended audience is Grade 5 learners at Baluan Elementary School. The Grades 1–6 survey provides broader context rather than Grade 5-specific findings.',
        '- The intended audience is Grade 5 learners at Baluan Elementary School. Survey figures in this chapter aggregate each respondent group across its represented grades.')

r = 'Manuscript/Chapter I Revision Notes.md'
replace(r, 'Revision 1, 2026-10-26.', 'Revision 2, 2026-10-26. This correction uses the supplied CSV grade fields and the user\'s corrected July 7 survey date.')
replace(r,
        '| Grades 1–6 survey respondents | Original wording implied Grade 5-only evidence | Use the user\'s confirmed cross-grade coverage; no Grade 5 subgroup is inferred. |',
        '| Survey respondent grade coverage | Earlier Grades 1–6 recollection; original manuscript implied Grade 5-only evidence | Parents: Grades 4–6. Teachers: Kindergarten and Grades 3–6. Grade 5 subsets contain six parent/five teacher records; main-text figures remain full-group summaries. |')
replace(r,
        '- Incorporated the July 1 survey date, Grades 1–6 coverage, present face-to-face teaching, and contingency use of modular learning from the direct user clarification.',
        '- Revision 1 used the earlier July 1/Grades 1–6 clarification. Revision 2 supersedes those details with the July 7 field-survey date and CSV-specific grades. Present face-to-face teaching and contingency modular use remain unchanged.')
replace(r,
        '| Project clarification, 2026 | [[Sources/Project Clarifications 2026-10-26|Direct user statement dated October 26, 2026]] | Survey date/coverage and reported current/contingency class arrangements. Formal treatment as personal communication or project evidence needs the chosen citation style. |',
        '| Project clarification, 2026 | [[Sources/Project Clarifications 2026-10-26|User statements and corrected date, October 26, 2026]] | July 7 field survey, July 13 digital-preparation context, and reported current/contingency class arrangements. Formal citation treatment remains subject to the selected style. |\n| Survey response exports | [[Sources/Baluan Survey CSV Records|Parent.csv and Teacher.csv]], column C, data records 2–21 | Corrected grade counts; available Grade 5 subsets; no change to full-group question/rating counts. |')
replace(r, '- **Q-09–Q-10:** Survey sampling, raw/instrument records, topic attribution/coding, and mathematics topic total of 14 versus sum of 13.',
        '- **Q-09–Q-10:** Sampling and original administration/approval records, topic attribution/coding, and mathematics topic total of 14 versus sum of 13. Response-level CSV exports are now retained.')
replace(r,
        'User confirmation resolves survey date, broad grade coverage, and the reported current class arrangement. Do not ask for those answers again unless new conflicting evidence arises.',
        'D-011 corrects the survey date and grade coverage using the later user reply and CSV records. The school-context clarification remains unchanged. Do not ask for these settled answers again unless new conflicting evidence arises.')

r = 'Manuscript/Drafting Dashboard.md'
replace(r,
        '- [x] Revise the four Chapter I sections from the supplied unrevised manuscript (2026-10-26); see [[Manuscript/Chapter I Revision Notes|revision notes]].',
        '- [x] Revise the four Chapter I sections from the supplied unrevised manuscript; revision 2 corrects the survey date/grades from the CSVs (2026-10-26). See [[Manuscript/Chapter I Revision Notes|revision notes]].')
replace(r, 'Needs evidence; revision 1 drafted 2026-10-26', 'Needs evidence; revision 2 saved 2026-10-26')
replace(r,
        'The user confirmed the survey date and Grades 1–6 coverage. Sampling, topic coding, and one topic-total discrepancy remain unresolved; no Grade 5-only baseline was supplied.',
        'D-011 corrects the field-survey date to July 7, 2026 and uses [[Sources/Baluan Survey CSV Records|CSV grade counts]]: parents Grades 4–6; teachers Kindergarten and Grades 3–6. Six Grade 5 parent records and five Grade 5 teacher records are available; current statistics use full groups. Sampling, topic coding, and one topic-total discrepancy remain unresolved.')

r = 'Current Focus.md'
replace(r, 'Chapter I revision 1 is saved in the working draft;', 'Chapter I revision 2 is saved in the working draft;')

r = 'Home.md'
replace(r,
        '- [[Sources/Baluan Survey Tally|Baluan survey tally]] — parent/teacher responses, subject difficulty ratings, and data checks for local context',
        '- [[Sources/Baluan Survey Tally|Baluan survey tally]] — parent/teacher responses, subject difficulty ratings, and data checks for local context\n- [[Sources/Baluan Survey CSV Records|Survey CSV records]] — verified grade counts, corrected survey date, and retained response exports')

r = 'Maintenance/Change Log.md'
changes[r] = get(r) + '''
### Survey CSV grade and date correction

- Added a source record for Parent.csv and Teacher.csv, retaining unchanged response-level copies in designated research storage outside the Obsidian vault. Aggregate summaries and source references are in the vault.
- Verified 20 parent records: Grade 4 = 6, Grade 5 = 6, Grade 6 = 8. Verified 20 teacher records: Kindergarten = 2, Grade 3 = 4, Grade 4 = 5, Grade 5 = 5, Grade 6 = 4. Neither export records Grade 1 or Grade 2.
- Recorded D-011, superseding D-010's date/grade portions. The user corrected the field-survey date to July 7, 2026 and explained July 13 as the Google Form version used to arrange/export the same survey data.
- Updated the current Chapter I text to revision 2, evidence register, survey provenance, questions, dashboard, and research context. Preserved historical quotes and the initial decision with an explicit correction marker. The intended Grade 5 game audience is unchanged.
- All 20 closed-question distributions and 16 subject-rating distributions match the Word tally; existing full-group statistics remain unchanged. Six Grade 5 parent records and five Grade 5 teacher records are available for a separate analysis, which was not substituted for the existing figures.
'''

# Update the current text counts without rewriting historical log entries.
chapter = changes['Manuscript/Drafts/Chapter I Introduction.md']
def wc(text):return len(re.findall(r"\b[\w]+(?:['’\-][\w]+)*\b",text))
main = 'This chapter presents' + chapter.split('This chapter presents',1)[1]
context = chapter.split('## Project Context\n\n',1)[1].split('\n## Purpose and Description',1)[0]
r = 'Manuscript/Chapter I Revision Notes.md'
changes[r] = re.sub(r'revised main text approximately [\d,]+; revised Project Context approximately [\d,]+',
                    f'revised main text approximately {wc(main):,}; revised Project Context approximately {wc(context):,}',get(r))

backup = ROOT / 'notes-before-grade-correction.zip'
assert not backup.exists()
with ZipFile(backup,'w',ZIP_DEFLATED) as archive:
    for relative in changes:
        archive.write(VAULT / relative, 'LandGrand/' + relative)

DATA.mkdir(parents=True)
for item in origins:
    payload = (ROOT/item['name']).read_bytes()
    assert hashlib.sha256(payload).hexdigest() == item['sha256']
    (DATA/item['name']).write_bytes(payload)
(DATA/'source-integrity.json').write_text(json.dumps({'recorded':DATE,'files':origins},indent=2)+'\n',encoding='utf-8')
new_note.write_text(note,encoding='utf-8')
for relative,text in changes.items():
    (VAULT/relative).write_text(text,encoding='utf-8')
result = {'new_note':str(new_note),'raw_research_files':[str(DATA/item['name']) for item in origins],
          'changed_notes':list(changes),'parent_grade_counts':checks['files']['Parent.csv']['grade_counts'],
          'teacher_grade_counts':checks['files']['Teacher.csv']['grade_counts'],
          'field_survey_date':'2026-07-07','google_form_version_date':'2026-07-13',
          'main_word_count':wc(main),'context_word_count':wc(context),'word_tally_mismatches':[]}
(ROOT/'correction-report.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
