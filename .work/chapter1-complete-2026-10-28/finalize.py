from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from pypdf import PdfReader
import hashlib,json,re,shutil

ROOT=Path(__file__).resolve().parent
VAULT=Path(r'D:\Projects\LandGrand-Sources\LandGrand')
OUT=VAULT/'Manuscript/Drafts/Land Grand - Chapter I - Revised - v7.docx'
records=json.loads((ROOT/'revision7.json').read_text(encoding='utf-8'))
build=json.loads((ROOT/'build-audit.json').read_text())
audit=json.loads((ROOT/'render-1/word-audit.json').read_text(encoding='utf-8-sig'))
assert audit['readOnly'] and audit['pages']==8 and audit['paragraphCount']==len(records)==59
assert [p['text'] for p in audit['paragraphs']]==[r[2] for r in records]
problem_indices=[i for i,r in enumerate(records) if r[0]=='problem']
objective_indices=[i for i,r in enumerate(records) if r[0]=='objective']
assert len(problem_indices)==len(objective_indices)==4
start=next(i for i,r in enumerate(records) if r[2]=='Project Context')
end=next(i for i,r in enumerate(records) if r[2]=='Purpose and Description of the Project')
context_start=audit['paragraphs'][start]['startPage']
context_end=audit['paragraphs'][end-1]['endPage']
assert context_end-context_start>=2
openings={}
for i,(role,_,text) in enumerate(records):
    if role in ('heading','subheading'):
        assert records[i+1][2].startswith('This section ')
        openings[text]={'heading_page':audit['paragraphs'][i]['startPage'],'intro_page':audit['paragraphs'][i+1]['startPage']}
assert len(openings)==6
pdf=PdfReader(ROOT/'render-1/revision7.pdf')
assert len(pdf.pages)==8
pdf_text='\n'.join(p.extract_text() for p in pdf.pages)
assert re.findall(r'(?m)^\s*([1-4])\.\s',pdf_text)==['1','2','3','4','1','2','3','4']
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(VAULT/'Manuscript/Drafts/Land Grand - Chapter I - Revised - v6.docx')==sha(ROOT/'reference.docx')
for name,expected in [('Parent.csv','a772bdc1ece510fc6181b13390e42ce717c9ca4ec5d25ab72af4b54d40daae57'),('Teacher.csv','88e0291776f88f1ea925b14e0377cc46aec65a808698ab590c3329704a14f9ac')]:
    assert sha(VAULT.parent/'Research Data/Baluan Survey'/name)==expected
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with ZipFile(OUT) as z:
    infos=z.infolist();parts={i.filename:z.read(i.filename) for i in infos}
body_hash=hashlib.sha256(parts['word/document.xml']).hexdigest()
app=etree.fromstring(parts['docProps/app.xml'])
app_ns={'a':'http://schemas.openxmlformats.org/officeDocument/2006/extended-properties'}
for name,key in [('Pages','pages'),('Words','words'),('Characters','characters'),('CharactersWithSpaces','charactersWithSpaces'),('Paragraphs','paragraphCount'),('Lines','lines')]:
    node=app.find('a:'+name,app_ns)
    if node is not None:node.text=str(audit[key])
parts['docProps/app.xml']=etree.tostring(app,encoding='UTF-8',xml_declaration=True,standalone=True)
temp=ROOT/'metadata-final.docx'
with ZipFile(temp,'w') as z:
    for info in infos:z.writestr(info,parts[info.filename])
shutil.copyfile(temp,OUT)
with ZipFile(ROOT/'reference.docx') as a,ZipFile(OUT) as b:
    assert b.testzip() is None and set(a.namelist())==set(b.namelist())
    changed=[n for n in a.namelist() if a.read(n)!=b.read(n)]
    assert set(changed)=={'word/document.xml','word/numbering.xml','docProps/app.xml'}
    before=etree.fromstring(a.read('word/document.xml')).find('w:body/w:sectPr',NS)
    after=etree.fromstring(b.read('word/document.xml')).find('w:body/w:sectPr',NS)
    assert etree.tostring(before,method='c14n',exclusive=True)==etree.tostring(after,method='c14n',exclusive=True)
    assert body_hash==hashlib.sha256(b.read('word/document.xml')).hexdigest()
for i in range(1,9):
    assert sha(ROOT/f'render-1/page-{i}.png')==sha(ROOT/f'fidelity-1/b_render/page-{i}.png')

