from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from copy import deepcopy
import hashlib,json,re

ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parent.parent
VAULT=WORKSPACE/'LandGrand'
OUT=WORKSPACE/'Deliverables'/'Chapter III Revision 2026-11-01'
if OUT.exists():
    existing={p.name for p in OUT.iterdir()}
    expected={'Land Grand - Chapter III - Revised - v1.docx','Land Grand - Chapter III - References.docx'}
    assert not existing or ((ROOT/'outputs.json').exists() and existing<=expected),'Preserve unrelated deliverables.'
else:OUT.mkdir(parents=True)
SOURCE=ROOT/'chapter3-source.docx'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()=='a4862da1fe16500cf708186be199e0833f43b21cb82caaaf762f67029cd94d4b'
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
REL='http://schemas.openxmlformats.org/package/2006/relationships'
WP='http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
A='http://schemas.openxmlformats.org/drawingml/2006/main'
PIC='http://schemas.openxmlformats.org/drawingml/2006/picture'
NS={'w':W,'r':R,'wp':WP,'a':A,'pic':PIC}
q=lambda s:'{'+W+'}'+s
xml=lambda x:E.tostring(x,xml_declaration=True,encoding='UTF-8',standalone=True)
with ZipFile(SOURCE) as z: package={p:z.read(p) for p in z.namelist()}
document=E.fromstring(package['word/document.xml'])
source_body=document.find('w:body',NS)
ps=source_body.findall('w:p',NS)
section=deepcopy(source_body.find('w:sectPr',NS))

def setprop(parent,name,**attrs):
    el=parent.find(q(name))
    if el is None:el=E.SubElement(parent,q(name))
    for key,value in attrs.items():el.set(q(key),str(value))
    return el

def paragraph(text,role='body',level=None,page_before=False):
    sample={'body':2,'heading':3 if level==1 else 5 if level==2 else 26,'bullet':16,'caption':42,'title':0}[role]
    p=deepcopy(ps[sample])
    for key in list(p.attrib):
        if E.QName(key).localname in ['paraId','textId']:del p.attrib[key]
    rp=p.find('w:r/w:rPr',NS)
    rp=deepcopy(rp) if rp is not None else E.Element(q('rPr'))
    for child in list(p):
        if child.tag!=q('pPr'):p.remove(child)
    pp=p.find('w:pPr',NS)
    if pp is None:pp=E.SubElement(p,q('pPr'))
    setprop(pp,'widowControl',val=1)
    if role=='heading':
        setprop(pp,'pStyle',val='Heading'+str(level))
        setprop(pp,'keepNext',val=1)
        setprop(pp,'keepLines',val=1)
        setprop(pp,'ind',left=0,firstLine=0)
        setprop(rp,'color',val='000000')
        setprop(rp,'sz',val=24);setprop(rp,'szCs',val=24)
        setprop(rp,'i',val=0);setprop(rp,'b',val=0)
    if role=='caption':
        setprop(pp,'ind',firstLine=0,left=0)
        setprop(pp,'spacing',before=80,after=160,line=240,lineRule='auto')
        setprop(pp,'keepLines',val=1)
        setprop(pp,'keepNext',val=0)
        setprop(rp,'sz',val=22);setprop(rp,'szCs',val=22)
        setprop(rp,'color',val='000000')
    if role=='title':setprop(pp,'keepNext',val=1)
    if page_before:setprop(pp,'pageBreakBefore',val=1)
    run=E.SubElement(p,q('r'));run.append(rp)
    t=E.SubElement(run,q('t'));t.set('{http://www.w3.org/XML/1998/namespace}space','preserve');t.text=text
    return p

