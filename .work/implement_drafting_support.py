from pathlib import Path
import hashlib
import json
import re
import shutil
import zipfile

ROOT = Path(r'D:\Projects\LandGrand-Sources')
V = ROOT / 'LandGrand'
DATE = '2026-10-24'
WORK = ROOT / '.work/drafting-support'
WORK.mkdir(parents=True, exist_ok=True)

new_notes = ['Manuscript/Drafting Dashboard.md', 'Manuscript/Evidence Register.md',
             'Manuscript/Drafts/Chapter I Introduction.md',
             'Manuscript/Drafts/Chapter II Review of Related Literature.md',
             'Manuscript/Drafts/Chapter III Technical Background.md',
             'Maintenance/Skill Reference.md']
assert not any((V / name).exists() for name in new_notes), 'Drafting support already exists; review in place'

# A local rollback snapshot, not a claim of independent backup protection.
snapshot = WORK / 'vault-before-drafting-support.zip'
assert not snapshot.exists(), 'Preserve the existing rollback snapshot'
with zipfile.ZipFile(snapshot, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
    for path in V.rglob('*'):
        if path.is_file():
            archive.write(path, path.relative_to(V).as_posix())
shutil.copy2(ROOT / 'AGENTS.md', WORK / 'Sources-AGENTS-before.md')


def write(relative, text):
    path = V / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + '\n', encoding='utf-8')


def note(kind, title, body, status='active', sources=()):
    header = f'---\ntype: {kind}\nstatus: {status}\nupdated: {DATE}\n'
    if sources:
        header += 'sources:\n' + ''.join(f'  - "[[{s}]]"\n' for s in sources)
    return header + f'---\n\n# {title}\n\n' + body.strip()


old_router = (V / 'Maintenance/Skill Guide.md').read_text(encoding='utf-8')
old_word_count = len(old_router.split())
reference = old_router.replace('# LandGrand Skill Guide', '# Skill Reference', 1)
start = reference.index('## Communication and token use')
end = reference.index('## Automatic selection', start)
reference = reference[:start] + ('Read [[Maintenance/Skill Guide|Skill Guide]] for the short entry route and communication preference. '
    'Use the detailed material below when the requested workflow needs it.\n\n') + reference[end:]
write('Maintenance/Skill Reference.md', reference)

write('Maintenance/Skill Guide.md', note('guide', 'LandGrand Skill Guide', '''
Read [[Current Focus]] for the active priority. For Chapters I–III, start at [[Manuscript/Drafting Dashboard|Drafting Dashboard]].

## Communication and token use

Use `caveman` for chat until the user requests `stop caveman` or `normal mode`. Preserve technical facts and necessary qualifications. Use normal prose for questions and persisted artifacts. Read its instructions at `C:\\Users\\user\\.codex\\skills\\caveman\\SKILL.md` when needed.

## Select the route

| Request | Read next |
| --- | --- |
| Draft or continue a chapter | Dashboard row for the target section, its working draft, and the relevant part of [[Manuscript/Chapter 1-3 Writing Guide|Writing Guide]] |
| Improve existing prose | [[Manuscript/Chapter 1-3 Writing Guide#Language editing skills|Language editing skills]] |
| Support a claim or add a reference | [[Manuscript/Evidence Register|Evidence Register]] and the actual source |
| Read or produce Word, PDF, or slides | The matching available artifact skill and relevant source record |
| Feature work, debugging, refactoring, or other workflows | Relevant branch in [[Maintenance/Skill Reference|Skill Reference]] |

Choose from the current skill catalog. Read the selected `SKILL.md`; add a specialist only for a distinct need. Respect explicit user choices and existing authorization. Ask only about material missing decisions; continue independent work. Preserve original sources and unresolved claims.

Load the target section and its evidence rather than every chapter or reference. Update the dashboard when drafting progress changes. Report the actual checks and remaining gaps.
'''))

