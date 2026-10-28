from pathlib import Path
from copy import deepcopy
from zipfile import ZipFile
from lxml import etree
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parent
VAULT=Path(r'D:\Projects\LandGrand-Sources\LandGrand')
OUTPUT=VAULT/'Manuscript/Drafts/Land Grand - Chapter I - Revised - v5.docx'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
q=lambda key:'{'+NS['w']+'}'+key
records=json.loads((ROOT/'revision5.json').read_text(encoding='utf-8'))
expected_headings=['Project Context','Purpose and Description of the Project','Objectives of the Project','Scope and Limitations of the Project','Scope','Limitations']
opening_map={}
for index,(role,_,text) in enumerate(records):
    if role in ('heading','subheading'):
        next_role,_,next_text=records[index+1]
        assert next_role in ('section_intro','subsection_intro')
        assert len(re.split(r'(?<=[.!?])\s+',next_text))>=2
        opening_map[text]=next_text
assert set(opening_map)==set(expected_headings)
assert sum(role=='objective' for role,_,_ in records)==4
context='\n\n'.join(text for role,_,text in records[4:next(i for i,r in enumerate(records) if r[2]=='Purpose and Description of the Project')])
assert context.count('85%')==1
assert context.count('20 parents and 20 teachers')==1
assert 'Seventeen of 20' not in context and '85% of parents' in context
full='\n\n'.join(r[2] for r in records)
assert all(token not in full for token in ('TODO','[confirmed','[[','P-01','O-01'))
reference=ROOT/'reference.docx'
assert hashlib.sha256(reference.read_bytes()).hexdigest()=='8701feed03dc35bf065cba7b20911eb7251335b14eee6e0ab58d3317962b72d7'
with ZipFile(reference) as z:
    infos=z.infolist()
    parts={i.filename:z.read(i.filename) for i in infos}
root=etree.fromstring(parts['word/document.xml'])
body=root.find('w:body',NS)
templates=[p for p in body.findall('w:p',NS) if ''.join(p.xpath('.//w:t/text()',namespaces=NS)).strip()]
assert len(templates)==41
section=deepcopy(body.find('w:sectPr',NS))
canonical=etree.tostring(section,method='c14n',exclusive=True)
for element in list(body):
    body.remove(element)
for role,number,text in records:
    source=templates[number-1]
    p=etree.Element(q('p'))
    properties=source.find('w:pPr',NS)
    if properties is not None:p.append(deepcopy(properties))
    props=p.find('w:pPr',NS)
    if props is None:props=etree.SubElement(p,q('pPr'))
    if role in ('heading','subheading','lead') and props.find('w:keepNext',NS) is None:
        props.insert(0,etree.Element(q('keepNext')))
    if role in ('section_intro','subsection_intro','problem','objective','scope','limit') and props.find('w:keepLines',NS) is None:
        props.insert(0,etree.Element(q('keepLines')))
    run=etree.SubElement(p,q('r'))
    source_run=next(r for r in source.findall('w:r',NS) if r.find('w:t',NS) is not None)
    rprops=source_run.find('w:rPr',NS)
    if rprops is not None:run.append(deepcopy(rprops))
    etree.SubElement(run,q('t')).text=text
    body.append(p)
body.append(section)
assert canonical==etree.tostring(body.find('w:sectPr',NS),method='c14n',exclusive=True)
patched=etree.tostring(root,encoding='UTF-8',xml_declaration=True,standalone=True)
with ZipFile(OUTPUT,'w') as z:
    for info in infos:z.writestr(info,patched if info.filename=='word/document.xml' else parts[info.filename])
with ZipFile(OUTPUT) as z:
    assert z.testzip() is None
    assert all(z.read(n)==data for n,data in parts.items() if n!='word/document.xml')
word_count=lambda t:len(re.findall(r"\b\w+(?:[’'–-]\w+)*\b",t))
sentences=[s.strip() for _,_,text in records for s in re.split(r'(?<=[.!?])\s+',text) if s.strip()]
lengths=[word_count(s) for s in sentences]
prior=json.loads((ROOT.parent/'chapter1-word-2026-10-26/chapter-paragraphs.json').read_text(encoding='utf-8'))
old_sentences=[s for _,_,t in prior for s in re.split(r'(?<=[.!?])\s+',t) if s]
audit={'revision':5,'output':str(OUTPUT),'paragraphs':len(records),'word_count':word_count(full),'context_word_count':word_count(context),'opening_map':opening_map,'specific_objectives':4,'mean_sentence_words':round(sum(lengths)/len(lengths),1),'sentences_over_30_words':[s for s in sentences if word_count(s)>30],'old_mean_sentence_words':round(sum(word_count(s) for s in old_sentences)/len(old_sentences),1),'old_sentences_over_30':sum(word_count(s)>30 for s in old_sentences)}
(ROOT/'build-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'revised-body.txt').write_text(full,encoding='utf-8')
print(json.dumps(audit,ensure_ascii=False,indent=2))
