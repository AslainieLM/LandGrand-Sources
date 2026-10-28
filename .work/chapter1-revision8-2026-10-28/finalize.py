from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from pypdf import PdfReader
import hashlib,json,re,shutil

ROOT=Path(__file__).resolve().parent
VAULT=Path(r'D:\Projects\LandGrand-Sources\LandGrand')
OUT=VAULT/'Manuscript/Drafts/Land Grand - Chapter I - Revised - v8.docx'
records=json.loads((ROOT/'revision8.json').read_text(encoding='utf-8'))
build=json.loads((ROOT/'build-audit.json').read_text())
audit=json.loads((ROOT/'render-1/word-audit.json').read_text(encoding='utf-8-sig'))
sha=lambda path:hashlib.sha256(Path(path).read_bytes()).hexdigest()
assert audit['readOnly'] and audit['pages']==8 and audit['paragraphCount']==len(records)==61
assert [p['text'] for p in audit['paragraphs']]==[r[2] for r in records]
problems=[r[2] for r in records if r[0]=='problem']
objectives=[r[2] for r in records if r[0]=='objective']
assert problems==build['problems'] and objectives==build['objectives']
assert len(problems)==len(objectives)==4
for i,r in enumerate(records):
    if r[0] in ('problem','objective'):
        assert audit['paragraphs'][i]['startPage']==audit['paragraphs'][i]['endPage']
opening_pages={}
for i,r in enumerate(records):
    if r[0] in ('heading','subheading'):
        assert records[i+1][2].startswith('This section ')
        opening_pages[r[2]]={'heading_page':audit['paragraphs'][i]['startPage'],'intro_page':audit['paragraphs'][i+1]['startPage']}
assert len(opening_pages)==6
a=next(i for i,r in enumerate(records) if r[2]=='Project Context')
b=next(i for i,r in enumerate(records) if r[2]=='Purpose and Description of the Project')
context_pages=[audit['paragraphs'][a]['startPage'],audit['paragraphs'][b-1]['endPage']]
assert context_pages==[1,4]
pdf=PdfReader(ROOT/'render-1/revision8.pdf')
assert len(pdf.pages)==8
pdf_text='\n'.join(p.extract_text() for p in pdf.pages)
assert re.findall(r'(?m)^\s*([1-4])\.\s',pdf_text)==['1','2','3','4','1','2','3','4']
assert 'may be limited' in pdf_text
assert all('Grade 5' not in t for t in problems[:3])
assert sha(VAULT/'Manuscript/Drafts/Land Grand - Chapter I - Revised - v7.docx')==sha(ROOT/'reference.docx')
for name,expected in [('Parent.csv','a772bdc1ece510fc6181b13390e42ce717c9ca4ec5d25ab72af4b54d40daae57'),('Teacher.csv','88e0291776f88f1ea925b14e0377cc46aec65a808698ab590c3329704a14f9ac')]:
    assert sha(VAULT.parent/'Research Data/Baluan Survey'/name)==expected
with ZipFile(OUT) as z:
    infos=z.infolist();parts={i.filename:z.read(i.filename) for i in infos}
body_hash=hashlib.sha256(parts['word/document.xml']).hexdigest()
app=etree.fromstring(parts['docProps/app.xml'])
ns_app={'a':'http://schemas.openxmlformats.org/officeDocument/2006/extended-properties'}
for name,key in [('Pages','pages'),('Words','words'),('Characters','characters'),('CharactersWithSpaces','charactersWithSpaces'),('Paragraphs','paragraphCount'),('Lines','lines')]:
    node=app.find('a:'+name,ns_app)
    if node is not None:node.text=str(audit[key])
parts['docProps/app.xml']=etree.tostring(app,encoding='UTF-8',xml_declaration=True,standalone=True)
tmp=ROOT/'metadata-final.docx'
with ZipFile(tmp,'w') as z:
    for info in infos:z.writestr(info,parts[info.filename])