BACKUP=ROOT/'vault-before-revision7'
def read(rel):return (VAULT/rel).read_text(encoding='utf-8')
def save(rel,text):
    p=VAULT/rel
    b=BACKUP/rel;b.parent.mkdir(parents=True,exist_ok=True)
    if not b.exists():shutil.copyfile(p,b)
    p.write_text(text,encoding='utf-8')

draft='Manuscript/Drafts/Chapter I Introduction.md'
old=read(draft)
front=old.split('---',2)[1]
front=re.sub(r'(?m)^revision:.*$','revision: 7',front)
lines=['---'+front+'---\n\n# Chapter I Introduction\n',
       f'> Revision 7, complete draft ready for user/adviser review. [[Manuscript/Drafts/Land Grand - Chapter I - Revised - v7.docx|Open the current Word copy]]. Integrates four survey-supported problems and four matching numbered objectives under D-017/D-018, basic academic English, and six introductions beginning “This section.” All eight pages were inspected; Context spans pages {context_start}–{context_end}. School geometry and typography are preserved. The November–December 2026 window retains D-015\u2019s disclosed contextual year assumption. [[Manuscript/Chapter I Revision Notes|Revision notes]] hold evidence, mapping, and remaining study/design questions. Earlier versions and original sources are unchanged; adviser approval and learning effectiveness are not implied.\n']
problem_number=objective_number=0
for role,_,text in records[2:]:
    prefix='## ' if role=='heading' else '### ' if role=='subheading' else '- ' if role in ('scope','limit') else ''
    if role=='problem':problem_number+=1;prefix=str(problem_number)+'. '
    if role=='objective':objective_number+=1;prefix=str(objective_number)+'. '
    lines.append(prefix+text+'\n')
save(draft,'\n'.join(lines))

