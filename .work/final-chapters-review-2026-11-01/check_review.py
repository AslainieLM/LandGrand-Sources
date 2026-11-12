from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from pypdf import PdfReader
import json, hashlib, re

ROOT = Path(__file__).resolve().parent
read = lambda name: json.loads((ROOT / name).read_text(encoding='utf-8-sig'))
manifest = read('input-manifest.json')
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W}
records = {key: read(key + '-extract.json') for key in manifest}
audits = {key: read(key + '-word-audit.json') for key in manifest}
headings = {
    'chapter1': ['Project Context', 'Purpose and Description of the Project', 'Objectives of the Project', 'Scope and Limitations of the Project', 'Scope', 'Limitations', 'BIBLIOGRAPHY'],
    'chapter2': ['Related Literature / Theoretical Background', 'Related Studies', 'Related Projects', 'Synopsis']
}
for key, record in records.items():
    assert hashlib.sha256((ROOT / (key + '.docx')).read_bytes()).hexdigest() == manifest[key]['sha256']
    assert audits[key]['readOnly']
    xml_texts = [p['text'] for p in record['paragraphs']]
    # Native Word exposes manual line breaks as vertical tabs. The XML extract
    # joined adjacent text runs; remove only those break markers for this check.
    normalized = lambda t: re.sub(r'\s+', ' ', t.replace('\x0b', '')).strip()
    assert [normalized(t) for t in xml_texts] == [normalized(p['text']) for p in audits[key]['paragraphs']]
    for heading in headings[key]:
        index = xml_texts.index(heading)
        assert xml_texts[index + 1].startswith('This section '), heading
    assert len(list((ROOT / (key + '-render')).glob('page-*.png'))) == audits[key]['pages']

chapter2_sources = ['Cutting & Deterding (2024)', 'Yachin & Barak (2024)', 'Dong et al. (2024)', 'Garzón et al. (2025)', 'Chung & Pan (2023)', 'Andrews et al. (2020)', 'Hodges & Flanagan (2026)', 'Ivgin & Akcay (2024)', 'Buray & Alferez (2025)', 'Rodríguez-Ferrer et al. (2023)', 'Ford (2005)', 'Calvo & Lucha (2024)', 'Pezzetti (n.d.)', 'Fannyflamingo (n.d.)', 'The Open University (n.d.)']
raw2 = '\n'.join(p['text'] for p in records['chapter2']['paragraphs'])
assert all(word in raw2 for word in ['Cutting', 'Yachin', 'Dong', 'Garzón', 'Chung', 'Andrews', 'Hodges', 'Ivgin', 'Buray', 'Rodríguez-Ferrer', 'Ford', 'Calvo', 'Pezzetti', 'Fannyflamingo', 'The Open University'])
assert 'BIBLIOGRAPHY' not in raw2 and 'REFERENCES' not in raw2
chapter1_links = [rel['Target'] for rel in records['chapter1']['external_links'] if rel.get('Type', '').endswith('/hyperlink')]
reader = PdfReader(ROOT / 'chapter1.pdf')
pdf_links = {str(ref.get_object().get('/A', {}).get('/URI')) for page in reader.pages for ref in page.get('/Annots', []) if ref.get_object().get('/A', {}).get('/URI')}
assert len(chapter1_links) == 3 and set(chapter1_links) <= pdf_links
report = {
    'date': '2026-11-01',
    'scope': 'Read-only review; complete source text and all rendered pages inspected. No Word or vault changes.',
    'source_hashes': {key: record['sha256'] for key, record in manifest.items()},
    'pages_and_native_words': {key: {'pages': audit['pages'], 'words': audit['words']} for key, audit in audits.items()},
    'section_openings': {'chapter1': 6, 'chapter1_bibliography': 1, 'chapter2': 4},
    'headings_checked': headings,
    'chapter1_four_problems_and_objectives': 'Both lists display 1–4; matches current user-selected topics in order.',
    'chapter2_objective_order': [1, 2, 3, 4],
    'chapter1_context_pages': [1, 2, 3, 4],
    'chapter1_bibliography_entries': 3,
    'chapter1_hyperlinks_and_pdf_targets': 3,
    'chapter2_unique_sources': chapter2_sources,
    'chapter2_reference_entries_in_supplied_files': 0,
    'year_rule_violations': ['Ford (2005)', 'Pezzetti (n.d.)', 'Fannyflamingo (n.d.)', 'The Open University (n.d.)'],
    'footnotes_endnotes': {key: {'footnotes': value['footnote_markers'], 'endnotes': value['endnote_markers']} for key, value in records.items()},
    'main_findings': [
        {'priority': 'before submission', 'location': 'Chapter II pp. 6–9', 'finding': 'Four citations do not meet the 2020–2026 publication-year rule. Obtain verified replacements or dated source versions; preserve truthful years.'},
        {'priority': 'before submission', 'location': 'Chapter II / manuscript back matter', 'finding': 'No bibliography for the fifteen Chapter II sources is included in either supplied file. A separate consolidated bibliography is acceptable, but its current matching version must accompany the manuscript.'},
        {'priority': 'restore scope detail', 'location': 'Chapter I Scope, p. 6', 'finding': 'Previously specified Unity, C#, Piskel and Clip Studio Paint no longer appear. Restore a short tools sentence; do not infer a changed toolchain.'},
        {'priority': 'wording', 'location': 'Chapter II objective-three paragraph, p. 6', 'finding': 'Those survey responses has no clear local antecedent after the preceding survey-link sentence was removed. State the relevant survey finding explicitly.'},
        {'priority': 'evidence documentation', 'location': 'Chapter I pp. 3–4 / Chapter II p. 7', 'finding': 'The specimen concern is correctly attributed to the researcher, but observation date, setting and specimen examples remain undocumented. The source is not the survey.'}
    ],
    'minor_clarifications': ['Keep RAM/storage targets explicitly subject to device testing.', 'Retain the distinction between in-text citations/bibliography and literal footnotes/endnotes; the slide does not settle a mandatory numbered-note style.'],
    'unresolved_design_and_research': ['Exact Grade 5 content/competencies and geological associations', 'How collection requires use of Science information', 'Star/completion rules and detailed evaluation method', 'Supporting observation and survey-method records'],
    'source_checks': 'Reopened all three official Chapter I references and the Ford, Dong and Calvo originals/records. Recent theory claims were checked against original Cutting and Deterding main text and Yachin/Barak abstract earlier in this chat. Prior verified unchanged study passages were reused. Garzon direct publisher request returned 403; prior publisher-preview verification retained. Dong, Ford and Yachin remain partial-access sources.',
    'visual_check': 'All nine Chapter I and ten Chapter II pages inspected at 120 DPI. Readable; no clipping, overlap, stranded headings or accidental nearly empty continuation page.'
}
(ROOT / 'review-checks.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({key: report[key] for key in ['pages_and_native_words', 'section_openings', 'chapter1_bibliography_entries', 'chapter2_reference_entries_in_supplied_files', 'year_rule_violations', 'visual_check']}, ensure_ascii=False, indent=2))
