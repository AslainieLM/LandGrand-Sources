from pathlib import Path
from zipfile import ZipFile
from lxml import etree
import hashlib
import json

ROOT=Path(__file__).resolve().parent
VAULT=Path(r'D:\Projects\LandGrand-Sources\LandGrand')
SOURCE=VAULT/'Manuscript/Drafts/Land Grand - Chapter I - Revised - v5.docx'
OUTPUT=VAULT/'Manuscript/Drafts/Land Grand - Chapter I - Revised - v6.docx'
records=json.loads((ROOT.parent/'chapter1-readable-2026-10-28/revision5.json').read_text(encoding='utf-8'))
openings={
 'Project Context':"This section explains the background and learning concerns that guide the development of Land Grand. It begins with educational technology worldwide, then discusses home learning in the Philippines and the needs reported at Baluan Elementary School.",
 'Purpose and Description of the Project':"This section explains the purpose of Land Grand and describes its main learning activities. It shows how the proposed game would support Grade 5 learners alongside printed learning materials.",
 'Objectives of the Project':"This section presents the general and specific objectives of Land Grand. The objectives connect the reported concerns and design needs with game features that can be built and checked.",
 'Scope and Limitations of the Project':"This section describes the coverage and boundaries of the Land Grand project. It explains what the game includes and the limits of its use and the survey findings.",
 'Scope':"This section outlines the learners, content, game activities, and technical requirements included in Land Grand. Project completion is planned for November–December 2026.",
 'Limitations':"This section explains the limits of the game and how the survey findings should be understood. It identifies the boundaries of the project's learners, content, and offline use."
}
source_hash=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
with ZipFile(SOURCE) as z:
    infos=z.infolist()
    parts={i.filename:z.read(i.filename) for i in infos}
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
tree=etree.fromstring(parts['word/document.xml'])
paras=tree.findall('w:body/w:p',ns)
assert len(paras)==len(records)==57
before=[etree.tostring(p) for p in paras]
changed=[]
for index,(role,_,text) in enumerate(records):
    actual=''.join(paras[index].xpath('.//w:t/text()',namespaces=ns))
    assert actual==text
    if role in ('heading','subheading'):
        assert records[index+1][0] in ('section_intro','subsection_intro')
        new=openings[text]
        runs=paras[index+1].xpath('.//w:t',namespaces=ns)
        assert len(runs)==1
        runs[0].text=new
        records[index+1][2]=new
        changed.append(index+1)
assert len(changed)==6
assert all(etree.tostring(p)==before[i] for i,p in enumerate(paras) if i not in changed)
patched=etree.tostring(tree,encoding='UTF-8',xml_declaration=True,standalone=True)
with ZipFile(OUTPUT,'w') as z:
    for info in infos:z.writestr(info,patched if info.filename=='word/document.xml' else parts[info.filename])
with ZipFile(OUTPUT) as z:
    assert z.testzip() is None
    assert all(z.read(name)==value for name,value in parts.items() if name!='word/document.xml')
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==source_hash
(ROOT/'revision6.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'edit-audit.json').write_text(json.dumps({'source':str(SOURCE),'source_sha256':source_hash,'output':str(OUTPUT),'changed_paragraph_indices_zero_based':changed,'openings':openings},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'output':str(OUTPUT),'introductory_paragraphs_updated':len(changed),'other_paragraphs_unchanged':True}))
