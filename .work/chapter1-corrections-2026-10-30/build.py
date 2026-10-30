from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from copy import deepcopy
from datetime import datetime, timezone
from lxml import etree
import hashlib, json, re, sys

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'reference.docx'
DELIVERABLE = Path(r'D:\Projects\LandGrand-Sources\LandGrand\Manuscript\Drafts\Land Grand - Chapter I - Revised - v9.docx')
FINAL = ROOT / 'stage3.docx' if '--stage3' in sys.argv else (ROOT / 'stage2.docx' if '--stage2' in sys.argv else DELIVERABLE)
EXPECTED = '6ad898c79899c91d506b625b992959af921c53fee88167390d2151f581ada3ad'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED
assert not FINAL.exists(), 'Preserve existing outputs; choose another revision instead.'
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
PR = 'http://schemas.openxmlformats.org/package/2006/relationships'
CT = 'http://schemas.openxmlformats.org/package/2006/content-types'
NS = {'w': W}

def w(name): return '{' + W + '}' + name
def text(p):
    return ''.join((el.text or '') if el.tag == w('t') else '\n' for el in p.iter() if el.tag in [w('t'),w('br')])
def xml(root): return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
def child(root, name):
    el = root.find(w(name))
    if el is None:
        el = etree.SubElement(root, w(name))
    return el

with ZipFile(SOURCE) as z:
    original = {i.filename: z.read(i.filename) for i in z.infolist()}
    infos = z.infolist()
doc = etree.fromstring(original['word/document.xml'])
body = doc.find(w('body'))
ps = body.findall(w('p'))
assert len(ps) == 60
slots = {i+1: p for i, p in enumerate(ps)}
changes = []

def replace(p, old, new):
    full = text(p)
    assert old in full, old
    start = full.index(old)
    end = start + len(old)
    nodes = p.xpath('.//w:t', namespaces=NS)
    offset = 0
    first = True
    for node in nodes:
        value = node.text or ''
        a, b = offset, offset + len(value)
        offset = b
        if b <= start or a >= end:
            continue
        prefix = value[:max(0, start-a)]
        suffix = value[max(0, end-a):] if end < b else ''
        node.text = prefix + (new if first else '') + suffix
        node.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        first = False
    assert text(p) == full[:start] + new + full[end:]

def set_text(p, new):
    old = text(p)
    assert old
    replace(p, old, new)
    changes.append({'before': old, 'after': new})

def clone_paragraph(pattern, value):
    p = deepcopy(pattern)
    for key in list(p.attrib):
        if key.rsplit('}', 1)[-1] in ['paraId','textId']:
            del p.attrib[key]
    set_text(p, value)
    return p

# Surgical wording changes retain run and paragraph formatting.
replace(slots[10], 'Respondent selection was random sampling.', 'The researcher reported using random selection.')
set_text(slots[13], 'Survey responses identified landforms, rocks, and minerals among the Science topics considered difficult. These reports provide a basis for selecting content for the game. The final lessons and selected items will be reviewed for scientific accuracy and Grade 5 Science curriculum alignment.')
set_text(slots[14], 'The researcher observed limited rock and mineral samples for classroom demonstrations. Digital illustrations can provide additional examples when specimens are unavailable. Land Grand will combine these illustrations with names and descriptions of collected items. These examples will serve as supplementary visual material for the selected Science topics.')
set_text(slots[17], 'The project focuses on the following reported problems:')
set_text(slots[21], 'The researcher observed limited rock and mineral samples for classroom demonstrations.')
set_text(slots[40], 'This section outlines the learners, content, game activities, and technical requirements included in Land Grand.')
audience = clone_paragraph(slots[25], 'The proposed game is for Grade 5 learners at Baluan Elementary School. Development will use Unity and C#. Piskel and Clip Studio Paint will be used for graphical assets. The application will include the following features:')
slots[40].addnext(audience)
replace(slots[45], '(2d)', '(2D)')
replace(slots[51], 'Minimum targets are 2 GB RAM and 300 MB free storage.', 'Minimum targets are 2 GB RAM and 300 MB free storage. These targets still require device testing.')
plan = clone_paragraph(slots[25], 'Development will test one complete level before expanding to all 60 levels. Checks will cover content, controls, item descriptions, review, local saving, and device performance.')
slots[51].addnext(plan)
set_text(slots[54], 'The game is intended for Grade 5 learners at Baluan Elementary School. The survey includes parent and teacher responses from several grades. Overall results should not be presented as findings for Grade 5 alone.')
set_text(slots[55], 'Content will cover the four landforms and selected rocks and minerals. It will undergo scientific and curriculum review before use.')
replace(slots[56], 'websites, and an administrator panel.', 'websites, or an administrator panel.')
excluded = clone_paragraph(slots[57], 'The game will exclude separate quiz screens, GPS functions, and real-world scanning.')
slots[57].addnext(excluded)