shutil.copyfile(tmp,OUT)
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with ZipFile(ROOT/'reference.docx') as before,ZipFile(OUT) as after:
    assert after.testzip() is None and set(before.namelist())==set(after.namelist())
    changed=[n for n in before.namelist() if before.read(n)!=after.read(n)]
    assert set(changed)=={'word/document.xml','docProps/app.xml'}
    old_section=etree.fromstring(before.read('word/document.xml')).find('w:body/w:sectPr',NS)
    new_section=etree.fromstring(after.read('word/document.xml')).find('w:body/w:sectPr',NS)
    assert etree.tostring(old_section,method='c14n',exclusive=True)==etree.tostring(new_section,method='c14n',exclusive=True)
    assert body_hash==hashlib.sha256(after.read('word/document.xml')).hexdigest()
for i in range(1,9):
    assert sha(ROOT/f'render-1/page-{i}.png')==sha(ROOT/f'fidelity-1/b_render/page-{i}.png')

BACKUP=ROOT/'vault-before-revision8'
def read(rel):return (VAULT/rel).read_text(encoding='utf-8')
def save(rel,text):
    p=VAULT/rel
    b=BACKUP/rel;b.parent.mkdir(parents=True,exist_ok=True)
    if p.exists() and not b.exists():shutil.copyfile(p,b)
    p.write_text(text,encoding='utf-8')

# Keep the Word body and Markdown mirror on one authoring source.
draft='Manuscript/Drafts/Chapter I Introduction.md'
front=read(draft).split('---',2)[1]
front=re.sub(r'(?m)^revision:.*$','revision: 8',front)
lines=['---'+front+'---\n\n# Chapter I Introduction\n',
       '> Revision 8, revised review draft. [[Manuscript/Drafts/Land Grand - Chapter I - Revised - v8.docx|Open the current Word copy]]. Uses the latest four short problems and matching objectives under D-019. Problems 1–3 describe the overall survey groups; problem 4 remains a possible physical-sample limitation pending Q-12. All eight pages were inspected, including six “This section” openings and both numbered 1–4 lists. Context spans pages 1–4. The planned November–December 2026 window retains D-015\u2019s disclosed year assumption. [[Manuscript/Chapter I Revision Notes|Revision notes]] contain the evidence mapping and remaining checks. Earlier versions and original sources remain unchanged.\n']
pi=oi=0
for role,_,text in records[2:]:
    prefix='## ' if role=='heading' else '### ' if role=='subheading' else '- ' if role in ('scope','limit') else ''
    if role=='problem':pi+=1;prefix=str(pi)+'. '
    if role=='objective':oi+=1;prefix=str(oi)+'. '
    lines.append(prefix+text+'\n')
save(draft,'\n'.join(lines))

# Record the user's selection for drafting, separately from factual verification.
feedback='Sources/Chapter I Readability Feedback 2026-10-28.md'
text=read(feedback)+'''\n## Revision 8 integration request

After the four short statements and matching potential objectives were drafted, the user asked:

> Can you revise the chapter 1 based on this one please?

D-019 records authorization to integrate that set into [[Manuscript/Drafts/Land Grand - Chapter I - Revised - v8.docx|revision 8]]. The request confirms the chosen draft direction, not the factual existence of a physical-sample shortage. Revision 8 keeps the fourth statement conditional and uses the broader survey coverage for the first three. The separate Grade 5 interest observation is retained as a source but is not substituted for material-availability evidence.
'''
save(feedback,text)
decisions='Decisions/Decision Register.md'
text=read(decisions)
row='| D-019 | 2026-10-28 | Revise Chapter I using the latest short four-problem set and its matching objectives: parent module explanations, teacher modular-learning concerns, combined Science-content difficulty, and a possible shortage of physical rock/mineral samples addressed through digital illustrations. Use the overall survey groups for findings; keep the game target Grade 5. The material-shortage statement remains conditional, not confirmed by this selection. | [[Sources/Chapter I Readability Feedback 2026-10-28#Revision 8 integration request|Direct revision request]]. | [[Manuscript/Drafts/Chapter I Introduction|Revision 8]], [[Manuscript/Chapter I Revision Notes#Problem and objective alignment|Mapping]], [[Questions/Open Questions|Q-12]] |'
assert '| D-019 |' not in text
text=text.replace('\n\nThe imported proposal is an initial documentary baseline.','\n'+row+'\n\nThe imported proposal is an initial documentary baseline.',1)
save(decisions,text)

