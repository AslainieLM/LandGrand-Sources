from pathlib import Path
from xml.etree import ElementTree as ET
import hashlib
import json
import re
import zipfile

WORK = Path(__file__).parent
VAULT = Path(r'D:\Projects\LandGrand-Sources\LandGrand')
errors = []
link_count = 0


def require(condition, message):
    if not condition:
        errors.append(message)


for path in VAULT.rglob('*.md'):
    text = path.read_text(encoding='utf-8')
    for raw in re.findall(r'\[\[([^\]]+)\]\]', text):
        link_count += 1
        target = raw.split('|', 1)[0]
        dest, _, anchor = target.partition('#')
        candidates = [VAULT / dest, VAULT / (dest + '.md')] if dest else [path]
        resolved = next((p for p in candidates if p.is_file()), None)
        if resolved is None:
            matches = [p for p in VAULT.rglob('*') if p.is_file() and (p.name == dest or p.stem == dest)]
            if len(matches) == 1:
                resolved = matches[0]
        require(resolved is not None, f'{path.relative_to(VAULT)}: missing {target}')
        if resolved and anchor and resolved.suffix == '.md':
            body = resolved.read_text(encoding='utf-8')
            if anchor.startswith('^'):
                require(anchor in body, f'Missing block {target}')
            else:
                require(anchor in re.findall(r'^#{1,6}\s+(.+)$', body, re.M), f'Missing heading {target}')

manifest = json.loads((WORK / 'import-manifest.json').read_text(encoding='utf-8'))
for source in manifest['sources']:
    data = (VAULT / 'Sources/Attachments' / source['file']).read_bytes()
    require(hashlib.sha256(data).hexdigest() == source['sha256'], f'Source changed: {source["file"]}')
    require(len(data) == source['bytes'], f'Source length changed: {source["file"]}')
    source_note = (VAULT / f'Sources/{source["note"]}.md').read_text(encoding='utf-8')
    require(source['sha256'] in source_note and source['origin'] in source_note, f'Provenance mismatch: {source["file"]}')

pdf_pages = json.loads((WORK / 'manuscript-pages.json').read_text(encoding='utf-8'))
pdf_extract = (VAULT / 'Sources/Capstone Manuscript BSIT Extract.md').read_text(encoding='utf-8')
for page in pdf_pages:
    quoted = '\n'.join('> ' + line for line in page['text'].split('\n'))
    require(quoted in pdf_extract, f'Missing PDF page text: {page["page"]}')

# Verify every bullet item, joining wrapped PDF lines, against the normalized TOC.
items = []
for page in pdf_pages:
    for line in page['text'].splitlines():
        match = re.match(r'^\s*[▪o•]\s+(.+)$', line)
        if match:
            items.append(match.group(1))
        elif line.strip() and items:
            items[-1] += ' ' + line.strip()
toc = (VAULT / 'Manuscript/Table of Contents.md').read_text(encoding='utf-8')
compact = lambda s: re.sub(r'\s+', ' ', s).casefold().strip()
toc_compact = compact(toc)
for item in items:
    require(compact(item) in toc_compact, 'Missing PDF outline item: ' + item)

slides = json.loads((WORK / 'guidelines-slides.json').read_text(encoding='utf-8'))['slides']
slide_extract = (VAULT / 'Sources/Chapter 1-3 Guidelines Extract.md').read_text(encoding='utf-8')
slide_text_blocks = 0
for slide in slides:
    require(f'## Slide {slide["slide"]:02d}\n' in slide_extract, f'Slide heading missing: {slide["slide"]}')
    for field in ['text', 'shape_text', 'notes']:
        for text in slide[field]:
            slide_text_blocks += 1
            text = text.replace('\r', '\n').replace('\v', '\n')
            require('\n'.join('> ' + line for line in text.split('\n')) in slide_extract,
                    f'Slide text missing: slide {slide["slide"]}, {field}')

discussion = (VAULT / 'Sources/Chapter1 Discussion Notes Extract.md').read_text(encoding='utf-8')
typed = json.loads((WORK / 'discussion-preserved-paragraphs.json').read_text(encoding='utf-8'))
for paragraph in typed:
    require('\n'.join('> ' + line for line in paragraph['text'].split('\n')) in discussion,
            f'Discussion paragraph missing: {paragraph["paragraph"]}')

with zipfile.ZipFile(VAULT / 'Sources/Attachments/Chapter1.docx') as archive:
    original_images = [archive.read(n) for n in archive.namelist() if n.startswith('word/media/')]
    for image in manifest['images']:
        data = (VAULT / image['path']).read_bytes()
        require(data in original_images, f'Image not preserved: {image["path"]}')
        require(hashlib.sha256(data).hexdigest() == image['sha256'], f'Image changed: {image["path"]}')
        require(f'### Screenshot {image["image"]:02d} - ' in discussion, f'Image transcription missing: {image["image"]}')

original = VAULT / 'Sources/Attachments/Land Grand - Aslainie - Final.docx'
require(hashlib.sha256(original.read_bytes()).hexdigest() == '9b753fecba2de5f50978395a4e38bbf7a336d358de9fab01eb1120508bd60d48',
        'Initial proposal changed')
requirements = (VAULT / 'Project/Scope and Requirements.md').read_text(encoding='utf-8')
require({int(x) for x in re.findall(r'LG-(\d+)', requirements)} == set(range(1, 26)), 'Requirement IDs changed')
for path in (VAULT / '.obsidian').glob('*.json'):
    try:
        json.loads(path.read_text(encoding='utf-8-sig'))
    except Exception as exc:
        errors.append(f'Invalid config: {path.name}: {exc}')

report = {'notes': len(list(VAULT.rglob('*.md'))), 'internal_links_checked': link_count,
          'original_hashes_checked': len(manifest['sources']) + 1,
          'pdf_pages_preserved': len(pdf_pages), 'outline_items_checked': len(items),
          'slides_preserved': len(slides), 'slide_text_blocks_checked': slide_text_blocks,
          'discussion_paragraphs_preserved': len(typed), 'embedded_images_preserved': len(manifest['images']),
          'errors': errors}
(WORK / 'validation.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
raise SystemExit(bool(errors))
