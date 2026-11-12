from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from pypdf import PdfReader
import hashlib, importlib.util, json, re, shutil, sys

ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[1]
read=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NS={'w':W}
c14n=lambda e:etree.tostring(e,method='c14n')
paragraph_text=lambda p:''.join(p.xpath('.//w:t/text()',namespaces=NS))
outputs={k:Path(v) for k,v in read(ROOT/'outputs.json').items()}
changes=read(ROOT/'change-slots.json')
manifest=read(ROOT/'input-manifest.json')
refs=read(ROOT/'references-corrected.json')
page_counts={}
chapters={}
package_changes={}
for key in ['chapter1','chapter2']:
    source=ROOT/(key+'.docx'); target=outputs[key]
    assert sha(source)==manifest[key]['sha256']
    with ZipFile(source) as a, ZipFile(target) as b:
        assert b.testzip() is None and set(a.namelist())==set(b.namelist())
        changed=[n for n in a.namelist() if a.read(n)!=b.read(n)]
        assert changed==['word/document.xml']
        package_changes[key]=changed
        x=etree.fromstring(a.read('word/document.xml'));y=etree.fromstring(b.read('word/document.xml'))
        assert c14n(x.find('w:body/w:sectPr',NS))==c14n(y.find('w:body/w:sectPr',NS))
        old=x.findall('w:body/w:p',NS); new=y.findall('w:body/w:p',NS)
        assert len(old)==len(new)
        for i,(p1,p2) in enumerate(zip(old,new)):
            if i not in changes[key]: assert c14n(p1)==c14n(p2),(key,i)
            assert c14n(p1.find('w:pPr',NS))==c14n(p2.find('w:pPr',NS))
        assert not y.xpath('//w:ins | //w:del | //w:commentReference',namespaces=NS)
        chapters[key]=[paragraph_text(p) for p in new if paragraph_text(p).strip()]
    audit=read(ROOT/(key+'-final-audit.json'))
    assert audit['readOnly']
    normalize=lambda t:re.sub(r'\s+',' ',t.replace('\x0b','')).strip()
    assert [normalize(t) for t in chapters[key]]==[normalize(p['text']) for p in audit['paragraphs']]
    page_counts[key]=audit['pages']
    assert len(list((ROOT/(key+'-render-final')).glob('page-*.png')))==audit['pages']
    headings={'chapter1':['Project Context','Purpose and Description of the Project','Objectives of the Project','Scope and Limitations of the Project','Scope','Limitations','BIBLIOGRAPHY'],
              'chapter2':['Related Literature / Theoretical Background','Related Studies','Related Projects','Synopsis']}[key]
    for heading in headings:
        index=chapters[key].index(heading)
        assert chapters[key][index+1].startswith('This section ')

c1='\n'.join(chapters['chapter1']);c2='\n'.join(chapters['chapter2']);all_text=c1+'\n'+c2
assert [next(i for i,t in enumerate(chapters['chapter2']) if t.startswith('The '+n+' objective')) for n in ['first','second','third','fourth']]==[15,18,23,26]
assert all(term in c1 for term in ['Unity and C#','Piskel and Clip Studio Paint','October 29, 2026','Grade 5 display','subject to device testing'])
assert 'October 29, 2026' in c2 and 'school\'s full specimen inventory' in c2
for forbidden in ['Ford (2005)','(n.d.)',', n.d.','Pezzetti','Fannyflamingo','The Digital Geology Kit','Those survey responses','Mayer (2024)','Brown et al. (1989)','DisasterSafetyGame','75 levels']:
    assert forbidden not in all_text,forbidden
assert '60 levels' in c1 and '60 planned levels' in c2 and 'Android 10 and above' in c1 and 'Android 10 and above' in c2
patterns={
    'andrews':r'Andrews et al\. \(2020\)', 'buray':r'Buray and Alferez \(2025\)',
    'calvo':r'Calvo and Lucha \(2024\)', 'chung':r'Chung and Pan \(2023\)',
    'cutting':r'Cutting and Deterding \(2024\)', 'deped':r'Department of Education, 2020',
    'dong':r'Dong et al\. \(2024\)', 'phivolcs':r'DOST-PHIVOLCS, 2026',
    'garzon':r'Garzón et al\. \(2025\)', 'hodges':r'Hodges and Flanagan \(2026\)',
    'ivgin':r'Ivgin and Akcay \(2024\)', 'legends':r'Legends of Learning \(2025\)',
    'oh':r'Oh \(2020\)', 'rader':r'Rader et al\. \(2021\)',
    'rodriguez':r'Rodríguez-Ferrer et al\. \(2023\)', 'unesco':r'UNESCO, 2023',
    'yachin':r'Yachin and Barak \(2024\)'}
