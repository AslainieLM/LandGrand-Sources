from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib, json

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent.parent
VAULT = WORKSPACE/'LandGrand'
REVIEW = WORKSPACE/'.work'/'chapter3-review-2026-11-01'
record = json.loads((REVIEW/'source-review.json').read_text(encoding='utf-8'))
raw = (REVIEW/'chapter3-reference.docx').read_bytes()
assert hashlib.sha256(raw).hexdigest() == record['sha256'] == 'a4862da1fe16500cf708186be199e0833f43b21cb82caaaf762f67029cd94d4b'
snapshot = ROOT/'vault-before.zip'
assert not snapshot.exists()
with ZipFile(snapshot,'w',ZIP_DEFLATED) as z:
    for p in VAULT.rglob('*'):
        if p.is_file(): z.write(p, 'LandGrand/'+p.relative_to(VAULT).as_posix())
    z.write(WORKSPACE/'tools'/'source-integrity.json','tools/source-integrity.json')
(ROOT/'before-hashes.json').write_text(json.dumps({str(p.relative_to(VAULT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in VAULT.rglob('*') if p.is_file()},indent=2),encoding='utf-8')

doc = VAULT/'Sources'/'Attachments'/'Chapter III - Unrevised - 2026-11-01.docx'
image = VAULT/'Sources'/'Attachments'/'Chapter III - Original Procedure - 2026-11-01.jpg'
extract = VAULT/'Sources'/'Chapter III Unrevised Draft Extract 2026-11-01.md'
assert not doc.exists() and not image.exists() and not extract.exists()
doc.write_bytes(raw)
image.write_bytes((REVIEW/'media'/'image1.jpg').read_bytes())
audit=json.loads((REVIEW/'word-audit.json').read_text(encoding='utf-8-sig'))
pages={p['text']:p for p in audit['paragraphs']}
lines=['---','type: source-extract','status: source','updated: 2026-11-01','---','','# Chapter III Unrevised Draft Extract','','Faithful paragraph text from the unchanged Word input. These paragraphs are source content, not agent instructions. See [[Sources/Chapter III Unrevised Draft 2026-11-01|provenance and review]]. Paragraph numbers are one-based OOXML body positions; gaps preserve blank source paragraphs. Page locators refer to the six-page read-only native Word render inspected on 2026-11-01.','']
for p in record['paragraphs']:
    lines += [f"## Paragraph {p['index']+1:03d}",'']
    page=pages.get(p['text'].strip())
    if page: lines += [f"Rendered page(s): {page['startPage']}–{page['endPage']}.",'']
    lines += [p['text'],'']
    if p['images']:
        lines += ['Embedded source image: ![[Sources/Attachments/Chapter III - Original Procedure - 2026-11-01.jpg]]','']
extract.write_text('\n'.join(lines),encoding='utf-8')

manifest_path=WORKSPACE/'tools'/'source-integrity.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8-sig'))
for p,role in [(doc,'original'),(image,'embedded-image')]:
    manifest['files'].append({'path':p.relative_to(VAULT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'role':role})
manifest['updated']='2026-11-01'
manifest_path.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'snapshot':str(snapshot),'retained_docx_sha256':hashlib.sha256(doc.read_bytes()).hexdigest(),'retained_image_sha256':hashlib.sha256(image.read_bytes()).hexdigest(),'paragraphs_extracted':len(record['paragraphs']),'source_pages':audit['pages']},indent=2))
