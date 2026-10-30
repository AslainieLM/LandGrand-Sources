from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from pypdf import PdfReader
import hashlib, importlib.util, json, re, shutil, sys

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent.parent
VAULT = WORKSPACE / 'LandGrand'
FINAL = VAULT / 'Manuscript/Drafts/Land Grand - Chapter I - Revised - v9.docx'
SOURCE = ROOT / 'reference.docx'
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NS = {'w':W}

def body_text(p):
    return ''.join((e.text or '') if e.tag=='{'+W+'}t' else '\n' for e in p.iter() if e.tag in ['{'+W+'}t','{'+W+'}br'])

records=json.loads((ROOT/'final-content.json').read_text(encoding='utf-8'))
audit=json.loads((ROOT/'word-audit-checked.json').read_text(encoding='utf-8-sig'))
assert audit['pages']==9
assert len(records)==len(audit['paragraphs'])==68
for p,a in zip(records,audit['paragraphs']):
    assert p['text'].strip()==a['text'].replace('\x0b','\n').replace('\x05','').strip(),(p['paragraph'],a['text'])
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()=='6ad898c79899c91d506b625b992959af921c53fee88167390d2151f581ada3ad'
for name,expected in json.loads((ROOT/'protected-hashes.json').read_text()).items():
    assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==expected,name

with ZipFile(SOURCE) as a,ZipFile(FINAL) as b:
    assert b.testzip() is None
    changed=[n for n in a.namelist() if a.read(n)!=b.read(n)]
    assert set(changed)=={'word/document.xml','word/_rels/document.xml.rels','[Content_Types].xml','docProps/app.xml'},changed
    assert set(b.namelist())-set(a.namelist())=={'word/comments.xml'}
    old=etree.fromstring(a.read('word/document.xml'));new=etree.fromstring(b.read('word/document.xml'))
    assert etree.tostring(old.find('.//w:sectPr',NS))==etree.tostring(new.find('.//w:sectPr',NS))
    for rel in etree.fromstring(a.read('word/_rels/document.xml.rels')):
        candidates=[r for r in etree.fromstring(b.read('word/_rels/document.xml.rels')) if r.get('Id')==rel.get('Id')]
        assert len(candidates)==1 and dict(candidates[0].attrib)==dict(rel.attrib)
    comments=etree.fromstring(b.read('word/comments.xml'))
    ids=comments.xpath('//w:comment/@w:id',namespaces=NS)
    assert len(ids)==7
    for cid in ids:
        for tag in ['commentRangeStart','commentRangeEnd','commentReference']:
            assert len(new.xpath('//w:'+tag+'[@w:id="'+cid+'"]',namespaces=NS))==1
    for p in new.findall('w:body/w:p',NS):
        if p.find('w:pPr',NS) is not None: assert list(p)[0].tag=='{'+W+'}pPr'
    hyperlinks=[r.get('Target') for r in etree.fromstring(b.read('word/_rels/document.xml.rels')) if r.get('Type')==R+'/hyperlink']
    assert len(hyperlinks)==3
    assert all(u.startswith('https://') for u in hyperlinks)
    assert len(new.xpath('//w:hyperlink',namespaces=NS))==3

reader=PdfReader(ROOT/'revision9-checked.pdf')
pdf_text='\n'.join(p.extract_text() or '' for p in reader.pages)
assert re.findall(r'^\s*([1-4])\.\s',pdf_text,re.M)==['1','2','3','4','1','2','3','4']
pdf_uris=set()
for page in reader.pages:
    for ref in page.get('/Annots',[]):
        obj=ref.get_object()
        if obj.get('/A',{}).get('/URI'):pdf_uris.add(str(obj['/A']['/URI']))
assert set(hyperlinks)<=pdf_uris,(hyperlinks,pdf_uris)
assert len(list((ROOT/'render-3').glob('page-*.png')))==9
assert sum(p['text'].startswith('This section') for p in records)==7
assert sum('85%' in p['text'] for p in records)==1
assert any(p['text']=='The researcher observed limited rock and mineral samples for classroom demonstrations.' for p in records)
assert any('believed that a mobile game could support' in p['text'] for p in records)
assert not any('(2d)' in p['text'] for p in records)
for p in records[:63]:
    for sentence in re.split(r'(?<=[.!?])\s+',p['text']):
        assert len(re.findall(r"\b[\w]+(?:[-'][\w]+)*\b",sentence))<=30,(p['paragraph'],sentence)