for p in body.findall(w('p')):
    for old,new in [('would','will'),('could','can')]:
        if old == 'could' and p is slots[15]:
            continue  # Preserve the historical survey expectation, not a tested capability.
        while re.search(r'\b'+old+r'\b', text(p)):
            match = re.search(r'\b'+old+r'\b', text(p))
            replace(p, match.group(), new)

# Append the verified bibliography, using source typography rather than a new design.
heading = clone_paragraph(slots[2], 'BIBLIOGRAPHY')
hpr = child(heading, 'pPr')
child(hpr, 'pageBreakBefore')
child(hpr, 'keepNext')
child(hpr, 'keepLines')
intro = clone_paragraph(slots[5], 'This section lists the sources cited in Chapter I.')
sect = body.find(w('sectPr'))
body.insert(body.index(sect), heading)
body.insert(body.index(sect), intro)
rels = etree.fromstring(original['word/_rels/document.xml.rels'])
used_ids = {rel.get('Id') for rel in rels}

def relationship(kind, target, external=False):
    n = 1
    while 'rId'+str(n) in used_ids:
        n += 1
    rid = 'rId'+str(n)
    used_ids.add(rid)
    rel = etree.SubElement(rels, '{'+PR+'}Relationship')
    rel.set('Id', rid)
    rel.set('Type', R+'/'+kind)
    rel.set('Target', target)
    if external: rel.set('TargetMode', 'External')
    return rid

def make_run(value, italic=False, underline=False):
    run = etree.Element(w('r'))
    rpr = etree.SubElement(run, w('rPr'))
    fonts = etree.SubElement(rpr, w('rFonts'))
    for a in ['ascii','hAnsi','cs']: fonts.set(w(a),'Times New Roman')
    for tag in ['sz','szCs']: etree.SubElement(rpr,w(tag)).set(w('val'),'24')
    etree.SubElement(rpr,w('color')).set(w('val'),'000000')
    if italic: etree.SubElement(rpr,w('i'))
    if underline: etree.SubElement(rpr,w('u')).set(w('val'),'single')
    t = etree.SubElement(run,w('t'));t.set('{http://www.w3.org/XML/1998/namespace}space','preserve');t.text=value
    return run

references = [
    {'author':'Department of Education','date':'2020, July 21','title':'Suggested strategies in implementing distance learning delivery modalities (DLDM) for school year 2020-2021','detail':' (DM-CI-2020-00162). Office of the Undersecretary for Curriculum and Instruction. ','url':'https://region8.deped.gov.ph/wp-content/uploads/2020/07/DM-CI-2020-00162-2.pdf'},
    {'author':'DOST-PHIVOLCS','date':'2026, June 8','title':'Tsunami information No. 2: Cancellation of tsunami warning','detail':'. ','url':'https://tsunami.phivolcs.dost.gov.ph/Tsunami_Information/2026_Tsunami_Information/Jun/07/20260607_2337z_Advisory2_2.pdf'},
    {'author':'UNESCO','date':'2023','title':'Global education monitoring report 2023: Technology in education: A tool on whose terms?','detail':'','url':'https://www.unesco.org/gem-report/en/publication/technology'},
]
for ref in references:
    p = deepcopy(slots[3])
    for key in list(p.attrib):
        if key.rsplit('}',1)[-1] in ['paraId','textId']: del p.attrib[key]
    for el in list(p):
        if el.tag != w('pPr'): p.remove(el)
    ppr = child(p,'pPr')
    for tag in ['numPr','ind','keepNext','pageBreakBefore','jc']:
        for el in list(ppr.findall(w(tag))): ppr.remove(el)
    ind = etree.SubElement(ppr,w('ind'));ind.set(w('left'),'720');ind.set(w('hanging'),'720')
    child(ppr,'jc').set(w('val'),'left')
    spacing = child(ppr,'spacing')
    for key,val in [('before','0'),('after','120'),('line','480'),('lineRule','auto')]: spacing.set(w(key),val)
    child(ppr,'keepLines')
    p.append(make_run(ref['author']+'. ('+ref['date']+'). '))
    p.append(make_run(ref['title'],italic=True))
    if ref['detail'].strip():
        p.append(make_run(ref['detail'].rstrip()))
    line_break = etree.SubElement(p,w('r'))
    etree.SubElement(line_break,w('br'))
    link = etree.SubElement(p,w('hyperlink'))
    link.set('{'+R+'}id',relationship('hyperlink',ref['url'],external=True))
    link.append(make_run(ref['url'],underline=True))
    body.insert(body.index(sect),p)

