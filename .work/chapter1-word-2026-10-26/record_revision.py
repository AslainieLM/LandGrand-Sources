"""Record the delivered chapter and verified provenance without editing originals."""
from pathlib import Path
from zipfile import ZipFile
from copy import deepcopy
import csv
import hashlib
import json
import re
import shutil
from collections import Counter
from lxml import etree
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
VAULT = Path(r'D:\Projects\LandGrand-Sources\LandGrand')
OUT = VAULT/'Manuscript/Drafts/Land Grand - Chapter I - Revised.docx'
DAY = '2026-10-28'
W = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
audit = json.loads((ROOT/'final-render/word-audit.json').read_text(encoding='utf-8-sig'))
records = json.loads((ROOT/'chapter-paragraphs.json').read_text(encoding='utf-8'))
assert [p['text'] for p in audit['paragraphs']] == [r[2] for r in records]
assert audit['readOnly'] and audit['pages'] == 9
assert audit['paragraphCount'] == len(records) == 54
context_start = next(p['startPage'] for p in audit['paragraphs'] if p['text']=='Project Context')
context_end = audit['paragraphs'][next(i for i,p in enumerate(audit['paragraphs']) if p['text']=='Purpose and Description of the Project')-1]['endPage']
assert context_end - context_start >= 2

research = VAULT.parent/'Research Data/Baluan Survey'
expected_hashes = {'Parent.csv':'a772bdc1ece510fc6181b13390e42ce717c9ca4ec5d25ab72af4b54d40daae57','Teacher.csv':'88e0291776f88f1ea925b14e0377cc46aec65a808698ab590c3329704a14f9ac'}
subgroups = {}
for name,science,topic,n,high in [('Parent.csv',19,23,6,6),('Teacher.csv',20,24,5,4)]:
    assert sha(research/name) == expected_hashes[name]
    with (research/name).open(encoding='utf-8-sig', newline='') as stream:
        rows=list(csv.reader(stream))
    chosen = [(i,r) for i,r in enumerate(rows[1:],2) if re.sub(r'\D','',r[2])=='5']
    counts = Counter(r[science].strip() for _,r in chosen)
    assert len(chosen)==n and sum(counts[str(k)] for k in (4,5))==high
    subgroups[name] = {'row_locators':[i for i,_ in chosen], 'science_column':science+1, 'topic_column':topic+1, 'science_rating_counts':dict(counts), 'topic_mentions':{term:[i for i,r in chosen if term in r[topic].lower()] for term in ('landform','mineral','rock')}}

# Refresh only statistical app properties from the native Word audit.
with ZipFile(OUT) as z:
    infos=z.infolist()
    parts={i.filename:z.read(i.filename) for i in infos}
app = etree.fromstring(parts['docProps/app.xml'])
app_ns = {'a':'http://schemas.openxmlformats.org/officeDocument/2006/extended-properties'}
for name,key in [('Pages','pages'),('Words','words'),('Characters','characters'),('CharactersWithSpaces','charactersWithSpaces'),('Paragraphs','paragraphCount'),('Lines','lines')]:
    node=app.find('a:'+name,app_ns)
    if node is not None:
        node.text=str(audit[key])
parts['docProps/app.xml']=etree.tostring(app,encoding='UTF-8',xml_declaration=True,standalone=True)
temp=ROOT/'metadata-final.docx'
with ZipFile(temp,'w') as z:
    for info in infos:
        z.writestr(info,parts[info.filename])
shutil.copyfile(temp,OUT)
with ZipFile(ROOT/'reference.docx') as a, ZipFile(OUT) as b:
    assert b.testzip() is None
    changed=[n for n in a.namelist() if a.read(n)!=b.read(n)]
    assert changed==['word/document.xml','docProps/app.xml'] or set(changed)=={'word/document.xml','docProps/app.xml'}
    old=etree.fromstring(a.read('word/document.xml')).find('w:body/w:sectPr',W)
    new=etree.fromstring(b.read('word/document.xml')).find('w:body/w:sectPr',W)
    assert etree.tostring(old,method='c14n',exclusive=True)==etree.tostring(new,method='c14n',exclusive=True)