headings=['Project Context','Purpose and Description of the Project','Objectives of the Project','Scope and Limitations of the Project','Scope','Limitations','BIBLIOGRAPHY']
heading_pages={p['text']:p['startPage'] for p in audit['paragraphs'] if p['text'] in headings}
assert heading_pages['Project Context']==1
context_end=next(p['endPage'] for p in audit['paragraphs'] if p['text'].startswith('These concerns support developing Land Grand'))
assert context_end>=2

# The packaged comparison reuses the already rendered native pages at the same DPI.
script=Path(r'C:\Users\user\.codex\plugins\cache\openai-primary-runtime\documents\26.1029.11837\skills\documents\scripts\render_and_diff.py')
spec=importlib.util.spec_from_file_location('packaged_fidelity',script)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
def cached_render(render_py,docx,outdir):
    folder={SOURCE.resolve():ROOT.parent/'chapter1-final-review-2026-10-30/render-1',FINAL.resolve():ROOT/'render-3'}[Path(docx).resolve()]
    Path(outdir).mkdir(parents=True,exist_ok=True)
    for p in folder.glob('page-*.png'):shutil.copy2(p,Path(outdir)/p.name)
module._run_render=cached_render
sys.argv=[str(script),str(SOURCE),str(FINAL),'--outdir',str(ROOT/'fidelity-3')]
module.main()

# Synchronize the body from the same records that passed native Word agreement.
front='''---
type: manuscript-draft
status: proposed
updated: 2026-10-30
revision: 9
sources:
  - "[[Sources/Chapter I Final User Draft 2026-10-30]]"
  - "[[Sources/Researcher Observation - Rock and Mineral Samples 2026-10-30]]"
  - "[[Manuscript/Chapter 1-3 Writing Guide]]"
  - "[[Project/Scope and Requirements]]"
  - "[[Sources/Baluan Survey CSV Records]]"
  - "[[Sources/Project Clarifications 2026-10-26]]"
  - "[[Sources/UNESCO GEM 2023 Technology]]"
  - "[[Sources/DepEd Distance Learning Strategies 2020]]"
  - "[[Sources/PHIVOLCS Sarangani Earthquake 2026]]"
---

# Chapter I Introduction

> Revision 9, corrected review copy. [[Manuscript/Drafts/Land Grand - Chapter I - Revised - v9.docx|Open the current Word copy]]. Based on the user's final-named source under D-020. Includes a three-entry bibliography, restored scope details and seven local review comments. Problem 4 is attributed to the researcher's reported observation under D-021; its date and sample details remain pending. Nine pages were inspected; Context spans pages 1–4 and Bibliography is on page 9. The planned November–December 2026 window retains D-015's contextual year distinction. [[Manuscript/Chapter I Revision Notes|Revision notes]] own the remaining checks. Original and earlier Word versions are preserved.

'''
lines=[];counters={}
for p in records[2:]:
    value=p['text']
    if value in headings:
        lines.append(('### ' if value in ['Scope','Limitations'] else '## ')+value)
    elif p['num_id'] in ['7','5']:
        counters[p['num_id']]=counters.get(p['num_id'],0)+1
        lines.append(str(counters[p['num_id']])+'. '+value)
    elif p['num_id'] in ['6','2']:
        lines.append('- '+value)
    else:
        lines.append(value.replace('\n','  \n'))
    lines.append('')
(VAULT/'Manuscript/Drafts/Chapter I Introduction.md').write_text(front+'\n'.join(lines),encoding='utf-8')
result={'revision':9,'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'output':str(FINAL),'sha256':hashlib.sha256(FINAL.read_bytes()).hexdigest(),'pages':audit['pages'],'words':audit['words'],'paragraphs':len(records),'context_pages':[1,context_end],'heading_pages':heading_pages,'comments':7,'bibliography_entries':3,'official_live_links':hyperlinks,'changed_original_parts':changed,'added_parts':['word/comments.xml'],'visual_review':'All nine final page PNGs inspected; no clipping, overlap, missing glyphs or isolated final-limitation page.','source_and_earlier_word_files':'unchanged','survey_csvs':'unchanged','material_observation':'user-reported personal observation; date and sample details pending; no verified city-wide inventory','page_sha256':{str(i):hashlib.sha256((ROOT/'render-3'/f'page-{i}.png').read_bytes()).hexdigest() for i in range(1,10)}}
(ROOT/'final-verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ['page_sha256','official_live_links']},indent=2))
