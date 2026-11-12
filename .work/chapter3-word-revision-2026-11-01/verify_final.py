from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from pypdf import PdfReader
from ctypes import wintypes
import ast,ctypes,hashlib,importlib.util,json,re,shutil,sys

ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parent.parent
VAULT=WORKSPACE/'LandGrand'
read=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
outputs={k:Path(v) for k,v in read(ROOT/'outputs.json').items()}
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NS={'w':W}
def text(p):
    return ''.join((node.text or '') if node.tag=='{'+W+'}t' else '\n' if node.tag=='{'+W+'}br' else '\t' if node.tag=='{'+W+'}tab' else '' for node in p.iter())
c14n=lambda e:E.tostring(e,method='c14n')
normalize=lambda s:re.sub(r'\s+',' ',s).strip()
source=ROOT/'chapter3-source.docx'
assert sha(source)==read(ROOT/'source-inventory.json')['sha256']
package_changes={};alltexts={};counts={}
with ZipFile(source) as src:
    old=E.fromstring(src.read('word/document.xml'))
    for key,target in outputs.items():
        with ZipFile(target) as z:
            assert z.testzip() is None
            assert set(src.namelist())<=set(z.namelist())
            changed=[p for p in src.namelist() if src.read(p)!=z.read(p)]
            allowed={'word/document.xml','word/_rels/document.xml.rels','[Content_Types].xml'} if key=='chapter' else {'word/document.xml','word/_rels/document.xml.rels'}
            assert set(changed)<=allowed,changed
            added=set(z.namelist())-set(src.namelist())
            assert added==({'word/media/landgrand-flow-a.png','word/media/landgrand-flow-b.png'} if key=='chapter' else set())
            package_changes[key]={'changed':changed,'added':sorted(added)}
            doc=E.fromstring(z.read('word/document.xml'))
            assert c14n(old.find('w:body/w:sectPr',NS))==c14n(doc.find('w:body/w:sectPr',NS))
            assert not doc.xpath('//w:ins | //w:del | //w:commentReference',namespaces=NS)
            ps=doc.findall('w:body/w:p',NS)
            alltexts[key]=[text(p) for p in ps if text(p).strip()]
            if key=='chapter':
                sourceps=old.findall('w:body/w:p',NS)
                assert c14n(ps[0])==c14n(sourceps[0]) and c14n(ps[1])==c14n(sourceps[1])
                headings=[]
                for i,p in enumerate(ps):
                    style=p.xpath('string(w:pPr/w:pStyle/@w:val)',namespaces=NS)
                    if style in ['Heading1','Heading2','Heading3']:
                        assert text(ps[i+1]).startswith('This section '),(text(p),text(ps[i+1]))
                        headings.append((style,text(p)))
                assert len(headings)==15
                assert [t for s,t in headings if s=='Heading1']==['Technicality of the project','Details of the technologies to be used','How the project will work']
                assert len(doc.findall('.//w:drawing',NS))==2
            else:
                assert alltexts[key][1].startswith('This section ')
                relationships=E.fromstring(z.read('word/_rels/document.xml.rels'))
                targets={x.get('Id'):x.get('Target') for x in relationships if x.get('Type')==R+'/hyperlink'}
                hrefs=[targets[h.get('{'+R+'}id')] for h in doc.findall('.//w:hyperlink',NS)]
                assert len(hrefs)==4
                for p in ps[2:]:
                    assert p.xpath('w:pPr/w:ind[@w:left="720"][@w:hanging="720"]',namespaces=NS)
                    assert p.xpath('w:pPr/w:jc[@w:val="left"]',namespaces=NS)
        audit=read(ROOT/('chapter-word-audit-2.json' if key=='chapter' else 'references-word-audit-2.json'))
        assert audit['readOnly']
        native=[normalize(p['text']) for p in audit['paragraphs'] if normalize(p['text']) not in ['/','\x01']]
        assert [normalize(t) for t in alltexts[key]]==native,(key,native)
        page_dir=ROOT/('chapter-pages-2' if key=='chapter' else 'references-pages-2')
        assert len(list(page_dir.glob('page-*.png')))==audit['pages']
        counts[key]={'pages':audit['pages'],'words':audit['words']}

