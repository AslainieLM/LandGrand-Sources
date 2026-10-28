from pathlib import Path
import shutil

VAULT=Path(r'D:\Projects\LandGrand-Sources\LandGrand')
BACKUP=VAULT.parent/'.work/alignment-review-before-2026-10-28'
def read(rel):return (VAULT/rel).read_text(encoding='utf-8')
def save(rel,text):
    p=VAULT/rel
    before=BACKUP/rel
    before.parent.mkdir(parents=True,exist_ok=True)
    if not before.exists():shutil.copyfile(p,before)
    p.write_text(text,encoding='utf-8')

feedback='Sources/Chapter I Readability Feedback 2026-10-28.md'
text=read(feedback)+'''\n## Problem evidence and objective alignment follow-up

The user asked whether the current four statements are problems supported by the survey tally, then specified:

> Specific Objectives - should be based on the Specific Problem that needs to be solved no. 1 ---> no.1

D-017 records this alignment instruction. [[Manuscript/Chapter I Revision Notes#Problem and objective alignment|The evidence review]] finds support for current problems 1 and 2, with source limits. Statements 3 and 4 are design requirements rather than additional survey-established problems. The proposed two-pair correction is an editorial recommendation, not adviser approval of a two-problem count. MW-01 remains open.
'''
save(feedback,text)

guide='Manuscript/Chapter 1-3 Writing Guide.md'
text=read(guide)
needle='As a drafting aid, make a problem-to-objective table and link each objective to a relevant requirement or documented evaluation plan.'
assert needle in text
text=text.replace(needle,'''Under D-017 and [[Sources/Chapter I Readability Feedback 2026-10-28#Problem evidence and objective alignment follow-up|the user's alignment instruction]], **Specific Problem 1 must match Specific Objective 1**, and so on. State the existing difficulty and its evidence before choosing the response. Each numbered objective should explain the planned response to its matching problem. A feature such as offline use, save/load, or touch controls belongs in scope unless evidence establishes a separate problem that the feature addresses. Do not count proposed features or favourable expectations as independently observed problems. Keep the distinction between a proposed response and demonstrated effectiveness.

As a drafting aid, make a problem-to-objective table and link each objective to its problem evidence and a relevant requirement or documented evaluation plan.''',1)
save(guide,text)

decisions='Decisions/Decision Register.md'
text=read(decisions)
row='| D-017 | 2026-10-28 | Align each numbered specific objective with the matching numbered specific problem (1 with 1, and so on). Establish the problem from evidence rather than treating a proposed feature as proof of a difficulty. | [[Sources/Chapter I Readability Feedback 2026-10-28#Problem evidence and objective alignment follow-up|Direct user instruction and evidence review]]. | [[Manuscript/Chapter 1-3 Writing Guide#Objectives of the Project|Writing rule]], [[Manuscript/Chapter I Revision Notes#Problem and objective alignment|Alignment review]], [[Manuscript/Drafting Dashboard|Dashboard]] |'
assert '| D-017 |' not in text
text=text.replace('\n\nThe imported proposal is an initial documentary baseline.','\n'+row+'\n\nThe imported proposal is an initial documentary baseline.',1)
save(decisions,text)