write('Manuscript/Drafting Dashboard.md', note('manuscript-dashboard', 'Chapters I–III Drafting Dashboard', '''
Use this as the entry point for the current manuscript work. The three working files contain headings and prompts only; no finished chapter prose or adviser approval is claimed. Status here covers drafts in this vault, not unseen files elsewhere.

## Now

- [ ] Draft the Purpose and Description section from the pre-proposal. This can begin without inventing local problem statistics.
- [ ] Assemble evidence for Project Context using [[Manuscript/Evidence Register|Evidence Register]].
- [ ] Record the intended citation style and page formatting when confirmed; see MW-02 in [[Manuscript/Chapter 1-3 Writing Guide#Clarifications to retain|writing clarifications]].

## Section board

| Chapter and section | Working draft | Status | Next action |
| --- | --- | --- | --- |
| I — Project Context | [[Manuscript/Drafts/Chapter I Introduction#Project Context|Open section]] | Scaffold only; evidence needed | Find credible global/national evidence and actual local observations; use E-01–E-03. |
| I — Purpose and Description | [[Manuscript/Drafts/Chapter I Introduction#Purpose and Description of the Project|Open section]] | Scaffold only; proposal available | Draft the intended function and learning loop; use E-04 and distinguish proposed benefits from results. |
| I — Objectives | [[Manuscript/Drafts/Chapter I Introduction#Objectives of the Project|Open section]] | Scaffold only | Draft a title-aligned general objective; link each specific objective to an evidenced problem. |
| I — Scope and Limitations | [[Manuscript/Drafts/Chapter I Introduction#Scope and Limitations of the Project|Open section]] | Scaffold only; proposal available | Normalize the current boundaries; keep E-09 open rather than choosing an Android range silently. |
| II — Related Literature / Theoretical Background | [[Manuscript/Drafts/Chapter II Review of Related Literature#Related Literature / Theoretical Background|Open section]] | Scaffold only; sources needed | Select and read actual literature and theory sources; use E-06. |
| II — Related Studies | [[Manuscript/Drafts/Chapter II Review of Related Literature#Related Studies|Open section]] | Scaffold only; sources needed | Read and compare real studies or projects; use E-07. |
| III — Technicality of the project | [[Manuscript/Drafts/Chapter III Technical Background#Technicality of the project|Open section]] | Scaffold only; proposal available | Explain the proposed technical approach in paragraphs. |
| III — Details of the technologies to be used | [[Manuscript/Drafts/Chapter III Technical Background#Details of the technologies to be used|Open section]] | Scaffold only; verification needed | Explain declared technologies and verify versions only when claiming actual configuration; use E-08. |
| III — How the project will work | [[Manuscript/Drafts/Chapter III Technical Background#How the project will work|Open section]] | Scaffold only; proposal available | Describe the intended offline flow; label unresolved rules and planned behavior. |

Progress states: **Scaffold only**, **Drafting**, **Needs evidence**, **Ready for user review**, and **Reviewed**. Add a date and the actual draft location when changing a state. Review status requires evidence of the review.

## Next

- Develop the remaining sections in the order the user requests.
- Keep problem/objective alignment in the Chapter I working file and claim/source tracking in Evidence Register.
- Apply grammar and academic polishing after each section's meaning and evidence are stable.
- When producing Word output, use the selected headings, automatic TOC, and the document skill's layout verification.

## Blocked claims and decisions

Local problem and local novelty claims need evidence before being presented as facts. Literature/theory claims need actual sources. MW-01 and MW-02 affect final presentation; retain them while drafting other sections. Q-01 affects the final device-support wording. Detailed scoring and unlocking decisions affect descriptions of those rules, not every manuscript section.

Research evaluation belongs under the supplied Chapter IV structure. For Chapters I–III, describe an intended benefit or objective honestly; do not present invented learning gains or a completed study.

## Section readiness check

- [ ] Required heading and discussion guidance followed.
- [ ] Factual claims have a source and locator, or a visible unresolved marker.
- [ ] Proposal intent, discussion recollection, verified facts, and measured results are distinguished.
- [ ] Problems and objectives agree; scope matches the canonical requirements.
- [ ] Terminology and citations are consistent; grammar has been reviewed.
- [ ] User decisions and remaining issues are recorded; no approval is assumed.

The [vault validator](../../tools/validate_vault.py) checks links, configuration syntax, and retained-source integrity. It does not verify scientific claims, manuscript quality, or adviser approval. Run it from the source workspace using the bundled Python runtime. See [[Maintenance/Vault Guide#Validation and recovery|validation and recovery]] for the exact command.
''', sources=['Manuscript/Table of Contents', 'Manuscript/Chapter 1-3 Writing Guide']))

