from pathlib import Path
from zipfile import ZipFile
from lxml import etree
import json

root = Path(__file__).resolve().parent
outputs = json.loads((root / 'outputs.json').read_text(encoding='utf-8'))
path = Path(outputs['chapter'])
items = json.loads((root / 'chapter-v2.json').read_text(encoding='utf-8'))
value = "The review informs Land Grand's explanations, activities, and visual examples. The proposed anchor theory guides the examination of Science content used during gameplay. Achievement tests, learner descriptions, engagement reports, and product features provide different evidence. Findings from other applications cannot establish Land Grand's effectiveness."
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
q = lambda key: '{' + W + '}' + key
with ZipFile(path) as z:
    infos = z.infolist(); parts = {x.filename: z.read(x.filename) for x in infos}
document = etree.fromstring(parts['word/document.xml'])
p = document.find(q('body')).findall(q('p'))[38]
assert ''.join(t.text or '' for t in p.iter(q('t'))) == items[38]['text']
ts = list(p.iter(q('t'))); assert len(ts) == 1
ts[0].text = value; items[38]['text'] = value
parts['word/document.xml'] = etree.tostring(document, xml_declaration=True, encoding='UTF-8', standalone=True)
temp = path.with_suffix('.revision.tmp')
with ZipFile(temp, 'w') as z:
    for info in infos: z.writestr(info, parts[info.filename])
temp.replace(path)
(root / 'chapter-v2.json').write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding='utf-8')
(root / 'manuscript-v2.txt').write_text('\n\n'.join(x['text'] for x in items), encoding='utf-8')
print('Removed repeated synthesis wording; all qualifications retained.')
