from pathlib import Path
from zipfile import ZipFile
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W = '{' + NS['w'] + '}'

def text_of(node):
    out = []
    for item in node.iter():
        if item.tag == W + 't':
            out.append(item.text or '')
        elif item.tag == W + 'tab':
            out.append('\t')
        elif item.tag in {W + 'br', W + 'cr'}:
            out.append('\n')
    return ''.join(out)

with ZipFile(ROOT / 'source.docx') as archive:
    assert archive.testzip() is None
    document = ET.fromstring(archive.read('word/document.xml'))
    body = document.find('w:body', NS)
    blocks = []
    paragraphs = tables = 0
    for node in body:
        if node.tag == W + 'p':
            paragraphs += 1
            blocks.append({'kind': 'paragraph', 'number': paragraphs, 'text': text_of(node)})
        elif node.tag == W + 'tbl':
            tables += 1
            rows = []
            for row in node.findall('w:tr', NS):
                rows.append(['\n'.join(text_of(p) for p in cell.findall('w:p', NS)) for cell in row.findall('w:tc', NS)])
            blocks.append({'kind': 'table', 'number': tables, 'rows': rows})
        else:
            blocks.append({'kind': node.tag.split('}')[-1], 'text': text_of(node)})
    media = []
    for name in archive.namelist():
        if name.startswith('word/media/'):
            dest = ROOT / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(archive.read(name))
            media.append({'name': name, 'bytes': dest.stat().st_size})
    ancillary = {}
    for name in archive.namelist():
        if name.startswith(('word/header', 'word/footer', 'word/footnotes', 'word/endnotes', 'word/comments')) and name.endswith('.xml'):
            ancillary[name] = text_of(ET.fromstring(archive.read(name)))
    revisions = {tag: len(document.findall('.//w:' + tag, NS)) for tag in ['ins', 'del', 'drawing', 'pict', 'txbxContent']}
    report = {'blocks': blocks, 'media': media, 'ancillary': ancillary, 'revisions': revisions,
              'app_properties': archive.read('docProps/app.xml').decode() if 'docProps/app.xml' in archive.namelist() else None}
    (ROOT / 'inspection.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