write('Manuscript/Evidence Register.md', note('evidence-register', 'Manuscript Evidence Register', '''
Track what a draft may claim and where that claim is supported. “Missing” means the vault currently has no supporting evidence entered here; it is not a finding that the claim is false. Add source details after reading the source, not from a citation guessed by a model.

## Claim and source inventory

| ID | Claim or material to support | Current evidence | State | Draft use and next action |
| --- | --- | --- | --- | --- |
| E-01 | Global context for the relevant Grade 5 learning problem | No specific research source entered | Missing | Chapter I Context: find relevant original studies or authoritative reports; retain population, date, and limitations. |
| E-02 | Philippine/national context for the same problem | No specific national source entered | Missing | Chapter I Context: find evidence matching the subject and population; do not substitute unrelated performance figures. |
| E-03 | Actual problem at Baluan Elementary School | Proposal identifies the setting but supplies no local baseline results | Missing | Chapter I Context: obtain an actual documented observation, school record, or discussion record with date and attribution. |
| E-04 | LandGrand audience, intended purpose, features, and exclusions | [[Sources/Pre-proposal|Pre-proposal]] and [[Project/Scope and Requirements|requirements]] | Proposal | Chapters I and III: describe these as proposed specifications unless later confirmation establishes more. |
| E-05 | Novelty or absence of similar local projects | [[Sources/Chapter1 Discussion Notes Extract#Paragraph 013|Discussion recollection]] only | Unverified | Purpose and Chapter II: verify the comparison and its limits before claiming no comparable local project exists. |
| E-06 | Selected theory and supporting literature | No theory or literature sources selected in the retained sources | Missing | Chapter II: record actual references and explain their relevance; do not invent an anchor theory. |
| E-07 | Related studies, games, or systems and their findings | No specific related-study references entered | Missing | Chapter II: record each study's method, participants, findings, limitations, and relevance. |
| E-08 | Technical choices, versions, and operation | [[Project/Technical Baseline|Declared technical baseline]] and [[Project/Game Flow|proposed flow]] | Proposal | Chapter III: use original documentation for technical explanations and direct project evidence for actual version/configuration claims. |
| E-09 | Supported Android version range | [[Project/Scope and Requirements#Device requirements requiring reconciliation|LG-25]] has inconsistent source wording | Conflict | Scope and Chapter III: retain Q-01 and obtain a confirmed range before presenting it as settled. |
| E-10 | Measured learning effectiveness | [[Project/Research and Evaluation|Evaluation method and results are undocumented]] | Missing | Describe the intended benefit; establish a method and results before claiming effectiveness. |

## Adding a reference

For each actual reference, record its title, authors/organization, date, URL or DOI, retained source note, and the exact page/section supporting the claim. Include what was studied, relevant findings, limits, the claim ID, and the chapter section using it. Keep bibliographic metadata usable while MW-02's citation-style choice remains open.

Use a source record in `Sources` and link to the retained material. Literature findings belong with their source note; this register owns their link to manuscript claims. Source files and quotations remain unchanged when editing prose.

## Claim-state rules

**Proposal** supports statements of intent. **Verified source** means the supporting source and locator were inspected; it does not make findings universal. **Conflict** retains competing evidence. **Missing** or **Unverified** claims remain visible in drafting notes and must be resolved or carefully limited before a section is ready for review.

The lecture and discussion notes guide writing. They do not establish geological facts, local school conditions, or the game's effectiveness.
'''))