assert sha(VAULT/'Sources/Attachments/CHAPTER I only.docx')==sha(ROOT/'reference.docx')=='8701feed03dc35bf065cba7b20911eb7251335b14eee6e0ab58d3317962b72d7'
pdf=PdfReader(ROOT/'final-render/final.pdf')
assert len(pdf.pages)==audit['pages']
pdf_text=' '.join(' '.join(p.extract_text().split()) for p in pdf.pages)
for heading in [r[2] for r in records if r[0]=='heading']:
    assert heading in pdf_text
assert 'November' in pdf_text and 'December 2026' in pdf_text
assert not any(token in '\n'.join(r[2] for r in records) for token in ('TODO','[confirmed','[[','P-01','O-01'))

backup = ROOT/'vault-before-revision4'
def save(rel,text):
    dest=VAULT/rel
    copy=backup/rel
    copy.parent.mkdir(parents=True,exist_ok=True)
    if dest.exists() and not copy.exists():
        shutil.copyfile(dest,copy)
    dest.write_text(text,encoding='utf-8')
def read(rel):
    return (VAULT/rel).read_text(encoding='utf-8-sig')
def dated(text):
    return re.sub(r'(?m)^updated: \d{4}-\d{2}-\d{2}$','updated: '+DAY,text,count=1)
def replace(rel,pairs):
    text=read(rel)
    for before,after in pairs:
        assert before in text,(rel,before)
        text=text.replace(before,after,1)
    save(rel,dated(text))

# Word body and Markdown body share the same paragraph source.
old=read('Manuscript/Drafts/Chapter I Introduction.md')
front=old.split('---',2)[1]
front=re.sub(r'(?m)^updated:.*$','updated: '+DAY,front)
front=re.sub(r'(?m)^revision:.*$','revision: 4',front)
lines=['---'+front+'---\n\n# Chapter I Introduction\n',
       '> Revision 4, ready for user review. [[Manuscript/Drafts/Land Grand - Chapter I - Revised.docx|Open the revised Word copy]]. Native Word rendering and inspection cover all nine pages. The original school-format file is unchanged. The planned completion window is November–December 2026; the user supplied the months and 2026 is the disclosed contextual year assumption. See [[Manuscript/Chapter I Revision Notes|revision notes]] for evidence, source mapping, and remaining adviser questions. This is a review draft, not an approved manuscript or completed study.\n']
for role,_,text in records[2:]:
    prefix='## ' if role=='heading' else '### ' if role=='subheading' else '- ' if role in ('problem','objective','scope','limit') else ''
    lines.append(prefix+text+'\n')
save('Manuscript/Drafts/Chapter I Introduction.md','\n'.join(lines))

replace('Sources/Project Clarifications 2026-10-26.md',[
('- A past closure, an official automatic modality-change trigger, topic-response coding, and the project completion date remain unestablished.', '- A past closure, an official automatic modality-change trigger, and the Word tally\u2019s topic-response coding remain unestablished. The later completion-window reply is recorded below; it does not establish an exact approved deadline or the full study schedule.')])
save('Sources/Project Clarifications 2026-10-26.md',read('Sources/Project Clarifications 2026-10-26.md')+'''\n## Completion-window follow-up, 2026-10-28\n\nWhen asked which completion date or month to use in the Word draft, the user replied:\n\n> project completion date is not yet indicated though, just put November-December\n\nUse **November–December** as the planned completion window. The drafting agent explicitly disclosed **2026** as an inference from the existing 2026 project timeline; the user supplied the months, not an explicit year or exact date. D-015 records this distinction. This window applies to planned project completion and is not a claim that survey administration or the entire study occurred during those months. The July 7, 2026 survey date remains unchanged.\n''')

text=read('Decisions/Decision Register.md')
point='\nThe imported proposal is an initial documentary baseline.'
assert point in text
text=text.replace(point,'\n| D-015 | 2026-10-28 | Use November–December as the planned project completion window for the revised Chapter I. The draft uses 2026 as the explicitly disclosed contextual year assumption; no exact date, approved deadline, or complete study schedule is asserted. | [[Sources/Project Clarifications 2026-10-26#Completion-window follow-up, 2026-10-28|Direct user reply and year distinction]]. | [[Manuscript/Drafts/Chapter I Introduction|Chapter I revision 4]], [[Project/Research and Evaluation|Research and Evaluation]], [[Questions/Open Questions|Q-11]] |\n'+point,1)
save('Decisions/Decision Register.md',dated(text))
replace('Questions/Open Questions.md',[
('| Q-11 | Before finalizing Chapter I | What project completion date and development/study period should make the objectives time-bound and define the scope? | [[Manuscript/Chapter I Revision Notes#Pending confirmations|Chapter I revision]] | Open |', '| Q-11 | Before formal schedule approval or evaluation | The user supplied November–December as the planned completion window (D-015); the draft assumes 2026 from context. What exact approved deadline and full development/evaluation schedule will be documented? | [[Manuscript/Chapter I Revision Notes#Pending confirmations|Chapter I revision]] | Drafting window supplied; exact date, explicit year confirmation, and full study schedule remain undocumented |')])

