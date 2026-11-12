from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from pypdf import PdfReader
import hashlib, importlib.util, json, re, shutil, sys

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / 'chapter2-revision-2026-10-30'
WORKSPACE = ROOT.parents[1]
OLD = WORKSPACE / 'Deliverables/Chapter II Revision 2026-10-30'
OUT = WORKSPACE / 'Deliverables/Chapter II Revision 2026-11-01'
FINAL = OUT / 'Land Grand - Chapter II - Revised - v2.docx'
BIB = OUT / 'Land Grand - Chapter II - APA References - v2.docx'
OLD_CHAPTER = OLD / 'Land Grand - Chapter II - Revised - v1.docx'
OLD_BIB = OLD / 'Land Grand - Chapter II - APA References.docx'
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NS = {'w': W}
q = lambda key: '{' + W + '}' + key
sha = lambda path: hashlib.sha256(Path(path).read_bytes()).hexdigest()
count = lambda value: len(re.findall(r'\b[\w’]+\b', value))
read = lambda path: json.loads(Path(path).read_text(encoding='utf-8-sig'))
inventory = lambda folder: {str(p.relative_to(folder)): sha(p) for p in sorted(folder.rglob('*')) if p.is_file()}
paragraph_text = lambda p: ''.join(p.xpath('.//w:t/text()', namespaces=NS))
c14n = lambda element: etree.tostring(element, method='c14n')
records = read(ROOT / 'chapter-v2.json')
refs = read(ROOT / 'references-v2.json')
old_records = read(BASE / 'chapter.json')
old_refs = read(BASE / 'references.json')
audit = read(ROOT / 'chapter-v2-final-audit-2.json')
bib_audit = read(ROOT / 'references-v2-audit.json')
assert audit['readOnly'] and bib_audit['readOnly']
assert audit['pages'] == 10 and bib_audit['pages'] == 3
assert len(records) == len(audit['paragraphs']) == 41
assert [x['text'] for x in records] == [x['text'] for x in audit['paragraphs']]
headings = [x['text'] for x in records if x['role'] in ['heading', 'subheading']]
assert headings == ['Related Literature / Theoretical Background', 'Related Studies', 'Related Projects', 'Synopsis']
for index, item in enumerate(records):
    if item['role'] in ['heading', 'subheading']:
        assert records[index + 1]['role'] == 'intro'
        assert records[index + 1]['text'].startswith('This section ')
assert sum(x['text'].startswith('This section ') for x in records) == 4
objective_order = []
for item in records:
    if 'objective' in item and (not objective_order or objective_order[-1] != item['objective']): objective_order.append(item['objective'])
assert objective_order == [1, 2, 3, 4]
manuscript = '\n'.join(x['text'] for x in records)
for forbidden in ['Mayer', 'CTML', 'Cognitive Theory of Multimedia Learning', 'DisasterSafetyGame', '75 levels', 'Research Review', 'TODO', '\ufffd']:
    assert forbidden not in manuscript
for required in ['proposes the Task-Attention Theory of Game Learning', '60 planned levels', 'Android 10 and above', 'single player', 'Baluan Elementary School']:
    assert required in manuscript
assert len(refs) == 15 and {x['id'] for x in refs} == ({x['id'] for x in old_refs} - {'mayer'}) | {'cutting'}
assert [x['id'] for x in refs] == ['andrews', 'brown', 'buray', 'calvo', 'chung', 'cutting', 'dong', 'geologyrocks', 'ford', 'garzon', 'hodges', 'ivgin', 'docduck', 'rodriguez', 'openuniversity']
for entry in old_refs:
    if entry['id'] != 'mayer': assert entry == next(x for x in refs if x['id'] == entry['id'])
