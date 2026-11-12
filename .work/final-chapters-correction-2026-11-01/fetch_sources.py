from pathlib import Path
from urllib.request import Request, urlopen
from pypdf import PdfReader
import json, hashlib

ROOT = Path(__file__).resolve().parent
url = 'https://data.kigam.re.kr/ieg/cmmn/downloadFile.do?fileName=JGGH20206174.PDF'
raw = urlopen(Request(url, headers={'User-Agent': 'LandGrand academic reference verification'}), timeout=45).read()
assert raw.startswith(b'%PDF')
path = ROOT / 'Oh-2020-original.pdf'; path.write_bytes(raw)
reader = PdfReader(path)
pages = [p.extract_text() for p in reader.pages]
(ROOT / 'Oh-2020-pages.json').write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding='utf-8')
metadata = {}
for name, doi in [('oh','10.5467/JKESS.2020.41.1.61'), ('rader','10.5194/gc-4-475-2021'), ('yachin','10.1007/s11165-023-10143-4')]:
    try:
        item = json.load(urlopen(Request('https://api.crossref.org/works/' + doi, headers={'User-Agent': 'LandGrand academic reference verification'}), timeout=45))['message']
        metadata[name] = {key:item.get(key) for key in ['title','author','published','published-print','published-online','container-title','volume','issue','page','DOI']}
    except Exception as exc: metadata[name] = {'error': str(exc)}
metadata['oh_pdf'] = {'url':url, 'sha256':hashlib.sha256(raw).hexdigest(), 'pages':len(pages), 'inspected': 'English title, author and abstract on printed page 61; Korean full text not treated as fully reviewed.'}
(ROOT / 'new-source-metadata.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')
print(pages[0][:6700])
print(json.dumps(metadata, ensure_ascii=False, indent=2))
