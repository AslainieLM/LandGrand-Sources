from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import quote
from pypdf import PdfReader
import hashlib, json

ROOT = Path(__file__).resolve().parent
url = 'https://spiral.imperial.ac.uk/server/api/core/bitstreams/11bbe6ea-6693-4141-ba42-a7bf620726b8/content'
with urlopen(Request(url, headers={'User-Agent':'Mozilla/5.0'}), timeout=40) as response:
    data = response.read()
assert data.startswith(b'%PDF')
pdf = ROOT/'Cutting and Deterding - Task Attention - 2024.pdf'
pdf.write_bytes(data)
reader = PdfReader(pdf)
pages = [p.extract_text() for p in reader.pages]
(ROOT/'article-pages.json').write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding='utf-8')
(ROOT/'article.txt').write_text('\n'.join(f'\n--- PDF PAGE {i+1} ---\n{t}' for i,t in enumerate(pages)), encoding='utf-8')
metadata = {'source_url':url,'sha256':hashlib.sha256(data).hexdigest(),'pdf_pages':len(reader.pages)}
try:
    with urlopen(Request('https://api.crossref.org/works/'+quote('10.1080/07370024.2022.2047971',safe=''),headers={'User-Agent':'LandGrand RRL source verification'}),timeout=20) as response:
        record = json.load(response)['message']
    metadata['crossref'] = {k:record.get(k) for k in ['title','author','volume','issue','page','published','published-print','published-online','URL']}
except Exception as error:
    metadata['crossref_error'] = str(error)
(ROOT/'source-metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(metadata,ensure_ascii=False,indent=2))
