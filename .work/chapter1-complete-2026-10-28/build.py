from pathlib import Path
from copy import deepcopy
from zipfile import ZipFile
from lxml import etree
import hashlib,json,re

ROOT=Path(__file__).resolve().parent
VAULT=Path(r'D:\Projects\LandGrand-Sources\LandGrand')
OUT=VAULT/'Manuscript/Drafts/Land Grand - Chapter I - Revised - v7.docx'
records=json.loads((ROOT.parent/'chapter1-openings-2026-10-28/revision6.json').read_text(encoding='utf-8'))
problems=[
 "Some surveyed parents of Grade 5 learners reported difficulty explaining lessons in printed modules to their children.",
 "Some surveyed Grade 5 teachers did not consider modular learning effective in helping learners understand lessons.",
 "Some parents of Grade 5 learners reported landforms as a difficult Science topic for their children.",
 "Some Grade 5 parent and teacher responses identified rocks or minerals as difficult Science topics."
]
objectives=[
 "Provide a short Science lesson before each level to give Grade 5 learners additional explanations during home study.",
 "Implement interactive exploration with movement and jumping controls and a review after each level to supplement printed Science learning materials.",
 "Develop four episodes covering Mountains, Hills, Plains, and Plateaus, with lessons and exploration activities focused on these landforms.",
 "Implement rock and mineral collection, with a pop-up showing each collected item's name and short description."
]
new=[]
pi=oi=0
for role,pattern,text in records:
    if text.startswith('The survey showed that 85%'):
        new.extend([
          ['body',5,'Difficulty explaining module lessons was reported by many parents. In the full parent group, 85% reported difficulty explaining these lessons to their children. Similar concerns appeared among parents of Grade 5 learners. These responses support providing additional explanations within the Science topics covered by the project.'],
          ['body',5,'Teachers held mixed views about the effectiveness of modular learning. Some surveyed Grade 5 teachers did not consider it effective in helping learners understand lessons. Others were uncertain or considered it effective. These views support considering additional learning activities alongside printed materials, while keeping the role of teacher guidance.'],
          ['body',5,'The Grade 5 topic responses give a more specific basis for the proposed content. Some parents mentioned landforms among the Science topics their children found difficult. Other parent and teacher responses mentioned rocks or minerals. These are distinct content areas that Land Grand would cover through lessons, exploration, and item descriptions.']
        ])
        continue
    if text.startswith('The survey findings describe adult observations'):
        text="The survey records adult observations and views across several grades. The Grade 5 groups contain six parent responses and five teacher responses. These small groups help describe local concerns but cannot represent all Grade 5 learners. The findings also do not establish whether Land Grand improves knowledge, since the survey did not evaluate the game."
    if text.startswith('The survey and school context identify two reported concerns'):
        text='The survey identified the following four reported problems relevant to the proposed Land Grand project:'
    if role=='problem':
        text=problems[pi];pi+=1
    if role=='objective':
        text=objectives[oi];oi+=1
    if role=='section_intro' and text.startswith('This section presents the general'):
        text='This section presents the general and specific objectives of Land Grand. The four specific objectives follow the same order as the reported problems and describe features that can be built and checked.'
    new.append([role,pattern,text])
records=new
assert pi==oi==4
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
q=lambda t:'{'+NS['w']+'}'+t
with ZipFile(ROOT/'reference.docx') as z:
    infos=z.infolist()
    parts={i.filename:z.read(i.filename) for i in infos}
assert hashlib.sha256((ROOT/'reference.docx').read_bytes()).hexdigest()=='ac0d6c09f6b092c824132d351c0035d663afda281cba5505700e7c65981f4f55'
source_records=json.loads((ROOT.parent/'chapter1-openings-2026-10-28/revision6.json').read_text(encoding='utf-8'))
tree=etree.fromstring(parts['word/document.xml'])
body=tree.find('w:body',NS)
old_paras=body.findall('w:p',NS)
assert [''.join(p.xpath('.//w:t/text()',namespaces=NS)) for p in old_paras]==[r[2] for r in source_records]
section=deepcopy(body.find('w:sectPr',NS))
patterns={}
for record,p in zip(source_records,old_paras):
    patterns.setdefault((record[0],record[1]),deepcopy(p))

