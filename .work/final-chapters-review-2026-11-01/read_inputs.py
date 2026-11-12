from pathlib import Path
from zipfile import ZipFile
from lxml import etree
import json, hashlib, ctypes

ROOT = Path(__file__).resolve().parent
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NS = {'w': W}
files = {
    'chapter1': Path(r'G:\Other computers\My Computer (1)\Lab Activities\SUMMER\CAPSTONE-2\Aslainie\Land Grand - Chapter I FINAL.docx'),
    'chapter2': Path(r'G:\Other computers\My Computer (1)\Lab Activities\SUMMER\CAPSTONE-2\Aslainie\CHAPTER 2 - FINAL.docx')
}

def read_shared(path):
    from ctypes import wintypes
    k = ctypes.WinDLL('kernel32', use_last_error=True)
    k.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
    k.CreateFileW.restype = wintypes.HANDLE
    k.ReadFile.argtypes = [wintypes.HANDLE, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(wintypes.DWORD), ctypes.c_void_p]
    k.CloseHandle.argtypes = [wintypes.HANDLE]
    handle = k.CreateFileW(str(path), 0x80000000, 7, None, 3, 0, None)
    if handle == wintypes.HANDLE(-1).value: raise ctypes.WinError(ctypes.get_last_error())
    data = bytearray()
    try:
        buf = ctypes.create_string_buffer(1048576)
        got = wintypes.DWORD()
        while True:
            if not k.ReadFile(handle, buf, len(buf), ctypes.byref(got), None): raise ctypes.WinError(ctypes.get_last_error())
            if not got.value: break
            data.extend(buf.raw[:got.value])
    finally: k.CloseHandle(handle)
    return bytes(data)

manifest = {}
for name, source in files.items():
    raw = read_shared(source)
    target = ROOT / (name + '.docx')
    assert not target.exists()
    target.write_bytes(raw)
    record = {'source': str(source), 'copy': str(target), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}
    with ZipFile(target) as z:
        assert z.testzip() is None
        document = etree.fromstring(z.read('word/document.xml'))
        ps = []
        for index, p in enumerate(document.findall('.//w:body//w:p', NS)):
            text = ''.join(p.xpath('.//w:t/text() | .//w:tab/text()', namespaces=NS))
            if not text.strip(): continue
            ps.append({'xml_index': index, 'text': text,
                       'style': p.xpath('string(w:pPr/w:pStyle/@w:val)', namespaces=NS),
                       'numbering': p.xpath('string(w:pPr/w:numPr/w:numId/@w:val)', namespaces=NS)})
        record['paragraphs'] = ps
        record['footnote_markers'] = len(document.findall('.//w:footnoteReference', NS))
        record['endnote_markers'] = len(document.findall('.//w:endnoteReference', NS))
        record['tracked_insertions'] = len(document.findall('.//w:ins', NS))
        record['tracked_deletions'] = len(document.findall('.//w:del', NS))
        record['tables'] = len(document.findall('.//w:tbl', NS))
        record['drawings'] = len(document.findall('.//w:drawing', NS))
        record['comment_markers'] = len(document.findall('.//w:commentReference', NS))
        record['extra_parts'] = {}
        for part in z.namelist():
            if part in ['word/footnotes.xml', 'word/endnotes.xml', 'word/comments.xml'] or part.startswith(('word/header', 'word/footer')) and part.endswith('.xml'):
                x = etree.fromstring(z.read(part))
                record['extra_parts'][part] = [''.join(p.xpath('.//w:t/text()', namespaces=NS)) for p in x.findall('.//w:p', NS)]
        rels = etree.fromstring(z.read('word/_rels/document.xml.rels'))
        record['external_links'] = [dict(x.attrib) for x in rels if x.get('TargetMode') == 'External']
        record['section_properties'] = [etree.tostring(x, encoding='unicode') for x in document.findall('.//w:sectPr', NS)]
    (ROOT / (name + '-extract.json')).write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    (ROOT / (name + '.txt')).write_text('\n\n'.join(f"[{p['xml_index']:03d}] {p['text']}" for p in ps), encoding='utf-8')
    manifest[name] = {k: record[k] for k in ['source', 'copy', 'sha256', 'bytes', 'footnote_markers', 'endnote_markers', 'tracked_insertions', 'tracked_deletions', 'tables', 'drawings', 'comment_markers']}
    manifest[name]['nonempty_paragraphs'] = len(ps)
(ROOT / 'input-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(manifest, ensure_ascii=False, indent=2))