questions='Questions/Open Questions.md'
text=read(questions)
row='| Q-12 | Before finalizing the material-shortage claim | Which researcher observation or teacher report, date, and inventory details establish limited physical rock/mineral samples for demonstrations? The material type is clarified; extent and source remain unspecified. | [[Manuscript/Drafts/Problem Candidates#Four-statement shortlist for review|Current shortlist]] and [[Sources/Chapter I Readability Feedback 2026-10-28#Physical-sample clarification|User clarification]] | Open; revision 8 uses conditional wording |'
assert '| Q-12 |' not in text
text=text.replace('\n\nNo answers have been inferred', '\n'+row+'\n\nNo answers have been inferred',1)
save(questions,text)

evidence='Manuscript/Evidence Register.md'
text=read(evidence)
old_line=next(line for line in text.splitlines() if line.startswith('| E-03 |'))
new_line='| E-03 | Local learning concerns reported in the school survey | [[Sources/Baluan Survey Tally|Full-group tally]], [[Sources/Baluan Survey CSV Records|CSV grade fields/response records]], and [[Sources/Project Clarifications 2026-10-26|user clarifications]] | Source inspected; date/coverage clarified; sampling limits remain | Revision 8 uses the overall 20-parent/20-teacher groups. Parent coverage is Grades 4–6; teachers Kindergarten and Grades 3–6. Parent explanation difficulty is 17/20 (85%); teacher modular-effectiveness views are mixed (7 Yes, 8 No, 5 Maybe). Direct responses mention the selected Science topics. July 7 is field administration; July 13 is digital preparation per the user. Grade 5-only checks remain separately labeled in the source note. No pupil test deficit or game-effectiveness result is inferred. |'
text=text.replace(old_line,new_line,1)
new_row='| E-13 | Possible shortage of physical rock/mineral samples for demonstrations | [[Sources/Chapter I Readability Feedback 2026-10-28#Physical-sample clarification|User proposal/material clarification]] and [[Manuscript/Drafts/Problem Candidates#Four-statement shortlist for review|shortlist]] | Unverified; Q-12 open | The user identified physical examples as the material type but did not establish source, date or extent of shortage. Revision 8 says may be limited. Digital illustrations are a proposed supplement, not provision of specimens. |'
assert '| E-13 |' not in text
text=text.replace('\n\n## Adding a reference','\n'+new_row+'\n\n## Adding a reference',1)
text=text.replace('Revision 7 retains November–December 2026','Revision 8 retains November–December 2026')
save(evidence,text)

# Consolidate the running review around the current version; retain historical anchors.
mapping_rows='\n'.join('| '+str(i+1)+' | '+problems[i]+' | '+objectives[i]+' | '+source+' | '+req+' |' for i,(source,req) in enumerate([
 ('Parent question 3; overall group','LG-07'),
 ('Teacher question 2; mixed overall-group views','LG-08, LG-12'),
 ('Direct topic responses; not learner tests','LG-03–LG-04, LG-07'),
 ('Potential constraint; E-13/Q-12 unverified','LG-09–LG-10, LG-18')]))
