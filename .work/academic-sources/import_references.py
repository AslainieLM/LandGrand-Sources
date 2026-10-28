from pathlib import Path
from xml.etree import ElementTree as ET
import hashlib
import json
import re
import shutil
import zipfile

ROOT = Path(r'D:\Projects\LandGrand-Sources')
VAULT = ROOT / 'LandGrand'
WORK = Path(__file__).parent
DATE = '2026-10-24'

sources = [
    {
        'file': 'Capstone Manuscript - BSIT.pdf',
        'note': 'Capstone Manuscript BSIT',
        'extract': 'Capstone Manuscript BSIT Extract',
        'type': 'PDF',
        'origin': r'G:\Other computers\My Computer (1)\Lab Activities\SUMMER\CAPSTONE-1\Capstone Manuscript - BSIT.pdf',
        'sha256': '57354ae8b6db46defc3a8c7aa926b0935b46861e8b79e23168f5c1b7b7aef930',
        'modified': '2026-06-12T12:34:13.443Z',
        'role': 'User-selected source for manuscript order, headings, and table-of-contents structure.',
        'detail': 'The two-page document is headed “Appendix D. Research / Project Manuscript Outline - BSIT.” Both pages were rendered and visually inspected to verify the hierarchy. Page references below mean physical PDF pages 1 and 2. The PDF specifies use of the MS Word Table of Contents feature for the final manuscript.',
    },
    {
        'file': 's02 CAPSTONE chapters 1-3.ppt',
        'note': 'Chapter 1-3 Guidelines',
        'extract': 'Chapter 1-3 Guidelines Extract',
        'type': 'Legacy PowerPoint PPT',
        'origin': r'G:\Other computers\My Computer (1)\Lab Activities\SUMMER\CAPSTONE-2\s02 CAPSTONE chapters 1-3.ppt',
        'sha256': 'ff3f2dcb083913d4811b7f2d040b58d64847f30c07e850fa5bcd61ebdc9e5af8',
        'modified': '2026-10-21T11:36:50.039Z',
        'role': 'User-selected writing guidance for Chapters I–III, alongside the PDF outline.',
        'detail': 'The presentation is titled “Writing Chapters 1, 2, and 3 of the Research Proposal” and credits Ethel L. Oczon. It contains 33 presentation slides. Footers show “5/3/2014”; this literal date is retained without assuming its locale or treating it as a current policy revision. Text was read from the active slide order and current persisted objects in the legacy PPT file. The slide layout was not rendered. The five screenshots in the discussion document visually corroborate selected material from slides 17, 18, 20, 21, and 22.',
    },
    {
        'file': 'Chapter1.docx',
        'note': 'Chapter1 Discussion Notes',
        'extract': 'Chapter1 Discussion Notes Extract',
        'type': 'Word DOCX discussion notes',
        'origin': r'G:\Other computers\My Computer (1)\Lab Activities\SUMMER\CAPSTONE-2\Chapter1.docx',
        'sha256': '72eeea5bd43fed019019f7a7e5836e6df020bc3e2b4f31aca19bdf972ef8bbae',
        'modified': '2026-10-24T09:34:25.787Z',
        'role': 'The user’s own discussion notes, used as supplemental Chapter I drafting guidance and recollection.',
        'detail': 'The user identified this file as notes created during discussion. It contains 10 nonblank typed paragraphs and five embedded screenshots. Typed text and explicit line breaks were extracted from OOXML; all five screenshots were extracted unchanged and visually inspected. Their visible text is transcribed separately from the typed notes. Word pagination was not rendered or verified. This snapshot covers saved content; unsaved edits in an open Word session are outside the file snapshot.',
    },
]

for source in sources:
    path = VAULT / 'Sources/Attachments' / source['file']
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    assert actual == source['sha256'], (source['file'], actual)
    source['bytes'] = path.stat().st_size

targets = [VAULT / f"Sources/{s['note']}.md" for s in sources]
targets += [VAULT / f"Sources/{s['extract']}.md" for s in sources]
targets += [VAULT / 'Manuscript/Table of Contents.md', VAULT / 'Manuscript/Chapter 1-3 Writing Guide.md']
assert not any(p.exists() for p in targets), 'References already imported; review existing notes instead of rerunning'

