from pathlib import Path
from zipfile import ZipFile
import hashlib, importlib.util, json, re

ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parent.parent
VAULT=WORKSPACE/'LandGrand'
draft=(VAULT/'Manuscript'/'Drafts'/'Chapter III Technical Background.md').read_text(encoding='utf-8')
body=draft.split('---',2)[2].strip()
refs=(VAULT/'Manuscript'/'Chapter III References.md').read_text(encoding='utf-8')
main=re.findall(r'^## (.+)$',body,re.M)
assert main==['Technicality of the project','Details of the technologies to be used','How the project will work'],main
lines=body.splitlines()
headings=[]
for i,line in enumerate(lines):
    if re.match(r'^#{2,4} ',line):
        nextline=next(s for s in lines[i+1:] if s.strip())
        assert nextline.startswith('This section '),(line,nextline)
        headings.append(line)
chapter_open=next(s for s in lines[1:] if s.strip())
assert chapter_open.startswith('This chapter ')
citations=set(re.findall(r'\((Celsys|Google|Microsoft|Unity Technologies), (20\d{2})\)',body))
entries=set(re.findall(r'^(Celsys|Google|Microsoft|Unity Technologies)\. \((20\d{2})',refs,re.M))
assert citations==entries and len(entries)==4,(citations,entries)
assert all(2020<=int(year)<=2026 for _,year in entries)
assert 'Not started in this vault' not in body and 'Working scaffold' not in body
assert 'Android 10 and above' in body and 'up to Android 14' not in body
assert 'planned total of 60 levels' in body
assert all(x in body for x in ['Grade 5 learners','Baluan Elementary School','Mountains, Hills, Plains, and Plateaus','2 GB RAM','300 MB free space','up to three gameplay stars'])
assert all(x in body for x in ['Piskel','Unity','C#','Clip Studio Paint','Visual Studio Code','Windows 11'])
assert '| D-025 |' in (VAULT/'Decisions'/'Decision Register.md').read_text(encoding='utf-8')
graph=re.search(r'```mermaid\s*\n([\s\S]*?)\n```',body).group(1)
assert graph.strip()==(ROOT/'proposed-flow.mmd').read_text().strip()
diagram=json.loads((ROOT/'diagram-check.json').read_text())
assert diagram['parsed'] is True
assert (VAULT/'Sources'/'Attachments'/'Chapter III - Proposed Flow - v1.svg').read_bytes()==(ROOT/'proposed-flow.svg').read_bytes()

before=json.loads((ROOT/'before-hashes.json').read_text())
after={str(p.relative_to(VAULT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in VAULT.rglob('*') if p.is_file()}
changed=[p for p in before if p in after and before[p]!=after[p]]
added=[p for p in after if p not in before]
assert not [p for p in before if p not in after]
assert not any(p.lower().endswith(('.docx','.pdf','.ppt','.jpg','.png','.csv')) for p in changed)
assert all(not p.startswith(('Sources\\Attachments\\','Sources\\Chapter III Unrevised Draft Extract')) for p in changed)
assert after[r'Sources\Attachments\Chapter III - Unrevised - 2026-11-01.docx']=='a4862da1fe16500cf708186be199e0833f43b21cb82caaaf762f67029cd94d4b'
assert hashlib.sha256((WORKSPACE/'Deliverables'/'Chapters I-II Corrections 2026-11-01'/'Land Grand - Chapter I - Corrected.docx').read_bytes()).hexdigest()=='8c877353238d7940924997b23539b1562cf42f683dc712179af9a6b281e014ed'
with ZipFile(ROOT/'vault-before.zip') as z: assert z.testzip() is None

spec=importlib.util.spec_from_file_location('vault_validator',WORKSPACE/'tools'/'validate_vault.py')
validator=importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
validation=validator.validate(VAULT,WORKSPACE/'tools'/'source-integrity.json')
assert not validation['errors'],validation
report={'required_main_sections':main,'section_introductions_checked':len(headings),'matching_cited_references':sorted(citations),'mermaid_parser_and_preview':'passed; complete raster preview visually inspected','live_obsidian_and_word_layout':'not checked; no Word revision requested','unchanged_existing_document_image_data_files':True,'source_extraction_unchanged':True,'retained_chapter3_hash_verified':True,'chapter1_reference_unchanged':True,'changed_notes':changed,'added_files':added,'vault_validation':validation}
(ROOT/'final-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