# Local Word comments make changes and remaining dependencies reviewable.
comments = etree.Element(w('comments'),nsmap={'w':W})
comment_specs = [
    (slots[10], 'Q-09: Wording now attributes random selection to the researcher. Record the actual selection steps, eligible parent/teacher groups and separate recruitment details in the methodology; no specific random-sampling technique has been inferred.'),
    (slots[13], 'Q-04: The text now states planned scientific-accuracy and curriculum checks. Identify the exact Grade 5 competencies, selected items, authoritative content sources and reviewer before content is finalized. No completed validation is claimed.'),
    (slots[21], 'Q-12 / E-13: The researcher identified personal observation as the source on October 30, 2026. The statement is now attributed accordingly. Record the actual observation date, school setting and available/missing samples before final submission. The separate perception of city-wide scarcity is not a verified materials inventory.'),
    (slots[40], 'Separated the Scope introduction from the learner/tool details, as required by the writing guide. Restored Unity/C#, Piskel and Clip Studio Paint in the following paragraph; this is the existing proposal baseline.'),
    (slots[48], 'Q-02 / Q-03: Specify star metrics, level-completion conditions and unlock requirements before implementing these systems. The existing up-to-three-star scope is retained; thresholds have not been invented.'),
    (plan, 'Added a proposed first-level content/device check to address the 60-level production dependency. This is a planned sequence, not proof that the prototype, device tests or schedule are complete.'),
    (heading, 'Added the three verified institutional sources matching the in-text citations, with official links. Retain this list with the standalone chapter, or place the entries in the full manuscript BIBLIOGRAPHY. Apply the school\'s final citation style consistently.'),
]
for cid,(p,ctext) in enumerate(comment_specs):
    start=etree.Element(w('commentRangeStart'));start.set(w('id'),str(cid))
    p.insert(1 if p.find(w('pPr')) is not None else 0,start)
    end=etree.SubElement(p,w('commentRangeEnd'));end.set(w('id'),str(cid))
    ref_run=etree.SubElement(p,w('r'))
    cref=etree.SubElement(ref_run,w('commentReference'));cref.set(w('id'),str(cid))
    comment=etree.SubElement(comments,w('comment'))
    comment.set(w('id'),str(cid));comment.set(w('author'),'Codex')
    comment.set(w('date'),datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z'))
    cp=etree.SubElement(comment,w('p'));cr=etree.SubElement(cp,w('r'));etree.SubElement(cr,w('t')).text=ctext
relationship('comments','comments.xml')
types=etree.fromstring(original['[Content_Types].xml'])
override=etree.SubElement(types,'{'+CT+'}Override')
override.set('PartName','/word/comments.xml')
override.set('ContentType','application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml')
modified={'word/document.xml':xml(doc),'word/_rels/document.xml.rels':xml(rels),'[Content_Types].xml':xml(types),'word/comments.xml':xml(comments)}
with ZipFile(FINAL,'w',ZIP_DEFLATED) as out:
    for info in infos: out.writestr(info,modified.get(info.filename,original[info.filename]))
    out.writestr('word/comments.xml',modified['word/comments.xml'])

records=[{'paragraph':i+1,'text':text(p),'num_id':p.find('w:pPr/w:numPr/w:numId',NS).get(w('val')) if p.find('w:pPr/w:numPr/w:numId',NS) is not None else None} for i,p in enumerate(body.findall(w('p')))]
(ROOT/'final-content.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'comments.json').write_text(json.dumps([{'id':i,'anchor':text(p),'text':ctext} for i,(p,ctext) in enumerate(comment_specs)],ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'references.json').write_text(json.dumps(references,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'build-audit.json').write_text(json.dumps({'source_sha256':EXPECTED,'output':str(FINAL),'paragraphs':len(records),'comments':len(comment_specs),'references':len(references),'editable_package_parts':list(modified),'section_sha256':hashlib.sha256(etree.tostring(sect)).hexdigest(),'word_count':sum(len(re.findall(r"\b[\w]+(?:[-'][\w]+)*\b",p['text'])) for p in records)},indent=2),encoding='utf-8')
print(json.dumps({'output':str(FINAL),'paragraphs':len(records),'comments':len(comment_specs),'bibliography_entries':len(references)}))