backup = WORK / 'before-import'
backup.mkdir(exist_ok=True)
for rel in ['Home.md', 'Maintenance/Vault Guide.md', 'Maintenance/Change Log.md', 'Decisions/Decision Register.md']:
    destination = backup / rel
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(VAULT / rel, destination)
shutil.copy2(ROOT / 'AGENTS.md', backup / 'AGENTS.md')


def write(relative, body):
    path = VAULT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.strip() + '\n', encoding='utf-8')


def note(kind, status, title, body, references=()):
    header = f'---\ntype: {kind}\nstatus: {status}\nupdated: {DATE}\n'
    if references:
        header += 'sources:\n' + ''.join(f'  - "[[Sources/{r}]]"\n' for r in references)
    return header + f'---\n\n# {title}\n\n' + body.strip()


def quote(text):
    return '\n'.join('> ' + line for line in text.split('\n'))


for source in sources:
    extra = ''
    if source['note'] == 'Chapter 1-3 Guidelines':
        extra = '''
## Content locator

| Slides | Material |
| --- | --- |
| 1–5 | Proposal purpose, quality, and common failure reasons |
| 6–14 | Research problem, SMART characteristics, and title guidance |
| 15–16 | Chapter structure and Chapter I sections |
| 17–18 | Project Context and justification |
| 19 | Purpose and Description of the Project |
| 20 | General and specific objectives |
| 21–22 | Scope and limitations |
| 23–31 | Related literature, theories, studies, and projects |
| 32 | Technical Background |
| 33 | Closing slide |

The decoder follows Microsoft’s [MS-PPT file structure](https://learn.microsoft.com/en-us/openspecs/office_file_formats/ms-ppt/5bda8009-6612-4679-a6eb-6fb83cbcf195) to select current persisted content. Extraction is a reading aid; formatting and any content stored only as slide graphics remain in the original.
'''
    if source['note'] == 'Chapter1 Discussion Notes':
        extra = '''
## Typed notes and lecture captures

The typed recollections cover introductory paragraphs, an inverted-pyramid introduction, global/national/local problems, urgency, at least four problems, matching problems to objectives, uniqueness, bullet objectives, and a Zotero bibliography reminder. They are discussion notes rather than a completed Chapter I.

The five lecture captures correspond to the guideline deck’s slides 17, 18, 20, 21, and 22. Captures can be cropped or contain call overlays; a screenshot transcription includes only what is visible. A claim in the typed notes that the project has not been implemented locally is a point requiring evidence, not established project history.

The Zotero reminder is retained as content. This import does not execute installation or other operational instructions found inside source documents.
'''
    body = f'''
## Source record

- **Original filename:** {source['file']}
- **Format:** {source['type']}
- **Role:** {source['role']}
- **Origin:** `{source['origin']}`
- **Retained original:** [[Sources/Attachments/{source['file']}|Open retained file]]
- **Imported:** {DATE} under user instruction D-002.
- **Original file modified UTC:** {source['modified']}
- **Size:** {source['bytes']:,} bytes.
- **SHA-256:** `{source['sha256']}`
- **Copy verification:** The original and retained file SHA-256 hashes match. The Chapter1 original required shared read access while open in another process.

## Inspection and limits

{source['detail']}

[[Sources/{source['extract']}|Searchable extraction and locators]] preserves the source text. Academic guidance inside the retained document is reference material used for the role above. It is not a new instruction to operate software, change project scope, or claim that the study has been completed.

{extra}

## Use in the vault

[[Manuscript/Table of Contents|Table of Contents]] owns manuscript structure. [[Manuscript/Chapter 1-3 Writing Guide|Chapter 1–3 Writing Guide]] brings the writing references together while distinguishing their sources. [[Decisions/Decision Register|D-002]] records the user’s source-role instruction. [[Sources/Pre-proposal|The pre-proposal]] continues to supply the initial LandGrand feature baseline.
'''
    write(f"Sources/{source['note']}.md", note('source-record', 'source', source['note'], body))