patterns = {
    'andrews': r'Andrews et al\. \(2020\)', 'brown': r'Brown et al\. \(1989\)',
    'buray': r'Buray and Alferez \(2025\)', 'calvo': r'Calvo and Lucha \(2024\)',
    'chung': r'Chung and Pan \(2023\)', 'cutting': r'Cutting and Deterding \(2024\)',
    'dong': r'Dong et al\. \(2024\)', 'geologyrocks': r'Fannyflamingo \(n\.d\.\)',
    'ford': r'Ford \(2005\)', 'garzon': r'Garzón et al\. \(2025\)',
    'hodges': r'Hodges and Flanagan \(2026\)', 'ivgin': r'Ivgin and Akcay \(2024\)',
    'docduck': r'\(Pezzetti, n\.d\.\)', 'rodriguez': r'Rodríguez-Ferrer et al\. \(2023\)',
    'openuniversity': r'The Open University \(n\.d\.\)'
}
assert all(re.search(pattern, manuscript) for pattern in patterns.values())
max_sentence = 0
for item in records:
    for sentence in re.split(r'(?<=[.!?])\s+(?=[A-Z])', item['text']):
        max_sentence = max(max_sentence, count(sentence))
        assert count(sentence) <= 30, sentence

allowed_original_indices = {4, 5, 6, 12, 22, 37}
package_changes = {}
for source, target in [(OLD_CHAPTER, FINAL), (OLD_BIB, BIB)]:
    with ZipFile(source) as a, ZipFile(target) as b:
        assert b.testzip() is None and set(a.namelist()) == set(b.namelist())
        changes = [name for name in a.namelist() if a.read(name) != b.read(name)]
        expected_changes = {'word/document.xml'} if target == FINAL else {'word/document.xml', 'word/_rels/document.xml.rels'}
        assert set(changes) == expected_changes
        package_changes[target.name] = changes
        old = etree.fromstring(a.read('word/document.xml'))
        new = etree.fromstring(b.read('word/document.xml'))
        assert c14n(old.find('w:body/w:sectPr', NS)) == c14n(new.find('w:body/w:sectPr', NS))
        assert not new.xpath('//w:commentRangeStart | //w:ins | //w:del | //w:drawing', namespaces=NS)
        old_ps = old.findall('w:body/w:p', NS); new_ps = new.findall('w:body/w:p', NS)
        if target == FINAL:
            assert [paragraph_text(p) for p in new_ps] == [x['text'] for x in records]
            for index, p in enumerate(old_ps):
                dest = new_ps[index if index <= 6 else index + 1]
                if index not in allowed_original_indices: assert c14n(p) == c14n(dest), index
                assert c14n(p.find(q('pPr'))) == c14n(dest.find(q('pPr'))), index
        else:
            assert [paragraph_text(p) for p in new_ps] == [x['text'] for x in bib_audit['paragraphs']]
            assert c14n(old_ps[0]) == c14n(new_ps[0]) and c14n(old_ps[1]) == c14n(new_ps[1])
            for index, entry in enumerate(old_refs):
                if entry['id'] == 'mayer': continue
                dest_index = next(i for i, item in enumerate(refs) if item['id'] == entry['id'])
                assert c14n(old_ps[index + 2]) == c14n(new_ps[dest_index + 2]), entry['id']
            rels = etree.fromstring(b.read('word/_rels/document.xml.rels'))
            targets = [n.get('Target') for n in rels if n.get('Type') == R + '/hyperlink']
            assert len(targets) == 15 and set(targets) == {x['url'] for x in refs}
            assert all(p.xpath('w:pPr/w:ind[@w:hanging="720"]', namespaces=NS) for p in new_ps[2:])
            old_rels = etree.fromstring(a.read('word/_rels/document.xml.rels'))
            changed_rels = [(x, next(y for y in rels if y.get('Id') == x.get('Id'))) for x in old_rels if dict(x.attrib) != dict(next(y for y in rels if y.get('Id') == x.get('Id')).attrib)]
            assert len(changed_rels) == 1
            assert changed_rels[0][0].get('Target') == 'https://doi.org/10.1007/s10648-023-09842-1'
            assert changed_rels[0][1].get('Target') == 'https://doi.org/10.1080/07370024.2022.2047971'

