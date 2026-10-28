from pathlib import Path
from zipfile import ZipFile
from lxml import etree
import hashlib
import json
import re
import shutil

ROOT=Path(__file__).resolve().parent
VAULT=Path(r'D:\Projects\LandGrand-Sources\LandGrand')
OUT=VAULT/'Manuscript/Drafts/Land Grand - Chapter I - Revised - v6.docx'
SOURCE=VAULT/'Manuscript/Drafts/Land Grand - Chapter I - Revised - v5.docx'
records=json.loads((ROOT/'revision6.json').read_text(encoding='utf-8'))
audit=json.loads((ROOT/'render/word-audit.json').read_text(encoding='utf-8-sig'))
edit=json.loads((ROOT/'edit-audit.json').read_text(encoding='utf-8'))
assert audit['pages']==8 and audit['readOnly']
assert [r[2] for r in records]==[p['text'] for p in audit['paragraphs']]
intro_pages={}
for i,(role,_,heading) in enumerate(records):
    if role in ('heading','subheading'):
        assert records[i+1][2].startswith('This section ')
        intro_pages[heading]={'heading_page':audit['paragraphs'][i]['startPage'],'intro_page':audit['paragraphs'][i+1]['startPage']}
assert len(intro_pages)==6
previous=json.loads((ROOT.parent/'chapter1-readable-2026-10-28/final-verification.json').read_text())
assert intro_pages==previous['opening_paragraphs']
with ZipFile(OUT) as z:
    infos=z.infolist()
    data={i.filename:z.read(i.filename) for i in infos}
app=etree.fromstring(data['docProps/app.xml'])
ns={'a':'http://schemas.openxmlformats.org/officeDocument/2006/extended-properties'}
for name,key in [('Pages','pages'),('Words','words'),('Characters','characters'),('CharactersWithSpaces','charactersWithSpaces'),('Paragraphs','paragraphCount'),('Lines','lines')]:
    node=app.find('a:'+name,ns)
    if node is not None:node.text=str(audit[key])
data['docProps/app.xml']=etree.tostring(app,encoding='UTF-8',xml_declaration=True,standalone=True)
temp=ROOT/'metadata-final.docx'
with ZipFile(temp,'w') as z:
    for info in infos:z.writestr(info,data[info.filename])
shutil.copyfile(temp,OUT)
with ZipFile(SOURCE) as a,ZipFile(OUT) as b:
    assert b.testzip() is None
    differences=[name for name in a.namelist() if a.read(name)!=b.read(name)]
    assert set(differences)=={'word/document.xml','docProps/app.xml'}
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==edit['source_sha256']

backup=ROOT/'vault-before-revision6'
def read(rel):return (VAULT/rel).read_text(encoding='utf-8')
def save(rel,text):
    p=VAULT/rel
    before=backup/rel
    before.parent.mkdir(parents=True,exist_ok=True)
    if not before.exists():shutil.copyfile(p,before)
    p.write_text(text,encoding='utf-8')

draft='Manuscript/Drafts/Chapter I Introduction.md'
text=read(draft)
old_records=json.loads((ROOT.parent/'chapter1-readable-2026-10-28/revision5.json').read_text(encoding='utf-8'))
for old,new in zip(old_records,records):
    if old[2]!=new[2]:
        assert text.count(old[2])==1
        text=text.replace(old[2],new[2],1)
text=text.replace('revision: 5','revision: 6',1).replace('> Revision 5,','> Revision 6,',1)
text=text.replace('Revised under D-016 for basic academic English, concise survey discussion, and six separate section/subsection introductions.', 'Revised under D-016 for basic academic English and concise survey discussion. Every section/subsection introduction now begins with the exact words “This section,” as requested.')
text=text.replace('Land Grand - Chapter I - Revised - v5.docx','Land Grand - Chapter I - Revised - v6.docx')
save(draft,text)

guide='Manuscript/Chapter 1-3 Writing Guide.md'
text=read(guide)
needle='Place a separate, short introductory paragraph immediately after each heading and before detailed explanations or bullets.'
assert needle in text
text=text.replace(needle,needle+' Begin its first sentence with the exact words **“This section”**, including under nested subsections such as Scope and Limitations.',1)
save(guide,text)