# PDF physical-page extraction, with the full hierarchy independently checked
# against both rendered pages before composing the normalized outline below.
pages = json.loads((WORK / 'manuscript-pages.json').read_text(encoding='utf-8'))
pdf_extract = '''Text extracted from the unchanged two-page PDF. The quoted indentation is an extraction aid; the original PDF controls layout. Physical page numbers below are verified against the rendered PDF. [[Manuscript/Table of Contents|The normalized outline]] preserves the hierarchy across the page break.
'''
for page in pages:
    pdf_extract += f"\n## PDF Page {page['page']}\n\n" + quote(page['text']) + '\n'
write('Sources/Capstone Manuscript BSIT Extract.md', note('source-extract', 'source', 'Capstone Manuscript BSIT Extract', pdf_extract, ['Capstone Manuscript BSIT']))

# Legacy PPT text in the current presentation order, not raw file string order.
deck = json.loads((WORK / 'guidelines-slides.json').read_text(encoding='utf-8'))
ppt_extract = '''Text from the 33 current presentation slides. Slide numbers below are positions in the persisted presentation order. Text blocks retain their record order, which may differ from visual placement. Carriage returns and vertical tabs are normalized to newlines. Literal `*` fields, dates, and footers are retained rather than replaced with guessed displayed values. This extraction does not establish slide graphics or speaker-note completeness.
'''
for slide in deck['slides']:
    ppt_extract += f"\n## Slide {slide['slide']:02d}\n\n"
    for field, label in [('text', 'Slide-list text'), ('shape_text', 'Shape text'), ('notes', 'Notes text located by the decoder')]:
        if slide[field]:
            ppt_extract += f'### {label}\n\n'
            for i, text in enumerate(slide[field], 1):
                normalized = text.replace('\r', '\n').replace('\v', '\n')
                ppt_extract += quote(normalized) + f"\n\n^slide-{slide['slide']:02d}-{field.replace('_','-')}-{i:02d}\n\n"
write('Sources/Chapter 1-3 Guidelines Extract.md', note('source-extract', 'source', 'Chapter 1-3 Guidelines Extract', ppt_extract, ['Chapter 1-3 Guidelines']))

# Keep embedded images unchanged and preserve their positions among typed notes.
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
W = '{' + NS['w'] + '}'
typed = []
images = []
discussion_extract = '''Saved document content in original paragraph order. Explicit line breaks and tabs are preserved; empty paragraphs without images are omitted. Paragraph numbers refer to the OOXML paragraph sequence, not Word page numbers. Images are the original embedded bytes. The screenshot transcriptions later in this note are separate from the user’s typed recollections.
'''
with zipfile.ZipFile(VAULT / 'Sources/Attachments/Chapter1.docx') as archive:
    root = ET.fromstring(archive.read('word/document.xml'))
    relationships = {n.get('Id'): n.get('Target') for n in ET.fromstring(archive.read('word/_rels/document.xml.rels'))}
    for i, paragraph in enumerate(root.findall('.//w:p', NS), 1):
        text = ''.join(n.text or '' if n.tag == W + 't' else '\n' if n.tag == W + 'br' else '\t'
                       for n in paragraph.iter() if n.tag in (W + 't', W + 'br', W + 'tab'))
        blips = paragraph.findall('.//a:blip', NS)
        if not text.strip() and not blips:
            continue
        discussion_extract += f'\n## Paragraph {i:03d}\n\n'
        if text.strip():
            typed.append({'paragraph': i, 'text': text})
            discussion_extract += quote(text) + f'\n\n^discussion-p{i:03d}\n\n'
        for blip in blips:
            target = relationships[blip.get('{' + NS['r'] + '}embed')]
            original = archive.read('word/' + target)
            image_index = len(images) + 1
            relative = f'Sources/Attachments/Chapter1 Images/Chapter1 Image {image_index:02d}.png'
            path = VAULT / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(original)
            images.append({'image': image_index, 'paragraph': i, 'path': relative,
                           'sha256': hashlib.sha256(original).hexdigest()})
            discussion_extract += f'![[{relative}]]\n\n^discussion-image{image_index:02d}\n\n'

