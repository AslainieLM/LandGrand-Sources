from pathlib import Path
from zipfile import ZipFile
from copy import deepcopy
from lxml import etree
import hashlib, json, re, unicodedata

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / 'chapter2-revision-2026-10-30'
SOURCE_DIR = ROOT.parents[1] / 'Deliverables' / 'Chapter II Revision 2026-10-30'
OUT = ROOT.parents[1] / 'Deliverables' / 'Chapter II Revision 2026-11-01'
VAULT = ROOT.parents[1] / 'LandGrand'
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NS = {'w': W, 'r': R}
q = lambda key: '{' + W + '}' + key

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def inventory(folder):
    return {str(p.relative_to(folder)): digest(p) for p in sorted(folder.rglob('*')) if p.is_file()}
def save_json(name, data):
    (ROOT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
def text(p): return ''.join(p.itertext()) if False else ''.join(p.xpath('.//w:t/text()', namespaces=NS))
def parts(path):
    with ZipFile(path) as z: return {n: z.read(n) for n in z.namelist()}
def serialize(root): return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
def write_package(source, target, replacements):
    with ZipFile(source) as zin, ZipFile(target, 'w') as zout:
        for item in zin.infolist(): zout.writestr(item, replacements.get(item.filename, zin.read(item.filename)))

chapter_src = SOURCE_DIR / 'Land Grand - Chapter II - Revised - v1.docx'
refs_src = SOURCE_DIR / 'Land Grand - Chapter II - APA References.docx'
assert digest(chapter_src) == 'd5fb25946966ade11d71e9153fc0fbee8f2431d635f2bd773370082f06ef6b2d'
assert digest(refs_src) == '83c1079b5832bc75c1e50567016c75ab3bb391ab28bf5eedc67f86ace2b176dc'
assert not OUT.exists(), 'Never overwrite an existing revision folder.'
save_json('protected-before.json', {'v1': inventory(SOURCE_DIR), 'vault': inventory(VAULT)})
OUT.mkdir(parents=True)

replacements = {
    4: "This section presents the proposed theoretical foundation and supporting literature for Land Grand. It begins with task-attention theory, then discusses learning through activities, mobile resources, and visual examples in Science education.",
    5: "The project proposes the Task-Attention Theory of Game Learning as its anchor theory. Cutting and Deterding (2024) explain that game tasks guide which information players notice and use. Attentional selection concerns what players focus on or ignore. Active sampling involves actions that make information available. Mechanics, goals, rewards, and uncertainty can guide these processes. Perceptual demands, mental effort, and pressure also affect attention. The authors treat attention as a factor that influences learning, rather than a complete explanation of learning.",
    6: "For Land Grand, this perspective suggests connecting Science content with the player's activities. The lesson before each level can identify the concept to notice. During collection, illustrations, names, and descriptions can direct attention to selected features of rocks and minerals. However, a player may reach an item without reading its description. Collection alone therefore does not establish that the Science content is part of the task. The proposed design needs to address this connection (Cutting & Deterding, 2024).",
    12: "These perspectives address different parts of the proposed resource. Task-attention theory guides the examination of what learners notice and use during gameplay. Situated cognition draws attention to the relationship between content and activity. Mobile learning research provides broader evidence about delivery. Their relevance must be examined through the game's actual lessons and activities. The following studies develop these connections in the order of the specific objectives.",
    22: "These studies support examining the purpose of each activity and how its outcomes are checked. In Land Grand, exploration will include collecting items and access to their descriptions. A review will follow each completed level. Obstacles, time limits, and stars are proposed gameplay features. Applying task-attention theory raises a design concern: players may focus on reaching items or finishing quickly while overlooking Science information (Cutting & Deterding, 2024). This possibility needs evaluation. Completed levels and collected items will remain gameplay records unless a separate assessment establishes learning.",
    37: "The review supports examining an educational game that connects explanation, activity, and visual examples. The proposed anchor theory focuses this examination on whether game tasks draw attention to the intended Science content. The type of evidence also matters. Achievement tests, learner descriptions, self-reported engagement, and product features answer different questions. Positive findings from other applications cannot establish the effectiveness of Land Grand. The four objectives provide a focused basis for selecting and reviewing its lessons and activities.",
}
extra = "The theory provides a basis for reviewing the proposed activities, but its predictions still require direct testing. The article develops a theory from earlier research; it does not report a trial with Grade 5 learners. It also does not explain post-play reflection (Cutting & Deterding, 2024). Land Grand's planned review after each level can revisit the Science ideas encountered during play. Its contribution to understanding requires separate evaluation."

chapter = json.loads((BASE / 'chapter.json').read_text(encoding='utf-8'))
source_parts = parts(chapter_src)
document = etree.fromstring(source_parts['word/document.xml'])
body = document.find(q('body'))
paragraphs = body.findall(q('p'))
assert [text(p) for p in paragraphs] == [item['text'] for item in chapter]

def replace_paragraph(p, value):
    run_template = deepcopy(p.find(q('r')))
    rp = deepcopy(run_template.find(q('rPr')))
    for child in list(p):
        if child.tag != q('pPr'): p.remove(child)
    run = etree.SubElement(p, q('r'))
    if rp is not None: run.append(rp)
    t = etree.SubElement(run, q('t')); t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve'); t.text = value

for index, value in replacements.items():
    replace_paragraph(paragraphs[index], value)
    chapter[index]['text'] = value
newp = deepcopy(paragraphs[6]); replace_paragraph(newp, extra)
body.insert(body.index(paragraphs[6]) + 1, newp)
chapter.insert(7, {'role': 'body', 'text': extra})
chapter_path = OUT / 'Land Grand - Chapter II - Revised - v2.docx'
write_package(chapter_src, chapter_path, {'word/document.xml': serialize(document)})

refs = json.loads((BASE / 'references.json').read_text(encoding='utf-8'))
cutting = {
    'id': 'cutting', 'author': 'Cutting, J., & Deterding, S.', 'year': '2024',
    'title': 'The task-attention theory of game learning: A theory and research agenda',
    'journal': 'Human–Computer Interaction', 'volume': '39', 'issue': '5–6',
    'pages': '257–287', 'url': 'https://doi.org/10.1080/07370024.2022.2047971'
}
ref_parts = parts(refs_src)
ref_document = etree.fromstring(ref_parts['word/document.xml'])
ref_body = ref_document.find(q('body'))
ref_ps = ref_body.findall(q('p'))
assert len(ref_ps) == 17 and len(refs) == 15
mayer_index = next(i for i, entry in enumerate(refs) if entry['id'] == 'mayer')
mayer_p = ref_ps[mayer_index + 2]
assert text(mayer_p).startswith('Mayer, R. E. (2024).')
link_template = deepcopy(mayer_p.find(q('hyperlink')))
rid = link_template.get('{' + R + '}id')
rel_document = etree.fromstring(ref_parts['word/_rels/document.xml.rels'])
rel_node = next(x for x in rel_document if x.get('Id') == rid)
assert rel_node.get('Target') == 'https://doi.org/10.1007/s10648-023-09842-1'
rel_node.set('Target', cutting['url'])
base_rp = deepcopy(mayer_p.find(q('r')).find(q('rPr')))
new_ref_p = deepcopy(mayer_p)
for child in list(new_ref_p):
    if child.tag != q('pPr'): new_ref_p.remove(child)
def add_run(parent, value, italic=False):
    run = etree.SubElement(parent, q('r')); rp = deepcopy(base_rp)
    for name in ('i', 'iCs'):
        old = rp.find(q(name))
        if old is not None: rp.remove(old)
        if italic: etree.SubElement(rp, q(name))
    run.append(rp)
    t = etree.SubElement(run, q('t')); t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve'); t.text = value
add_run(new_ref_p, cutting['author'] + ' (2024). ')
add_run(new_ref_p, cutting['title'] + '. ')
add_run(new_ref_p, cutting['journal'] + ', 39', True)
add_run(new_ref_p, '(5–6), 257–287. ')
for child in list(link_template): link_template.remove(child)
add_run(link_template, cutting['url']); new_ref_p.append(link_template)
ref_body.remove(mayer_p)
refs.pop(mayer_index)
new_index = next(i for i, entry in enumerate(refs) if entry['id'] == 'dong')
ref_body.insert(new_index + 2, new_ref_p)
refs.insert(new_index, cutting)
refs_path = OUT / 'Land Grand - Chapter II - APA References - v2.docx'
write_package(refs_src, refs_path, {'word/document.xml': serialize(ref_document), 'word/_rels/document.xml.rels': serialize(rel_document)})

save_json('chapter-v2.json', chapter)
save_json('references-v2.json', refs)
save_json('revision-slots.json', {'replaced_original_indices': sorted(replacements), 'insert_after_original_index': 6,
                               'bibliography_removed': 'mayer', 'bibliography_added': cutting})
save_json('outputs.json', {'chapter': str(chapter_path), 'references': str(refs_path), 'directory': str(OUT)})
(ROOT / 'manuscript-v2.txt').write_text('\n\n'.join(item['text'] for item in chapter), encoding='utf-8')
print(json.dumps({'chapter': str(chapter_path), 'references': str(refs_path), 'paragraphs': len(chapter),
                  'before_words': len(re.findall(r'\b[\w’]+\b', ' '.join(item['text'] for item in json.loads((BASE / 'chapter.json').read_text(encoding='utf-8'))))),
                  'after_words': len(re.findall(r'\b[\w’]+\b', ' '.join(item['text'] for item in chapter)))}, indent=2))
