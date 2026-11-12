from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from ctypes import wintypes
import ast,ctypes,hashlib,json
ROOT=Path(__file__).resolve().parent
VAULT=ROOT.parent.parent/'LandGrand'
helper=ROOT.parent/'chapter3-review-2026-11-01'/'inspect_input.py'
fn=next(n for n in ast.parse(helper.read_text(encoding='utf-8')).body if isinstance(n,ast.FunctionDef) and n.name=='shared_read')
exec(compile(ast.Module(body=[fn],type_ignores=[]),'shared-reader','exec'))
source=Path(r'G:\Other computers\My Computer (1)\Lab Activities\SUMMER\CAPSTONE-2\Aslainie\Chapter_3_Technical_Background_Land_Grand - Need to be revised.docx')
raw=shared_read(source)
copy=ROOT/'chapter3-source.docx'
assert not copy.exists()
copy.write_bytes(raw)
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
record={'source':str(source),'copy':str(copy),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
with ZipFile(copy) as z:
    assert z.testzip() is None
    x=etree.fromstring(z.read('word/document.xml'))
    record['paragraphs']=[{'index':i,'text':''.join(p.xpath('.//w:t/text()',namespaces=ns)),'style':p.xpath('string(w:pPr/w:pStyle/@w:val)',namespaces=ns),'pPr':etree.tostring(p.find('w:pPr',ns),encoding='unicode') if p.find('w:pPr',ns) is not None else None} for i,p in enumerate(x.findall('.//w:body//w:p',ns))]
    record['section_properties']=[etree.tostring(s,encoding='unicode') for s in x.findall('.//w:sectPr',ns)]
    record['package_parts']={p:{'bytes':len(z.read(p)),'sha256':hashlib.sha256(z.read(p)).hexdigest()} for p in z.namelist()}
    record['comments'] = ''.join(etree.fromstring(z.read('word/comments.xml')).xpath('.//w:t/text()',namespaces=ns)) if 'word/comments.xml' in z.namelist() else ''
    record['tables']=len(x.findall('.//w:tbl',ns))
    record['drawings']=len(x.findall('.//w:drawing',ns))
    record['tracked_changes']=len(x.findall('.//w:ins',ns))+len(x.findall('.//w:del',ns))
    for p in z.namelist():
        if p.startswith('word/media/'):
            media=ROOT/'media'/Path(p).name
            media.parent.mkdir(exist_ok=True)
            media.write_bytes(z.read(p))
(ROOT/'source-inventory.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'source-text.txt').write_text('\n\n'.join(f"[{p['index']:03}] {p['text']}" for p in record['paragraphs'] if p['text'].strip()),encoding='utf-8')
(ROOT/'vault-before.json').write_text(json.dumps({str(p.relative_to(VAULT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in VAULT.rglob('*') if p.is_file()},indent=2),encoding='utf-8')
print(json.dumps({k:record[k] for k in ['source','sha256','bytes','comments','tables','drawings','tracked_changes','section_properties']},indent=2))
