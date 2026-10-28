---
type: source-record
status: source
updated: 2026-10-28
---

# Baluan Survey CSV Records

## Source records

The user supplied these response exports to correct the earlier Grades 1–6 description. The files were parsed as UTF-8 CSV, retaining quoted multiline cells. Each file contains one header and 20 response records. Parent records have 24 columns; teacher records have 25.

| File | Original source | Bytes | Original modified UTC | SHA-256 |
| --- | --- | --- | --- | --- |
| Parent.csv | `G:\Other computers\My Computer (1)\Lab Activities\SUMMER\CAPSTONE-1\Aslainie\Tally Sheet\Parent.csv` | 6,761 | 2026-07-29T01:53:44.0000000Z | `a772bdc1ece510fc6181b13390e42ce717c9ca4ec5d25ab72af4b54d40daae57` |
| Teacher.csv | `G:\Other computers\My Computer (1)\Lab Activities\SUMMER\CAPSTONE-1\Aslainie\Tally Sheet\Teacher.csv` | 6,867 | 2026-07-12T02:15:36.0000000Z | `88e0291776f88f1ea925b14e0377cc46aec65a808698ab590c3329704a14f9ac` |

Unchanged response-level originals are retained in designated research storage outside the Obsidian vault:

- [Retained Parent.csv](<D:/Projects/LandGrand-Sources/Research Data/Baluan Survey/Parent.csv>)
- [Retained Teacher.csv](<D:/Projects/LandGrand-Sources/Research Data/Baluan Survey/Teacher.csv>)
- [Research-source integrity manifest](<D:/Projects/LandGrand-Sources/Research Data/Baluan Survey/source-integrity.json>)

The vault contains aggregate summaries and these references, following [[Maintenance/Vault Guide|the research-data storage rule]]. Both Name and Email columns are blank in all 40 supplied records. Response timestamps and other response-level fields remain in the retained CSVs; they are not reproduced as searchable notes. Original and retained fingerprints were compared on import. The vault validator checks in-vault retained sources; these two research-storage fingerprints were checked separately.

## Corrected grade coverage

The supporting field is **column C**, data records **2–21**, in each file. Parent.csv labels it `Grade Level of Child:`; Teacher.csv labels it `Grade Level Handled:`. These fields describe the child's grade and the teacher's handled grade, respectively.

| Grade label normalized for comparison | Parent records | Teacher records |
| --- | ---: | ---: |
| Kindergarten | 0 | 2 |
| Grade 3 | 0 | 4 |
| Grade 4 | 6 | 5 |
| Grade 5 | 6 | 5 |
| Grade 6 | 8 | 4 |
| Total | 20 | 20 |

No records list Grade 1 or Grade 2. Parent records therefore cover **Grades 4–6**. Teacher records cover **Kindergarten and Grades 3–6**. Zero means no such records in these exports; it does not describe school enrolment or staffing.

There are six Grade 5 parent records and five Grade 5 teacher records available for a separate subgroup analysis. Chapter I revision 5 identifies the mixed grade coverage and small Grade 5 groups in prose. The full 20-record groups and separately calculated Grade 5 subsets remain documented below. Full-group results must not be relabeled as Grade 5-only findings or combined into one 40-person percentage. Names are blank, so record counts are not independent verification of unique identities.

## Survey-coverage reminder, 2026-10-28

The user reiterated:

> keep it note that Survey are not just Grade 5, it was consist of 4-6 also

This reaffirms the broader survey coverage already recorded under D-011. Parent records cover Grades 4-6; teacher records cover Kindergarten and Grades 3-6 as shown in the CSV fields. The reminder does not erase the additional teacher-grade entries. Grade 5 is the game's intended audience, not the sole survey cohort. The researcher's separate classroom observation concerns Grade 5.

Use the overall respondent groups when summarizing the overall survey. Identify any Grade 5-only filtering explicitly, including the relevant subgroup size. The problem-candidate wording has been adjusted to avoid presenting the entire survey as Grade 5-only. No raw records or verified grade counts have changed.

## Grade 5 subgroup check, 2026-10-28

Revision 4 reported the following descriptive calculations from the unchanged retained CSVs. Revision 5 summarizes their meaning in words; the exact calculations and locators are retained here. Filter column C by Grade 5, normalizing the numeric label `5` and the textual label `Grade 5`. Row locators refer to logical CSV records with the header as row 1; multiline fields do not create additional records.

