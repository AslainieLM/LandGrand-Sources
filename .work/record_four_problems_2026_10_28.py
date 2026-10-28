from pathlib import Path
from collections import Counter
import json,shutil

VAULT=Path(r'D:\Projects\LandGrand-Sources\LandGrand')
BACKUP=VAULT.parent/'.work/before-four-problem-review-2026-10-28'
def read(rel):return (VAULT/rel).read_text(encoding='utf-8')
def save(rel,text):
    path=VAULT/rel
    backup=BACKUP/rel
    backup.parent.mkdir(parents=True,exist_ok=True)
    if not backup.exists():shutil.copyfile(path,backup)
    path.write_text(text,encoding='utf-8')

evidence=json.loads((VAULT.parent/'.work/four-problem-evidence-2026-10-28.json').read_text())
assert evidence['Parent.csv']['grade5_counts']=={'Maybe':1,'Yes':4,'No':1}
assert evidence['Teacher.csv']['grade5_counts']=={'Maybe':2,'Yes':1,'No':2}

feedback='Sources/Chapter I Readability Feedback 2026-10-28.md'
text=read(feedback)+'''\n## Minimum four problems confirmed

In the continuing Chapter I problem-list discussion, the user stated:

> atleast 4 problems are required for the

The context confirms a minimum of four Chapter I problem statements. D-018 resolves the minimum-count part of MW-01. The earlier two-pair recommendation is superseded as a drafting plan. The revised four-item candidate uses parent explanation difficulty, a separate teacher-reported concern about modular-learning effectiveness, and two directly mentioned content areas. It does not retain the broad Science-difficulty statement alongside its two content subproblems or count proposed offline/save features as problems.

[[Manuscript/Chapter I Revision Notes#Four problem statements for the next revision|The current four statements and evidence]] remain proposed manuscript wording, not adviser approval or measured learning results. [[Sources/Baluan Survey CSV Records#Additional Grade 5 response check, 2026-10-28|The additional Grade 5 check]] records the teacher and parent response counts and locators.
'''
text=text.replace('The proposed two-pair correction is an editorial recommendation, not adviser approval of a two-problem count. MW-01 remains open.', 'The two-pair correction was an editorial recommendation before the minimum-count confirmation below. D-018 now confirms at least four and supersedes that two-pair drafting plan.')
save(feedback,text)

decisions='Decisions/Decision Register.md'
text=read(decisions)
row='| D-018 | 2026-10-28 | Require at least four Chapter I problem statements. Supersede the earlier two-pair drafting recommendation; retain D-017\u2019s matching-number objective rule and evidence requirements. This confirms the minimum count, not approval of any wording or invented empirical findings. | [[Sources/Chapter I Readability Feedback 2026-10-28#Minimum four problems confirmed|Direct user clarification]]. | [[Manuscript/Chapter 1-3 Writing Guide#Clarifications to retain|MW-01]], [[Manuscript/Chapter I Revision Notes#Four problem statements for the next revision|Current problem wording]], [[Manuscript/Drafting Dashboard|Dashboard]] |'
assert '| D-018 |' not in text
text=text.replace('\n\nThe imported proposal is an initial documentary baseline.','\n'+row+'\n\nThe imported proposal is an initial documentary baseline.',1)
save(decisions,text)

guide='Manuscript/Chapter 1-3 Writing Guide.md'
text=read(guide)
text=text.replace('The notes say “atleast 4 problem.” Its exact counting scope is unresolved below.', 'The notes say “atleast 4 problem.” The user confirms **at least four Chapter I problem statements** under D-018. Each must have a matching numbered objective under D-017 and support from relevant evidence.')
text=text.replace('| MW-01 | Does “at least four problems” mean four overall, four local problems, or another grouping? | The typed note does not settle how the count applies. |', '| MW-01 | Minimum count resolved: at least four Chapter I problem statements, confirmed by the user under D-018. | Use four or more supported, relevant problems with matching objectives. Approval of wording and evidence limits remain separate. |')
save(guide,text)

