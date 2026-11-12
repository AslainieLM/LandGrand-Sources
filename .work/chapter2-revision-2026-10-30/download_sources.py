from pathlib import Path
from urllib.request import urlopen, Request
from concurrent.futures import ThreadPoolExecutor
from pypdf import PdfReader
import json

ROOT = Path(__file__).resolve().parent / 'research'
ROOT.mkdir(exist_ok=True)
URLS = {
    'ivgin': 'https://files.eric.ed.gov/fulltext/EJ1438370.pdf',
    'buray': 'https://scimatic.org/storage/journals/11/pdfs/4779.pdf',
    'calvo': 'https://zaguan.unizar.es/record/145422/files/texto_completo.pdf',
    'rodriguez': 'https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2023.1163441/pdf',
    'chung': 'https://mdpi-res.com/d_attachment/sustainability/sustainability-15-00983/article_deploy/sustainability-15-00983.pdf',
    'mayer': 'https://link.springer.com/content/pdf/10.1007/s10648-023-09842-1.pdf',
    'brown': 'https://www.csus.edu/indiv/s/stonerm/brown-collins-duguid--situatedcognitionandcultureoflearning.pdf',
    'rock-listing': 'https://itch.io/games/new-and-popular/genre-platformer/tag-rock',
}

def acquire(item):
    name, url = item
    try:
        with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30) as response:
            data = response.read()
            final_url = response.url
        record = dict(name=name, url=url, final_url=final_url, bytes=len(data))
        if data.startswith(b'%PDF'):
            path = ROOT / (name + '.pdf')
            path.write_bytes(data)
            doc = PdfReader(path)
            (ROOT / (name + '.txt')).write_text('\n'.join(
                f'\n--- PDF PAGE {i+1} ---\n' + page.extract_text()
                for i, page in enumerate(doc.pages)), encoding='utf-8')
            record['pages'] = len(doc.pages)
        else:
            (ROOT / (name + '.html')).write_bytes(data)
            record['type'] = 'html'
        return record
    except Exception as error:
        return dict(name=name, url=url, error=str(error))

with ThreadPoolExecutor(max_workers=8) as pool:
    records = list(pool.map(acquire, URLS.items()))
(ROOT / 'acquisition.json').write_text(json.dumps(records, indent=2), encoding='utf-8')
print(json.dumps(records, indent=2))