def image_paragraph(part,relid,width_in):
    drawing=deepcopy(document.find('.//w:drawing',NS))
    inline=drawing.find('wp:inline',NS)
    if inline is None:
        anchor=drawing.find('wp:anchor',NS)
        assert anchor is not None
        inline=E.Element('{'+WP+'}inline',distT='0',distB='0',distL='0',distR='0')
        for child in anchor:
            if E.QName(child).localname in ['extent','effectExtent','docPr','cNvGraphicFramePr','graphic']:inline.append(deepcopy(child))
        drawing.replace(anchor,inline)
    sizes=json.loads((ROOT/'figure-sizes.json').read_text())
    size=next(x for x in sizes if x['id']==part)
    cx=round(width_in*914400);cy=round(cx*size['height']/size['width'])
    for el in drawing.findall('.//wp:extent',NS)+drawing.findall('.//a:xfrm/a:ext',NS):
        el.set('cx',str(cx));el.set('cy',str(cy))
    drawing.find('.//a:blip',NS).set('{'+R+'}embed',relid)
    dp=drawing.find('.//wp:docPr',NS)
    dp.set('id','101' if part=='a' else '102');dp.set('name','Land Grand proposed flow '+part.upper())
    dp.set('descr','Proposed menu and local progress loading flow.' if part=='a' else 'Proposed lesson, exploration, item information, results, replay and episode progression flow with abstract completion conditions.')
    picid=drawing.find('.//pic:cNvPr',NS)
    picid.set('id',dp.get('id'));picid.set('name',dp.get('name'))
    p=paragraph('','caption')
    for child in list(p):
        if child.tag!=q('pPr'):p.remove(child)
    pp=p.find('w:pPr',NS)
    setprop(pp,'keepNext',val=1)
    setprop(pp,'spacing',before=0,after=0,line=240,lineRule='auto')
    E.SubElement(p,q('r')).append(drawing)
    return p

text=(VAULT/'Manuscript'/'Drafts'/'Chapter III Technical Background.md').read_text(encoding='utf-8').split('---',2)[2].strip()
text=re.sub(r'^# Chapter III Technical Background\s*','',text)
text=re.sub(r'```mermaid[\s\S]*?```\s*\n\*Proposed Gameplay and Local Progress Flow of Land Grand\*\s*','',text)
text=text.replace('The following figure presents the proposed gameplay flow. Solid arrows show the main screen and activity paths. Dashed arrows show the relationship between gameplay and local progress data.\n\n','')
text=text.replace('a two-dimensional environment with touch controls.','a two-dimensional (2D) environment with touch controls.',1)
text=text.replace('16 GB RAM, 2400 MHz','16 GB random-access memory (RAM), 2400 MHz')
text=text.replace('256 GB SSD','256 GB solid-state drive (SSD)')
text=text.replace("Unity's Android documentation identifies Android Build Support, the Android Software Development Kit, the Native Development Kit, and a Java Development Kit as build dependencies.","Unity's Android documentation identifies Android Build Support and the Android Software Development Kit (SDK) as build dependencies. It also lists the Native Development Kit (NDK) and a Java Development Kit (JDK).")
text=text.replace('An Android Package, or APK, contains application components needed for installation and use on Android devices (Google, 2025).','An Android Package (APK) contains the components needed to install and run an application on Android devices (Google, 2025).')
text=text.replace("The developer and researcher will prepare the application, organize its learning materials, and carry out the planned technical checks.","The researcher, acting as the developer, will prepare the application and organize its learning materials. The researcher will also carry out the planned technical checks.")
flow_replacements={
 'The Landform Map will contain four episodes covering Mountains, Hills, Plains, and Plateaus. Only unlocked episodes will be available for selection. Each episode will have 3 Easy, 5 Normal, and 7 Hard levels, for a planned total of 60 levels. Progression will move from Easy to Normal and then Hard as the required content is completed.': 'The Landform Map will show Mountains, Hills, Plains, and Plateaus. Learners can select unlocked episodes and available levels. Each episode will have 3 Easy, 5 Normal, and 7 Hard levels. The planned total is 60 levels. Normal will follow Easy, and Hard will follow Normal.',
 'A short lesson will appear before each level. It will introduce the selected landform and related rock or mineral content. The learner will then control an explorer character through the two-dimensional environment. Movement, jumping, and item collection will form the main actions. Challenges will include obstacles, traps, pitfalls, and time limits.': 'Each level will begin with a short lesson about its landform and selected rocks or minerals. The learner will then move, jump, and collect items with an explorer character. Challenges will include obstacles, traps, pitfalls, and time limits.',
 'When an item is collected, the game will show its illustration, name, and short description. The learner can then continue exploring. These digital examples will provide information during the activity. They will not provide physical specimens or hands-on examination of real rocks and minerals.': 'Collected items will display an illustration, name, and short description. The learner can read this information before continuing. Digital examples will supplement physical specimens without providing hands-on examination.',
 "After a completed level, the Result Screen will present the collected items, a short review, and up to three gameplay stars. The learner may replay the level or continue to available content. The game will display an episode summary when the episode's required levels are completed. It will then unlock the next episode when applicable.": "After level completion, the Result Screen will show collected items, a short review, and up to three gameplay stars. Learners may replay the level or continue. Completing an episode's required levels will show its summary and unlock the next episode when applicable.",
 'After all four episodes are completed, the final screen will present the total stars, collected items, and a completion message. Stars and completed levels will describe gameplay progress. They will not, by themselves, measure gains in Science knowledge.': 'After all four episodes, the final screen will show total stars, collected items, and a completion message. These records describe gameplay progress. They do not measure gains in Science knowledge.',
 "The game will automatically save the player's name, unlocked episodes, completed levels, stars, and collected items on the device. It will load available progress in a later play session so the learner can continue. This local record will support continued use of the game without an online account.": "The application will automatically save the player's name, unlocked episodes, completed levels, stars, and collected items on the device. Later sessions will load available progress so the learner can continue without an online account."
}
for old,new in flow_replacements.items():
    assert old in text
    text=text.replace(old,new)