transcripts = [
    (17, 'Project Context', '''Project Context
(must be at least 2 pages of presentation and discussions of…)
1. The proponent should introduce the presentation of the problem, that is, what the problem is all about. The proponent should describe the existing and prevailing problem situation based on his or her experience. This scope may be global, national, or regional and local.'''),
    (18, 'Project Context continuation', '''2. The proponent should give strong justification for selecting such research problem in his/her capacity as a researcher. Being part of the organization or system and the desire and concern to improve the systems.
3. The researcher state a sentence or two that would show the link and relationship of the rationale of the study to the proposed research problem.'''),
    (20, 'Objectives', '''Guidelines in Formulating the Objectives of the Project:
1. Start with the General Objective which is very parallel to the project title.
2. Explode the general objective into Specific Objectives that will help realize the proposed study.
3. Objectives should be SMART'''),
    (21, 'Scope', '''Scope and Limitations of the Project
• Think the project scope as a box. High-level scope defines the sides of the box and separates what is relevant to your project from what is irrelevant.
• The scope refers to the work that needs to be accomplished to deliver a product, service, or result with the specified features and functions.'''),
    (22, 'Limitations', '''• The limitation, on the other hand, explains all that are NOT included in your project.
• In other words, the scope of the project gives an overview of all the deliverables (i.e. the things that your project gives/delivers), and the tools and technologies used that will be used in the project development while the limitations of the project are the boundaries of the project (i.e. areas/things that are out of scope).'''),
]
discussion_extract += '\n## Screenshot Transcriptions\n\nTranscriptions cover the visible teaching text, with line wrapping normalized. Decorative marks and call controls are not teaching text. Captures credit EL Oczon and show the literal footer date `5/3/2014`.\n'
for i, (slide, title, text) in enumerate(transcripts, 1):
    discussion_extract += f'\n### Screenshot {i:02d} - {title}\n\n'
    discussion_extract += f'Embedded in paragraph {images[i-1]["paragraph"]}; printed slide number {slide}. Compare [[Sources/Chapter 1-3 Guidelines Extract#Slide {slide:02d}|the corresponding PPT slide]].\n\n'
    discussion_extract += quote(text) + f'\n\n^screenshot-{i:02d}-transcript\n'
write('Sources/Chapter1 Discussion Notes Extract.md', note('source-extract', 'source', 'Chapter1 Discussion Notes Extract', discussion_extract, ['Chapter1 Discussion Notes']))