replace('Sources/Baluan Survey CSV Records.md',[
('The existing Chapter I figures describe each full 20-record group. They must not be relabeled as Grade 5-only results or combined into one 40-person percentage.', 'Chapter I revision 4 distinguishes the full 20-record groups from the separately calculated Grade 5 subsets below. Full-group results must not be relabeled as Grade 5-only findings or combined into one 40-person percentage.')])
text=read('Sources/Baluan Survey CSV Records.md')
section='''\n## Grade 5 subgroup check, 2026-10-28\n\nThe revised Word chapter uses the following descriptive calculations from the unchanged retained CSVs. Filter column C by Grade 5, normalizing the numeric label `5` and the textual label `Grade 5`. Row locators refer to logical CSV records with the header as row 1; multiline fields do not create additional records.\n\n| Group | Grade 5 record rows | Science field | Ratings 3 / 4 / 5 | Difficult or Very Difficult |\n| --- | --- | --- | --- | --- |\n| Parents | 8, 16, 17, 18, 19, 20 | Column T | 0 / 3 / 3 | 6 of 6 |\n| Teachers | 13–17 | Column U | 1 / 3 / 1 | 4 of 5 |\n\nThe parent scale labels 4 as Difficult and 5 as Very Difficult. Parent free-topic field X mentions landforms in rows 16 and 18 and minerals in row 8. Teacher free-topic field Y mentions minerals in row 15 and rock topics in rows 15 and 17. These support the chapter's limited statement that Grade 5 responses include those topics. The prose does not claim they are the most common difficulties. Other mentions, including soil, do not expand the game's scope.\n\nThese small subsets describe respondent perceptions, not pupil test scores, unique-identity verification, all-school prevalence, or game effectiveness. The direct-response check does not adjudicate the Word tally's complete topic coding or resolve Q-10's mathematics total discrepancy. Source hashes were rechecked against the import fingerprints. Calculation records remain in `.work/chapter1-word-2026-10-26/final-verification.json` outside the vault; the aggregate method and locators here make the check reproducible from retained research sources.\n'''
text=text.replace('\n## Survey and encoding dates',section+'\n## Survey and encoding dates',1)
save('Sources/Baluan Survey CSV Records.md',dated(text))

replace('Project/Research and Evaluation.md',[
('Grade 5 subsets contain six parent records and five teacher records. Current chapter figures remain full-group summaries.', 'Grade 5 subsets contain six parent records and five teacher records. Chapter I revision 4 distinguishes the full-group figures from the Grade 5 Science-rating summaries (6/6 parent and 4/5 teacher ratings of Difficult or Very Difficult); [[Sources/Baluan Survey CSV Records#Grade 5 subgroup check, 2026-10-28|the CSV source note]] owns the calculation and locators.'),
('Do not treat these perceptions as Grade 5-only findings, all-school prevalence, or learning gains.', 'Do not treat the cross-grade figures as Grade 5-only findings or treat either group\u2019s perceptions as all-school prevalence or measured learning gains.')])
text=read('Project/Research and Evaluation.md')
text=text.replace('\n## What remains undocumented','''\n## Planned completion window\n\nUnder D-015, the user supplied **November–December** as the planned project completion window. [[Sources/Project Clarifications 2026-10-26#Completion-window follow-up, 2026-10-28|The follow-up record]] distinguishes those supplied months from the drafting agent's disclosed **2026** contextual year assumption. This supports provisional time-bound objectives. An exact approved date and the full development/evaluation schedule remain undocumented; the preliminary survey occurred July 7, 2026.\n\n## What remains undocumented''',1)
save('Project/Research and Evaluation.md',dated(text))

