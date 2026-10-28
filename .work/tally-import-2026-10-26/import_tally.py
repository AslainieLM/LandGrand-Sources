"""One-time import of the user-supplied aggregate Baluan survey tally."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
import math
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent.parent
VAULT = WORKSPACE / 'LandGrand'
DATE = '2026-10-26'
origin = json.loads((ROOT / 'origin.json').read_text(encoding='utf-8-sig'))
report = json.loads((ROOT / 'inspection.json').read_text(encoding='utf-8'))
tables = {b['number']: b['rows'] for b in report['blocks'] if b['kind'] == 'table'}
snapshot = (ROOT / 'source.docx').read_bytes()
assert hashlib.sha256(snapshot).hexdigest() == origin['sha256']

new_paths = ['Sources/Baluan Survey Tally.md', 'Sources/Baluan Survey Tally Extract.md',
             'Sources/Attachments/Tally - Baluan.docx',
             'Sources/Attachments/Baluan Survey Tally Images/Baluan Survey Tally Image 01.png',
             'Sources/Attachments/Baluan Survey Tally Images/Baluan Survey Tally Image 02.png']
for relative in new_paths:
    assert not (VAULT / relative).exists(), f'Already exists: {relative}'

changes = {}
def edit(relative, old, new):
    text = changes.get(relative, (VAULT / relative).read_text(encoding='utf-8-sig'))
    assert text.count(old) == 1, f'Expected one replacement in {relative}: {old[:70]}'
    changes[relative] = text.replace(old, new, 1)

def updated(relative):
    edit(relative, 'updated: 2026-10-24', 'updated: ' + DATE)

# Prepare every canonical-note change before writing any vault files.
relative = 'Home.md'
updated(relative)
edit(relative, '- [[Research/Proposal Review|Proposal review]]',
     '- [[Sources/Baluan Survey Tally|Baluan survey tally]] — parent/teacher responses, subject difficulty ratings, and data checks for local context\n- [[Research/Proposal Review|Proposal review]]')

relative = 'Manuscript/Evidence Register.md'
updated(relative)
edit(relative,
     '| E-03 | Actual problem at Baluan Elementary School | Proposal identifies the setting but supplies no local baseline results | Missing | Chapter I Context: obtain an actual documented observation, school record, or discussion record with date and attribution. |',
     '| E-03 | Actual problem at Baluan Elementary School | [[Sources/Baluan Survey Tally|User-supplied parent/teacher tally]], including reported difficulty explaining modules, subject ratings, and science-topic frequencies | Source inspected; provenance incomplete | Chapter I Context: cite the tally as reported perceptions with exact table/question locators. Confirm collection date, grade coverage, sampling, and instruments; resolve Q-09–Q-10. It does not establish pupil test performance or measured learning gains. |')
edit(relative,
     '| E-10 | Measured learning effectiveness | [[Project/Research and Evaluation|Evaluation method and results are undocumented]] | Missing | Describe the intended benefit; establish a method and results before claiming effectiveness. |',
     '| E-10 | Measured learning effectiveness | [[Project/Research and Evaluation|Evaluation method and results are undocumented]]; [[Sources/Baluan Survey Tally|the survey tally]] reports perceptions and expectations | Missing | Describe the intended benefit; establish a method and results before claiming effectiveness. Survey expectations are not evidence of Land Grand learning gains. |')

relative = 'Project/Research and Evaluation.md'
updated(relative)
edit(relative, '  - "[[Sources/Pre-proposal]]"',
     '  - "[[Sources/Pre-proposal]]"\n  - "[[Sources/Baluan Survey Tally]]"')
edit(relative, '## What remains undocumented', '''## Supplied local survey tally

[[Sources/Baluan Survey Tally|Tally - Baluan.docx]] was supplied by the user on 2026-10-26. Its parent and teacher closed-question tables each report 20 responses per item. It also contains subject-difficulty rating distributions, descriptive statistics, two charts, and topic-frequency tables. These are aggregate reported responses; individual records were not supplied.

The tally can support a carefully attributed account of local perceptions and willingness to use mobile learning tools for [[Manuscript/Evidence Register|E-03]]. It does not document the collection date, respondent grade coverage, sampling, or a completed evaluation of Land Grand. Do not infer Grade 5 participation, all-school conditions, or learning gains from the filename or project audience.

The source record owns the figures and calculation checks. Q-09–Q-10 in [[Questions/Open Questions|Open Questions]] track missing provenance and a mathematics-topic total discrepancy. The supplied questions do not authorize additional game features or alter the proposal scope.

## What remains undocumented''')
edit(relative,
     'No claim of effectiveness can currently be supported by this source.',
     'No claim of effectiveness can currently be supported by the pre-proposal or the supplied perception tally.')

relative = 'Manuscript/Drafting Dashboard.md'
updated(relative)
edit(relative,
     '| I — Project Context | [[Manuscript/Drafts/Chapter I Introduction#Project Context|Open section]] | Scaffold only; evidence needed | Find credible global/national evidence and actual local observations; use E-01–E-03. |',
     '| I — Project Context | [[Manuscript/Drafts/Chapter I Introduction#Project Context|Open section]] | Scaffold only; local tally available | Find global/national evidence; use [[Sources/Baluan Survey Tally|the local tally]] within its limits and confirm Q-09–Q-10; use E-01–E-03. |')
edit(relative,
     'Local problem and local novelty claims need evidence before being presented as facts.',
     'The local survey tally is available for attributed perceptions, with provenance and one topic-total discrepancy unresolved. Stronger local problem claims and local novelty claims still need supporting evidence.')

relative = 'Manuscript/Drafts/Chapter I Introduction.md'
updated(relative)
edit(relative, '  - "[[Sources/Pre-proposal]]"',
     '  - "[[Sources/Pre-proposal]]"\n  - "[[Sources/Baluan Survey Tally]]"')
edit(relative,
     'The writing guide records the two-page guidance and the unresolved meaning of “at least four problems.”',
     'The writing guide records the two-page guidance and the unresolved meaning of “at least four problems.”\n\n**Local evidence available:** [[Sources/Baluan Survey Tally|The supplied survey tally]] records parent/teacher perceptions and topic frequencies. Use exact question/table locators and retain its missing collection/grade/sampling details and arithmetic discrepancy. These responses do not establish pupil test scores or the game\'s effectiveness.')

relative = 'Questions/Open Questions.md'
updated(relative)
edit(relative, '  - "[[Sources/Pre-proposal]]"',
     '  - "[[Sources/Pre-proposal]]"\n  - "[[Sources/Baluan Survey Tally]]"')
edit(relative, 'These gaps come from reviewing the proposal.',
     'These gaps come from reviewing the proposal and later supplied sources.')
edit(relative,
     '\nNo answers have been inferred from the Unity project.',
     '\n| Q-09 | Before generalizing survey findings | When was the Baluan survey administered, which grades and respondent groups were included, how were respondents selected, and where are the administered instruments and underlying records? The tally alone does not supply these details. | [[Sources/Baluan Survey Tally|Survey provenance]] | Open |\n| Q-10 | Before citing topic totals | Why does the mathematics-topic table report 14 when its listed frequencies sum to 13? Are the topic frequencies parent responses, teacher responses, or a combination, and how were multiple mentions coded? | [[Sources/Baluan Survey Tally#Data checks|Survey data checks]] | Open |\n\nNo answers have been inferred from the Unity project.')
# Keep the question rows in the same table, without a blank line before Q-09.
changes[relative] = changes[relative].replace('| Open |\n\n| Q-09', '| Open |\n| Q-09')

relative = 'Decisions/Decision Register.md'
updated(relative)
edit(relative,
     '\nThe imported proposal is an initial documentary baseline.',
     '\n| D-008 | 2026-10-26 | Retain the user-supplied Tally - Baluan.docx as survey source material in the vault, with a searchable extraction and links to manuscript evidence. Import does not certify the survey method, resolve discrepancies, or approve scope changes. | User supplied the file and requested its addition to the vault on this date. | [[Sources/Baluan Survey Tally|Survey tally]], [[Manuscript/Evidence Register|Evidence Register]], [[Project/Research and Evaluation|Research and Evaluation]] |\n\nThe imported proposal is an initial documentary baseline.')
changes[relative] = changes[relative].replace('|\n\n| D-008', '|\n| D-008')

# Read-only arithmetic checks; retain reported figures unchanged.
checks = {'closed_question_rows': 0, 'rating_rows': [], 'topic_totals': []}
for table_id in [1, 3]:
    for row in tables[table_id][1:]:
        assert sum(map(int, row[2:5])) == int(row[5]) == 20
        checks['closed_question_rows'] += 1
for table_id in [2, 4]:
    for row in tables[table_id][1:]:
        counts = list(map(int, row[3:8]))
        n = sum(counts)
        assert n == 20
        weighted = sum((i+1)*v for i, v in enumerate(counts))
        mean = Decimal(weighted) / Decimal(n)
        variance_sum = sum(v*((i+1)-float(mean))**2 for i, v in enumerate(counts))
        sample_sd = math.sqrt(variance_sum / (n-1))
        assert mean.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP) == Decimal(row[1])
        assert Decimal(str(sample_sd)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP) == Decimal(row[2])
        checks['rating_rows'].append({'table': table_id, 'subject': row[0], 'n': n,
                                    'mean_from_counts': str(mean), 'sample_sd_from_counts': sample_sd})
for table_id in range(5, 11):
    rows = tables[table_id]
    calculated = sum(int(row[1]) for row in rows[1:-1])
    checks['topic_totals'].append({'table': table_id, 'calculated': calculated, 'reported': int(rows[-1][1])})
assert [(r['table'], r['calculated'], r['reported']) for r in checks['topic_totals'] if r['calculated'] != r['reported']] == [(7, 13, 14)]
(ROOT / 'arithmetic-checks.json').write_text(json.dumps(checks, indent=2), encoding='utf-8')

# Record rollback copies before the first mutation.
backup = ROOT / 'notes-before-import.zip'
assert not backup.exists()
with ZipFile(backup, 'w', ZIP_DEFLATED) as archive:
    for relative in changes:
        archive.write(VAULT / relative, 'LandGrand/' + relative)
    for relative in ['LandGrand/Maintenance/Change Log.md', 'tools/source-integrity.json']:
        archive.write(WORKSPACE / relative, relative)

new_files = {'Sources/Attachments/Tally - Baluan.docx': snapshot}
media_paths = {}
for index, item in enumerate(report['media'], 1):
    relative = f'Sources/Attachments/Baluan Survey Tally Images/Baluan Survey Tally Image {index:02d}.png'
    new_files[relative] = (ROOT / item['name']).read_bytes()
    media_paths[item['name']] = relative

with ZipFile(ROOT / 'source.docx') as archive:
    rel_root = ET.fromstring(archive.read('word/_rels/document.xml.rels'))
    relationships = {node.attrib['Id']: node.attrib['Target'] for node in rel_root}
    document = ET.fromstring(archive.read('word/document.xml'))
    body = document.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}body')
    paragraph_images = {}
    paragraph = 0
    for child in body:
        if child.tag.endswith('}p'):
            paragraph += 1
            embeds = child.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}blip')
            if embeds:
                paragraph_images[paragraph] = [media_paths['word/' + relationships[e.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed']]] for e in embeds]

table_labels = {
    1: 'Parents Part I', 2: 'Parents Subject Difficulty',
    3: 'Teachers Part I', 4: 'Teachers Subject Difficulty',
    5: 'Science Topic Frequencies', 6: 'English Topic Frequencies',
    7: 'Mathematics Topic Frequencies', 8: 'MAPEH Topic Frequencies',
    9: 'Araling Panlipunan Topic Frequencies', 10: 'EPP Topic Frequencies'}
extract = ['---', 'type: source-extract', 'status: source', 'updated: ' + DATE,
           'sources:', '  - "[[Sources/Baluan Survey Tally]]"', '---', '',
           '# Baluan Survey Tally Extract', '',
           'Faithful text and table extraction from the retained DOCX. The ten tables and nonblank body paragraphs follow OOXML body order, which is not a verified visual page order. Paragraph numbers include omitted blank paragraphs. Table numbers and descriptive labels are extraction locators, not source-assigned captions. Original wording and reported numbers are retained; table cell line breaks use `<br>`. Embedded chart bytes are unchanged, and chart text transcriptions are identified separately. See the source record for interpretation limits and the mathematics-total discrepancy.', '']
def cell(value):
    return value.replace('|', '\\|').replace('\n', '<br>')
for block in report['blocks']:
    if block['kind'] == 'paragraph':
        number = block['number']
        if block['text'].strip() or number in paragraph_images:
            extract.extend([f'## Paragraph {number:03d}', ''])
            if block['text'].strip():
                extract.extend(['> ' + line for line in block['text'].split('\n')])
                extract.append('')
            for relative in paragraph_images.get(number, []):
                extract.extend([f'![[{relative}]]', ''])
    elif block['kind'] == 'table':
        rows = block['rows']
        extract.extend([f"## Table {block['number']:02d} {table_labels[block['number']]}", '',
                        '| ' + ' | '.join(cell(v) for v in rows[0]) + ' |',
                        '| ' + ' | '.join('---' for _ in rows[0]) + ' |'])
        extract.extend('| ' + ' | '.join(cell(v) for v in row) + ' |' for row in rows[1:])
        extract.append('')
extract.extend(['## Chart text transcriptions', '',
                'The two images were visually inspected. The following prose transcribes their prompts, scale labels, and categories with line wrapping normalized. Their bars are visually consistent with the corresponding typed rating tables; the typed tables above retain the exact numerical frequencies.', '',
                '### Chart 01 Parents', '',
                '> Based on your observation, rate how difficult each subject is for your child using the scale below.  5 - Very Difficult | 4 - Difficult | 3 - Neutral | 2 - Slightly Difficult | 1 - Not Difficult', '',
                '### Chart 02 Teachers', '',
                '> Based on your teaching experience, rate how difficult each subject is for your students using the scale below.  5 - Very Difficult | 4 - Difficult | 3 - Neutral | 2 - Slightly Difficult | 1 - Not Difficult', '',
                'Both charts show rating legends in the order 5, 4, 3, 2, 1 and labeled vertical ticks 0, 5, 10, 15. Categories run English; Mathematics; Filipino; Araling Panlipunan (History); Science; MAPEH (Music, Arts, Physical Education, and Health); GMRC (Good Manners and Right Conduct); EPP (Edukasyong Pantahanan at Pangkabuhayan). These are chart labels, not verified descriptions of the sampled curriculum.', ''])
new_files['Sources/Baluan Survey Tally Extract.md'] = '\n'.join(extract).encode('utf-8')

record = f'''---
type: source-record
status: source
updated: {DATE}
---

# Baluan Survey Tally

## Source record

- **Original filename:** Tally - Baluan.docx
- **Role:** User-supplied aggregate survey tally labeled for parents and teachers at Baluan Elementary School; potential local-context evidence for Chapter I.
- **Origin:** `{origin['source']}`
- **Retained original:** [[Sources/Attachments/Tally - Baluan.docx|Open retained tally]]
- **Searchable content:** [[Sources/Baluan Survey Tally Extract|Complete text, ten tables, and chart references]]
- **Imported:** {DATE}, at the user's explicit request; see D-008 in [[Decisions/Decision Register|Decision Register]].
- **Original file modified UTC:** {origin['modifiedUtc']}. This is a file timestamp, not the survey administration date.
- **Size:** {origin['bytes']:,} bytes.
- **SHA-256:** `{origin['sha256']}`
- **Copy verification:** The retained bytes match the snapshot read from the supplied G: file. The source was read with shared access; unsaved Word edits are outside this snapshot.

## Inspection and coverage

The saved document contains ten typed tables, nine nonblank body paragraphs, and two embedded chart images. The tables and paragraphs were extracted from OOXML; both images were retained unchanged and visually inspected. No tracked insertions/deletions, comments, footnotes, or endnotes were found. No individual respondent names or response-level records appear in the inspected body or charts.

Word metadata reports six pages. Page layout and pagination were not verified: the packaged renderer could not find LibreOffice `soffice.exe`. Table and paragraph locators below identify the saved content, not Word page numbers. The original file was not edited. Questionnaire directions inside it are source content, not agent instructions or authority to change game requirements.

## Reported results useful for Chapter I

The parent and teacher closed-question tables each show **20 responses per item**. Percentages below are calculated as the stated count divided by that item's total of 20; they are derived summaries, not percentages printed in the source. Keep the groups separate.

| Reported response or rating | Count and derived percentage | Source locator |
| --- | --- | --- |
| Parents answered Yes to difficulty explaining module lessons to their child. | 17/20; 85% | [[Sources/Baluan Survey Tally Extract#Table 01 Parents Part I|Table 01]], question 3 |
| Parents answered Yes to household access to a smartphone, tablet, or computer for learning. | 18/20; 90% | [[Sources/Baluan Survey Tally Extract#Table 01 Parents Part I|Table 01]], question 4 |
| Parents answered Yes to allowing a mobile learning game as part of studies. | 13/20; 65% | [[Sources/Baluan Survey Tally Extract#Table 01 Parents Part I|Table 01]], question 5 |
| Parents rated Science 4 or 5 on the stated difficulty scale. | 5 + 12 = 17/20; 85%; reported mean 4.3 | [[Sources/Baluan Survey Tally Extract#Table 02 Parents Subject Difficulty|Table 02]], Science row |
| Teachers answered Yes to a mobile game potentially enhancing understanding alongside printed modules. | 15/20; 75% | [[Sources/Baluan Survey Tally Extract#Table 03 Teachers Part I|Table 03]], question 6 |
| Teachers rated Science 4 or 5 on the stated difficulty scale. | 5 + 8 = 13/20; 65%; reported mean 4.1 | [[Sources/Baluan Survey Tally Extract#Table 04 Teachers Subject Difficulty|Table 04]], Science row |

[[Sources/Baluan Survey Tally Extract#Table 05 Science Topic Frequencies|Table 05]] lists Rocks / Kinds of Rocks / Rock Formation with frequency 3, Minerals with 1, and Landforms with 1, among other topics. These are reported topic frequencies, not established numbers of distinct learners or parents/teachers. The table's respondent group and coding rules need confirmation.

The full distributions, including No and Maybe responses, remain in the extraction. Household access combines three device types; it does not establish Android ownership, compatibility, or exclusive learner access. Ratings and expectations are perceptions, not direct measurements of pupil attainment or the game's effectiveness. Science-topic mentions can support relevance cautiously; they do not establish that the game's chosen topics are the most prevalent difficulties.

## Data checks

- All 20 closed-question rows satisfy Yes + No + Maybe = the reported total of 20.
- All 16 subject-rating distributions sum to 20. Weighted means reproduce the reported one-decimal means under rounding half up. Sample standard deviations computed from the displayed frequencies also reproduce the reported one-decimal SDs. The source does not state its SD or rounding convention; these checks establish arithmetic consistency with those conventions, not the validity of underlying responses.
- Five of the six topic-frequency table totals equal the sum of their listed frequencies.
- **Discrepancy:** [[Sources/Baluan Survey Tally Extract#Table 07 Mathematics Topic Frequencies|Table 07]] reports Total **14**, while its eight listed frequencies sum to **13**. The original total and entries remain unchanged. Do not silently correct the source or cite 14 as verified; check the underlying tally with the researcher.

## Evidence limits and follow-up

The supplied file does not document the survey administration date, grade coverage, selection method, unique respondent identities, complete administration protocol, raw responses, or approvals. Its file date and school label do not establish those details. In particular, the document does not identify the responses as Grade 5-only. Confirm provenance and the source instruments before generalizing beyond these reported responses.

Topic tables follow a prompt after the teacher section, but are not explicitly labeled as teacher-only or combined responses. Confirm their respondent group, whether multiple topics per respondent were permitted, and how similar answers were grouped. See Q-09–Q-10 in [[Questions/Open Questions|Open Questions]].

[[Manuscript/Evidence Register|E-03]] links this tally to Chapter I local context. [[Project/Research and Evaluation|Research and Evaluation]] owns the distinction between this supplied survey and a future evaluation of Land Grand. No approval, implemented feature, local novelty, or measured learning gain is established by this import.
'''
new_files['Sources/Baluan Survey Tally.md'] = record.encode('utf-8')

relative = 'Maintenance/Change Log.md'
log = (VAULT / relative).read_text(encoding='utf-8-sig')
log = log.replace('updated: 2026-10-24', 'updated: ' + DATE, 1)
log += '''
## 2026-10-26

### Baluan survey tally import

- Recorded D-008 and preserved the supplied Tally - Baluan.docx unchanged, with its origin, file timestamp, size, and SHA-256 fingerprint.
- Extracted all ten tables and nine nonblank body paragraphs. Retained and visually inspected both embedded charts, including their rating-scale text.
- Linked the source from Home, Research and Evaluation, E-03, Drafting Dashboard, and the Chapter I scaffold. No manuscript prose or game feature was added.
- Checked closed-question totals, subject-rating distributions, and topic sums. Preserved the mathematics-topic total of 14 while flagging that its listed counts sum to 13.
- Added Q-09–Q-10 for survey provenance and topic-table clarification. Kept Grade 5 participation, administration date, sampling, local novelty, and measured learning gains unconfirmed.
- Word page layout was not verified because the packaged renderer could not find LibreOffice. Original-byte and link validation is recorded after the import checks.
'''
changes[relative] = log

manifest_path = WORKSPACE / 'tools/source-integrity.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
existing = {item['path'] for item in manifest['files']}
for relative, data in new_files.items():
    if relative.startswith('Sources/Attachments/'):
        assert relative not in existing
        manifest['files'].append({'path': relative, 'sha256': hashlib.sha256(data).hexdigest(),
                                  'role': 'original' if relative.endswith('.docx') else 'embedded-image'})
manifest['recorded'] = DATE

for relative, data in new_files.items():
    path = VAULT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
for relative, text in changes.items():
    (VAULT / relative).write_text(text, encoding='utf-8')
manifest_path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'new_files': list(new_files), 'updated_notes': list(changes),
                  'paragraph_image_locations': paragraph_images,
                  'retained_source_sha256': hashlib.sha256((VAULT / new_paths[2]).read_bytes()).hexdigest(),
                  'mathematics_topic_total': checks['topic_totals'][2]}, indent=2))
