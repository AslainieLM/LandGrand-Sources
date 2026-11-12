from pathlib import Path
from zipfile import ZipFile
from lxml import etree
import json

ROOT=Path(__file__).resolve().parent
path=Path(json.loads((ROOT/'outputs.json').read_text(encoding='utf-8'))['bibliography'])
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
q=lambda name:'{'+W+'}'+name
with ZipFile(path) as z:
    infos=z.infolist(); data={x.filename:z.read(x.filename) for x in infos}
root=etree.fromstring(data['word/document.xml'])
for p in root.find(q('body')).findall(q('p'))[2:]:
    pp=p.find(q('pPr'))
    for tag,value in [('keepLines','1'),('widowControl','1')]:
        el=pp.find(q(tag))
        if el is None:el=etree.SubElement(pp,q(tag))
        el.set(q('val'),value)
data['word/document.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
temp=path.with_suffix('.layout.tmp')
with ZipFile(temp,'w') as z:
    for info in infos:z.writestr(info,data[info.filename])
temp.replace(path)
print('Kept each complete bibliography entry on one page.')