notes='Manuscript/Chapter I Revision Notes.md'
text=read(notes)
a=text.index('## Revision and status')
b=text.index('## Readability review and evidence placement',a)
table='\n'.join('| '+title+' | '+str(p['heading_page'])+' | '+str(p['intro_page'])+' |' for title,p in openings.items())
overview=f'''## Revision and status

**Revision 7, complete draft ready for user/adviser review, 2026-10-28.** [[Manuscript/Drafts/Land Grand - Chapter I - Revised - v7.docx|Open the current Word copy]] or [[Manuscript/Drafts/Chapter I Introduction|the synchronized Markdown]]. The latest full-chapter request authorizes integration of the four reported problems, four corresponding objectives, and all confirmed writing rules. The prior Context/Objective structural correction is now implemented.

All **eight** Word pages were visually inspected. Project Context spans pages **{context_start}–{context_end}**, satisfying the two-page minimum. Both numbered lists display **1–4** independently. The six separate introductions begin with **This section**, and the chapter introduction retains **This chapter**.

| Heading | Heading page | Introductory paragraph page |
| --- | ---: | ---: |
{table}

The school reference's page geometry, fonts, spacing, indents, title block, styles, relationships and author metadata remain unchanged. To make D-017's matching numbers explicit, one new decimal list definition and two restarted list instances were appended; every original numbering definition is unchanged. Only manuscript body XML, appended numbering entries, and app statistics differ from revision 6. The entire first page is pixel-identical to revision 6.

QA contract, builder, native Word audit, packaged image/text diff, and final verification record are at D:\\Projects\\LandGrand-Sources\\.work\\chapter1-complete-2026-10-28. Prior Word versions, the original school-format source, survey tally and response CSVs remain unchanged. The chapter is a completed review draft; formal adviser approval, detailed game rules, validated lesson inventory, and research effectiveness remain separate evidence claims.

'''
text=text[:a]+overview+text[b:]
text=text.replace('## Problem and objective alignment\n','## Problem and objective alignment\n\n**Current result:** The revision 7 mapping below supersedes the earlier analysis of revision 6. That earlier four-item list contained design needs; the replacement uses four reported concerns and matching responses.\n',1)
text=text.replace('### Four problem statements for the next revision','### Four problem statements for the next revision',1) # Keep existing anchors stable.
text=text.replace('The following four related concerns have separate source support or directly mentioned content areas.', 'The following four related concerns have separate source support or directly mentioned content areas and are now integrated in revision 7.')
old_next='**Next alignment:** Create four matching objectives in this exact order. Pre-level explanations can respond to problem 1, interactive supplementary learning/review to problem 2, landform episodes to problem 3, and rock/mineral collection descriptions to problem 4. These are planned responses, not established effectiveness. Offline use, saving, Android support, and touch controls remain supporting scope features.'
new_next='**Alignment implemented:** Four objectives now follow this exact order: pre-level lessons for problem 1, interactive supplementary exploration/review for problem 2, four landform episodes for problem 3, and rock/mineral collection descriptions for problem 4. These are planned responses, not established effectiveness. Offline use, saving, Android support, and touch controls remain supporting scope features.'
assert old_next in text;text=text.replace(old_next,new_next,1)
old_status="**Current draft status:** Word revision 6 and its mirrored body still contain the earlier list. The new four-statement wording is prepared here first, as requested; integration and objective rewriting remain subsequent manuscript work. MW-01's minimum count is resolved. D-017's one-to-one alignment still applies."
assert old_status in text
mapping='\n'.join('| '+str(i+1)+' | '+build['problems'][i]+' | '+build['objectives'][i]+' | '+req+' |' for i,req in enumerate(['LG-07','LG-08, LG-11–LG-12','LG-01, LG-03–LG-05, LG-07','LG-09–LG-10']))
text=text.replace(old_status,'''**Current draft status:** Revision 7 and its Markdown mirror contain the four revised problems and four matching objectives. MW-01's minimum count is resolved under D-018. D-017's numbered alignment is implemented.

| No. | Reported problem | Matching objective in the Word chapter | Proposed requirement trace |
| --- | --- | --- | --- |
'''+mapping+'\n',1)
text=re.sub(r'(?m)^- \*\*Word count:\*\* Current revision 6:.*$',f'- **Word count:** Current revision 7: {build["words"]} words by the reproducible token rule, {build["context_words"]} in Context, and {audit["words"]} by native Word. Eight rendered pages. Earlier revision comparisons above are historical.',text)
text=text.replace('## Revision 6 opening-sentence check','## Historical revision 6 opening-sentence check')
text+='''\n## Revision 7 completion checks

- Four selected main sections are complete; the Context uses the required global, national/regional, and local sequence and ends with the project rationale.
- All six section/subsection openings begin This section. The four problems and four objectives are separately numbered 1–4 in the same order, checked in XML, native Word text, PDF text, and page images.
- The sample/grade coverage and 85% appear once in Context. The added teacher concern retains mixed views; Grade 5 parent/teacher group sizes and the distinction between adult reports and learner assessment are explicit.
- The four-problem source locators remain in the CSV note. No topic report was converted into a tested identification/classification deficit, and offline/save features are no longer counted as survey problems.
- Scope and limitations retain the proposal, Android 10+, local saves, level inventory, tools and exclusions. No detailed star/unlock/failure rule or evaluation protocol was invented.
- Native Word paragraph text matches the authoring source. The synchronized Markdown body uses that same source. All eight pages were inspected; numbering, fonts and page layout are clean.
- All original numbering entries and preserve-only ZIP parts match revision 6; only intended body/new-list/app-statistics changes remain. Prior versions and all survey-source fingerprints are unchanged.
'''
save(notes,text)

focus='Current Focus.md'
text=read(focus)
start=text.index('- Distinguish [[Sources/Chapter1 Discussion Notes')
end=text.index('\n- Keep chat concise',start)
text=text[:start]+'- Distinguish [[Sources/Chapter1 Discussion Notes|Chapter1.docx discussion notes]] from [[Sources/Chapter I Unrevised Draft|the original school-format manuscript]]. [[Manuscript/Drafts/Land Grand - Chapter I - Revised - v7.docx|Chapter I revision 7]] and its synchronized Markdown are complete review drafts. The four survey-supported problems and four matching objectives are integrated under D-017/D-018. [[Manuscript/Chapter I Revision Notes|Revision notes]] record all eight inspected pages, six “This section” openings, and remaining adviser/study questions. Apply [[Manuscript/Chapter 1-3 Writing Guide#Readability and subsection openings|the writing rules]] to future chapter work. The planned window remains November–December, with 2026 the disclosed contextual year assumption under D-015.'+text[end:]
save(focus,text)