opening_rows='\n'.join('| '+title+' | '+str(p['heading_page'])+' | '+str(p['intro_page'])+' |' for title,p in opening_pages.items())
notes=f'''---
type: revision-review
status: reviewed
updated: 2026-10-28
sources:
  - "[[Sources/Chapter I Unrevised Draft]]"
  - "[[Sources/Chapter I Readability Feedback 2026-10-28]]"
  - "[[Sources/Baluan Survey Tally]]"
  - "[[Sources/Baluan Survey CSV Records]]"
  - "[[Manuscript/Chapter 1-3 Writing Guide]]"
---

# Chapter I Revision Notes

## Revision and status

**Revision 8, revised review draft, 2026-10-28.** [[Manuscript/Drafts/Land Grand - Chapter I - Revised - v8.docx|Open the current Word copy]] or [[Manuscript/Drafts/Chapter I Introduction|the synchronized Markdown]]. D-019 authorizes integration of the latest short problems and objectives. This is not adviser approval or confirmation of all local claims.

The chapter has **eight rendered pages**. Project Context spans **pages 1–4**, meeting the two-page requirement. All six section/subsection introductions begin **This section**. The problem and objective lists each restart at **1** and run through **4** in matching order.

**Material evidence remains open:** The fourth statement says physical rock/mineral samples **may be limited**. It is a potential constraint, not a finding established by the survey. Q-12 tracks the source, date and extent needed before using definite shortage wording. Digital illustrations remain supplementary visual material.

The game target remains Grade 5. The survey is broader: parents of children in Grades 4–6 and teachers handling Kindergarten and Grades 3–6. Revision 8 uses the overall groups for the first three concerns. Earlier Grade 5 subgroup calculations remain valid as labeled subgroup checks, not descriptions of the entire survey.

## Problem and objective alignment

| No. | Current problem/concern | Matching proposed objective | Evidence basis | Requirement trace |
| --- | --- | --- | --- | --- |
{mapping_rows}

The objectives are observable development deliverables within the planned November–December 2026 window under D-015. The user supplied the months; the year remains the disclosed contextual assumption. No exact approved deadline, evaluation protocol, measured knowledge gain or motivation gain is invented.

Parent explanation difficulty concerns modules generally. The proposed game offers support only for the selected Science content. Teacher views are mixed; negative and uncertain answers are not combined as proof of ineffectiveness. Topic mentions do not establish that these are the most common difficulties or prove a tested identification/classification deficit.

## Writing and page checks

The revision follows the four selected main headings, global-to-national/regional-to-local Context sequence, clear section introductions and short academic sentences. Problem openings vary without repeating Some. Required uncertainty is retained.

| Heading | Heading page | Introductory paragraph page |
| --- | ---: | ---: |
{opening_rows}

The sample size, grade coverage and field-survey date appear once in Context; the 85% parent finding appears once. Full No/Maybe distributions, subgroup counts and source locators remain in the source notes. Parent views about allowing mobile learning and device-access limits remain visible. Public citations retain their existing author–date form; the user handles citation style and margins.

Word count: **{build['words']}** by the reproducible builder rule; **{build['context_words']}** in Context; **{audit['words']}** by native Word. Count differences include Word's list labels and token conventions.

## Verification

- Native Microsoft Word 16.0 rendered the document read-only. All eight final page PNGs were inspected. No clipped text, overlap, missing glyphs or stranded headings were observed.
- Both numbered lists display 1–4; no numbered problem/objective paragraph splits across pages. PDF numbering and native Word paragraph text match the authoring source.
- Page size, margins, section XML, typography, spacing, list definitions, styles, relationships and author metadata are unchanged from revision 7. Only body XML and refreshed app statistics differ.
- The complete first page is pixel-identical to revision 7. The packaged image/text diff records intended later body changes.
- The original manuscript and earlier Word versions remain unchanged. Both research CSV hashes match the retained import values; no survey data was edited.
- Scope retains the four episodes, 3/5/7 level modes, offline Android 10+, proposed minimum device targets, local saves, menus, controls, tools and exclusions. No quiz, 3D viewer, specimen-supply program or online feature was added.
- Digital illustrations are described as a supplement. The separate [[Sources/Researcher Observation - Science Interest 2026-10-28|Grade 5 interest observation]] remains a source but is not used as evidence of sample shortages or measured game effectiveness.

QA contract, source snapshot, builder, native render audit, packaged diff and final verification record: D:\\Projects\\LandGrand-Sources\\.work\\chapter1-revision8-2026-10-28. PDF/PNG files are internal QA. A full pre-update snapshot of these review notes is retained there under vault-before-revision8.

## Reference and source mapping

| Citation/source | Supported use |
| --- | --- |
| [[Sources/UNESCO GEM 2023 Technology|UNESCO, 2023]] | Context-appropriate educational technology rationale; no game-effectiveness claim. |
| [[Sources/DepEd Distance Learning Strategies 2020|Department of Education, 2020]] | Historical distance-learning and supplementary-resource context. |
| [[Sources/PHIVOLCS Sarangani Earthquake 2026|DOST-PHIVOLCS, 2026]] | Earthquake occurrence/date/magnitude; not proof of Baluan closure. |
| [[Sources/Baluan Survey Tally|Survey tally]] and [[Sources/Baluan Survey CSV Records|response exports]] | Reported module/Science concerns, views and grade coverage. |
| [[Sources/Project Clarifications 2026-10-26|User clarifications]] | Corrected survey date, current/contingency school context, Android target, format ownership and planned completion window. |
| [[Sources/Chapter I Readability Feedback 2026-10-28|Revision feedback]] | Selected short wording, physical-sample clarification and revision authorization; not a verified inventory. |

## Pending confirmations

- **Q-12 / E-13:** Source, date, availability and extent of the proposed physical rock/mineral sample shortage.
- **Q-04–Q-05:** Final content/curriculum validation and any method supporting learning or motivation claims.
- **Q-09–Q-10:** Detailed sampling/administration records, complete topic coding and the mathematics total discrepancy.
- **Q-11:** Exact approved deadline, explicit year confirmation and full study schedule beyond the supplied November–December window.
- **Q-02–Q-03 and Q-06–Q-08:** Detailed game rules, save/progression behavior and proposal approval remain separate decisions.
- **MW-01:** Minimum four is resolved under D-018; the fourth current concern still needs factual confirmation. **MW-02:** Word format and user ownership of citation style/margins are settled. Novelty claims remain unverified under MW-03.

## Four problem statements in revision 7

This stable historical anchor preserves earlier source/decision links. [[Manuscript/Drafts/Land Grand - Chapter I - Revised - v7.docx|Revision 7]] used separate landform and rock/mineral concerns with Grade 5-specific evidence. D-019 supersedes that draft structure with the broader-survey short statements, one combined content concern and a conditional material limitation.

Earlier review history is retained in the feedback source, pre-update review-note snapshot and previous Word versions. Revision 5 simplified the language; revision 6 standardized This section openings; revision 7 introduced explicit matching numbering. None of those deliveries established adviser approval or learning effectiveness.
'''
save('Manuscript/Chapter I Revision Notes.md',notes)