source='Sources/Baluan Survey CSV Records.md'
text=read(source)
addition='''## Additional Grade 5 response check, 2026-10-28

For the minimum-four-problem review, the unchanged CSVs were filtered again using column C. Both relevant closed questions are in **column H**:

| Group and question | Grade 5 sample | Yes | No | Maybe | Interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| Parent question 3: difficulty explaining module lessons | 6 | 4 | 1 | 1 | Some Grade 5 parents report explanation difficulty; the question is not specific to Science. |
| Teacher question 2: modular learning effective in helping learners understand lessons | 5 | 1 | 2 | 2 | Two Grade 5 teachers answered No and two Maybe. This supports a bounded concern, not a majority claim or measured ineffectiveness. |

Grade 5 parent rows are 8, 16, 17, 18, 19, and 20; Grade 5 teacher rows are 13–17. Teacher No responses for question 2 are rows 15 and 16. The full teacher group is 7 Yes, 8 No, and 5 Maybe, matching the Word tally.

Direct topic evidence remains parent column X (landforms rows 16/18, minerals row 8) and teacher column Y (rock topics rows 15/17, minerals row 15). These are different reported content areas. They do not establish a tested inability to identify, classify, or distinguish objects, and they do not identify each proposed landform separately.

These small adult-response groups support four related concerns for drafting: explanation at home, teachers' views of modular learning, reported landform difficulty, and reported rock/mineral difficulty. The general Science concern is not counted again as an additional problem. Responses record the July survey context; they do not imply that the school is currently under modular learning. Both original CSV hashes still match the import record. The calculation record is .work/four-problem-evidence-2026-10-28.json outside the vault.

'''
assert '## Additional Grade 5 response check, 2026-10-28' not in text
text=text.replace('## Survey and encoding dates',addition+'## Survey and encoding dates',1)
save(source,text)

notes='Manuscript/Chapter I Revision Notes.md'
text=read(notes)
a=text.index('### Problem wording prepared first')
b=text.index('## Main-text discipline audit',a)
block='''### Four problem statements for the next revision

**Latest count decision:** D-018 confirms at least four problems. This supersedes the earlier two-pair drafting plan. The following four related concerns have separate source support or directly mentioned content areas. The broad Science-difficulty statement is replaced by its specific content concerns, rather than counted again beside them.

The survey at Baluan Elementary School identified the following reported problems relevant to the proposed Land Grand project:

1. Some surveyed parents of Grade 5 learners reported difficulty explaining lessons in printed modules to their children.
2. Some surveyed Grade 5 teachers did not consider modular learning effective in helping learners understand lessons.
3. Some parents of Grade 5 learners reported landforms as a difficult Science topic for their children.
4. Some Grade 5 parent and teacher responses identified rocks or minerals as difficult Science topics.

| Problem | Direct evidence | Boundary |
| --- | --- | --- |
| 1. Parent explanation difficulty | Grade 5 Parent.csv column H: 4 Yes, 1 No, 1 Maybe among 6 | This question concerns modules generally. Land Grand can offer explanations only within its selected Science content. |
| 2. Teacher concern about modular-learning effectiveness | Grade 5 Teacher.csv column H: 2 No, 2 Maybe, 1 Yes among 5; No rows 15/16 | A minority directly answered No; uncertainty is not counted as No. These are opinions in the survey context, not proof that modular learning is ineffective. |
| 3. Landform difficulty | Grade 5 Parent.csv column X, rows 16/18 | Direct mentions, not evidence of prevalence or a diagnosis for every learner. No teacher Grade 5 landform mention is invented. |
| 4. Rock/mineral difficulty | Grade 5 Parent.csv column X, row 8 (minerals); Teacher.csv column Y, rows 15/17 (rocks), row 15 (minerals) | Topic reports do not prove a specific identification/classification deficit or name the final teaching inventory. |

[[Sources/Baluan Survey CSV Records#Additional Grade 5 response check, 2026-10-28|The CSV source note]] owns the aggregate check and locators. This is proposed final wording for review, not adviser approval, pupil assessment evidence, or a claim that Land Grand has solved the concerns.

**Next alignment:** Create four matching objectives in this exact order. Pre-level explanations can respond to problem 1, interactive supplementary learning/review to problem 2, landform episodes to problem 3, and rock/mineral collection descriptions to problem 4. These are planned responses, not established effectiveness. Offline use, saving, Android support, and touch controls remain supporting scope features.

**Current draft status:** Word revision 6 and its mirrored body still contain the earlier list. The new four-statement wording is prepared here first, as requested; integration and objective rewriting remain subsequent manuscript work. MW-01's minimum count is resolved. D-017's one-to-one alignment still applies.

'''
text=text[:a]+block+text[b:]
text=text.replace('- **MW-01:** Meaning of at least four problems. Review P-03–P-04 as design needs; do not relabel them as measured problems without evidence.', '- **MW-01 resolved under D-018:** At least four problem statements are required. Review and integrate the four evidence-supported statements above; approval of their wording remains separate.')
save(notes,text)