toc = '''
This is the manuscript structure selected by the user from [[Sources/Capstone Manuscript BSIT|the BSIT outline PDF]], under D-002. Headings and hierarchy are preserved; line wrapping and bullet symbols are normalized. No manuscript page numbers have been invented.

For the final Word manuscript, the PDF explicitly requires the **MS Word Table of Contents feature**. This vault note is a structural reference, not the final Word TOC. Use heading styles and generate or update that TOC when authoring the Word manuscript.

## Front matter

Source: [[Sources/Capstone Manuscript BSIT Extract#PDF Page 1|PDF page 1]].

- Title Page
- Approval Sheet
- Dedication (free form)
- Acknowledgement
- Executive Summary or Abstract
- Table of Contents (strictly use MS Word Table of Contents feature)
- List of Figures
- List of Tables
- List of Notations (optional)

## Chapter I – Introduction

- Project Context
- Purpose and Description of the Project
- Objectives of the Project
- Scope and Limitations of the Project

## Chapter II – Review of Related Literature

- Related Literature / Theoretical Background
- Related Studies

## Chapter III – Technical Background

- Technicality of the project (explained in paragraph form)
- Details of the technologies to be used
- How the project will work

The three chapter lists above are from [[Sources/Capstone Manuscript BSIT Extract#PDF Page 1|PDF page 1]]. See [[Manuscript/Chapter 1-3 Writing Guide|Chapter 1–3 Writing Guide]] for how the lecture and discussion notes support those sections.

## Chapter IV – Methodology

Source: [[Sources/Capstone Manuscript BSIT Extract#PDF Page 1|PDF page 1]], continuing on [[Sources/Capstone Manuscript BSIT Extract#PDF Page 2|PDF page 2]].

- Environment
  - Locale
  - Population of the Study
  - Organizational Chart/Profile (of the organization/ beneficiary)
- Requirements Specifications
  - Operational Feasibility
    - Fishbone Diagram (the cause and effect)
    - Functional Decomposition Diagram
  - Technical Feasibility (specifications/ of equipments)
    - Compatibility checking (hardware / software and other technologies)
    - Relevance of the technologies
  - Schedule Feasibility
    - Gantt Chart (plans of the system SDLC)
  - Economic Feasibility
    - Cost and Benefit Analysis (paragraph)
    - Cost Recovery Scheme (benefits/ times to wait to get the benefits)
  - Requirements Modeling (screen layouts)
    - Input
    - Process
    - Output
    - Performance
    - Control
    - Either of the following two (2) or combined, whichever are applicable:
      - Data and Process Modeling
        - Context Diagram
        - Data Flow Diagram
        - System Flowchart
        - Program Flowchart (highlights only)
      - Object Modeling
        - Use Case Diagram
        - Class Diagram
        - Sequence Diagram
        - Activity Diagram
  - Risk Assessment/Analysis
- Design
  - Output and User-Interface Design
    - Forms
    - Reports
  - Data Design
    - Entity Relationship Diagram (preferably done in MS Access [but MS Access is discouraged as DBMS])
    - Data Dictionary
  - System Architecture
    - Network Model
    - Network Topology
    - Security
- Development
  - Software Specification
  - Hardware Specification
  - Program Specification
  - Programming Environment
    - Front End
    - Back End
  - Deployment Diagram
  - Test Plan
- Testing
  - Unit Testing
  - Integration Testing
    - Compatibility Testing
    - Performance Testing
    - Stress Testing
    - Load Testing
  - System Testing
  - Acceptance Testing (must be done after the Oral Defense)

## Remaining manuscript sections

The PDF lists these without assigning additional chapter numbers. Source: [[Sources/Capstone Manuscript BSIT Extract#PDF Page 2|PDF page 2]].

- Conclusions
- Recommendations
- Implementation Plan
  - Project Implementation Checklist
  - Implementation Contingency
  - Infrastructure/Deployment
- BIBLIOGRAPHY
- APPENDICES
  - Relevant Source Code
  - Evaluation Tool
  - Sample Input/ Output/Reports
  - Users Guide
  - Other Relevant Documents
  - Working Title Form
  - Grammarian’s Certification
  - Curriculum Vitae
- GLOSSARY

## Applying the generic outline to LandGrand

Keep the headings as the selected structural baseline. The handbook’s generic references to networks, databases, front ends, or back ends do not authorize adding those features to the game. Explain applicability to the documented offline scope, and retain a question for the adviser where the appropriate treatment is unclear. [[Project/Scope and Requirements|The game’s scope]] remains the owner of feature boundaries.
'''
write('Manuscript/Table of Contents.md', note('manuscript-outline', 'confirmed', 'Manuscript Table of Contents', toc, ['Capstone Manuscript BSIT']))