feedback='Sources/Chapter I Readability Feedback 2026-10-28.md'
text=read(feedback)
text=text.replace('[[Manuscript/Drafts/Land Grand - Chapter I - Revised - v5.docx|Revision 5]] is a separate file and the current review copy.', '[[Manuscript/Drafts/Land Grand - Chapter I - Revised - v5.docx|Revision 5]] is retained as a separate file. The follow-up below is incorporated in [[Manuscript/Drafts/Land Grand - Chapter I - Revised - v6.docx|revision 6, the current review copy]].')
text+='''\n## Introductory wording follow-up

The user specified:

> Make it like, in each section or subsection indicates "This section" for the introductory sentence

Revision 6 applies the exact opening words **This section** to all six section/subsection introductions. The chapter-level introduction retains **This chapter**. D-016 and the writing guide include this clarification for future drafting.
'''
save(feedback,text)

decisions='Decisions/Decision Register.md'
text=read(decisions)
needle='Make these review requirements persistent in the vault and revise Chapter I accordingly.'
assert needle in text
text=text.replace(needle,needle+' The user\u2019s follow-up specifies that each introductory first sentence starts with “This section.”',1)
save(decisions,text)

for rel in ['Current Focus.md','Home.md','Manuscript/Drafting Dashboard.md']:
    text=read(rel).replace('Land Grand - Chapter I - Revised - v5.docx','Land Grand - Chapter I - Revised - v6.docx')
    text=text.replace('revision 5','revision 6').replace('Revision 5','Revision 6')
    if rel=='Manuscript/Drafting Dashboard.md':
        text=text.replace('each section/subsection has its own introductory paragraph before details or lists.', 'each section/subsection has its own introductory paragraph beginning with “This section” before details or lists.')
    save(rel,text)

notes='Manuscript/Chapter I Revision Notes.md'
text=read(notes)
old='Revision 5, 2026-10-28. [[Manuscript/Drafts/Land Grand - Chapter I - Revised - v5.docx|Open the current Word review copy]]'
new='Revision 6, 2026-10-28. [[Manuscript/Drafts/Land Grand - Chapter I - Revised - v6.docx|Open the current Word review copy]]'
assert old in text
text=text.replace(old,new,1)
text=text.replace('It uses basic academic English, reduces repeated survey figures, and gives every section/subsection a separate introductory paragraph.', 'It retains basic academic English and concise survey discussion. The follow-up changes only the six introductory paragraphs so that each begins with “This section.” Revision 5 is preserved.',1)
text=text.replace('## Revision 5 delivery checks','## Historical revision 5 delivery checks')
text+='''\n## Revision 6 opening-sentence check

All six section/subsection introductory paragraphs now begin with **This section**. The chapter introduction continues to begin with **This chapter**. The six-heading page map above is unchanged; all eight final pages were rendered and visually inspected.

Only those six paragraphs and refreshed app statistics differ from revision 5. The other 51 paragraphs, fonts, margins, styles, numbering, relationships, and retained sources are unchanged. The current Word text and Markdown mirror agree. QA and the version 5 hash are retained in D:\\Projects\\LandGrand-Sources\\.work\\chapter1-openings-2026-10-28.
'''
save(notes,text)

log='Maintenance/Change Log.md'
text=read(log)+'''\n### Chapter I opening wording follow-up

- Clarified D-016 and the writing guide: every section/subsection introductory sentence starts with “This section.”
- Saved revision 6 and synchronized its six revised introductions with the Markdown draft. Preserved revision 5 and all other paragraph content and formatting.
- Rendered and inspected all eight pages. The six heading/intro page positions and the two-page Context requirement remain satisfied. Updated current vault links to revision 6.
'''
save(log,text)
report={'revision':6,'output':str(OUT),'pages':8,'words':audit['words'],'openings':intro_pages,'changed_paragraphs':6,'other_paragraphs_unchanged':51,'changed_zip_parts':differences,'visual_review':'All eight pages inspected and clean.','output_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest()}
(ROOT/'final-verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='openings'},indent=2))
