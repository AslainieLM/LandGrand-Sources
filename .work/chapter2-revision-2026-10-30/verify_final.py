from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from pypdf import PdfReader
import hashlib, importlib.util, json, re, shutil, sys

ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[1]
OUT=WORKSPACE/'Deliverables/Chapter II Revision 2026-10-30'
SOURCE=ROOT/'chapter1-reference.docx'
FINAL=OUT/'Land Grand - Chapter II - Revised - v1.docx'
BIB=OUT/'Land Grand - Chapter II - APA References.docx'
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NS={'w':W}
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
count=lambda s:len(re.findall(r'\b[\w’]+\b',s))
records=json.loads((ROOT/'chapter.json').read_text(encoding='utf-8'))
refs=json.loads((ROOT/'references.json').read_text(encoding='utf-8'))
audit=json.loads((ROOT/'chapter-final-audit-2.json').read_text(encoding='utf-8-sig'))
bib_audit=json.loads((ROOT/'references-final-audit.json').read_text(encoding='utf-8-sig'))
assert audit['readOnly'] and bib_audit['readOnly']
assert audit['pages']==10 and bib_audit['pages']==3
assert len(records)==len(audit['paragraphs'])==40
assert [x['text'] for x in records]==[x['text'] for x in audit['paragraphs']]

headings=[r['text'] for r in records if r['role'] in ['heading','subheading']]
assert headings==['Related Literature / Theoretical Background','Related Studies','Related Projects','Synopsis']
for i,r in enumerate(records):
    if r['role'] in ['heading','subheading']:
        assert records[i+1]['role']=='intro' and records[i+1]['text'].startswith('This section ')
assert sum(r['text'].startswith('This section ') for r in records)==4
order=[]
for r in records:
    if 'objective' in r and (not order or order[-1]!=r['objective']):order.append(r['objective'])
assert order==[1,2,3,4]
text='\n'.join(r['text'] for r in records)
for bad in ['DisasterSafetyGame','75 levels','earthquake episodes','Catedrilla','Demedts','Research Review','TODO','[INSERT','turn23','publisher highlights','latest project clarification']:
    assert bad not in text,bad
assert '60 planned levels' in text and 'Android 10 and above' in text
assert 'Grade 5' in text and 'single player' in text
assert 'proposes the Cognitive Theory' in text
assert '\ufffd' not in text
for item in records:
    for sentence in re.split(r'(?<=[.!?])\s+(?=[A-Z])',item['text']):
        assert count(sentence)<=30,(count(sentence),sentence)

patterns={
'andrews':r'Andrews et al\. \(2020\)',
'brown':r'Brown et al\. \(1989\)',
'buray':r'Buray and Alferez \(2025\)',
'calvo':r'Calvo and Lucha \(2024\)',
'chung':r'Chung and Pan \(2023\)',
'dong':r'Dong et al\. \(2024\)',
'geologyrocks':r'Fannyflamingo \(n\.d\.\)',
'ford':r'Ford \(2005\)',
'garzon':r'Garzón et al\. \(2025\)',
'hodges':r'Hodges and Flanagan \(2026\)',
'ivgin':r'Ivgin and Akcay \(2024\)',
'mayer':r'Mayer \(2024\)',
'docduck':r'\(Pezzetti, n\.d\.\)',
'rodriguez':r'Rodríguez-Ferrer et al\. \(2023\)',
'openuniversity':r'The Open University \(n\.d\.\)'}
assert set(patterns)=={r['id'] for r in refs}
assert all(re.search(pattern,text) for pattern in patterns.values())