draft_sources = ['Manuscript/Table of Contents', 'Manuscript/Chapter 1-3 Writing Guide', 'Sources/Pre-proposal']
write('Manuscript/Drafts/Chapter I Introduction.md', note('manuscript-draft', 'Chapter I Introduction', '''
> [!todo] Working scaffold
> This file contains the selected headings and drafting prompts. Replace prompts with supported prose as work proceeds. No completed chapter is claimed. [[Manuscript/Drafting Dashboard|Dashboard]] owns progress; [[Manuscript/Evidence Register|Evidence Register]] owns claim/source status.

## Project Context

Introduce the relevant problem, move from global/national context to the actual local situation, explain the rationale, and close with the reason for the proposed study. Use E-01–E-03. The writing guide records the two-page guidance and the unresolved meaning of “at least four problems.”

**Draft prose:** Not started in this vault.

## Purpose and Description of the Project

Explain the proposed game's function, learner experience, relevance, and evidenced distinctiveness using E-04–E-05. Keep proposed benefits distinct from measured results. Introductory paragraphs and discussion details are in the writing guide.

**Draft prose:** Not started in this vault.

## Objectives of the Project

Draft a general objective aligned with the official title, then specific SMART objectives. Derive problems from evidence before claiming corresponding solutions.

### Drafting notes on problem and objective alignment

This planning table is a working aid, not an added required manuscript subsection. Move it out of final chapter prose when preparing a submission.

| Problem ID | Evidence-supported problem and source | Corresponding specific objective | Related requirement or evaluation evidence |
| --- | --- | --- | --- |
| To assign | No problem statement entered yet | To draft after its problem is supported | To link |

**Draft prose:** Not started in this vault.

## Scope and Limitations of the Project

Use [[Project/Scope and Requirements|the canonical scope]] and describe proposed coverage and exclusions accurately. Retain Q-01 for the Android range. Keep unresolved detailed game rules identified rather than silently specifying them.

**Draft prose:** Not started in this vault.
''', status='proposed', sources=draft_sources))

write('Manuscript/Drafts/Chapter II Review of Related Literature.md', note('manuscript-draft', 'Chapter II Review of Related Literature', '''
> [!todo] Working scaffold
> These headings and prompts are not a completed literature review. Add only references actually read and recorded in [[Manuscript/Evidence Register|Evidence Register]]. [[Manuscript/Drafting Dashboard|Dashboard]] owns progress.

## Related Literature / Theoretical Background

Use E-06. Identify an appropriate anchor theory and supporting literature after inspecting their sources. Explain the relationship to this project and retain each source's limits. Follow the writing guide's continuity and citation guidance.

**Draft prose:** Not started in this vault.

## Related Studies

Use E-07. Present real related studies/projects with accurate evidence, then synthesize similarities, differences, and the project's supported gap. The lecture suggests considering three to six projects; it does not establish a mandatory count or fixed publication-year cutoff.

**Comparison working notes:** Record each study's population, topic, learning activity, platform, offline behavior, findings, limitations, and relevance when applicable. These are suggested comparison dimensions.

**Draft prose:** Not started in this vault.
''', status='proposed', sources=draft_sources))

write('Manuscript/Drafts/Chapter III Technical Background.md', note('manuscript-draft', 'Chapter III Technical Background', '''
> [!todo] Working scaffold
> Explain the proposed system in paragraphs. Confirm actual implementation claims separately from planned behavior. Use E-08–E-09 in [[Manuscript/Evidence Register|Evidence Register]]. [[Manuscript/Drafting Dashboard|Dashboard]] owns progress.

## Technicality of the project

Explain the technical approach and how it supports the intended learning activities. Distinguish the existing setting from the proposed application. Follow the relevant Chapter III guidance rather than presenting an invented finished system.

**Draft prose:** Not started in this vault.

## Details of the technologies to be used

Explain the purpose and relevance of the declared hardware and software, and relevant peopleware/network considerations. Use [[Project/Technical Baseline|the technical baseline]] as proposal evidence. Verify versions from direct project evidence when stating actual configuration. Explain the documented offline boundaries accurately.

**Draft prose:** Not started in this vault.

## How the project will work

Describe the intended offline learner flow using [[Project/Game Flow|Game Flow]] and [[Project/Scope and Requirements|requirements]]. Mark pending scoring, progression, and save-policy details where they affect the explanation. Methodology remains Chapter IV under the supplied outline.

**Draft prose:** Not started in this vault.
''', status='proposed', sources=draft_sources))