replace('Manuscript/Evidence Register.md',[
('Grade 5 subsets of six parent/five teacher records are available; current chapter statistics use the full groups.', 'Revision 4 distinguishes the full groups from Grade 5 subsets: 6/6 parent and 4/5 teacher Science ratings are Difficult or Very Difficult. [[Sources/Baluan Survey CSV Records#Grade 5 subgroup check, 2026-10-28|Direct CSV calculations]] also support limited topic mentions, without claiming the most frequent Grade 5 difficulty.')])
text=read('Manuscript/Evidence Register.md')
text=text.replace('\n## Adding a reference','''\n| E-11 | Planned completion window | [[Sources/Project Clarifications 2026-10-26#Completion-window follow-up, 2026-10-28|User's November–December reply]] and D-015 | Months user-supplied; 2026 inferred and disclosed | Revision 4 uses November–December 2026 as a planned window, not an exact approved deadline or full study period. |\n\n## Adding a reference''',1)
save('Manuscript/Evidence Register.md',dated(text))

replace('Sources/Chapter I Unrevised Draft.md',[
('Word metadata reports six pages; visual pagination was not verified. The bundled renderer is unavailable because LibreOffice was not found in this environment.', 'Initial import could not verify pagination because bundled LibreOffice was unavailable. During the Word revision, native Microsoft Word 16.0 read-only PDF export succeeded: all six source pages were rasterized and visually inspected. Geometry and role-specific fonts, spacing, indents, headings, and bullet patterns were recorded before authoring. This verifies the saved reference layout, not adviser approval.')])

notes=read('Manuscript/Chapter I Revision Notes.md')
start=notes.index('Revision 3, 2026-10-26.')
end=notes.index('\n## Terminology ledger',start)
notes=notes[:start]+f'''Revision 4, {DAY}. [[Manuscript/Drafts/Land Grand - Chapter I - Revised.docx|Open the revised Word chapter]] or [[Manuscript/Drafts/Chapter I Introduction|the synchronized Markdown text]]. The user requested the Word revision through Documents and later instructed continuation. All four selected sections are drafted for user/adviser review; approval, implementation, and measured effectiveness are separate claims. [[Sources/Chapter I Unrevised Draft|The original school-format file]] remains unchanged.\n\nThe revised Word file renders to **nine pages**, all visually inspected. Project Context runs from page **{context_start} through {context_end}**, meeting the lecture's two-page requirement. Native Microsoft Word 16.0 read-only PDF export and the packaged renderer with a PDFium adapter supplied the layout proof despite unavailable bundled LibreOffice. The title block, section geometry, fonts, double spacing, indents, and existing bullet definitions are preserved. Only manuscript body XML and app statistics differ from the reference package; styles, numbering, relationships, author metadata, and all retained originals are unchanged.\n\nThe task-local template contract, builder, native render audit, page images, and verification record are retained under `D:\\Projects\\LandGrand-Sources\\.work\\chapter1-word-2026-10-26`. PDF/PNG files are internal QA, not additional deliverables.\n''' +notes[end:]
notes=notes.replace('Grade 5 subsets contain six parent/five teacher records; main-text figures remain full-group summaries.', 'Revision 4 distinguishes full-group summaries from the six-parent/five-teacher Grade 5 subsets and preserves their denominators.')
notes=notes.replace('Kept the completion date visible rather than claiming all SMART requirements are finalized.', 'Revision 4 replaces the date placeholder with the user-supplied November–December window and the disclosed contextual 2026 year assumption.')
notes=notes.replace('The retained four-bullet format is provisional.', 'The revised chapter retains four bullets addressing reported concerns and design needs.')
notes=notes.replace('The objectives specify observable deliverables. Their time-bound element remains incomplete until Q-11 is answered. They do not promise a numerical learning gain or add an evaluation protocol.', 'The four objectives specify observable deliverables within the planned November–December 2026 completion window under D-015. They do not promise a numerical learning gain or introduce an evaluation protocol. Q-11 now concerns the exact approved date, explicit year confirmation, and complete study schedule rather than a missing drafting window.')
notes=notes.replace('- **Statistics retained:** Selected question counts and derived 85% for parental explanation difficulty; subject-rating counts and topic mentions.', '- **Statistics retained:** Selected full-group question counts, derived 85% for parental explanation difficulty, and subject-rating counts. Revision 4 adds separately labeled Grade 5 Science summaries (6/6 parent, 4/5 teacher), with direct topic mentions checked against the CSVs rather than unresolved Word topic frequencies.')
old_count=next(line for line in notes.splitlines() if line.startswith('- **Word count:**'))
notes=notes.replace(old_count,'- **Word count:** Native Word reports '+str(audit['words'])+' words for revision 4. The builder\u2019s reproducible token rule counts 1,735 words including titles/headings and 909 in Project Context. Word pagination is nine pages; word-count rules differ slightly. Original extracted revision was approximately 1,377 words. These counts describe evidence-supported revision, not a compression target.')
notes=notes.replace('The working text retains provisional author–date citations and source locators.', 'The Word text retains provisional author–date citations for public sources. Complete source locators, survey provenance, and unresolved coding issues remain in the vault; internal IDs and wikilinks are excluded from the Word chapter.')
notes=notes.replace('- **Q-11:** Project completion date and development/study period; required for final time-bound objectives and scope wording.', '- **Q-11:** Drafting window supplied under D-015. An exact approved deadline, explicit year confirmation beyond the contextual 2026 assumption, and the full development/evaluation schedule remain undocumented; these are not silently converted into dates.')
notes=notes.replace('Revision notes]] contain','Revision notes]] contain')
notes += '''\n## Revision 4 delivery checks\n\n- Word body and Markdown body derive from the same 54-paragraph source; all four main headings and four specific objective bullets are present.\n- Original ZIP passes integrity checks and retains its import SHA-256; revised ZIP also passes. Section XML is identical. Only document.xml and refreshed app.xml statistics differ.\n- Native Word text matches the complete authoring paragraph sequence. All nine final page PNGs were inspected; no clipping, overlap, missing glyphs, or stranded headings were observed. The final page contains the natural continuation of limitation bullets.\n- Survey source hashes and Grade 5 filters, denominators, rating counts, and direct topic locators were rechecked. No changes were made to raw CSVs or the original tally.\n- Completion-window wording appears in Objectives and Scope without an exact-date placeholder. User ownership of citation style and margins is preserved.\n- MW-01, local novelty evidence, Q-04–Q-05, detailed game mechanics, and remaining survey-method/coding questions stay visible for subsequent author/adviser review. None is represented as approved or empirically resolved by this draft.\n'''
save('Manuscript/Chapter I Revision Notes.md',dated(notes))

