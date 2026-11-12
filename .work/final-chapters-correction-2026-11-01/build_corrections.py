from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from copy import deepcopy
import hashlib, json, re

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[1]
OUT = WORKSPACE / 'Deliverables' / 'Chapters I-II Corrections 2026-11-01'
assert not OUT.exists(), 'Preserve earlier deliverables.'
OUT.mkdir(parents=True)
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
REL = 'http://schemas.openxmlformats.org/package/2006/relationships'
NS = {'w': W}
q = lambda key: '{' + W + '}' + key
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
dump = lambda name,data: (ROOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
dump('vault-before.json', {str(p.relative_to(WORKSPACE/'LandGrand')):sha(p) for p in (WORKSPACE/'LandGrand').rglob('*') if p.is_file()})
manifest = read(ROOT/'input-manifest.json')

changes1 = {
    13: "On October 29, 2026, the researcher observed the Grade 5 learning materials at Baluan Elementary School. The display included physical rock samples, while granite and examples of gold and silver were shown only in pictures and posters. This observation suggested a limited range of physical examples for demonstrations. Land Grand will provide digital illustrations with item names and short descriptions. These will supplement the classroom materials.",
    20: "The researcher observed limited physical rock and mineral examples in the Grade 5 display.",
    40: "The proposed game is for Grade 5 learners at Baluan Elementary School. Development will use Unity and C#, with Piskel and Clip Studio Paint for graphical assets. The application will include the following features:",
    51: "The game will work offline on Android phones and tablets running Android 10 and above. Minimum targets are 2 GB RAM and 300 MB free storage. These targets remain subject to device testing."
}
changes2 = {
    23: "The third objective organizes selected content into Mountains, Hills, Plains, and Plateaus episodes. It responds to survey reports that landforms, rocks, and minerals are difficult Science topics. These reports justify investigating the selected content. They do not identify every learner's misconception or establish that every selected topic belongs to a verified Grade 5 competency.",
    24: "Oh (2020) compared the descriptions used by 24 Grade 3 learners for three types of sedimentary rocks. Learners completed descriptive tasks and tasks that asked them to infer how the rocks formed. Everyday descriptors were used less often in the inferential tasks. More scientifically appropriate descriptors were associated with more valid explanations of rock formation. The study examined physical rocks and younger learners rather than a digital game. It does not validate Land Grand's episode arrangement. For Land Grand, its findings support reviewing whether the item descriptions explain meaningful rock features and concepts.",
    26: "The fourth objective provides digital rock and mineral illustrations with names and short descriptions. It responds to the researcher's observation at Baluan Elementary School on October 29, 2026. The Grade 5 display contained physical rock samples, while other examples were shown in pictures and posters. This observation concerns the materials on display. It does not establish the school's full specimen inventory.",
    31: "Legends of Learning (2025) describes DocDuck: Rock Cycle as a game for middle-school learners. Its content follows changes among igneous, sedimentary, and metamorphic rocks. This geological focus relates to Land Grand's selected rock content. Land Grand instead proposes four landform episodes for Grade 5 learners. The platform's description provides a content comparison. It does not establish Android compatibility, offline operation, or learning outcomes for the proposed game.",
    32: "Rader et al. (2021) developed and evaluated a virtual geology field camp using Minecraft. University learners explored geological structures and practiced mapping in teams. The mixed methods evaluation used pre- and post-course surveys and observations. Participants reported positive experiences, although technical problems affected the course. Land Grand has a smaller scope: two-dimensional exploration and selected Science content for Grade 5 learners. The field camp's university audience, online teamwork, and instructor support limit direct comparison with an offline single-player game.",
    33: "The digital rock and mineral models described by Andrews et al. (2020) provide another comparison. The collection was developed for remote geology instruction and offers three-dimensional visual examples. Land Grand proposes two-dimensional illustrations within a game. These resources differ in presentation and instructional setting. Neither digital format provides physical specimens or hands-on property tests.",
    34: "These resources connect geological content with game activities or digital visual examples in different ways. Land Grand proposes short lessons, exploration, reviews, and labeled illustrations within its documented scope. The game will remain offline and single player on Android 10 and above. It will not require a website, online account, or central teacher dashboard. These are planned delivery boundaries, not verified advantages over every existing resource."
}

def xml_bytes(element): return etree.tostring(element,xml_declaration=True,encoding='UTF-8',standalone=True)
def pkg(path):
    with ZipFile(path) as z: return {name:z.read(name) for name in z.namelist()}
def save_package(source, target, updates):
    with ZipFile(source) as zin, ZipFile(target,'w') as zout:
        for info in zin.infolist(): zout.writestr(info, updates.get(info.filename, zin.read(info.filename)))
def replace_text(p, text):
    rp = p.find('w:r/w:rPr', NS)
    rp = deepcopy(rp) if rp is not None else None
    for child in list(p):
        if child.tag != q('pPr'): p.remove(child)
    r=etree.SubElement(p,q('r'))
    if rp is not None: r.append(rp)
    t=etree.SubElement(r,q('t')); t.set('{http://www.w3.org/XML/1998/namespace}space','preserve'); t.text=text

outputs = {}
for key, changes, filename in [
    ('chapter1',changes1,'Land Grand - Chapter I - Corrected.docx'),
    ('chapter2',changes2,'Land Grand - Chapter II - Corrected.docx')]:
    source=ROOT/(key+'.docx'); assert sha(source)==manifest[key]['sha256']
    data=pkg(source); document=etree.fromstring(data['word/document.xml']); ps=document.findall('w:body/w:p',NS)
    extract=read(ROOT/(key+'-extract.json'))
    by_index={p['xml_index']:p['text'] for p in extract['paragraphs']}
    for index,value in changes.items():
        assert ''.join(ps[index].xpath('.//w:t/text()',namespaces=NS))==by_index[index]
        replace_text(ps[index],value)
    target=OUT/filename
    save_package(source,target,{'word/document.xml':xml_bytes(document)})
    outputs[key]=str(target)
    dump(key+'-corrected-text.json', [{'index':i,'text':''.join(p.xpath('.//w:t/text()',namespaces=NS))} for i,p in enumerate(ps)])

old_refs=read(WORKSPACE/'.work/chapter2-revision-2026-10-30/references.json')
refs=[item for item in old_refs if item['id'] not in ['brown','ford','mayer','docduck','geologyrocks','openuniversity']]
refs.extend([
    {'id':'cutting','author':'Cutting, J., & Deterding, S.','year':'2024','title':'The task-attention theory of game learning: A theory and research agenda','journal':'Human–Computer Interaction','volume':'39','issue':'5–6','pages':'257–287','url':'https://doi.org/10.1080/07370024.2022.2047971'},
    {'id':'yachin','author':'Yachin, T., & Barak, M.','year':'2024','title':'Science-based educational escape games: A game design methodology','journal':'Research in Science Education','volume':'54','issue':'2','pages':'299–313','url':'https://doi.org/10.1007/s11165-023-10143-4'},
    {'id':'oh','author':'Oh, P. S.','year':'2020','title':'Analyzing rock descriptors used by elementary school students in different task contexts','journal':'Journal of the Korean Earth Science Society','volume':'41','issue':'1','pages':'61–74','url':'https://doi.org/10.5467/JKESS.2020.41.1.61'},
    {'id':'rader','author':'Rader, E., Love, R., Reano, D., Dousay, T. A., & Wingerter, N.','year':'2021','title':'Pandemic Minecrafting: An analysis of the perceptions of and lessons learned from a gamified virtual geology field camp','journal':'Geoscience Communication','volume':'4','issue':'4','pages':'475–492','url':'https://doi.org/10.5194/gc-4-475-2021'},
    {'id':'legends','author':'Legends of Learning.','year':'2025','date':'2025, February 5','title':'10 top-rated science games for kids','url':'https://www.legendsoflearning.com/blog/10-top-rated-science-games-for-kids/'},
    {'id':'deped','author':'Department of Education.','year':'2020','date':'2020, July 21','title':'Suggested strategies in implementing distance learning delivery modalities (DLDM) for school year 2020-2021','suffix':' (DM-CI-2020-00162). Office of the Undersecretary for Curriculum and Instruction. ','url':'https://region8.deped.gov.ph/wp-content/uploads/2020/07/DM-CI-2020-00162-2.pdf'},
    {'id':'phivolcs','author':'DOST-PHIVOLCS.','year':'2026','date':'2026, June 8','title':'Tsunami information No. 2: Cancellation of tsunami warning','url':'https://tsunami.phivolcs.dost.gov.ph/Tsunami_Information/2026_Tsunami_Information/Jun/07/20260607_2337z_Advisory2_2.pdf'},
    {'id':'unesco','author':'UNESCO.','year':'2023','title':'Global education monitoring report 2023: Technology in education: A tool on whose terms?','url':'https://www.unesco.org/gem-report/en/publication/technology'}
])
refs.sort(key=lambda x:x['author'].casefold())
assert len(refs)==17 and all(2020<=int(x['year'])<=2026 for x in refs)
dump('references-corrected.json',refs)

source=ROOT/'chapter1.docx'; data=pkg(source)
document=etree.fromstring(data['word/document.xml']); body=document.find(q('body')); patterns=body.findall(q('p'))
sect=deepcopy(body.find(q('sectPr')))
title=deepcopy(patterns[62]); intro=deepcopy(patterns[63]); reference=deepcopy(patterns[64])
base_rp=deepcopy(reference.find('w:r/w:rPr',NS))
for child in list(body): body.remove(child)
replace_text(title,'BIBLIOGRAPHY'); replace_text(intro,'This section lists the sources cited in Chapters I and II.')
body.append(title); body.append(intro)
rels=etree.fromstring(data['word/_rels/document.xml.rels'])
url_to_rid={x.get('Target'):x.get('Id') for x in rels if x.get('Type')==R+'/hyperlink'}
used={x.get('Id') for x in rels}
def add_run(parent,value,italic=False):
    run=etree.SubElement(parent,q('r'))
    rp=deepcopy(base_rp)
    if rp is None: rp=etree.Element(q('rPr'))
    for tag in ['i','iCs','u']:
        for old in rp.findall(q(tag)): rp.remove(old)
    if italic:
        etree.SubElement(rp,q('i')); etree.SubElement(rp,q('iCs'))
    color=rp.find(q('color'))
    if color is not None: color.set(q('val'),'000000')
    run.append(rp)
    t=etree.SubElement(run,q('t')); t.set('{http://www.w3.org/XML/1998/namespace}space','preserve'); t.text=value
for number,ref in enumerate(refs,1):
    p=deepcopy(reference)
    for child in list(p):
        if child.tag!=q('pPr'): p.remove(child)
    pp=p.find(q('pPr'))
    for tag in ['numPr','tabs']:
        for child in pp.findall(q(tag)): pp.remove(child)
    ind=pp.find(q('ind'))
    if ind is None: ind=etree.SubElement(pp,q('ind'))
    ind.attrib.clear(); ind.set(q('left'),'720'); ind.set(q('hanging'),'720')
    jc=pp.find(q('jc'))
    if jc is None: jc=etree.SubElement(pp,q('jc'))
    jc.set(q('val'),'left')
    spacing=pp.find(q('spacing'))
    if spacing is None: spacing=etree.SubElement(pp,q('spacing'))
    spacing.set(q('before'),'0'); spacing.set(q('after'),'160'); spacing.set(q('line'),'480'); spacing.set(q('lineRule'),'auto')
    if pp.find(q('keepLines')) is None: etree.SubElement(pp,q('keepLines'))
    add_run(p,ref['author']+' ('+ref.get('date',ref['year'])+'). ')
    if 'journal' in ref:
        add_run(p,ref['title']+'. ')
        add_run(p,ref['journal']+', '+ref['volume'],True)
        if ref.get('issue'): add_run(p,'('+ref['issue']+')')
        add_run(p,', '+ref.get('pages','Article '+ref.get('article',''))+'. ')
    else:
        add_run(p,ref['title'],True)
        add_run(p,ref.get('suffix',' ' if ref['title'].endswith(('.', '?', '!')) else '. '))
    if ref['url'] in url_to_rid: rid=url_to_rid[ref['url']]
    else:
        rid='rIdLandGrandCorrected'+str(number); assert rid not in used; used.add(rid)
        rel=etree.SubElement(rels,'{'+REL+'}Relationship')
        for key,value in [('Id',rid),('Type',R+'/hyperlink'),('Target',ref['url']),('TargetMode','External')]:rel.set(key,value)
    link=etree.SubElement(p,q('hyperlink'));link.set('{'+R+'}id',rid);add_run(link,ref['url'])
    body.append(p)
body.append(sect)
target=OUT/'Land Grand - Chapters I-II - Bibliography.docx'
save_package(source,target,{'word/document.xml':xml_bytes(document),'word/_rels/document.xml.rels':xml_bytes(rels)})
outputs['bibliography']=str(target)
dump('outputs.json',outputs)
dump('change-slots.json',{'chapter1':sorted(changes1),'chapter2':sorted(changes2)})
dump('observation-clarification.json',{'received':'2026-11-01','observation_date':'2026-10-29','user_reply':'October 29, 2026, At Baluan Elementary School, Grade 5, only normal rocks are display, such as gold, silver, metal, granite only in picture and poster though','interpretation':'Researcher-reported Grade 5 display limitation; identities/counts of physical rocks and school-wide inventory unverified. Metal is not treated as a single mineral type. No game content list is established.'})
print(json.dumps({'outputs':outputs,'bibliography_sources':len(refs),'chapter2_sources':len(refs)-3,'old_or_undated_references':0},indent=2))