blocks=[]
for block in text.split('\n\n'):
    block=block.strip()
    if not block:continue
    if block.startswith('|'):
        for row in block.splitlines()[2:]:
            cells=[c.strip() for c in row.strip('|').split('|')]
            blocks.append({'role':'bullet','text':'•  '+cells[0]+': '+cells[1]})
    elif block.startswith('##'):
        m=re.match(r'^(#{2,4}) (.+)$',block)
        assert m,block
        blocks.append({'role':'heading','level':len(m.group(1))-1,'text':m.group(2)})
    else:blocks.append({'role':'body','text':block.replace('\n',' ')})

body=E.Element(q('body'))
body.extend([deepcopy(ps[0]),deepcopy(ps[1])])
for block in blocks:
    body.append(paragraph(**block))
    if block['text'].startswith('The learner will open the installed application'):
        body.append(paragraph('Figures 4A and 4B summarize the proposed flow. Connector A joins the panels, and B returns to the Landform Map. Dashed arrows show local progress data.'))
        body.append(image_paragraph('a','rIdLandGrandFlowA',4.5))
        body.append(paragraph('Figure 4A. Proposed gameplay flow: starting a play session','caption'))
body.append(paragraph('Figure 4B continues the flow through learning activities, results, and episode completion.'))
body.append(image_paragraph('b','rIdLandGrandFlowB',6))
body.append(paragraph('Figure 4B. Proposed gameplay flow: learning and progression','caption'))
body.append(section)
finaldoc=deepcopy(document);finaldoc.replace(finaldoc.find('w:body',NS),body)
rels=E.fromstring(package['word/_rels/document.xml.rels'])
for part,rid in [('a','rIdLandGrandFlowA'),('b','rIdLandGrandFlowB')]:
    E.SubElement(rels,'{'+REL+'}Relationship',Id=rid,Type=R+'/image',Target='media/landgrand-flow-'+part+'.png')
