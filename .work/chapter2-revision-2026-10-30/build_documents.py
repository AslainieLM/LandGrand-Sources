from pathlib import Path
from zipfile import ZipFile
from copy import deepcopy
from lxml import etree
import hashlib, json, re

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parents[1] / 'Deliverables' / 'Chapter II Revision 2026-10-30'
OUT.mkdir(parents=True, exist_ok=True)
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
REL = 'http://schemas.openxmlformats.org/package/2006/relationships'
NS = {'w': W, 'r': R}
q = lambda s: '{'+W+'}'+s
source = ROOT / 'chapter1-reference.docx'
assert hashlib.sha256(source.read_bytes()).hexdigest() == '6ad898c79899c91d506b625b992959af921c53fee88167390d2151f581ada3ad'
chapter = json.loads((ROOT/'chapter.json').read_text(encoding='utf-8'))
refs = json.loads((ROOT/'references.json').read_text(encoding='utf-8'))
for ref in refs:
    if ref['id'] == 'dong': ref['issue'] = '1'
(ROOT/'references.json').write_text(json.dumps(refs,ensure_ascii=False,indent=2),encoding='utf-8')

with ZipFile(source) as z:
    parts = {n: z.read(n) for n in z.namelist()}
base = etree.fromstring(parts['word/document.xml'])
base_body = base.find(q('body'))
patterns = base_body.findall(q('p'))
styles = etree.fromstring(parts['word/styles.xml'])
style_ids = {el.get(q('styleId')) for el in styles.findall(q('style'))}

def prop(parent, name, val=None):
    el = parent.find(q(name))
    if el is None: el = etree.SubElement(parent,q(name))
    if val is not None: el.set(q('val'),str(val))
    return el

def paragraph(role, text=''):
    idx = {'chapter':0,'title':1,'opening':2,'heading':3,'subheading':3,'intro':4,'body':5,'reference':5}[role]
    p = deepcopy(patterns[idx])
    p.attrib.clear()
    for el in list(p):
        if el.tag != q('pPr'): p.remove(el)
    pp = p.find(q('pPr'))
    # Use genuine heading semantics without inheriting a new visual preset.
    if role in ['title','heading','subheading']:
        style = {'title':'Title','heading':'Heading1','subheading':'Heading2'}[role]
        if style in style_ids:
            ps = etree.Element(q('pStyle')); ps.set(q('val'),style);pp.insert(0,ps)
        prop(pp,'outlineLvl',{'title':0,'heading':1,'subheading':2}[role])
        prop(pp,'keepNext');prop(pp,'keepLines')
    prop(pp,'widowControl')
    if role == 'chapter': prop(pp,'keepNext')
    if role in ['chapter','title']:
        spacing=prop(pp,'spacing');spacing.set(q('before'),'0');spacing.set(q('after'),'0')
    if role in ['heading','subheading']:
        prop(pp,'jc','left')
    if role == 'reference':
        prop(pp,'jc','left')
        ind = prop(pp,'ind');ind.attrib.clear();ind.set(q('left'),'720');ind.set(q('hanging'),'720')
        sp=prop(pp,'spacing');sp.set(q('before'),'0');sp.set(q('after'),'160')
        prop(pp,'keepLines')
    if text: add_run(p,text,role)
    return p

def run_properties(role, italic=False):
    rp=etree.Element(q('rPr'))
    f=etree.SubElement(rp,q('rFonts'))
    name='Cambria' if role in ['chapter','title'] else 'Times New Roman'
    for a in ['ascii','hAnsi','cs']:f.set(q(a),name)
    if role in ['chapter','title']:prop(rp,'b');prop(rp,'bCs')
    else:prop(rp,'b','0');prop(rp,'bCs','0')
    if italic:prop(rp,'i');prop(rp,'iCs')
    prop(rp,'color','000000');prop(rp,'sz',28 if role in ['chapter','title'] else 24)
    prop(rp,'szCs',28 if role in ['chapter','title'] else 24)
    prop(rp,'lang','en-PH')
    return rp

def add_run(p,text,role='body',italic=False):
    r=etree.SubElement(p,q('r'));r.append(run_properties(role,italic))
    t=etree.SubElement(r,q('t'));t.set('{http://www.w3.org/XML/1998/namespace}space','preserve');t.text=text
    return r

def xml_bytes(el):
    return etree.tostring(el,xml_declaration=True,encoding='UTF-8',standalone=True)

def new_document():
    root=deepcopy(base);body=root.find(q('body'))
    sect=deepcopy(body.find(q('sectPr')))
    for el in list(body):body.remove(el)
    return root,body,sect

def save(root,body,sect,path,newrels=None):
    body.append(sect)
    modified=dict(parts)
    modified['word/document.xml']=xml_bytes(root)
    if newrels is not None:modified['word/_rels/document.xml.rels']=xml_bytes(newrels)
    with ZipFile(path,'w') as zout:
        with ZipFile(source) as zin:
            for info in zin.infolist():zout.writestr(info,modified[info.filename])
    return {n:hashlib.sha256(b).hexdigest() for n,b in modified.items()}

root,body,sect=new_document()
for item in chapter: body.append(paragraph(item['role'],item['text']))
chapter_path=OUT/'Land Grand - Chapter II - Revised - v1.docx'
chapter_inventory=save(root,body,sect,chapter_path)

root,body,sect=new_document()
body.append(paragraph('title','BIBLIOGRAPHY'))
body.append(paragraph('intro','This section lists the sources cited in Chapter II.'))
rels=etree.fromstring(parts['word/_rels/document.xml.rels'])
used={x.get('Id') for x in rels}
for i,ref in enumerate(refs,1):
    p=paragraph('reference')
    add_run(p,ref['author']+' ('+ref['year']+'). ')
    if 'journal' in ref:
        add_run(p,ref['title']+'. ')
        add_run(p,ref['journal']+', '+ref['volume'],italic=True)
        if ref.get('issue'):add_run(p,'('+ref['issue']+')')
        if ref.get('pages'):add_run(p,', '+ref['pages']+'. ')
        elif ref.get('article'):add_run(p,', Article '+ref['article']+'. ')
        else:add_run(p,'. ')
    else:
        add_run(p,ref['title'],italic=True)
        add_run(p,' ['+ref['type']+']. '+ref['publisher']+'. ')
    rid=f'rIdLandGrandSource{i}'
    assert rid not in used
    rel=etree.SubElement(rels,'{'+REL+'}Relationship')
    rel.set('Id',rid);rel.set('Type',R+'/hyperlink');rel.set('Target',ref['url']);rel.set('TargetMode','External')
    link=etree.SubElement(p,q('hyperlink'));link.set('{'+R+'}id',rid)
    add_run(link,ref['url'])
    body.append(p)
refs_path=OUT/'Land Grand - Chapter II - APA References.docx'
refs_inventory=save(root,body,sect,refs_path,rels)

inventory={'reference':{n:hashlib.sha256(b).hexdigest() for n,b in parts.items()},
           'chapter':chapter_inventory,'references':refs_inventory,
           'outputs':[str(chapter_path),str(refs_path)]}
(ROOT/'package-inventories.json').write_text(json.dumps(inventory,indent=2),encoding='utf-8')
# A plain-text companion of the prose is internal QA, not a vault update.
(ROOT/'manuscript.txt').write_text('\n\n'.join(x['text'] for x in chapter),encoding='utf-8')
print(json.dumps({'outputs':inventory['outputs'],'chapter_paragraphs':len(chapter),'chapter_words':len(re.findall(r'\b[\w’]+\b',' '.join(x['text'] for x in chapter))),'references':len(refs)},indent=2))