replace('Current Focus.md',[
('Chapter I revision 3 is saved in the working draft; [[Manuscript/Chapter I Revision Notes|revision notes]] track remaining checks.', 'Chapter I revision 4 is saved as a [[Manuscript/Drafts/Land Grand - Chapter I - Revised.docx|revised Word copy]] and synchronized Markdown, ready for user review on 2026-10-28. [[Manuscript/Chapter I Revision Notes|Revision notes]] record all nine inspected pages and the remaining adviser questions. The planned completion window is November–December, with 2026 the disclosed contextual year assumption (D-015).')])

dash=read('Manuscript/Drafting Dashboard.md')
dash=dash.replace('- [x] Revise the four Chapter I sections from the supplied unrevised manuscript; revision 2 corrects the survey date/grades from the CSVs (2026-10-26). See [[Manuscript/Chapter I Revision Notes|revision notes]].', '- [x] Draft all four Chapter I sections in revision 4 and deliver a [[Manuscript/Drafts/Land Grand - Chapter I - Revised.docx|revised Word copy]] with synchronized Markdown (2026-10-28). [[Manuscript/Chapter I Revision Notes|Revision notes]] record native Word rendering and inspection of all nine pages.')
dash=dash.replace('- [ ] Review Chapter I problem framing and confirm the completion date. Android 10 and above is settled under D-012.', '- [ ] Obtain user/adviser review of Chapter I problem framing, especially MW-01. D-015 supplies a November–December drafting window; 2026 is the disclosed contextual year assumption, with exact schedule approval still separate. Android 10 and above is settled under D-012.')
rows={
'| I — Project Context |':'| I — Project Context | [[Manuscript/Drafts/Chapter I Introduction#Project Context|Open section]] | Ready for user review; revision 4, 2026-10-28 | Context spans pages 1–5. Review two reported concerns plus two design needs under MW-01; retain full-group/Grade 5 distinctions. |',
'| I — Purpose and Description |':'| I — Purpose and Description | [[Manuscript/Drafts/Chapter I Introduction#Purpose and Description of the Project|Open section]] | Ready for user review; revision 4, 2026-10-28 | Review the proposed learner experience and intended benefits; no local novelty or effectiveness claim is established. |',
'| I — Objectives |':'| I — Objectives | [[Manuscript/Drafts/Chapter I Introduction#Objectives of the Project|Open section]] | Ready for user review; revision 4, 2026-10-28 | Four deliverables share the planned November–December 2026 window; review the concern/objective mapping and formal schedule later. |',
'| I — Scope and Limitations |':'| I — Scope and Limitations | [[Manuscript/Drafts/Chapter I Introduction#Scope and Limitations of the Project|Open section]] | Ready for user review; revision 4, 2026-10-28 | Android 10+ and the planned completion window are incorporated; detailed game/evaluation rules remain separate decisions. |'}
dash='\n'.join(next((new for prefix,new in rows.items() if line.startswith(prefix)),line) for line in dash.splitlines())+'\n'
dash=dash.replace('Six Grade 5 parent records and five Grade 5 teacher records are available; current statistics use full groups.', 'Revision 4 distinguishes full-group statistics from the six-parent/five-teacher Grade 5 subgroup summaries; source locators and calculation limits remain in the CSV source note.')
dash=dash.replace('- When producing Word output, use the selected headings, automatic TOC, and the document skill\u2019s layout verification.', '- Word revision 4 preserves the supplied Chapter I format and has passed layout verification. Integrate the automatic TOC when assembling the full manuscript; no new TOC page was inserted into this chapter-only reference.')
save('Manuscript/Drafting Dashboard.md',dated(dash))

