from pathlib import Path
from copy import deepcopy
from zipfile import ZipFile
from lxml import etree
import hashlib,json,re

ROOT=Path(__file__).resolve().parent
VAULT=Path(r'D:\Projects\LandGrand-Sources\LandGrand')
OUT=VAULT/'Manuscript/Drafts/Land Grand - Chapter I - Revised - v8.docx'
old=json.loads((ROOT.parent/'chapter1-complete-2026-10-28/revision7.json').read_text(encoding='utf-8'))
problems=[
 'Parents reported difficulty explaining printed module lessons to their children.',
 'Teachers questioned whether modular learning helps learners understand lessons.',
 'Survey responses identified landforms, rocks, and minerals as difficult Science topics.',
 'Physical rock and mineral samples may be limited for classroom demonstrations.'
]
objectives=[
 'Provide short Science lessons before each level to support explanations during home study.',
 'Implement interactive exploration and end-of-level reviews to supplement printed Science modules.',
 'Develop four episodes covering Mountains, Hills, Plains, and Plateaus, including selected rock and mineral topics.',
 'Present digital illustrations of selected rocks and minerals with names and short descriptions.'
]
records=[];pi=oi=0
for role,pattern,text in old:
    if text.startswith('Difficulty explaining module lessons was reported'):
        text='Parent responses showed difficulty explaining lessons in printed modules. In the parent group, 85% reported this concern. This finding supports considering additional explanations for home study. Land Grand would focus those explanations on the selected Science topics.'
    elif text.startswith('Teachers held mixed views'):
        text="Teacher responses reflected mixed views about modular learning. Responses included doubts about how well it helped learners understand lessons. Other responses were positive or uncertain. The project therefore proposes additional activities alongside printed materials and teacher guidance."
    elif text.startswith('The Grade 5 topic responses'):
        text='Survey responses identified landforms, rocks, and minerals among the Science topics considered difficult. These reports provide a basis for selecting content for the game. The final lessons and selected items would still need content and curriculum validation.'
    elif text.startswith('The survey records adult observations'):
        text='The survey describes the views of parents and teachers from several grades. It does not directly measure pupil achievement or the effectiveness of Land Grand. The Grade 5 target of the game is separate from the survey population. The findings provide local background for the proposed learning resource.'
    elif text.startswith('The survey identified the following four reported problems'):
        text='The project focuses on the following reported problems and potential material limitation:'
    elif role=='section_intro' and text.startswith('This section presents the general'):
        text='This section presents the general and specific objectives of Land Grand. The specific objectives follow the same order as the project concerns and describe features that can be built and checked.'
    elif role=='body' and text.startswith('The project connects lesson explanations'):
        text='The project combines short explanations, interactive practice, and digital examples in one offline application. Digital examples would supplement physical specimens as additional visual material. The game is intended to support printed materials and teacher guidance during home study.'
    elif role=='scope' and text.startswith('Short lessons before each level'):
        text='Short lessons before each level, digital illustrations with item names and descriptions during collection, and a review after completion.'
    if role=='problem':
        text=problems[pi];pi+=1
    if role=='objective':
        text=objectives[oi];oi+=1
    if role=='limit' and text.startswith('The initial survey describes'):
        records.append(['limit',36,'Digital illustrations are supplementary visual materials. They do not provide physical specimens or hands-on examination of real rocks and minerals.'])
    records.append([role,pattern,text])
    if role=='body' and text.startswith('Survey responses identified landforms'):
        records.append(['body',5,'The project also considers the use of examples during Science lessons. When physical rock or mineral samples are limited, digital illustrations can provide an additional way to present the material. Land Grand would combine these illustrations with names and descriptions of collected items. The digital examples would serve as supplementary learning material for the selected Science topics.'])
assert pi==oi==4
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with ZipFile(ROOT/'reference.docx') as z:
    infos=z.infolist();parts={i.filename:z.read(i.filename) for i in infos}
assert hashlib.sha256((ROOT/'reference.docx').read_bytes()).hexdigest()=='1bc664f937cf9f49c3fedcb14f07e1b69aa84274bedf80f5ff22cd1be10ce594'
root=etree.fromstring(parts['word/document.xml'])
body=root.find('w:body',NS)
old_paras=body.findall('w:p',NS)
assert [''.join(p.xpath('.//w:t/text()',namespaces=NS)) for p in old_paras]==[r[2] for r in old]
patterns={}
for record,p in zip(old,old_paras):patterns.setdefault((record[0],record[1]),deepcopy(p))
section=deepcopy(body.find('w:sectPr',NS))
section_xml=etree.tostring(section,method='c14n',exclusive=True)
for child in list(body):body.remove(child)
openings={}
for i,(role,pattern,text) in enumerate(records):
    p=deepcopy(patterns[(role,pattern)])
    nodes=p.xpath('.//w:t',namespaces=NS)
    assert len(nodes)==1
    nodes[0].text=text
    if role in ('heading','subheading'):
        assert records[i+1][0] in ('section_intro','subsection_intro')
        assert records[i+1][2].startswith('This section ')
        openings[text]=records[i+1][2]
    body.append(p)
body.append(section)
assert len(openings)==6
assert section_xml==etree.tostring(body.find('w:sectPr',NS),method='c14n',exclusive=True)
patched=etree.tostring(root,encoding='UTF-8',xml_declaration=True,standalone=True)
with ZipFile(OUT,'w') as z:
    for info in infos:z.writestr(info,patched if info.filename=='word/document.xml' else parts[info.filename])
with ZipFile(OUT) as z:
    assert z.testzip() is None
    assert all(z.read(n)==value for n,value in parts.items() if n!='word/document.xml')
words=lambda s:len(re.findall(r"\b\w+(?:[’'–-]\w+)*\b",s))
text='\n\n'.join(r[2] for r in records)
a=next(i for i,r in enumerate(records) if r[2]=='Project Context')
b=next(i for i,r in enumerate(records) if r[2]=='Purpose and Description of the Project')
context='\n\n'.join(r[2] for r in records[a+1:b])
assert context.count('85%')==1 and context.count('20 parents and 20 teachers')==1
assert context.count('Parent responses covered Grades')==1
assert not any(t in text for t in ('TODO','[confirmed','[[','P-01','O-01'))
assert all('Grade 5' not in p for p in problems[:3])
assert 'may be limited' in problems[3]
long=[s for _,_,t in records for s in re.split(r'(?<=[.!?])\s+',t) if words(s)>30]
assert not long,long
report={'revision':8,'output':str(OUT),'paragraphs':len(records),'words':words(text),'context_words':words(context),'problems':problems,'objectives':objectives,'openings':openings,'long_sentences':long}
(ROOT/'revision8.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'build-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('problems','objectives','openings')},indent=2))