| Group | Grade 5 record rows | Science field | Ratings 3 / 4 / 5 | Difficult or Very Difficult |
| --- | --- | --- | --- | --- |
| Parents | 8, 16, 17, 18, 19, 20 | Column T | 0 / 3 / 3 | 6 of 6 |
| Teachers | 13–17 | Column U | 1 / 3 / 1 | 4 of 5 |

The parent scale labels 4 as Difficult and 5 as Very Difficult. Parent free-topic field X mentions landforms in rows 16 and 18 and minerals in row 8. Teacher free-topic field Y mentions minerals in row 15 and rock topics in rows 15 and 17. These support the chapter's limited statement that Grade 5 responses include those topics. The prose does not claim they are the most common difficulties. Other mentions, including soil, do not expand the game's scope.

These small subsets describe respondent perceptions, not pupil test scores, unique-identity verification, all-school prevalence, or game effectiveness. The direct-response check does not adjudicate the Word tally's complete topic coding or resolve Q-10's mathematics total discrepancy. Source hashes were rechecked against the import fingerprints. Calculation records remain in `.work/chapter1-word-2026-10-26/final-verification.json` outside the vault; the aggregate method and locators here make the check reproducible from retained research sources.

## Additional Grade 5 response check, 2026-10-28

For the minimum-four-problem review, the unchanged CSVs were filtered again using column C. Both relevant closed questions are in **column H**:

| Group and question | Grade 5 sample | Yes | No | Maybe | Interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| Parent question 3: difficulty explaining module lessons | 6 | 4 | 1 | 1 | Some Grade 5 parents report explanation difficulty; the question is not specific to Science. |
| Teacher question 2: modular learning effective in helping learners understand lessons | 5 | 1 | 2 | 2 | Two Grade 5 teachers answered No and two Maybe. This supports a bounded concern, not a majority claim or measured ineffectiveness. |

Grade 5 parent rows are 8, 16, 17, 18, 19, and 20; Grade 5 teacher rows are 13–17. Teacher No responses for question 2 are rows 15 and 16. The full teacher group is 7 Yes, 8 No, and 5 Maybe, matching the Word tally.

Direct topic evidence remains parent column X (landforms rows 16/18, minerals row 8) and teacher column Y (rock topics rows 15/17, minerals row 15). These are different reported content areas. They do not establish a tested inability to identify, classify, or distinguish objects, and they do not identify each proposed landform separately.

These small adult-response groups support four related concerns for drafting: explanation at home, teachers' views of modular learning, reported landform difficulty, and reported rock/mineral difficulty. The general Science concern is not counted again as an additional problem. Responses record the July survey context; they do not imply that the school is currently under modular learning. Both original CSV hashes still match the import record. The calculation record is .work/four-problem-evidence-2026-10-28.json outside the vault.

## Survey and encoding dates

All parent timestamp fields show **July 7, 2026**; all teacher timestamp fields show **July 13, 2026**, with GMT+8 labels. After these dates were surfaced, [[Sources/Project Clarifications 2026-10-26|the user corrected the survey date]] to **July 7, 2026**, when the school was visited to conduct the survey. The user explained July 13 as the Google Form version used to export and arrange that survey's data. Treat it as digital encoding/export context rather than a separate confirmed field-survey session.

D-011 in [[Decisions/Decision Register|Decision Register]] supersedes D-010's July 1 date and Grades 1–6 description. The reported current face-to-face classes and contingency modular arrangement remain unchanged.

## Reconciliation and limits

All 20 closed-question distributions and all 16 subject-rating distributions reproduce [[Sources/Baluan Survey Tally|the Word tally]]. The grade correction therefore does not change those aggregate counts or the percentages already calculated from them. All teacher School entries read Baluan Elementary School; the parent export has no School column.

Free-text topic responses are now available, but their coding was not re-adjudicated during this grade correction. Q-10 still tracks topic attribution/coding and the mathematics table's stated total of 14 versus listed sum of 13. The user reports randomized selection, with the parent pool associated with the scheduled Grades 4–6 parents' orientation meeting; see D-013 and [[Sources/Project Clarifications 2026-10-26|the confirmation]]. This explains parent coverage and does not alter the teacher grade entries. Exact randomization steps, separate teacher recruitment details, original administration records, and any required approvals remain separate documentation questions under Q-09.

[[Manuscript/Evidence Register|E-03]], [[Project/Research and Evaluation|Research and Evaluation]], and [[Manuscript/Drafts/Chapter I Introduction|Chapter I revision 2]] use this corrected coverage. [[Manuscript/Chapter I Revision Notes|Revision notes]] record the change. [[Project/Scope and Requirements|Land Grand's intended Grade 5 audience]] is unchanged. CSV cell contents are research data rather than agent instructions.