chapter='\n'.join(alltexts['chapter']);references='\n'.join(alltexts['references'])
citations=set(re.findall(r'\((Celsys|Google|Microsoft|Unity Technologies), (20\d{2})\)',chapter))
entries=set(re.findall(r'^(Celsys|Google|Microsoft|Unity Technologies)\. \((20\d{2})',references,re.M))
assert citations==entries and len(entries)==4
assert all(2020<=int(y)<=2026 for _,y in entries)
assert all(x in chapter for x in ['Android 10 and above','single-player','Grade 5 learners','Baluan Elementary School','Mountains, Hills, Plains, and Plateaus','60 levels','3 Easy, 5 Normal, and 7 Hard levels','up to three gameplay stars','2 GB RAM','300 MB free space','Figure 4A','Figure 4B'])
assert not any(x in chapter for x in ['DisasterSafetyGame','75 levels','up to Android 14','was validated','proved effective','n.d.'])
with PdfReader(ROOT/'references-final-2.pdf') as pdf:
    uris={str(a.get_object().get('/A',{}).get('/URI')) for page in pdf.pages for a in page.get('/Annots',[]) if a.get_object().get('/A',{}).get('/URI')}
assert set(hrefs)<=uris
before=read(ROOT/'vault-before.json')
assert before=={str(p.relative_to(VAULT)):sha(p) for p in VAULT.rglob('*') if p.is_file()}

helper=ROOT/'read_input.py'
function=next(n for n in ast.parse((ROOT.parent/'chapter3-review-2026-11-01'/'inspect_input.py').read_text(encoding='utf-8')).body if isinstance(n,ast.FunctionDef) and n.name=='shared_read')
exec(compile(ast.Module(body=[function],type_ignores=[]),'shared-reader','exec'))
source_path=read(ROOT/'source-inventory.json')['source']
assert hashlib.sha256(shared_read(source_path)).hexdigest()==sha(source)

script=Path(r'C:\Users\user\.codex\plugins\cache\openai-primary-runtime\documents\26.1026.10807\skills\documents\scripts\render_and_diff.py')
spec=importlib.util.spec_from_file_location('chapter3_fidelity',script)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
mapping={source.resolve():ROOT/'source-pages',outputs['chapter'].resolve():ROOT/'chapter-pages-2',outputs['references'].resolve():ROOT/'references-pages-2'}
def cached_render(render_py,docx,outdir):
    Path(outdir).mkdir(parents=True,exist_ok=True)
    for p in mapping[Path(docx).resolve()].glob('page-*.png'):shutil.copy2(p,Path(outdir)/p.name)
module._run_render=cached_render
for key in ['chapter','references']:
    out=ROOT/(key+'-fidelity')
    assert not out.exists()
    sys.argv=[str(script),str(source),str(outputs[key]),'--outdir',str(out)]
    module.main()
report={'pages_and_words':counts,'total_final_pages_inspected':sum(v['pages'] for v in counts.values()),'section_introductions':15,'matched_references':sorted(entries),'reference_links_live':True,'original_G_source_unchanged':True,'vault_files_unchanged':len(before),'source_page_geometry_and_opaque_parts_preserved':True,'package_changes':package_changes,'output_hashes':{k:sha(p) for k,p in outputs.items()},'limits':['Working figure number 4 retained as 4A/4B; confirm numbering during manuscript assembly.','Scoring, exact completion/unlocks, failure/retry/pause and save policies remain open.','No Android build/device/learning-effectiveness result is established.','Canonical vault has not been synchronized with this Word pass.']}
(ROOT/'final-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