# Append new decimal numbering without modifying any existing definition.
numbering=etree.fromstring(parts['word/numbering.xml'])
original_numbering_children=[etree.tostring(x,method='c14n',exclusive=True) for x in numbering]
abstract_id=max(int(x.get(q('abstractNumId'))) for x in numbering.findall('w:abstractNum',NS))+1
first_id=max(int(x.get(q('numId'))) for x in numbering.findall('w:num',NS))+1
abstract=etree.Element(q('abstractNum'))
abstract.set(q('abstractNumId'),str(abstract_id))
for key,value in [('nsid','4C474337'),('multiLevelType','singleLevel')]:
    child=etree.SubElement(abstract,q(key));child.set(q('val'),value)
source_lvl=numbering.xpath('./w:abstractNum[@w:abstractNumId="1"]/w:lvl[@w:ilvl="0"]',namespaces=NS)[0]
level=deepcopy(source_lvl)
level.find('w:start',NS).set(q('val'),'1')
level.find('w:numFmt',NS).set(q('val'),'decimal')
level.find('w:lvlText',NS).set(q('val'),'%1.')
rprops=level.find('w:rPr',NS)
if rprops is not None:level.remove(rprops)
rprops=etree.SubElement(level,q('rPr'))
fonts=etree.SubElement(rprops,q('rFonts'))
fonts.set(q('ascii'),'Times New Roman');fonts.set(q('hAnsi'),'Times New Roman')
size=etree.SubElement(rprops,q('sz'));size.set(q('val'),'24')
abstract.append(level)
first_num=next(i for i,x in enumerate(numbering) if x.tag==q('num'))
numbering.insert(first_num,abstract)
for number in (first_id,first_id+1):
    num=etree.SubElement(numbering,q('num'));num.set(q('numId'),str(number))
    ref=etree.SubElement(num,q('abstractNumId'));ref.set(q('val'),str(abstract_id))
    override=etree.SubElement(num,q('lvlOverride'));override.set(q('ilvl'),'0')
    start=etree.SubElement(override,q('startOverride'));start.set(q('val'),'1')
remaining=[x for x in numbering if x is not abstract and not (x.tag==q('num') and int(x.get(q('numId')))>=first_id)]
assert [etree.tostring(x,method='c14n',exclusive=True) for x in remaining]==original_numbering_children

for child in list(body):body.remove(child)
openings={}
for i,(role,pattern,text) in enumerate(records):
    p=deepcopy(patterns[(role,pattern)])
    runs=p.xpath('.//w:t',namespaces=NS)
    assert len(runs)==1
    runs[0].text=text
    if role in ('problem','objective'):
        num_id=p.find('w:pPr/w:numPr/w:numId',NS)
        assert num_id is not None
        num_id.set(q('val'),str(first_id if role=='problem' else first_id+1))
    if role in ('heading','subheading'):
        assert records[i+1][0] in ('section_intro','subsection_intro')
        assert records[i+1][2].startswith('This section ')
        openings[text]=records[i+1][2]
    body.append(p)
body.append(section)
assert len(openings)==6
patched={'word/document.xml':etree.tostring(tree,encoding='UTF-8',xml_declaration=True,standalone=True),'word/numbering.xml':etree.tostring(numbering,encoding='UTF-8',xml_declaration=True,standalone=True)}
with ZipFile(OUT,'w') as z:
    for info in infos:z.writestr(info,patched.get(info.filename,parts[info.filename]))
with ZipFile(OUT) as z:
    assert z.testzip() is None
    assert all(z.read(name)==value for name,value in parts.items() if name not in patched)

word_count=lambda s:len(re.findall(r"\b\w+(?:[’'–-]\w+)*\b",s))
full='\n\n'.join(r[2] for r in records)
start=next(i for i,r in enumerate(records) if r[2]=='Project Context')
end=next(i for i,r in enumerate(records) if r[2]=='Purpose and Description of the Project')
context='\n\n'.join(r[2] for r in records[start+1:end])
assert context.count('85%')==1 and context.count('20 parents and 20 teachers')==1
assert all(t not in full for t in ('TODO','[confirmed','[[','P-01','O-01','design needs for the proposed project'))
sentences=[s for _,_,t in records for s in re.split(r'(?<=[.!?])\s+',t) if s]
report={'revision':7,'output':str(OUT),'paragraphs':len(records),'words':word_count(full),'context_words':word_count(context),'section_openings':openings,'problems':problems,'objectives':objectives,'numbering_ids':{'abstract':abstract_id,'problems':first_id,'objectives':first_id+1},'long_sentences':[s for s in sentences if word_count(s)>30]}
assert not report['long_sentences']
(ROOT/'revision7.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'build-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('section_openings','problems','objectives')},indent=2))