notes='Manuscript/Chapter I Revision Notes.md'
text=read(notes)
a=text.index('## Problem and objective alignment')
b=text.index('## Main-text discipline audit',a)
review='''## Problem and objective alignment

**Evidence review, 2026-10-28:** The user correctly identified a distinction that the current list does not fully resolve. The four bullets mix two reported concerns with two design requirements. D-017 requires numbered problem/objective pairs; giving features matching numbers does not make them survey-established problems.

| Current item | Review finding | Evidence and limits |
| --- | --- | --- |
| 1. Parents have difficulty explaining module lessons | Supported as a reported concern | Parent Part I question 3: 17 Yes, 2 No, 1 Maybe out of 20. The question concerns modules generally, so the game offers a response only within its selected Science content. |
| 2. Reported Science difficulty and selected topics | Supported with qualification | Subject ratings and direct Grade 5 CSV responses support adult-reported Science concerns and some landform/rock/mineral mentions. The groups are small and span several grades; these are not pupil test results or proof that the chosen topics are the most common difficulties. |
| 3. Need to connect explanations with exploration/review | A design requirement | Positive views of a possible mobile game do not establish that current learning lacks interaction or review. Controls and exploration are proposed responses, not observed problems. |
| 4. Need for offline use and progress saving | A design requirement | The survey does not directly establish unreliable home internet or lost learning progress. The teacher's combined computer/projector/internet question cannot isolate connectivity. Offline/local-save operation is already proposed scope; the school-disruption account does not demonstrate lost saves. |

Sources: [[Sources/Baluan Survey Tally Extract#Table 01 Parents Part I|Parent questions]], [[Sources/Baluan Survey Tally Extract#Table 03 Teachers Part I|teacher questions]], subject-rating Tables 02/04, and [[Sources/Baluan Survey CSV Records#Grade 5 subgroup check, 2026-10-28|direct Grade 5 response locators]]. Teacher question 2 also records mixed views of modular-learning effectiveness (7 Yes, 8 No, 5 Maybe); this is a separate possible concern, not proof of current items 3 or 4.

### Proposed correction for review

These two pairs reflect the strongest support for the current problem list. They are recommended wording, not a confirmed adviser decision about the required count.

| Number | Specific problem | Matching specific objective | Requirement trace |
| --- | --- | --- | --- |
| 1 | Some surveyed parents reported difficulty explaining lessons in printed modules to their children. | Develop short Science lessons and clear item descriptions to provide additional explanations for home study within the project's selected content. | LG-07, LG-10 |
| 2 | Surveyed parents and teachers reported Science difficulty, and some Grade 5 responses identified landforms, rocks, and minerals as difficult topics. | Develop four landform episodes with exploration, collection, and review activities covering the selected Science topics for Grade 5 learners. | LG-01, LG-03–LG-05, LG-08–LG-10, LG-12 |

The existing objectives 1 and 2 broadly relate to the reported concerns, but objective 2 needs the learning activities and content focus, not only an episode count. Existing objectives 3 and 4 describe implementation features. They can remain supporting scope requirements and be traced to the relevant learning response without inventing a separate problem for each feature.

The planned November–December 2026 window under D-015 can apply to all retained deliverables. No objective promises a measured learning gain without a defined evaluation method.

**Current draft status:** Word revision 6 and its mirrored body still contain the earlier four concern/design-need bullets and four objectives. This review does not silently replace them or approve two as the required number. Context and Objectives require structural revision. If the adviser requires four independently supported problems, identify further distinct, relevant evidence or obtain clarification of the counting rule. Do not split one concern or relabel features merely to reach four. MW-01 remains open.

'''
text=text[:a]+review+text[b:]
text=text.replace('This revision addresses [[Sources/Chapter I Readability Feedback 2026-10-28|the user\u2019s readability feedback]]','This revision addresses [[Sources/Chapter I Readability Feedback 2026-10-28|the user\u2019s readability feedback]]')
text=text.replace('## Revision and status\n','## Revision and status\n\n**Review update:** Context and Objectives need structural revision following the survey-evidence/alignment review below. Layout and opening-sentence checks passed; that does not make the current four-item mapping satisfactory.\n',1)
save(notes,text)

dash='Manuscript/Drafting Dashboard.md'
text=read(dash)
text=text.replace('- [ ] Obtain user/adviser review of Chapter I problem framing, especially MW-01.', '- [ ] Correct the Context/Objective pairing under D-017: current items 1–2 are reported concerns; 3–4 are design requirements. Review the proposed two-pair mapping and retain MW-01 for the adviser\u2019s required problem count.')
lines=[]
for line in text.splitlines():
    if line.startswith('| I — Project Context |'):
        line='| I — Project Context | [[Manuscript/Drafts/Chapter I Introduction#Project Context|Open section]] | Needs structural revision after evidence review, 2026-10-28 | Use the [[Manuscript/Chapter I Revision Notes#Problem and objective alignment|alignment review]]; current items 3–4 are design requirements, not survey-established problems. |'
    if line.startswith('| I — Objectives |'):
        line='| I — Objectives | [[Manuscript/Drafts/Chapter I Introduction#Objectives of the Project|Open section]] | Needs structural revision after evidence review, 2026-10-28 | Match each objective to its numbered evidenced problem under D-017; feature inventory alone is insufficient. |'
    lines.append(line)
text='\n'.join(lines)+'\n'
text=text.replace('- [ ] Problems and objectives agree; scope matches the canonical requirements.', '- [ ] Each numbered objective responds to its matching evidenced problem under D-017; scope matches the canonical requirements.')
save(dash,text)

draft='Manuscript/Drafts/Chapter I Introduction.md'
text=read(draft).replace('> Revision 6, ready for user review.', '> Revision 6, requires Context/Objective alignment revision after the 2026-10-28 evidence review.',1)
save(draft,text)

focus='Current Focus.md'
text=read(focus).replace('and synchronized Markdown, ready for user review on 2026-10-28.', 'and synchronized Markdown. The 2026-10-28 evidence review identifies a required Context/Objective alignment correction; see [[Manuscript/Chapter I Revision Notes#Problem and objective alignment|the review and proposed pairing]].',1)
save(focus,text)

log='Maintenance/Change Log.md'
text=read(log)+'''\n### Survey-problem and objective alignment review

- Checked all parent/teacher closed questions, subject ratings, and the recorded Grade 5 response locators against the current four statements.
- Confirmed that current items 1–2 are supported reported concerns with limitations. Items 3–4 are design requirements, not additional survey-established problems.
- Recorded D-017 and strengthened the writing rule: each numbered objective must address the matching evidenced problem. Saved a concrete two-pair recommendation in the owning revision note without approving the required problem count.
- Marked Context and Objectives as needing structural revision. Preserved Word revision 6, its mirrored body, all source data, and project feature scope. MW-01 remains open rather than treating layout verification as substantive approval.
'''
save(log,text)
print('Recorded evidence review, proposed mapping, D-017, and corrected readiness status. Word body and survey sources unchanged.')