reader = PdfReader(ROOT / 'references-v2.pdf')
uris = {str(ref.get_object().get('/A', {}).get('/URI')) for page in reader.pages for ref in page.get('/Annots', []) if ref.get_object().get('/A', {}).get('/URI')}
assert {x['url'] for x in refs} <= uris
assert len(list((ROOT / 'chapter-render-final').glob('page-*.png'))) == 10
assert len(list((ROOT / 'references-render').glob('page-*.png'))) == 3
before = read(ROOT / 'protected-before.json')
assert before['v1'] == inventory(OLD), 'v1 outputs changed'
assert before['vault'] == inventory(WORKSPACE / 'LandGrand'), 'vault changed'
assert sha(BASE / 'chapter1-reference.docx') == '6ad898c79899c91d506b625b992959af921c53fee88167390d2151f581ada3ad'
assert sha(BASE / 'chapter2-original.docx') == '168781620da2b47b7390cce5a3182656610f60d34ece8c91a28d5114f9b85180'

script = Path(r'C:\Users\user\.codex\plugins\cache\openai-primary-runtime\documents\26.1026.10807\skills\documents\scripts\render_and_diff.py')
spec = importlib.util.spec_from_file_location('packaged_diff', script)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
def cached_render(render_py, docx, outdir):
    folders = {
        OLD_CHAPTER.resolve(): BASE / 'chapter-render-2', OLD_BIB.resolve(): BASE / 'references-render',
        FINAL.resolve(): ROOT / 'chapter-render-final', BIB.resolve(): ROOT / 'references-render'
    }
    Path(outdir).mkdir(parents=True, exist_ok=True)
    for path in folders[Path(docx).resolve()].glob('page-*.png'): shutil.copy2(path, Path(outdir) / path.name)
mod._run_render = cached_render
for source, target, label in [(OLD_CHAPTER, FINAL, 'chapter-v1-v2-diff'), (OLD_BIB, BIB, 'bibliography-v1-v2-diff')]:
    sys.argv = [str(script), str(source), str(target), '--outdir', str(ROOT / label)]
    mod.main()

report = {
    'date': '2026-11-01', 'chapter_pages': 10, 'bibliography_pages': 3,
    'chapter_words_native': audit['words'], 'chapter_words_tokenized': count(manuscript),
    'v1_words_tokenized': count(' '.join(x['text'] for x in old_records)),
    'maximum_sentence_words': max_sentence, 'matched_citations_and_references': 15,
    'live_word_and_pdf_reference_targets': 15, 'this_section_openings': 4, 'objective_order': objective_order,
    'replaced_original_paragraph_indices': sorted(allowed_original_indices), 'new_body_paragraphs': 1,
    'other_paragraphs_and_reference_entries_preserved': True,
    'package_changes': package_changes, 'originals_and_v1_preserved': True,
    'vault_files_unchanged': len(before['vault']),
    'source': read(ROOT / 'source-metadata.json'),
    'source_reading': 'Full original article main text, PDF pages 2–26 (printed 257–281), plus published cover metadata. References were not independently verified.',
    'visual_review': 'All 10 final chapter and 3 bibliography page PNGs inspected at 120 DPI. No clipping, overlap, stranded headings or near-empty continuation page.',
    'uncompleted_checks': ['Adviser approval of anchor theory', 'Curriculum/content validation and local observation details', 'Full text of unchanged Dong, Garzon and Ford partial-access sources', 'Game implementation, device tests and measured learning; not part of this manuscript revision'],
    'output_hashes': {str(path): sha(path) for path in [FINAL, BIB]}
}
(ROOT / 'final-verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k: v for k, v in report.items() if k not in ['source', 'output_hashes', 'package_changes']}, ensure_ascii=False, indent=2))