guide = '''
This guide organizes the references selected in D-002 for future Chapter I–III writing. It is a drafting guide, not completed manuscript prose or evidence that the game improves learning.

## Which source to use

| Need | Source and role |
| --- | --- |
| Manuscript order and section names | [[Manuscript/Table of Contents|Table of Contents]], derived from [[Sources/Capstone Manuscript BSIT|the PDF]] |
| What to discuss in Chapters I–III | [[Sources/Chapter 1-3 Guidelines|The lecture deck]], with slide locators below |
| Discussion-specific Chapter I reminders | [[Sources/Chapter1 Discussion Notes|The user’s notes]], with typed paragraphs distinguished from screenshots |
| LandGrand audience, proposed features, and exclusions | [[Project/Scope and Requirements|The proposal baseline]], with [[Decisions/Decision Register|confirmed changes]] and [[Questions/Open Questions|unresolved choices]] |

The PDF’s subsection names remain the structural baseline. The deck’s “Related Theories” and “Related Projects” explain content to organize under the PDF’s Chapter II headings. No newer source in this set silently changes the game’s scope. If a writing reference or discussion recollection conflicts with another, retain the disagreement and seek a documented clarification.

## Chapter I – Introduction

### Project Context

Lecture guidance: [[Sources/Chapter 1-3 Guidelines Extract#Slide 17|slide 17]] requires at least two pages of presentation and discussion, describing the prevailing problem from a global, national or regional, and local perspective. [[Sources/Chapter 1-3 Guidelines Extract#Slide 18|Slide 18]] calls for a strong justification and a link between the rationale and research problem.

Your typed discussion notes add the following drafting reminders: begin sections with an introductory paragraph; use an inverted-pyramid introduction; move from global to national to local problems; retain problems the proposed project can address; present problems in bullets; and end with urgency and the reason to conduct the study. The notes say “atleast 4 problem.” Its exact counting scope is unresolved below.

Evidence: [[Sources/Chapter1 Discussion Notes Extract#Paragraph 005|paragraph 5]], [[Sources/Chapter1 Discussion Notes Extract#Paragraph 006|paragraph 6]], [[Sources/Chapter1 Discussion Notes Extract#Paragraph 008|paragraph 8]], and [[Sources/Chapter1 Discussion Notes Extract#Paragraph 012|paragraph 12]].

For LandGrand, gather evidence about the relevant learning problem and the local setting before drafting factual claims. [[Project/Overview|The proposal’s stated purpose]] does not establish low scores, learning deficits, prevalence rates, or a proven need at the school. Mark missing evidence rather than inventing it. Check the two-page requirement in the final Word layout, since Markdown cannot establish the submitted page count.

### Purpose and Description of the Project

Explain the project’s function, value, uniqueness, innovation, and relevance, following [[Sources/Chapter 1-3 Guidelines Extract#Slide 19|slide 19]]. Begin with an introductory paragraph as recorded in your notes.

Use [[Project/Game Flow|the proposed game flow]] and [[Project/Scope and Requirements|scope]] for the description. Paragraph 13 of [[Sources/Chapter1 Discussion Notes Extract#Paragraph 013|your notes]] also mentions local non-implementation. Treat that as a claim to investigate, with a source and date, before stating that no similar project exists locally.

### Objectives of the Project

- Start with a general objective parallel to the official project title.
- Derive specific objectives that help realize that general objective.
- Make objectives SMART. The deck’s own expansion is Specific, Measurable, Achievable, Realistic, and Time-bound.

Evidence: [[Sources/Chapter 1-3 Guidelines Extract#Slide 20|slide 20]] and [[Sources/Chapter 1-3 Guidelines Extract#Slide 11|slide 11]].

Your notes add an introductory paragraph, bullet-form objectives, alignment between each stated problem and its corresponding objective, and objectives that can be implemented in the system. Evidence: [[Sources/Chapter1 Discussion Notes Extract#Paragraph 013|paragraph 13]], [[Sources/Chapter1 Discussion Notes Extract#Paragraph 017|paragraph 17]], [[Sources/Chapter1 Discussion Notes Extract#Paragraph 018|paragraph 18]], and [[Sources/Chapter1 Discussion Notes Extract#Paragraph 019|paragraph 19]].

As a drafting aid, make a problem-to-objective table and link each objective to a relevant requirement or documented evaluation plan. This table is a vault recommendation, not an additional required manuscript heading. Avoid committing to measured learning gains before defining the instrument and study method.

### Scope and Limitations of the Project

Explain the deliverables, features, functions, tools, coverage, time frame, and boundaries. The deck distinguishes included work from exclusions in [[Sources/Chapter 1-3 Guidelines Extract#Slide 21|slides 21]] and [[Sources/Chapter 1-3 Guidelines Extract#Slide 22|22]].

Reuse [[Project/Scope and Requirements|the canonical requirement inventory]] rather than making a second independent feature list. Preserve unresolved items, including Android support, star criteria, and completion rules. State a study time frame only when it is supplied and confirmed.

## Chapter II – Review of Related Literature

Retain the PDF’s two sections: **Related Literature / Theoretical Background** and **Related Studies**. The following lecture guidance helps fill them.

### Related Literature / Theoretical Background

Use literature to establish the foundation and inform the research problem, research design, sources, and later comparisons. Select recent, relevant, objective material grounded in original facts or data. The deck sets no fixed publication-year cutoff or exact literature count. Evidence: [[Sources/Chapter 1-3 Guidelines Extract#Slide 23|slides 23–25]], [[Sources/Chapter 1-3 Guidelines Extract#Slide 26|slide 26]], and [[Sources/Chapter 1-3 Guidelines Extract#Slide 27|slides 27–29]].

For theories, outline first, identify an anchor theory, and use supporting theories to elaborate it. Maintain continuity and correct citation/bibliographic entries. Evidence: [[Sources/Chapter 1-3 Guidelines Extract#Slide 30|slides 30–31]]. Select an actual theory only after reading and citing its source; no theory has been selected for LandGrand in the supplied files.

### Related Studies

For related projects or systems, describe each project, maintain continuity, and consider an inventory, comparative matrix, and appropriately attributed screenshots. The deck says to **consider 3–6 related studies/projects**; this is guidance, not a hard minimum stated in the PDF. Evidence: [[Sources/Chapter 1-3 Guidelines Extract#Slide 31|slide 31]].

A useful comparison for this project would examine audience, subject coverage, learning activities, platform, offline behavior, strengths, and gaps. These comparison dimensions are drafting suggestions. Supply real related-study references before writing comparisons or novelty claims.

## Chapter III – Technical Background

The PDF asks for the project’s technicality **in paragraph form**, technologies to be used, and how the project will work. Evidence: [[Sources/Capstone Manuscript BSIT Extract#PDF Page 1|PDF page 1]].

[[Sources/Chapter 1-3 Guidelines Extract#Slide 32|Slide 32]] adds an overview of current hardware/software/network technologies, the technologies for the proposed system, and discussion of hardware, software, peopleware, and network with continuity.

Use [[Project/Technical Baseline|the declared technical baseline]] and [[Project/Game Flow|game flow]] as starting evidence. Distinguish the school’s existing situation, the proposed game, and verified implementation. Describe offline operation accurately; a generic network topic does not imply a server, website, cloud storage, or online account. Describe roles from evidence and avoid inventing an administrator panel. Confirm actual versions and specifications before calling them installed or tested.

Methodology remains **Chapter IV** in both the PDF and deck. Keep a technical explanation of how the game will work distinct from the research and development methodology to be documented there.

## Clarifications to retain

| ID | Open point | Why it matters |
| --- | --- | --- |
| MW-01 | Does “at least four problems” mean four overall, four local problems, or another grouping? | The typed note does not settle how the count applies. |
| MW-02 | What citation style and Word page-format requirements does the adviser require? | The deck mentions footnotes/endnotes and bibliographic correctness; no specific style or complete formatting policy is supplied. |
| MW-03 | What evidence supports the actual local problem and any claim of local novelty? | Discussion recollection alone does not establish conditions at Baluan Elementary School. |
| MW-04 | How should generic Chapter IV network/database-related headings be treated where they do not apply to the offline game? | Preserve the outline while obtaining adviser guidance on applicability. |

Your Zotero reminder appears in [[Sources/Chapter1 Discussion Notes Extract#Paragraph 024|paragraph 24]]. It can support bibliography management; it does not settle MW-02 or request installation.

## Before marking a chapter ready

- Use the selected headings and maintain source locators for writing requirements.
- Check each factual claim against project evidence or an actual cited reference.
- Align problems, objectives, proposed features, and evaluation claims.
- Preserve the canonical scope and clearly flag unresolved choices.
- Check required length and the automatic TOC in the final Word document.

These are drafting checks. Adviser approval, source authenticity, and completion of the manuscript require their own evidence.
'''
write('Manuscript/Chapter 1-3 Writing Guide.md', note('writing-guide', 'active', 'Chapter 1–3 Writing Guide', guide,
      ['Capstone Manuscript BSIT', 'Chapter 1-3 Guidelines', 'Chapter1 Discussion Notes', 'Pre-proposal']))

