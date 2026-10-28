from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from collections import Counter
from pypdf import PdfReader
import csv
import hashlib
import json
import re
import shutil

ROOT=Path(__file__).resolve().parent
VAULT=Path(r'D:\Projects\LandGrand-Sources\LandGrand')
OUTPUT=VAULT/'Manuscript/Drafts/Land Grand - Chapter I - Revised - v5.docx'
RECORDS=json.loads((ROOT/'revision5.json').read_text(encoding='utf-8'))
BUILD=json.loads((ROOT/'build-audit.json').read_text(encoding='utf-8'))
AUDIT=json.loads((ROOT/'render-1/word-audit.json').read_text(encoding='utf-8-sig'))
W={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert AUDIT['readOnly'] and AUDIT['pages']==8
assert [p['text'] for p in AUDIT['paragraphs']]==[r[2] for r in RECORDS]
assert AUDIT['paragraphCount']==len(RECORDS)==57
assert not BUILD['sentences_over_30_words']
intro_pages={}
for index,(role,_,text) in enumerate(RECORDS):
    if role in ('heading','subheading'):
        assert RECORDS[index+1][0] in ('section_intro','subsection_intro')
        intro_pages[text]={'heading_page':AUDIT['paragraphs'][index]['startPage'],'intro_page':AUDIT['paragraphs'][index+1]['startPage']}
assert len(intro_pages)==6
start=next(i for i,r in enumerate(RECORDS) if r[2]=='Project Context')
end=next(i for i,r in enumerate(RECORDS) if r[2]=='Purpose and Description of the Project')
context_start=AUDIT['paragraphs'][start]['startPage']
context_end=AUDIT['paragraphs'][end-1]['endPage']
assert context_end-context_start>=2
assert len(PdfReader(ROOT/'render-1/revision5.pdf').pages)==8
assert sha(ROOT/'revision4.docx')=='7a36e13c404ec006d00aef523847e59fa0fa0d49501df0c42f8ba856f90669f8'
assert sha(VAULT/'Manuscript/Drafts/Land Grand - Chapter I - Revised.docx')==sha(ROOT/'revision4.docx')

research=VAULT.parent/'Research Data/Baluan Survey'
for name,expected in {'Parent.csv':'a772bdc1ece510fc6181b13390e42ce717c9ca4ec5d25ab72af4b54d40daae57','Teacher.csv':'88e0291776f88f1ea925b14e0377cc46aec65a808698ab590c3329704a14f9ac'}.items():
    assert sha(research/name)==expected
with (research/'Parent.csv').open(encoding='utf-8-sig',newline='') as stream:
    parent=list(csv.reader(stream))
matches=[i for i,h in enumerate(parent[0]) if 'explain' in h.lower() and 'module' in h.lower()]
assert len(matches)==1,matches
answers=Counter(r[matches[0]].strip().lower() for r in parent[1:])
assert len(parent)-1==20 and answers['yes']==17 and 100*answers['yes']/20==85

# Only app statistics change after the verified render; body/geometry stay identical.
with ZipFile(OUTPUT) as z:
    infos=z.infolist()
    data={i.filename:z.read(i.filename) for i in infos}
rendered_body_hash=hashlib.sha256(data['word/document.xml']).hexdigest()
app=etree.fromstring(data['docProps/app.xml'])
app_ns={'a':'http://schemas.openxmlformats.org/officeDocument/2006/extended-properties'}
for name,key in [('Pages','pages'),('Words','words'),('Characters','characters'),('CharactersWithSpaces','charactersWithSpaces'),('Paragraphs','paragraphCount'),('Lines','lines')]:
    node=app.find('a:'+name,app_ns)
    if node is not None:node.text=str(AUDIT[key])
data['docProps/app.xml']=etree.tostring(app,encoding='UTF-8',xml_declaration=True,standalone=True)
temp=ROOT/'metadata-final.docx'
with ZipFile(temp,'w') as z:
    for info in infos:z.writestr(info,data[info.filename])
shutil.copyfile(temp,OUTPUT)
with ZipFile(ROOT/'reference.docx') as a,ZipFile(OUTPUT) as b:
    assert b.testzip() is None
    assert set(a.namelist())==set(b.namelist())
    changed=[name for name in a.namelist() if a.read(name)!=b.read(name)]
    assert set(changed)=={'word/document.xml','docProps/app.xml'}
    old=etree.fromstring(a.read('word/document.xml')).find('w:body/w:sectPr',W)
    new=etree.fromstring(b.read('word/document.xml')).find('w:body/w:sectPr',W)
    assert etree.tostring(old,method='c14n',exclusive=True)==etree.tostring(new,method='c14n',exclusive=True)
    assert rendered_body_hash==hashlib.sha256(b.read('word/document.xml')).hexdigest()
assert sha(VAULT/'Sources/Attachments/CHAPTER I only.docx')==sha(ROOT/'reference.docx')
for n in range(1,9):
    assert sha(ROOT/f'render-1/page-{n}.png')==sha(ROOT/f'fidelity-1/b_render/page-{n}.png')

BACKUP=ROOT/'vault-before-revision5'
def read(rel):return (VAULT/rel).read_text(encoding='utf-8-sig')
def save(rel,text):
    path=VAULT/rel
    backup=BACKUP/rel
    backup.parent.mkdir(parents=True,exist_ok=True)
    if path.exists() and not backup.exists():shutil.copyfile(path,backup)
    text=re.sub(r'(?m)^updated: \d{4}-\d{2}-\d{2}$','updated: 2026-10-28',text,count=1)
    path.write_text(text,encoding='utf-8')
def patch(rel,pairs):
    text=read(rel)
    for before,after in pairs:
        assert before in text,(rel,before)
        text=text.replace(before,after,1)
    save(rel,text)

feedback='Sources/Chapter I Readability Feedback 2026-10-28.md'
save(feedback,'''---
type: source-record
status: source
updated: 2026-10-28
---

# Chapter I Readability Feedback 2026-10-28

## Direct user request

The user reviewed the revised Word chapter and requested a clearer revision and persistent vault rules:

> Kindly review the Lang Grand - Chapter 1 - Revised? I think that the essay and sentence is so difficult to read, and also avoid repetitive numbers in survey tally in the Project Context, Use Basic but Academic English to make it more understandable, and also the introductory paragraph for each sub section was not implemented, improvise the vault and add it to the rules

The user invoked ask-matt for routing. The official project spelling remains Land Grand. D-016 records the requested writing standard; [[Manuscript/Chapter 1-3 Writing Guide#Readability and subsection openings|the writing guide]] owns its operational rules.

## Review finding and response

Revision 4 presented many survey distributions in sequence and used abstract phrasing. Its openings did not consistently function as separate introductions; Objectives combined its opening with the general objective. Revision 5 uses basic academic English, summarizes the survey in a few connected paragraphs, and gives all four main sections plus Scope and Limitations their own opening paragraphs.

The survey sample/grade coverage is stated once, and the 85% parent-explanation finding is reported once. Other results are summarized in words, including mixed parental views, device-access limits, and small cross-grade samples. Detailed figures remain unchanged in [[Sources/Baluan Survey Tally|the tally]] and [[Sources/Baluan Survey CSV Records|the CSV source record]]. This is an editorial change, not new data or a scope amendment.

## Version handling

The earlier revised Word file was open and write-locked by another process. It was retained unchanged as revision 4. [[Manuscript/Drafts/Land Grand - Chapter I - Revised - v5.docx|Revision 5]] is a separate file and the current review copy. [[Manuscript/Chapter I Revision Notes|Revision notes]] hold verification and remaining questions.
''')

guide='Manuscript/Chapter 1-3 Writing Guide.md'
text=read(guide)
assert '\n## Readability and subsection openings\n' not in text
rules='''## Readability and subsection openings

Apply these requirements whenever drafting or revising Chapters I–III. They implement D-016 and [[Sources/Chapter I Readability Feedback 2026-10-28|the user's readability feedback]].

1. **Use basic academic English.** Choose familiar, precise words, direct verbs, and one main idea per sentence. Split sentences that combine several ideas. Keep necessary technical terms and explain unfamiliar ones when first used. Read each paragraph for a clear topic and a useful connection to the next paragraph.
2. **Introduce every section and subsection.** Place a separate, short introductory paragraph immediately after each heading and before detailed explanations or bullets. Usually 2–3 sentences should explain the topic and what the discussion will cover. In Chapter I, check Project Context, Purpose and Description, Objectives, Scope and Limitations, Scope, and Limitations. Keep the Objectives introduction separate from the general objective.
3. **Summarize the survey to explain the problem.** State the survey date, sample size, and grade coverage once in Project Context. Select only the figures needed for the argument. Report a finding as a count or percentage once, with the relevant denominator clear. Explain its meaning rather than listing every answer category. Keep full distributions and calculations in the source notes.
4. **Preserve evidence limits.** Include mixed or opposing views when they affect the interpretation. Retain the cross-grade coverage, small Grade 5 groups, and distinction between adult views and measured learning. A shorter summary must remain faithful to the data.
5. **Review before delivery.** Read the complete text for clarity, check every heading's opening paragraph, and remove repeated tally figures or repeated explanations. Verify the final Word pages and the two-page Context requirement. Meet required length through relevant discussion, not padding.

Use normal academic prose in the manuscript; the concise chat preference applies to conversation. These rules change presentation, not project scope or the original research data.

'''
text=text.replace('## Chapter I – Introduction',rules+'## Chapter I – Introduction',1)
text=text.replace('Preserve unresolved items, including Android support, star criteria, and completion rules. State a study time frame only when it is supplied and confirmed.', 'Preserve unresolved items, including device validation, star criteria, and completion rules. Android 10 and above is settled under D-012. Use the documented planned completion window under D-015 without treating it as an exact approved deadline or full study period.')
text=text.replace('- Use the selected headings and maintain source locators for writing requirements.', '- Apply [[Manuscript/Chapter 1-3 Writing Guide#Readability and subsection openings|the readability and opening-paragraph requirements]], then use the selected headings and source locators.')
save(guide,text)

patch('Maintenance/Skill Guide.md',[
('| Draft or continue a chapter | Dashboard row for the target section, its working draft, and the relevant part of [[Manuscript/Chapter 1-3 Writing Guide|Writing Guide]] |','| Draft or revise a chapter | Read [[Manuscript/Chapter 1-3 Writing Guide#Readability and subsection openings|the required writing rules]], then the dashboard row, target draft, and relevant chapter guidance. |'),
('| Improve existing prose | [[Manuscript/Chapter 1-3 Writing Guide#Language editing skills|Language editing skills]] |','| Improve existing prose | Apply [[Manuscript/Chapter 1-3 Writing Guide#Readability and subsection openings|the required writing rules]] with the [[Manuscript/Chapter 1-3 Writing Guide#Language editing skills|language editing skills]]. |')])

text=read('Decisions/Decision Register.md')
row='| D-016 | 2026-10-28 | Use basic academic English, concise survey summaries without repeated tally figures, and a separate introductory paragraph for every manuscript section/subsection. Make these review requirements persistent in the vault and revise Chapter I accordingly. | [[Sources/Chapter I Readability Feedback 2026-10-28|Direct user feedback and revision request]]. | [[Manuscript/Chapter 1-3 Writing Guide#Readability and subsection openings|Writing rules]], [[Manuscript/Drafts/Chapter I Introduction|Chapter I revision 5]], [[Maintenance/Skill Guide|Skill routing]] |'
assert '| D-016 |' not in text
text=text.replace('\n\nThe imported proposal is an initial documentary baseline.','\n'+row+'\n\nThe imported proposal is an initial documentary baseline.',1)
save('Decisions/Decision Register.md',text)

old=read('Manuscript/Drafts/Chapter I Introduction.md')
front=old.split('---',2)[1]
front=re.sub(r'(?m)^revision:.*$','revision: 5',front)
front+='  - "[[Sources/Chapter I Readability Feedback 2026-10-28]]"\n'
lines=['---'+front+'---\n\n# Chapter I Introduction\n',
       f'> Revision 5, ready for user review. [[Manuscript/Drafts/Land Grand - Chapter I - Revised - v5.docx|Open the current Word copy]]. Revised under D-016 for basic academic English, concise survey discussion, and six separate section/subsection introductions. All eight Word pages were inspected; Project Context spans pages {context_start}–{context_end}. Earlier revision 4 and the original school-format file remain unchanged. The planned completion window retains the D-015 distinction: user-supplied November–December, with 2026 inferred and disclosed. See [[Manuscript/Chapter I Revision Notes|revision notes]] for evidence and remaining adviser questions.\n']
for role,_,text in RECORDS[2:]:
    prefix='## ' if role=='heading' else '### ' if role=='subheading' else '- ' if role in ('problem','objective','scope','limit') else ''
    lines.append(prefix+text+'\n')
save('Manuscript/Drafts/Chapter I Introduction.md','\n'.join(lines))

notes=read('Manuscript/Chapter I Revision Notes.md')
a=notes.index('## Revision and status')
b=notes.index('## Terminology ledger',a)
intro_rows='\n'.join('| '+title+' | '+str(p['heading_page'])+' | '+str(p['intro_page'])+' |' for title,p in intro_pages.items())
new=f'''## Revision and status

Revision 5, 2026-10-28. [[Manuscript/Drafts/Land Grand - Chapter I - Revised - v5.docx|Open the current Word review copy]] or [[Manuscript/Drafts/Chapter I Introduction|the synchronized Markdown]]. This revision addresses [[Sources/Chapter I Readability Feedback 2026-10-28|the user's readability feedback]] under D-016. It uses basic academic English, reduces repeated survey figures, and gives every section/subsection a separate introductory paragraph.

All **eight** final Word pages were visually inspected. Project Context spans pages **{context_start}–{context_end}**, satisfying the two-page minimum. The six openings were checked both in document structure and on rendered pages:

| Heading | Heading page | Introductory paragraph page |
| --- | ---: | ---: |
{intro_rows}

The previous [[Manuscript/Drafts/Land Grand - Chapter I - Revised.docx|revision 4 Word file]] was open and write-locked, so it remains unchanged. The original school-format source is also unchanged. Current output preserves its page geometry, typography, title block, spacing, bullet definitions, styles, relationships, and author metadata. Only document.xml and refreshed app statistics differ from the source package.

QA contract, builder, native Word audit, packaged image/text diff, and all page images are in D:\\Projects\\LandGrand-Sources\\.work\\chapter1-readable-2026-10-28. These are internal verification records. Adviser approval, unresolved game rules, and evidence of learning gains remain separate matters.

## Readability review and evidence placement

| Review issue | Revision 5 response |
| --- | --- |
| Abstract or dense wording | Use direct verbs and familiar terms; replace “full-group results” and “application deliverables” with clear descriptions. |
| Tally results dominate Context | State the sample/coverage once and retain 85% once. Summarize other findings in words, with their implications. |
| Openings blended with details | Give all six headings a separate paragraph before details, general objectives, or lists. |
| Qualifications repeated throughout prose | Keep a clear account of cross-grade coverage, small Grade 5 groups, access differences, and the limit of survey views. |

The key argument is: difficulty explaining modules and reported Science concerns support considering an additional resource; interest in mobile learning informs the format; offline use responds to the stated school context. The survey does not prove game effectiveness.

| Evidence | Main-text placement | Complete record |
| --- | --- | --- |
| Date, sample and grade coverage | Once in Context | [[Sources/Baluan Survey CSV Records|CSV provenance]] and D-011/D-013 |
| Parent explanation difficulty | 85% once, using the stated parent sample as denominator | [[Sources/Baluan Survey Tally|Question distribution]]; 17 Yes, 2 No, 1 Maybe among 20 |
| Science ratings and topic mentions | Qualitative summary, with small Grade 5 groups identified | [[Sources/Baluan Survey CSV Records#Grade 5 subgroup check, 2026-10-28|Rating counts and response locators]] |
| Mobile-learning views and access | Qualitative summary including reservations and compatibility limits | [[Sources/Baluan Survey Tally|Complete response distributions]] |

Revision 4 contained 1,735 words and 909 in Context under the builder's consistent token rule. Revision 5 contains **{BUILD['word_count']} words**, with **{BUILD['context_word_count']} in Context**; native Word reports {AUDIT['words']} words. The reduction replaces repeated numeric reports with a shorter evidence chain and adds the missing standalone introductions. Sentence-length flags are editing aids, not a validated reading-level assessment.

'''
notes=notes[:a]+new+notes[b:]
notes=notes.replace('Revision 4 distinguishes full-group summaries from the six-parent/five-teacher Grade 5 subsets and preserves their denominators.', 'Revision 5 identifies mixed grade coverage and small Grade 5 groups; exact counts and derived summaries remain in the owning source note.')
old_stat=next(line for line in notes.splitlines() if line.startswith('- **Statistics retained:**'))
notes=notes.replace(old_stat,'- **Statistics retained in revision 5 prose:** The sample/coverage and 85% module-explanation finding appear once. Other findings are summarized in words with their evidence limits. All full-group and Grade 5 calculations remain in the source records; no raw data or calculated result was changed.')
old_words=next(line for line in notes.splitlines() if line.startswith('- **Word count:**'))
notes=notes.replace(old_words,f'- **Word count:** Current revision 5: {BUILD["word_count"]} words by the reproducible builder rule, {BUILD["context_word_count"]} in Context, and {AUDIT["words"]} by native Word. Eight rendered pages; see the current readability review above.')
notes=notes.replace('## Revision 4 delivery checks','## Historical revision 4 delivery checks')
notes+='''\n## Revision 5 delivery checks

- All 57 Word paragraphs match the native Word export audit. The same paragraph source generates the Markdown mirror.
- The four main headings, two nested subheadings, six standalone introductions, four concerns/design needs, and four specific objectives are present.
- The sample description and 85% occur once in Context. The retained percentage was recomputed from the unchanged parent responses; mixed views and grade-coverage limits remain visible.
- All eight page images were inspected. No clipped text, overlap, missing glyphs, or stranded headings were observed.
- The packaged reference/final image and text diff records the intended body changes. Page geometry and the entire title block are unchanged; every preserve-only ZIP part matches the reference.
- Original Word sources, revision 4, and both research CSVs retain their expected hashes. The full tally was preserved.
- The new writing rules are owned by the writing guide, reached through the skill router, and checked in the drafting dashboard. No game scope or implementation changed.
'''
save('Manuscript/Chapter I Revision Notes.md',notes)

patch('Current Focus.md',[
('Chapter I revision 4 is saved as a [[Manuscript/Drafts/Land Grand - Chapter I - Revised.docx|revised Word copy]] and synchronized Markdown, ready for user review on 2026-10-28. [[Manuscript/Chapter I Revision Notes|Revision notes]] record all nine inspected pages and the remaining adviser questions.', 'Chapter I revision 5 is saved as a [[Manuscript/Drafts/Land Grand - Chapter I - Revised - v5.docx|current Word copy]] and synchronized Markdown, ready for user review on 2026-10-28. [[Manuscript/Chapter I Revision Notes|Revision notes]] record all eight inspected pages, six separate introductions, and remaining adviser questions. Apply [[Manuscript/Chapter 1-3 Writing Guide#Readability and subsection openings|the required writing rules]] to future chapter work.')])
text=read('Home.md').replace('[[Manuscript/Drafts/Land Grand - Chapter I - Revised.docx|revised Word copy]]','[[Manuscript/Drafts/Land Grand - Chapter I - Revised - v5.docx|current revised Word copy]]')
save('Home.md',text)

dash=read('Manuscript/Drafting Dashboard.md')
dash=dash.replace('- [x] Draft all four Chapter I sections in revision 4 and deliver a [[Manuscript/Drafts/Land Grand - Chapter I - Revised.docx|revised Word copy]] with synchronized Markdown (2026-10-28). [[Manuscript/Chapter I Revision Notes|Revision notes]] record native Word rendering and inspection of all nine pages.', '- [x] Revise all four Chapter I sections in basic academic English and save [[Manuscript/Drafts/Land Grand - Chapter I - Revised - v5.docx|revision 5 Word]] with synchronized Markdown (2026-10-28). [[Manuscript/Chapter I Revision Notes|Revision notes]] record eight inspected pages and six separate introductory paragraphs.')
dash=dash.replace('Ready for user review; revision 4, 2026-10-28','Ready for user review; revision 5, 2026-10-28')
dash=dash.replace('Context spans pages 1–5. Review two reported concerns plus two design needs under MW-01; retain full-group/Grade 5 distinctions.',f'Context spans pages {context_start}–{context_end}. Survey details are summarized; review the two concerns/two design needs under MW-01.')
dash=dash.replace('Revision 4 distinguishes full-group statistics from the six-parent/five-teacher Grade 5 subgroup summaries; source locators and calculation limits remain in the CSV source note.', 'Revision 5 summarizes the survey in words while retaining mixed grade coverage and small Grade 5 groups; exact distributions and subgroup calculations remain in the source notes.')
dash=dash.replace('Word revision 4 preserves','Word revision 5 preserves')
dash=dash.replace('## Section readiness check\n','## Section readiness check\n\nApply [[Manuscript/Chapter 1-3 Writing Guide#Readability and subsection openings|the required writing rules]] before marking any section ready.\n',1)
dash=dash.replace('- [ ] Required heading and discussion guidance followed.', '- [ ] Required headings and discussion guidance followed; each section/subsection has its own introductory paragraph before details or lists.\n- [ ] Basic academic English reviewed; survey findings are selective, explained, and free from repeated tally reports.')
save('Manuscript/Drafting Dashboard.md',dash)

patch('Manuscript/Evidence Register.md',[
('Revision 4 distinguishes the full groups from Grade 5 subsets: 6/6 parent and 4/5 teacher Science ratings are Difficult or Very Difficult.', 'Grade 5 calculations show 6/6 parent and 4/5 teacher Science ratings of Difficult or Very Difficult. Revision 5 summarizes these in words, keeps the small-group/cross-grade limits, and reports the 85% parent-explanation result once.'),
('Revision 4 uses November–December 2026 as a planned window','Revision 5 retains November–December 2026 as a planned window')])
patch('Project/Research and Evaluation.md',[
('Chapter I revision 4 distinguishes the full-group figures from the Grade 5 Science-rating summaries (6/6 parent and 4/5 teacher ratings of Difficult or Very Difficult);', 'Chapter I revision 5 summarizes the survey without repeating full numeric distributions. The verified Grade 5 Science-rating counts remain 6/6 parent and 4/5 teacher ratings of Difficult or Very Difficult;')])
patch('Sources/Baluan Survey CSV Records.md',[
('Chapter I revision 4 distinguishes the full 20-record groups from the separately calculated Grade 5 subsets below.', 'Chapter I revision 5 identifies the mixed grade coverage and small Grade 5 groups in prose. The full 20-record groups and separately calculated Grade 5 subsets remain documented below.'),
('The revised Word chapter uses the following descriptive calculations from the unchanged retained CSVs.', 'Revision 4 reported the following descriptive calculations from the unchanged retained CSVs. Revision 5 summarizes their meaning in words; the exact calculations and locators are retained here.')])

text=read('Maintenance/Change Log.md')
text+='''\n### Chapter I readability revision, D-016

- Recorded the user's request for basic academic English, reduced survey-number repetition, and introductory paragraphs for every section/subsection. The writing guide owns the persistent rules; skill routing and readiness checks point to it.
- Saved revision 5 as a separate current Word copy because revision 4 was open and write-locked. Preserved the original manuscript, revision 4, complete tally, and raw survey data.
- Replaced the tally catalogue with a short explanation of the relevant findings. Retained the sample/coverage and 85% once, along with mixed views, access limits, and small cross-grade samples.
- Added and verified six separate introductory paragraphs. Revised prose contains 1,514 words, with 657 in Context under the consistent builder rule. All eight pages were visually inspected; Context spans pages 1–4.
- Verified native Word/body agreement, unchanged title block and section geometry, and all preserve-only ZIP parts. Updated the Markdown mirror, dashboard, focus, evidence notes, and review history. Scope, open decisions, and adviser-approval status remain unchanged.
'''
save('Maintenance/Change Log.md',text)

result={'revision':5,'output':str(OUTPUT),'sha256':sha(OUTPUT),'pages':AUDIT['pages'],'native_word_count':AUDIT['words'],'builder_word_count':BUILD['word_count'],'context_word_count':BUILD['context_word_count'],'context_start_page':context_start,'context_end_page':context_end,'opening_paragraphs':intro_pages,'specific_objectives':4,'changed_zip_parts':changed,'rendered_body_sha256':rendered_body_hash,'visual_review':'Passed: all eight final PNGs inspected; no clipping, overlap, missing glyphs or stranded headings.','page_sha256':{str(n):sha(ROOT/f'render-1/page-{n}.png') for n in range(1,9)},'survey_percentage_check':{'parent_records':20,'yes':17,'percent':85},'reference_sha256':sha(ROOT/'reference.docx'),'previous_revision_sha256':sha(ROOT/'revision4.docx')}
(ROOT/'final-verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ('page_sha256','opening_paragraphs')},indent=2))
