from pathlib import Path
from zipfile import ZipFile
from copy import deepcopy
from lxml import etree
import json

root = Path(__file__).resolve().parent
outputs = json.loads((root / 'outputs.json').read_text(encoding='utf-8'))
path = Path(outputs['chapter'])
items = json.loads((root / 'chapter-v2.json').read_text(encoding='utf-8'))
updates = {
    6: "For Land Grand, lessons before each level can identify Science concepts to notice. Item illustrations, names, and descriptions can draw attention to selected rock and mineral features. Yet players may collect items without reading their descriptions. The proposed design therefore needs to connect the Science information with the collection activity (Cutting & Deterding, 2024).",
    7: "The article develops a theory from earlier research. Its predictions need direct testing, and it does not report a Grade 5 trial. It also does not explain post-play reflection (Cutting & Deterding, 2024). Land Grand's planned level reviews can revisit Science ideas, but their contribution to understanding requires separate evaluation.",
    23: "These studies support examining each activity's purpose and outcomes. In Land Grand, exploration will include item collection and descriptions. A review will follow each completed level. Obstacles, time limits, and stars are proposed gameplay features. Task-attention theory raises a design concern: players may focus on reaching items or finishing quickly while overlooking Science information (Cutting & Deterding, 2024). This possibility needs evaluation. Completed levels and collected items remain gameplay records unless a separate assessment establishes learning.",
}
with ZipFile(path) as z:
    infos = z.infolist(); parts = {x.filename: z.read(x.filename) for x in infos}
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
q = lambda key: '{' + W + '}' + key
document = etree.fromstring(parts['word/document.xml'])
ps = document.find(q('body')).findall(q('p'))
for index, value in updates.items():
    p = ps[index]
    assert ''.join(p.iter(q('t'))[0]) if False else True
    assert ''.join(t.text or '' for t in p.iter(q('t'))) == items[index]['text']
    rp = deepcopy(p.find(q('r')).find(q('rPr')))
    for child in list(p):
        if child.tag != q('pPr'): p.remove(child)
    run = etree.SubElement(p, q('r')); run.append(rp)
    t = etree.SubElement(run, q('t')); t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve'); t.text = value
    items[index]['text'] = value
parts['word/document.xml'] = etree.tostring(document, xml_declaration=True, encoding='UTF-8', standalone=True)
temporary = path.with_suffix('.revision.tmp')
with ZipFile(temporary, 'w') as z:
    for info in infos: z.writestr(info, parts[info.filename])
temporary.replace(path)
(root / 'chapter-v2.json').write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding='utf-8')
(root / 'manuscript-v2.txt').write_text('\n\n'.join(x['text'] for x in items), encoding='utf-8')
print('Tightened three authorized paragraphs to remove a two-line overflow page.')