dash='Manuscript/Drafting Dashboard.md'
text=read(dash)
text=text.replace('Review the proposed two-pair mapping and retain MW-01 for the adviser’s required problem count.', 'Use the four-statement candidate in the revision notes. D-018 resolves MW-01: at least four problems are required.')
text=text.replace('MW-01 remains open.', 'MW-01\u2019s minimum count is resolved under D-018; four-statement wording and matching objectives remain under review.')
text=text.replace('current items 3–4 are design requirements, not survey-established problems.', 'replace the current design-need bullets with the four evidenced concerns prepared under D-018.')
text=text.replace('Match each objective to its numbered evidenced problem under D-017; feature inventory alone is insufficient.', 'Prepare four objectives matching the new four-problem order under D-017/D-018; keep supporting features in scope.')
save(dash,text)

focus='Current Focus.md'
text=read(focus)
needle='The 2026-10-28 evidence review identifies a required Context/Objective alignment correction;'
text=text.replace(needle, 'D-018 confirms at least four problem statements; the revised four-problem candidate is prepared for review. The 2026-10-28 evidence review identifies a required Context/Objective alignment correction;',1)
save(focus,text)

register='Manuscript/Evidence Register.md'
text=read(register)
needle='Exact sampling procedure and Q-10 topic checks remain separate gaps.'
assert needle in text
text=text.replace(needle, 'The [[Sources/Baluan Survey CSV Records#Additional Grade 5 response check, 2026-10-28|additional Grade 5 check]] supports parent explanation difficulty and a bounded teacher concern about modular-learning effectiveness, plus separate direct landform and rock/mineral mentions for the four-problem candidate. '+needle,1)
save(register,text)

log='Maintenance/Change Log.md'
text=read(log)+'''\n### Minimum four problems confirmed and rechecked

- Recorded D-018: the user confirms at least four Chapter I problems, resolving MW-01's minimum count and superseding the two-pair drafting recommendation.
- Rechecked Grade 5 CSV responses: parent explanation difficulty (4 Yes/1 No/1 Maybe among 6) and teacher modular-effectiveness views (1 Yes/2 No/2 Maybe among 5), plus direct landform and rock/mineral topic mentions.
- Prepared four related, survey-grounded problem statements in the owning revision note. Replaced the broad Science item with two specifically evidenced content concerns rather than counting all three together.
- Updated the writing guide, source locators, evidence register, dashboard, and current focus. Retained small-sample/perception limits, source data, Word revision 6, and the task order of finalizing problems before revising objectives.
'''
save(log,text)
print('Minimum four recorded as D-018; four-problem wording and evidence saved; raw data and Word draft unchanged.')