focus='Current Focus.md'
text=read(focus)
a=text.index('- Distinguish [[Sources/Chapter1 Discussion Notes')
b=text.index('\n- Survey coverage is not Grade 5-only',a)
new='- Distinguish [[Sources/Chapter1 Discussion Notes|discussion notes]] from [[Sources/Chapter I Unrevised Draft|the original school-format manuscript]]. [[Manuscript/Drafts/Land Grand - Chapter I - Revised - v8.docx|Revision 8]] and its synchronized Markdown integrate the selected four short problems and matching objectives under D-019. Eight pages were inspected; Context spans pages 1–4 and six introductions begin This section. Problem 4 remains conditional pending [[Questions/Open Questions|Q-12]] on physical rock/mineral samples.\n- [[Manuscript/Chapter I Revision Notes|Revision notes]] own the current mapping, checks and remaining evidence questions. The [[Sources/Researcher Observation - Science Interest 2026-10-28|Grade 5 interest observation]] remains separate from survey and material-availability evidence. The planned window remains November–December, with 2026 the disclosed contextual year assumption under D-015.'
text=text[:a]+new+text[b:]
save(focus,text)

dash='Manuscript/Drafting Dashboard.md'
text=read(dash)
text=text.replace('- Review [[Manuscript/Drafts/Problem Candidates|the eight-candidate problem pool]] and its evidence labels before choosing the final distinct problems.', '- [x] Integrate the latest [[Manuscript/Drafts/Problem Candidates#Four-statement shortlist for review|four-statement shortlist]] and matching objectives into revision 8 under D-019. The eight-candidate pool remains reference material.\n- [ ] Confirm the physical rock/mineral sample limitation under Q-12 before treating problem 4 as an established local finding.')
text=text.replace('Land Grand - Chapter I - Revised - v7.docx','Land Grand - Chapter I - Revised - v8.docx')
text=text.replace('revision 7 Word','revision 8 Word')
text=text.replace('- [x] Integrate four reported problems and matching objectives under D-017/D-018 in revision 7. User/adviser review remains separate from this completion check.', '- [x] Preserve matching numbered problems/objectives under D-017/D-018. Three concern statements are survey-based; the fourth is a conditional material limitation. User/adviser approval remains separate.')
rows={
'| I — Project Context |':'| I — Project Context | [[Manuscript/Drafts/Chapter I Introduction#Project Context|Open section]] | Revised review draft; revision 8, 2026-10-28 | Broader survey coverage restored; confirm conditional problem 4 under Q-12. Context spans pages 1–4. |',
'| I — Purpose and Description |':'| I — Purpose and Description | [[Manuscript/Drafts/Chapter I Introduction#Purpose and Description of the Project|Open section]] | Ready for user/adviser review; revision 8, 2026-10-28 | Review short lessons, exploration and supplementary digital examples; no effectiveness or novelty claim is established. |',
'| I — Objectives |':'| I — Objectives | [[Manuscript/Drafts/Chapter I Introduction#Objectives of the Project|Open section]] | Ready for user/adviser review; revision 8, 2026-10-28 | Four objectives match the selected problems 1–4. Digital examples supplement physical specimens; the shortage is unconfirmed. |',
'| I — Scope and Limitations |':'| I — Scope and Limitations | [[Manuscript/Drafts/Chapter I Introduction#Scope and Limitations of the Project|Open section]] | Ready for user/adviser review; revision 8, 2026-10-28 | Existing offline Android/local-save scope retained; digital illustrations are supplementary, and detailed rules remain open. |'}
text='\n'.join(next((value for prefix,value in rows.items() if line.startswith(prefix)),line) for line in text.splitlines())+'\n'
text=text.replace('Word revision 7 preserves','Word revision 8 preserves')
text=text.replace('Revision 6 summarizes the survey in words while retaining mixed grade coverage and small Grade 5 groups;', 'Revision 8 summarizes the overall survey groups and keeps the Grade 5 game target separate;')
text=text.replace('the four statements and matching objectives are integrated in revision 7 for user/adviser review.', 'the latest statements and matching objectives are integrated in revision 8, with Q-12 preserving the conditional fourth concern.')
save(dash,text)