home = (V / 'Home.md').read_text(encoding='utf-8')
home = home.replace('## Manuscript writing references\n', '## Manuscript writing references\n\n- [[Manuscript/Drafting Dashboard|Drafting Dashboard]] — start here for working drafts, section progress, and evidence gaps\n')
write('Home.md', home)

focus = (V / 'Current Focus.md').read_text(encoding='utf-8')
focus = focus.replace('## Manuscript work now\n', '## Manuscript work now\n\n- Start at [[Manuscript/Drafting Dashboard|Drafting Dashboard]] for the target section and its working draft. Use [[Manuscript/Evidence Register|Evidence Register]] to track claims and missing support.\n')
focus = focus.replace('Game development and general workflow improvements are deferred while this manuscript focus remains active.', 'Game development remains deferred while this manuscript focus is active. D-007 authorizes the lightweight drafting supports now in place; broader maintenance work remains deferred.')
focus = focus.replace('1. Add vault version history and an independent backup, and test recovery. Move reusable validators from `.work` into maintained tooling.', '1. Add vault version history and an independent backup, and test recovery. The link/source validator has been promoted to `tools`; the local pre-change snapshot is rollback material, not an independent backup.')
focus = focus.replace('2. Shorten the mandatory skill router and load detailed references only when relevant.', '2. Completed for drafting support: the mandatory skill router is now short; detailed scenarios are in [[Maintenance/Skill Reference|Skill Reference]].')
focus = focus.replace('3. Create a small Now / Next / Blocked board, linking tasks to requirement IDs, acceptance criteria, implementation, and verification evidence.', '3. Completed for the current manuscript: [[Manuscript/Drafting Dashboard|Drafting Dashboard]] tracks sections, next actions, and evidence blockers. A game-implementation task board remains deferred.')
write('Current Focus.md', focus)

writing = (V / 'Manuscript/Chapter 1-3 Writing Guide.md').read_text(encoding='utf-8')
writing = writing.replace('## Which source to use', 'Start at [[Manuscript/Drafting Dashboard|Drafting Dashboard]] for working drafts and progress. Track factual support in [[Manuscript/Evidence Register|Evidence Register]]. Read the section below that matches the requested work.\n\n## Which source to use', 1)
write('Manuscript/Chapter 1-3 Writing Guide.md', writing)

guide = (V / 'Maintenance/Vault Guide.md').read_text(encoding='utf-8')
guide = guide.replace("[[Maintenance/Skill Guide|Skill Guide]] owns workflow routing. Agents select from the current skill catalog and read the selected instructions; the guide's examples are not a fixed inventory or implementation requirements.", "[[Maintenance/Skill Guide|Skill Guide]] is the short routing entry point. [[Maintenance/Skill Reference|Skill Reference]] holds the detailed workflow scenarios. Load details only when relevant to the requested task.")
guide = guide.replace('## Status vocabulary', 'For drafting, [[Manuscript/Drafting Dashboard|Drafting Dashboard]] owns section progress and readiness. [[Manuscript/Evidence Register|Evidence Register]] owns claim-to-source tracking. Working chapter files live in `Manuscript/Drafts`; their scaffolds are not completed prose.\n\n## Status vocabulary', 1)
guide += '''
## Validation and recovery

The maintained validator is `D:\\Projects\\LandGrand-Sources\\tools\\validate_vault.py`. Its adjacent `source-integrity.json` records retained-original and embedded-image hashes. The validator reads current notes, resolves internal links and anchors, parses Obsidian JSON settings, and checks those retained bytes. It is independent of the historical `.work` extraction files. It does not validate research claims or approval.

Run from PowerShell:

```powershell
& 'C:\\Users\\user\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe' 'D:\\Projects\\LandGrand-Sources\\tools\\validate_vault.py'
```

A pre-change vault snapshot is retained at `D:\\Projects\\LandGrand-Sources\\.work\\drafting-support\\vault-before-drafting-support.zip`. It includes the source attachments and Obsidian settings. This same-drive snapshot supports rollback for this change; independent backup storage and vault version history remain deferred.
'''
write('Maintenance/Vault Guide.md', guide)