dash='Manuscript/Drafting Dashboard.md'
text=read(dash)
text=text.replace('Land Grand - Chapter I - Revised - v6.docx','Land Grand - Chapter I - Revised - v7.docx')
text=text.replace('revision 6 Word','revision 7 Word')
text=text.replace('eight inspected pages and six separate introductory paragraphs.', 'eight inspected pages, six “This section” introductions, and four matching numbered problem/objective pairs.')
lines=[]
for line in text.splitlines():
    if line.startswith('- [ ] Correct the Context/Objective pairing under D-017:'):
        line='- [x] Integrate four reported problems and matching objectives under D-017/D-018 in revision 7. User/adviser review remains separate from this completion check.'
    if line.startswith('| I — Project Context |'):
        line='| I — Project Context | [[Manuscript/Drafts/Chapter I Introduction#Project Context|Open section]] | Ready for user/adviser review; revision 7, 2026-10-28 | Four reported problems integrated; Context spans pages 1–4. Review wording and local evidence limits. |'
    if line.startswith('| I — Objectives |'):
        line='| I — Objectives | [[Manuscript/Drafts/Chapter I Introduction#Objectives of the Project|Open section]] | Ready for user/adviser review; revision 7, 2026-10-28 | Four numbered objectives match the four problems in order; planned November–December 2026 completion remains provisional under D-015. |'
    line=line.replace('Ready for user review; revision 6, 2026-10-28','Ready for user/adviser review; revision 7, 2026-10-28')
    lines.append(line)
text='\n'.join(lines)+'\n'
text=text.replace('Word revision 6 preserves','Word revision 7 preserves')
text=text.replace('four-statement wording and matching objectives remain under review.', 'the four statements and matching objectives are integrated in revision 7 for user/adviser review.')
save(dash,text)

home='Home.md'
save(home,read(home).replace('Land Grand - Chapter I - Revised - v6.docx','Land Grand - Chapter I - Revised - v7.docx'))

feedback='Sources/Chapter I Readability Feedback 2026-10-28.md'
text=read(feedback).replace('revision 6, the current review copy','revision 6, retained before the full integration revision')
text+='''\n## Full Chapter I integration request

After reviewing the four-problem requirement and revised problem statements, the user requested the full Chapter I with the correct content and rules. [[Manuscript/Drafts/Land Grand - Chapter I - Revised - v7.docx|Revision 7 is the current full review copy]]. It integrates four reported problems, four corresponding numbered objectives, and all six This section introductions. The request authorizes manuscript integration, not adviser approval or a change to game scope.
'''
save(feedback,text)

evidence='Manuscript/Evidence Register.md'
text=read(evidence).replace('for the four-problem candidate.', 'for the four problems integrated in revision 7.')
text=text.replace('Revision 5 retains November–December 2026','Revision 7 retains November–December 2026')
save(evidence,text)

log='Maintenance/Change Log.md'
text=read(log)+'''\n### Complete Chapter I integration, revision 7

- Produced the full revised Word chapter and synchronized Markdown at the user's request. Integrated the confirmed four reported problems and four specific objectives in the same order under D-017/D-018.
- Added separate restarted 1–4 lists for problems and objectives while retaining all original numbering definitions, page geometry, body fonts, styles, and original sources.
- Updated Context's evidence discussion for the Grade 5 parent explanation concern, mixed teacher views of modular learning, and direct landform/rock/mineral topic reports. Preserved small-sample, cross-grade, access, and effectiveness limits without repeating tally distributions.
- All six introductions begin This section. The chapter contains all four selected main sections, the planned completion window, and unchanged proposed scope/limitations.
- Rendered and inspected all eight pages; Context spans pages 1–4. Checked native Word/body agreement, PDF list numbering, packaged image/text diff, preserve-only ZIP parts, original list definitions, and source hashes.
- Updated the dashboard, current focus, Home, evidence status and revision notes. The chapter is ready for user/adviser review; no approval, implementation, or measured learning gain is claimed.
'''
save(log,text)

report={'revision':7,'output':str(OUT),'sha256':sha(OUT),'pages':8,'paragraphs':59,'native_word_count':audit['words'],'builder_word_count':build['words'],'context_words':build['context_words'],'context_pages':[context_start,context_end],'openings':openings,'problem_objective_pairs':[{'number':i+1,'problem':build['problems'][i],'objective':build['objectives'][i]} for i in range(4)],'changed_zip_parts':changed,'rendered_body_sha256':body_hash,'visual_review':'All eight final pages inspected; both lists display 1–4, no clipping/overlap/missing glyphs/stranded headings.','page_sha256':{str(i):sha(ROOT/f'render-1/page-{i}.png') for i in range(1,9)}}
(ROOT/'final-verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('openings','problem_objective_pairs','page_sha256')},indent=2))
