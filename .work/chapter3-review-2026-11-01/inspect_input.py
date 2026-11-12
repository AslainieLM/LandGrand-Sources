from pathlib import Path
import ctypes, hashlib, io, json
from ctypes import wintypes
from zipfile import ZipFile
from lxml import etree

ROOT = Path(__file__).resolve().parent
SOURCE = Path(r'G:\Other computers\My Computer (1)\Lab Activities\SUMMER\CAPSTONE-2\Aslainie\Chapter_3_Technical_Background_Land_Grand.docx')
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main', 'a':'http://schemas.openxmlformats.org/drawingml/2006/main', 'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}

def shared_read(path):
    k = ctypes.WinDLL('kernel32', use_last_error=True)
    k.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
    k.CreateFileW.restype = wintypes.HANDLE
    k.ReadFile.argtypes = [wintypes.HANDLE, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(wintypes.DWORD), ctypes.c_void_p]
    k.CloseHandle.argtypes = [wintypes.HANDLE]
    h = k.CreateFileW(str(path), 0x80000000, 7, None, 3, 0, None)
    if h == wintypes.HANDLE(-1).value: raise ctypes.WinError(ctypes.get_last_error())
    data = bytearray()
    try:
        buf, got = ctypes.create_string_buffer(1048576), wintypes.DWORD()
        while True:
            if not k.ReadFile(h, buf, len(buf), ctypes.byref(got), None): raise ctypes.WinError(ctypes.get_last_error())
            if not got.value: break
            data.extend(buf.raw[:got.value])
    finally: k.CloseHandle(h)
    return bytes(data)

raw = shared_read(SOURCE)
record = {'source':str(SOURCE), 'sha256':hashlib.sha256(raw).hexdigest(), 'bytes':len(raw)}
target = ROOT/'chapter3-reference.docx'
assert not target.exists()
target.write_bytes(raw)
with ZipFile(io.BytesIO(raw)) as z:
    assert z.testzip() is None
    doc = etree.fromstring(z.read('word/document.xml'))
    record['paragraphs'] = []
    for i,p in enumerate(doc.findall('.//w:body//w:p',NS)):
        text = ''.join(p.xpath('.//w:t/text()',namespaces=NS))
        images = p.xpath('.//a:blip/@r:embed',namespaces=NS)
        if text.strip() or images:
            record['paragraphs'].append({'index':i,'text':text,'images':images,'style':p.xpath('string(w:pPr/w:pStyle/@w:val)',namespaces=NS)})
    record['tables'] = len(doc.findall('.//w:tbl',NS))
    record['tracked_insertions'] = len(doc.findall('.//w:ins',NS))
    record['tracked_deletions'] = len(doc.findall('.//w:del',NS))
    record['comment_count'] = len(doc.findall('.//w:commentReference',NS))
    record['comments'] = []
    if 'word/comments.xml' in z.namelist():
        comments = etree.fromstring(z.read('word/comments.xml'))
        w = '{'+NS['w']+'}'
        for c in comments:
            cid=c.get(w+'id')
            anchors=doc.xpath('.//w:p[.//w:commentRangeStart[@w:id=$cid] or .//w:commentReference[@w:id=$cid]]',cid=cid,namespaces=NS)
            record['comments'].append({'id':cid,'author':c.get(w+'author'),'date':c.get(w+'date'),'text':' '.join(c.xpath('.//w:t/text()',namespaces=NS)),'anchors':[''.join(p.xpath('.//w:t/text()',namespaces=NS)) for p in anchors]})
    rels = etree.fromstring(z.read('word/_rels/document.xml.rels'))
    record['relationships'] = [dict(r.attrib) for r in rels]
    media=ROOT/'media'
    media.mkdir(exist_ok=True)
    record['media'] = []
    for name in z.namelist():
        if name.startswith('word/media/'):
            out=media/Path(name).name
            out.write_bytes(z.read(name))
            record['media'].append({'part':name,'path':str(out),'bytes':out.stat().st_size})
(ROOT/'source-review.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'chapter3-text.txt').write_text('\n\n'.join(f"[{p['index']:03}] {p['text']} {'IMAGES:'+','.join(p['images']) if p['images'] else ''}" for p in record['paragraphs']),encoding='utf-8')
vault=ROOT.parent.parent/'LandGrand'
(ROOT/'vault-before.json').write_text(json.dumps({str(p.relative_to(vault)):hashlib.sha256(p.read_bytes()).hexdigest() for p in vault.rglob('*') if p.is_file()},indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in record.items() if k not in ['paragraphs','relationships']},ensure_ascii=False,indent=2))