home='Home.md'
save(home,read(home).replace('Land Grand - Chapter I - Revised - v7.docx','Land Grand - Chapter I - Revised - v8.docx'))
candidate='Manuscript/Drafts/Problem Candidates.md'
text=read(candidate)
text=text.replace('Proposed wording:\n','The following short wording is integrated in [[Manuscript/Drafts/Land Grand - Chapter I - Revised - v8.docx|revision 8]] under D-019, with item 4 still conditional:\n',1)
text=text.replace('This section proposes four development objectives in the same order as the four short problems.', 'This section records the four development objectives integrated in revision 8 in the same order as the short problems. They remain proposed functions, not implemented behavior or proven learning results.',1)
text=text.replace('No source data, Word manuscript, final problem count, or implemented game behavior changes through this brainstorming note.', 'The eight-candidate pool remains brainstorming material. D-019 selects the four-statement shortlist for Word revision 8; no source data or implemented game behavior changed.')
save(candidate,text)

log='Maintenance/Change Log.md'
text=read(log)+'''\n### Chapter I revision 8: short problems and matching objectives

- Recorded D-019 and produced the requested full Word revision using the latest four short concerns and four corresponding objectives.
- Used the overall survey cohorts for the first three statements. Preserved the Grade 5 game target, all six This section introductions, short academic English, existing school formatting and separate numbered 1–4 lists.
- Kept the fourth material concern conditional, added E-13/Q-12 for its source and extent, and clarified digital illustrations as supplementary visual examples. No sample-inventory result or physical-specimen supply was invented.
- Revised Context, Purpose, Scope and Limitations for consistency. Preserved the proposal baseline, Android 10+, local saving, existing exclusions and D-015's planned window/year distinction.
- Rendered and inspected all eight pages. Context spans pages 1–4; numbered items are intact, and the first page is unchanged from revision 7. All preserve-only package parts, including numbering, match the reference.
- Synchronized the Markdown manuscript, current pointers and dashboard. Consolidated the running revision note around the current draft while retaining historical anchors, a full pre-update snapshot, source feedback and prior Word versions.
'''
save(log,text)

report={'revision':8,'output':str(OUT),'sha256':sha(OUT),'pages':8,'paragraphs':61,'native_words':audit['words'],'builder_words':build['words'],'context_words':build['context_words'],'context_pages':context_pages,'opening_pages':opening_pages,'problems':problems,'objectives':objectives,'fourth_problem_evidence_status':'Conditional; E-13/Q-12 open','changed_zip_parts':changed,'rendered_body_sha256':body_hash,'visual_review':'All eight pages inspected; numbering, paragraph flow, fonts, glyphs and page layout clean.','page_sha256':{str(i):sha(ROOT/f'render-1/page-{i}.png') for i in range(1,9)}}
(ROOT/'final-verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('opening_pages','problems','objectives','page_sha256')},indent=2))