register = (V / 'Decisions/Decision Register.md').read_text(encoding='utf-8')
row = '| D-007 | 2026-10-24 | Implement the improvements useful for Chapters I–III drafting now: a short skill router, working outlines and progress board, claim/evidence tracking, and maintained vault checks. Keep game development and broader maintenance deferred. | User asked to implement the improvements necessary to make the vault more usable for current drafting. | [[Manuscript/Drafting Dashboard|Drafting Dashboard]], [[Maintenance/Skill Guide|Skill Guide]] |'
pos = register.index('\n\nThe imported proposal')
register = register[:pos] + '\n' + row + register[pos:]
write('Decisions/Decision Register.md', register)

log = (V / 'Maintenance/Change Log.md').read_text(encoding='utf-8')
log += '''
### Drafting support

- Recorded D-007 and added the Chapters I–III Drafting Dashboard, nine-section progress board, three clearly marked working outlines, and an Evidence Register.
- Separated the short skill router from the detailed Skill Reference while preserving existing links to communication preferences. Updated manuscript entry points to load only relevant sections.
- Promoted link, configuration, and retained-source integrity checks to maintained tooling outside `.work`.
- Retained a local pre-change ZIP snapshot. Independent backup/version history and game implementation remain deferred.
- Preserved all original references, unresolved academic and game-design questions, and the distinction between chapter scaffolds and finished prose.
'''
write('Maintenance/Change Log.md', log)

agent = (ROOT / 'AGENTS.md').read_text(encoding='utf-8')
agent = agent.replace('- Manuscript drafting: read `LandGrand/Manuscript/Table of Contents.md` for structure and `LandGrand/Manuscript/Chapter 1-3 Writing Guide.md` for source-attributed guidelines before writing Chapters I–III.', '- Manuscript drafting: start at `LandGrand/Manuscript/Drafting Dashboard.md`; read the target draft section and its cited guidance rather than all chapters. Use `LandGrand/Manuscript/Evidence Register.md` for claim/source status.')
(ROOT / 'AGENTS.md').write_text(agent, encoding='utf-8')

tools = ROOT / 'tools'
tools.mkdir(exist_ok=True)
manifest = json.loads((ROOT / '.work/academic-sources/import-manifest.json').read_text(encoding='utf-8'))
integrity = [{'path': 'Sources/Attachments/' + s['file'], 'sha256': s['sha256'], 'role': 'original'} for s in manifest['sources']]
integrity.append({'path': 'Sources/Attachments/Land Grand - Aslainie - Final.docx',
                  'sha256': '9b753fecba2de5f50978395a4e38bbf7a336d358de9fab01eb1120508bd60d48', 'role': 'original'})
integrity.extend({'path': s['path'], 'sha256': s['sha256'], 'role': 'embedded-image'} for s in manifest['images'])
(tools / 'source-integrity.json').write_text(json.dumps({'recorded': DATE, 'files': integrity}, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'new_notes': len(new_notes), 'router_words_before': old_word_count,
                  'router_words_after': len((V / 'Maintenance/Skill Guide.md').read_text(encoding='utf-8').split()),
                  'snapshot': str(snapshot), 'integrity_entries': len(integrity)}, indent=2))