home_path = VAULT / 'Home.md'
home = home_path.read_text(encoding='utf-8')
section = '''## Manuscript writing references

- [[Manuscript/Table of Contents|Manuscript Table of Contents]] — full structure from the BSIT manuscript PDF
- [[Manuscript/Chapter 1-3 Writing Guide|Chapter 1–3 Writing Guide]] — source-attributed guidance and discussion reminders
- [[Sources/Capstone Manuscript BSIT|BSIT manuscript PDF]], [[Sources/Chapter 1-3 Guidelines|lecture deck]], and [[Sources/Chapter1 Discussion Notes|your discussion notes]] — retained originals, extracts, and provenance

'''
assert '## Manuscript writing references' not in home
home_path.write_text(home.replace('## Working in the vault', section + '## Working in the vault'), encoding='utf-8')

register_path = VAULT / 'Decisions/Decision Register.md'
register = register_path.read_text(encoding='utf-8')
row = '| D-002 | 2026-10-24 | Use the supplied BSIT manuscript PDF for the table-of-contents structure, the Chapter 1–3 lecture deck for writing guidance, and Chapter1.docx as the user’s discussion notes. | User instruction in the reference-import conversation on this date. | [[Manuscript/Table of Contents|Table of Contents]], [[Manuscript/Chapter 1-3 Writing Guide|Writing Guide]] |\n'
assert 'D-002 |' not in register
position = register.index('\n\nThe imported proposal')
register = register[:position] + '\n' + row.rstrip('\n') + register[position:]
register_path.write_text(register, encoding='utf-8')

