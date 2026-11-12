from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib,json

ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parent.parent
VAULT=WORKSPACE/'LandGrand'
DELIVERY=WORKSPACE/'Deliverables'/'Chapter III Revision 2026-11-01'
verified=json.loads((ROOT.parent/'chapter3-word-revision-2026-11-01'/'final-verification.json').read_text(encoding='utf-8'))
files=[('chapter','Land Grand - Chapter III - Revised - v1.docx','Land Grand - Chapter III - Revised - v1.docx'),('references','Land Grand - Chapter III - References.docx','Land Grand - Chapter III - References - v1.docx')]
assert not (ROOT/'vault-before.zip').exists()
with ZipFile(ROOT/'vault-before.zip','w',ZIP_DEFLATED) as z:
    for p in VAULT.rglob('*'):
        if p.is_file():z.write(p,'LandGrand/'+p.relative_to(VAULT).as_posix())
    z.write(WORKSPACE/'tools'/'source-integrity.json','tools/source-integrity.json')
(ROOT/'before-hashes.json').write_text(json.dumps({str(p.relative_to(VAULT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in VAULT.rglob('*') if p.is_file()},indent=2),encoding='utf-8')
manifest_path=WORKSPACE/'tools'/'source-integrity.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8-sig'))
saved=[]
for key,origin,dest in files:
    source=DELIVERY/origin
    data=source.read_bytes()
    checksum=hashlib.sha256(data).hexdigest()
    assert checksum==verified['output_hashes'][key],f'Delivery changed after QA: {source}'
    target=VAULT/'Manuscript'/'Drafts'/dest
    assert not target.exists()
    target.write_bytes(data)
    with ZipFile(target) as z:assert z.testzip() is None
    entry={'path':target.relative_to(VAULT).as_posix(),'sha256':checksum,'role':'manuscript-snapshot'}
    assert not any(p['path']==entry['path'] for p in manifest['files'])
    manifest['files'].append(entry)
    saved.append({'delivery':str(source),'vault_copy':str(target),'sha256':checksum,'bytes':len(data)})
manifest['updated']='2026-11-01'
manifest_path.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(ROOT/'saved-artifacts.json').write_text(json.dumps(saved,indent=2),encoding='utf-8')
print(json.dumps(saved,indent=2))