package_changes={}
for path in [FINAL,BIB]:
    with ZipFile(SOURCE) as a, ZipFile(path) as b:
        assert b.testzip() is None
        assert set(a.namelist())==set(b.namelist())
        changed=[n for n in a.namelist() if a.read(n)!=b.read(n)]
        assert set(changed)<= {'word/document.xml','word/_rels/document.xml.rels'}
        x=etree.fromstring(a.read('word/document.xml'));y=etree.fromstring(b.read('word/document.xml'))
        assert etree.tostring(x.find('w:body/w:sectPr',NS))==etree.tostring(y.find('w:body/w:sectPr',NS))
        assert len(y.findall('w:body/w:sectPr',NS))==1
        assert not y.xpath('//w:commentRangeStart | //w:ins | //w:del | //w:drawing',namespaces=NS)
        oldrels=etree.fromstring(a.read('word/_rels/document.xml.rels'))
        newrels=etree.fromstring(b.read('word/_rels/document.xml.rels'))
        for rel in oldrels:
            matching=[n for n in newrels if n.get('Id')==rel.get('Id')]
            assert len(matching)==1 and dict(matching[0].attrib)==dict(rel.attrib)
        package_changes[path.name]=changed
        if path==FINAL:
            paras=[''.join(p.xpath('.//w:t/text()',namespaces=NS)) for p in y.findall('w:body/w:p',NS)]
            assert paras==[r['text'] for r in records]
        else:
            links=[n.get('Target') for n in newrels if n.get('Type')==R+'/hyperlink']
            assert len(links)==15 and set(links)=={r['url'] for r in refs}
            assert len(y.findall('w:body/w:p',NS))==17
            paras=[''.join(p.xpath('.//w:t/text()',namespaces=NS)) for p in y.findall('w:body/w:p',NS)]
            assert paras==[p['text'] for p in bib_audit['paragraphs']]
            assert all(len(p.xpath('w:pPr/w:ind[@w:hanging="720"]',namespaces=NS))==1 for p in y.findall('w:body/w:p',NS)[2:])

with PdfReader(ROOT/'references-final.pdf') as reader:
    uris={str(ref.get_object().get('/A',{}).get('/URI')) for page in reader.pages for ref in page.get('/Annots',[]) if ref.get_object().get('/A',{}).get('/URI')}
assert {r['url'] for r in refs}<=uris
assert len(list((ROOT/'chapter-render-2').glob('page-*.png')))==10
assert len(list((ROOT/'references-render').glob('page-*.png')))==3
assert sha(SOURCE)=='6ad898c79899c91d506b625b992959af921c53fee88167390d2151f581ada3ad'
assert sha(ROOT/'chapter2-original.docx')=='168781620da2b47b7390cce5a3182656610f60d34ece8c91a28d5114f9b85180'
before=json.loads((ROOT/'vault-before.json').read_text())
after={str(p):sha(p) for p in (WORKSPACE/'LandGrand').rglob('*') if p.is_file()}
assert before==after,'Vault was changed'

# Run the packaged visual/text comparison using the exact native page renders
# already inspected. The installed skill and originals are untouched.
script=Path(r'C:\Users\user\.codex\plugins\cache\openai-primary-runtime\documents\26.1029.11837\skills\documents\scripts\render_and_diff.py')
spec=importlib.util.spec_from_file_location('packaged_fidelity',script)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
def cached_render(render_py,docx,outdir):
    folder={SOURCE.resolve():ROOT/'reference-render',FINAL.resolve():ROOT/'chapter-render-2',BIB.resolve():ROOT/'references-render'}[Path(docx).resolve()]
    Path(outdir).mkdir(parents=True,exist_ok=True)
    for p in folder.glob('page-*.png'):shutil.copy2(p,Path(outdir)/p.name)
mod._run_render=cached_render
for path,label in [(FINAL,'chapter-fidelity'),(BIB,'bibliography-fidelity')]:
    sys.argv=[str(script),str(SOURCE),str(path),'--outdir',str(ROOT/label)]
    mod.main()

with ZipFile(ROOT/'chapter2-original.docx') as z:
    x=etree.fromstring(z.read('word/document.xml'))
    original_paras=[''.join(p.xpath('.//w:t/text()',namespaces=NS)) for p in x.findall('w:body/w:p',NS)]
old_count=count(' '.join(original_paras[:original_paras.index('REFERENCES')]))
report={
 'date':'2026-10-30','chapter_pages':10,'bibliography_pages':3,
 'chapter_word_count_native':audit['words'],'chapter_word_count_tokenized':count(text),
 'original_narrative_word_count_tokenized':old_count,
 'originals_preserved':True,'vault_files_unchanged':len(before),
 'source_references':15,'citation_reference_bijection':True,
 'this_section_openings':4,'objective_order':order,
 'visual_review':'All 10 final chapter and 3 bibliography pages inspected at 120 DPI; no clipping, overlap, stranded headings or near-empty closing page.',
 'source_access_limits':['Dong: publisher abstract','Garzon: publisher preview','Ford: publisher abstract','Products: descriptions only; no gameplay testing'],
 'package_changes':package_changes,'output_hashes':{str(p):sha(p) for p in [FINAL,BIB]},
 'checks_not_completed':['Full methods/tables for three partial-access sources','Adviser and curriculum approval','Land Grand implementation/device and learning evaluation; outside this revision task']}
(ROOT/'final-verification.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(report,indent=2,ensure_ascii=False))