ct=E.fromstring(package['[Content_Types].xml'])
ctns='http://schemas.openxmlformats.org/package/2006/content-types'
if not any(c.get('Extension')=='png' for c in ct):E.SubElement(ct,'{'+ctns+'}Default',Extension='png',ContentType='image/png')

def write(target,updates,additions=None):
    with ZipFile(SOURCE) as zin,ZipFile(target,'w') as zout:
        for info in zin.infolist():zout.writestr(info,updates.get(info.filename,zin.read(info.filename)))
        for name,data in (additions or {}).items():zout.writestr(name,data)

chapter=OUT/'Land Grand - Chapter III - Revised - v1.docx'
write(chapter,{'word/document.xml':xml(finaldoc),'word/_rels/document.xml.rels':xml(rels),'[Content_Types].xml':xml(ct)},{'word/media/landgrand-flow-'+i+'.png':(ROOT/f'flow-{i}.png').read_bytes() for i in ['a','b']})

reftext=(VAULT/'Manuscript'/'Chapter III References.md').read_text(encoding='utf-8').split('---',2)[2]
entries=[b.strip() for b in reftext.split('\n\n') if re.match(r'^(Celsys|Google|Microsoft|Unity Technologies)\. ',b.strip())]
assert len(entries)==4
refbody=E.Element(q('body'));refbody.append(paragraph('BIBLIOGRAPHY','title'))
refbody.append(paragraph('This section lists the technical sources cited in Chapter III.'))
refrels=E.fromstring(package['word/_rels/document.xml.rels'])
for i,entry in enumerate(entries):
    prefix,url=entry.rsplit(' ',1)
    p=paragraph('')
    pp=p.find('w:pPr',NS);setprop(pp,'ind',left=720,hanging=720,firstLine=0)
    setprop(pp,'jc',val='left')
    pp.find(q('ind')).attrib.pop(q('firstLine'),None)
    setprop(pp,'keepLines',val=1)
    for c in list(p):
        if c.tag!=q('pPr'):p.remove(c)
    for j,segment in enumerate(prefix.split('*')):
        r=E.SubElement(p,q('r'));rp=deepcopy(ps[2].find('w:r/w:rPr',NS))
        if j%2:setprop(rp,'i',val=1)
        r.append(rp);t=E.SubElement(r,q('t'));t.text=segment;t.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
    r=E.SubElement(p,q('r'));E.SubElement(r,q('br'))
    rid='rIdLandGrandReference'+str(i+1)
    h=E.SubElement(p,q('hyperlink'));h.set('{'+R+'}id',rid)
    r=E.SubElement(h,q('r'));r.append(deepcopy(ps[2].find('w:r/w:rPr',NS)));E.SubElement(r,q('t')).text=url
    E.SubElement(refrels,'{'+REL+'}Relationship',Id=rid,Type=R+'/hyperlink',Target=url,TargetMode='External')
    refbody.append(p)
refbody.append(deepcopy(section));refdoc=deepcopy(document);refdoc.replace(refdoc.find('w:body',NS),refbody)
references=OUT/'Land Grand - Chapter III - References.docx'
write(references,{'word/document.xml':xml(refdoc),'word/_rels/document.xml.rels':xml(refrels)})
(ROOT/'chapter3-word-blocks.json').write_text(json.dumps(blocks,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'chapter3-polished-text.md').write_text(text,encoding='utf-8')
(ROOT/'outputs.json').write_text(json.dumps({'chapter':str(chapter),'references':str(references)},indent=2),encoding='utf-8')
plain=' '.join(b['text'] for b in blocks if b['role']=='body')
long=[s.strip() for s in re.split(r'(?<=[.!?])\s+(?=[A-Z])',plain) if len(s.split())>30]
(ROOT/'long-sentences.json').write_text(json.dumps(long,indent=2),encoding='utf-8')
print(json.dumps({'chapter':str(chapter),'references':str(references),'blocks':len(blocks),'long_sentences_over_30_words':long},ensure_ascii=False,indent=2))