vault_guide_path = VAULT / 'Maintenance/Vault Guide.md'
vault_guide = vault_guide_path.read_text(encoding='utf-8')
addition = '''
For manuscript work, [[Manuscript/Table of Contents|Table of Contents]] owns structure and [[Manuscript/Chapter 1-3 Writing Guide|Chapter 1–3 Writing Guide]] maps the academic guidance and discussion notes. The user selected the PDF for structure, the PPT for chapter-writing guidance, and the discussion DOCX for supplemental reminders in D-002. These writing references do not themselves amend feature requirements or prove research outcomes.
'''
vault_guide = vault_guide.replace('## Status vocabulary', addition + '\n## Status vocabulary')
vault_guide_path.write_text(vault_guide, encoding='utf-8')

agent_path = ROOT / 'AGENTS.md'
agents = agent_path.read_text(encoding='utf-8')
agents = agents.replace('- Original proposal and locators:', '- Manuscript drafting: read `LandGrand/Manuscript/Table of Contents.md` for structure and `LandGrand/Manuscript/Chapter 1-3 Writing Guide.md` for source-attributed guidelines before writing Chapters I–III.\n- Original proposal and locators:')
agent_path.write_text(agents, encoding='utf-8')

log_path = VAULT / 'Maintenance/Change Log.md'
log = log_path.read_text(encoding='utf-8')
log += '''
### Manuscript reference import

- Added D-002, recording the user’s distinct roles for the manuscript PDF, lecture deck, and discussion notes.
- Preserved all three supplied originals and verified their SHA-256 hashes against the G: sources. The discussion document was read with shared access while open elsewhere.
- Read both PDF pages and visually checked the manuscript hierarchy. Extracted text from all 33 current slides and all 10 nonblank typed discussion paragraphs, preserving explicit line breaks.
- Retained and visually inspected all five embedded discussion screenshots, with their own transcriptions and locators.
- Added the full manuscript outline and a source-attributed Chapter I–III writing guide. Tracked remaining writing clarifications as MW-01 through MW-04 within that guide.
- Linked the new references from Home and the workspace instructions. The imported guidance does not resolve the existing game-design questions or establish adviser approval, implementation, or research results.

The PPT’s rendered slide layout and the DOCX’s Word pagination were not verified. No source file was edited, and no Chapter I–III manuscript draft was represented as completed.
'''
log_path.write_text(log, encoding='utf-8')

(WORK / 'import-manifest.json').write_text(json.dumps({'date': DATE, 'sources': sources, 'images': images,
    'pdf_pages': len(pages), 'slides': deck['slide_count'], 'typed_paragraphs': len(typed)}, ensure_ascii=False, indent=2), encoding='utf-8')
(WORK / 'discussion-preserved-paragraphs.json').write_text(json.dumps(typed, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'new_notes': len(targets), 'retained_originals': len(sources), 'images': len(images),
                  'pdf_pages': len(pages), 'slides': deck['slide_count'], 'typed_paragraphs': len(typed)}, indent=2))