text=read('Home.md')
text=text.replace('[[Sources/Chapter I Unrevised Draft|Unrevised Chapter I]] and [[Manuscript/Drafts/Chapter I Introduction|working revision]]', '[[Sources/Chapter I Unrevised Draft|Unrevised Chapter I]], [[Manuscript/Drafts/Chapter I Introduction|working revision]], and [[Manuscript/Drafts/Land Grand - Chapter I - Revised.docx|revised Word copy]]')
save('Home.md',dated(text))

text=dated(read('Maintenance/Change Log.md'))
text+='''\n## 2026-10-28 — Revised Chapter I Word delivery\n\n- Continued the authorized Documents request and produced a separate revised Word draft, preserving the original school-format package and all retained source files. Chapter I revision 4 and its Markdown mirror contain all four selected sections and four specific objective bullets.\n- Recorded D-015: November–December is the user-supplied planned completion window; 2026 is the disclosed contextual year assumption. No exact approved deadline or full study schedule was invented.\n- Verified Grade 5 subgroup Science ratings directly from unchanged CSVs (parents 6/6, teachers 4/5 rated Difficult or Very Difficult), with aggregate methods and topic-mention locators recorded in the owning source note. Kept full-group results distinct.\n- Native Microsoft Word read-only PDF export resolved the earlier layout-verification limitation. Inspected all six reference pages and all nine revised pages; Project Context spans pages 1–5. Preserved styles, numbering, margins, fonts, relationships, and author metadata. Only body XML and app statistics changed.\n- Updated Current Focus, dashboard, evidence, clarification and research notes, and Q-11. Chapter I is ready for user review; MW-01 and other documented evidence/design questions remain open. Chapters II–III remain scaffolds.\n'''
save('Maintenance/Change Log.md',text)

result={'date':DAY,'output':str(OUT),'sha256':sha(OUT),'pages':audit['pages'],'native_word_count':audit['words'],'paragraphs':len(records),'context_start_page':context_start,'context_end_page':context_end,'changed_zip_parts':changed,'source_original_sha256':sha(ROOT/'reference.docx'),'research_hashes':expected_hashes,'grade5_calculations':subgroups,'body_matches_native_word':True,'markdown_body_matches_authoring_source':True,'visual_review':'All nine final page PNGs must be inspected before delivery; recorded separately after the final render.'}
(ROOT/'final-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ('grade5_calculations','research_hashes')},ensure_ascii=False,indent=2))