assert set(patterns)=={item['id'] for item in refs}
assert len(refs)==17 and all(re.search(pattern,all_text) for pattern in patterns.values())
assert all(2020<=int(item['year'])<=2026 for item in refs)
assert refs==sorted(refs,key=lambda x:x['author'].casefold())
with ZipFile(ROOT/'chapter1.docx') as a, ZipFile(outputs['bibliography']) as b:
    assert b.testzip() is None
    assert set(a.namelist())==set(b.namelist())
    changed=[n for n in a.namelist() if a.read(n)!=b.read(n)]
    assert set(changed)=={'word/document.xml','word/_rels/document.xml.rels'}
    package_changes['bibliography']=changed
    x=etree.fromstring(a.read('word/document.xml')); y=etree.fromstring(b.read('word/document.xml'))
    assert c14n(x.find('w:body/w:sectPr',NS))==c14n(y.find('w:body/w:sectPr',NS))
    ps=y.findall('w:body/w:p',NS)
    assert len(ps)==19
    assert paragraph_text(ps[1]).startswith('This section ')
    for p in ps[2:]:
        assert p.xpath('w:pPr/w:ind[@w:left="720"][@w:hanging="720"]',namespaces=NS)
        assert p.xpath('w:pPr/w:keepLines[@w:val="1"]',namespaces=NS)
    rels=etree.fromstring(b.read('word/_rels/document.xml.rels'))
    targets={x.get('Id'):x.get('Target') for x in rels if x.get('Type')==R+'/hyperlink'}
    links=y.findall('.//w:hyperlink',NS)
    used={targets[x.get('{'+R+'}id')] for x in links}
    assert len(links)==17 and used=={x['url'] for x in refs}
    for p,ref in zip(ps[2:],refs):
        assert paragraph_text(p).startswith(ref['author']+' ('+ref.get('date',ref['year'])+'). ')
        assert ref['title'] in paragraph_text(p) and ref['url'] in paragraph_text(p)
audit=read(ROOT/'bibliography-final-audit-2.json'); assert audit['readOnly']
page_counts['bibliography']=audit['pages']
assert [paragraph_text(p) for p in ps]==[p['text'] for p in audit['paragraphs']]
assert len(list((ROOT/'bibliography-render-final-2').glob('page-*.png')))==audit['pages']
with PdfReader(ROOT/'bibliography-final-2.pdf') as pdf:
    uris={str(a.get_object().get('/A',{}).get('/URI')) for page in pdf.pages for a in page.get('/Annots',[]) if a.get_object().get('/A',{}).get('/URI')}
assert {x['url'] for x in refs}<=uris
before=read(ROOT/'vault-before.json')
after={str(p.relative_to(WORKSPACE/'LandGrand')):sha(p) for p in (WORKSPACE/'LandGrand').rglob('*') if p.is_file()}
assert before==after,'Canonical vault changed'

# Packaged comparison, using exactly the native-render pages inspected above.
script=Path(r'C:\Users\user\.codex\plugins\cache\openai-primary-runtime\documents\26.1026.10807\skills\documents\scripts\render_and_diff.py')
spec=importlib.util.spec_from_file_location('packaged_final_diff',script)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
def cached_render(render_py,docx,outdir):
    mapping={
        (ROOT/'chapter1.docx').resolve():WORKSPACE/'.work/final-chapters-review-2026-11-01/chapter1-render',
        (ROOT/'chapter2.docx').resolve():WORKSPACE/'.work/final-chapters-review-2026-11-01/chapter2-render',
        outputs['chapter1'].resolve():ROOT/'chapter1-render-final',outputs['chapter2'].resolve():ROOT/'chapter2-render-final',
        outputs['bibliography'].resolve():ROOT/'bibliography-render-final-2'}
    Path(outdir).mkdir(parents=True,exist_ok=True)
    for p in mapping[Path(docx).resolve()].glob('page-*.png'):shutil.copy2(p,Path(outdir)/p.name)
module._run_render=cached_render
for key in ['chapter1','chapter2','bibliography']:
    source=ROOT/('chapter1.docx' if key=='bibliography' else key+'.docx')
    sys.argv=[str(script),str(source),str(outputs[key]),'--outdir',str(ROOT/(key+'-fidelity'))]
    module.main()
report={
    'date':'2026-11-01','pages':page_counts,'total_pages':sum(page_counts.values()),
    'native_words':{key:read(ROOT/(key+'-final-audit.json'))['words'] for key in ['chapter1','chapter2']},
    'bibliography_sources':17,'chapter2_sources':14,'citation_reference_matching':True,
    'year_rule':'Every cited published reference is dated 2020–2026; no undated references.',
    'source_and_output_text_verified':True,'allowed_changed_paragraphs':changes,
    'all_other_paragraphs_and_properties_preserved':True,'package_changes':package_changes,
    'original_reference_hashes_preserved':True,'vault_files_unchanged':len(before),
    'live_bibliography_word_and_pdf_targets':17,
    'visual_review':'All nine Chapter I, ten Chapter II and three latest bibliography pages inspected at 120 DPI. No clipping, overlap, stranded headings or near-empty overflow page.',
    'observation':'User-reported October 29, 2026 Grade 5 display at Baluan; not a complete school inventory.',
    'limits':['Oh: original English abstract/header inspected; Korean methods and tables not fully reviewed','Dong: publisher abstract; Garzon: publisher preview; Yachin: publisher abstract','Rader: article has inconsistent enrollment totals 24/25; no participant count reused','Adviser/curriculum approval, detailed gameplay and actual learning evaluation remain outside these document corrections','APA author–date and matching bibliography used; mandatory numbered-note format not established'],
    'output_hashes':{str(p):sha(p) for p in outputs.values()}
}
(ROOT/'final-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ['output_hashes','package_changes','limits']},ensure_ascii=False,indent=2))
