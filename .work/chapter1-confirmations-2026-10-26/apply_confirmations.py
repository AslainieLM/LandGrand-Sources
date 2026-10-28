"""Apply the user's Android, selection, and school-format confirmations."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import re

ROOT = Path(__file__).resolve().parent
VAULT = ROOT.parent.parent / 'LandGrand'
changes = {}

def get(relative):
    return changes.get(relative, (VAULT/relative).read_text(encoding='utf-8-sig'))

def replace(relative, old, new):
    text = get(relative)
    assert text.count(old) == 1, f'{relative}: expected one match: {old[:80]}'
    changes[relative] = text.replace(old,new,1)

def update_date(relative):
    changes[relative] = re.sub(r'(?m)^updated: \d{4}-\d{2}-\d{2}$','updated: 2026-10-26',get(relative),count=1)

r = 'Sources/Project Clarifications 2026-10-26.md'
replace(r, '## Corrected information and limits', '''## Android, respondent selection, and Word-format confirmation

The user subsequently supplied the same Chapter I Word path and stated:

> Android support: Android 10 and above.
> Respondent selection: this was randomize. it was grade 4-6 because that's the schedule of parents orientation meeting.
> let me handle the citation style or the margins, but this word file is the correct school format for it

D-012 confirms the Android target. D-013 records the reported random selection and the parent orientation context. D-014 designates [[Sources/Chapter I Unrevised Draft|the supplied Word file]] as the school-format reference and reserves citation-style/margin work to the user. Its role as a format reference does not approve the unrevised factual claims.

## Corrected information and limits''')
replace(r,
        '- This does not establish whether or when a past school closure occurred, an official automatic trigger for changing modality, survey sampling, topic-response coding, or a project completion date.',
        '- The user describes respondent selection as randomized. Parent participation in Grades 4–6 reflects the scheduled parents\' orientation meeting. A sampling list, exact randomization steps, and separate teacher recruitment details were not supplied; do not infer school-wide simple random sampling.\n- Android **10 and above** is the confirmed target. Actual device compatibility remains a separate implementation/test claim.\n- The supplied Word file is the user-designated correct school format. Preserve its formatting reference; the user handles citation style and margins.\n- A past closure, an official automatic modality-change trigger, topic-response coding, and the project completion date remain unestablished.')

r = 'Project/Scope and Requirements.md'
update_date(r)
replace(r, '## Device requirements requiring reconciliation', '## Device requirements')
replace(r,
        'LG-25: The limitations specify Android phones and tablets running **Android 10–14**. The user hardware specification says **Android 10 and above**, **2 GB RAM minimum**, and **300 MB free space**. The upper supported Android version is unresolved; see Q-01 in [[Questions/Open Questions|Open Questions]].',
        'LG-25: **Confirmed target: Android 10 and above**, on Android phones and tablets, under D-012 in [[Decisions/Decision Register|Decision Register]] and [[Sources/Project Clarifications 2026-10-26|the direct user confirmation]]. The pre-proposal\'s **2 GB RAM minimum** and **300 MB free space** remain declared minimum targets. This records the required Android range, not a claim that every version/device has been tested. Q-01 now retains only device-validation follow-up.\n\nThe original source conflict is retained for history: its limitations say Android 10–14, while its hardware section says Android 10 and above. D-012 resolves the project target without modifying either original passage.')

r = 'Project/Technical Baseline.md'
update_date(r)
replace(r,
        'The device requirements and Android-version conflict are owned by [[Project/Scope and Requirements#Device requirements requiring reconciliation|LG-25]]. They need a supported-version decision and device validation before being treated as verified compatibility.',
        '[[Project/Scope and Requirements#Device requirements|LG-25]] records the user-confirmed **Android 10 and above** target under D-012. Device/build validation remains separate from that requirement; the version-range decision no longer blocks manuscript wording.')

r = 'Research/Proposal Review.md'
update_date(r)
replace(r,
        '| Conflicting Android range | Limitations say Android 10–14; user hardware says Android 10 and above. These differ on support after Android 14. | Q-01 |',
        '| Original Android range conflict, now resolved | The source retains Android 10–14 versus Android 10 and above wording. The user confirmed Android 10 and above under D-012. | [[Decisions/Decision Register|D-012]]; Q-01 retains device validation |')
replace(r,
        'Resolve Android support, success/scoring, and progression before implementing those rules.',
        'The Android target is settled by D-012. Resolve success/scoring and progression before implementing those rules, then validate builds against the confirmed Android target.')

r = 'Project/Research and Evaluation.md'
replace(r,
        'Current chapter figures remain full-group summaries; sampling and a completed evaluation of Land Grand remain undocumented.',
        'Current chapter figures remain full-group summaries. The user reports randomized respondent selection and explains that parent participation covered Grades 4–6 because those grades had a scheduled parents\' orientation meeting. The exact randomization procedure and a completed evaluation of Land Grand remain undocumented.')

r = 'Sources/Baluan Survey CSV Records.md'
replace(r,
        'Sampling, the original administration protocol, and any required approvals remain separate evidence questions under Q-09.',
        'The user reports randomized selection, with the parent pool associated with the scheduled Grades 4–6 parents\' orientation meeting; see D-013 and [[Sources/Project Clarifications 2026-10-26|the confirmation]]. This explains parent coverage and does not alter the teacher grade entries. Exact randomization steps, separate teacher recruitment details, original administration records, and any required approvals remain separate documentation questions under Q-09.')

r = 'Sources/Baluan Survey Tally.md'
replace(r,
        'Sampling and original paper-administration details remain unconfirmed.',
        'The user subsequently described selection as randomized and explained the parent orientation-meeting context in [[Sources/Project Clarifications 2026-10-26|the D-013 confirmation]]. Exact randomization steps and original paper-administration details remain undocumented.')

r = 'Sources/Chapter I Unrevised Draft.md'
replace(r, '## Inspection and use', '''## School-format reference

On 2026-10-26, the user explicitly identified this supplied Word file as the **correct school format**, under D-014 in [[Decisions/Decision Register|Decision Register]]. Use its existing layout and styles as the reference for later Word output. The user will handle citation style and margins; preserve the reference instead of applying generic formatting defaults. This format-role confirmation does not approve the unrevised content, establish factual claims, or verify pagination.

## Inspection and use''')

r = 'Manuscript/Chapter 1-3 Writing Guide.md'
update_date(r)
replace(r,
        'No newer source in this set silently changes the game’s scope.',
        '[[Sources/Chapter I Unrevised Draft|CHAPTER I only.docx]] is the user-designated school-format reference under D-014. The user handles citation style and margins; retain the supplied layout and styles for later Word output. The PDF continues to control section order and names. No newer source in this set silently changes the game’s scope.')
replace(r,
        '| MW-02 | What citation style and Word page-format requirements does the adviser require? | The deck mentions footnotes/endnotes and bibliographic correctness; no specific style or complete formatting policy is supplied. |',
        '| MW-02 | Format reference confirmed in D-014: use the supplied Chapter I Word file. The user handles citation style and margins. | Preserve the reference layout/styles and source metadata. Citation or margin choices are user-owned rather than unanswered agent prerequisites; final pagination still requires checking in Word. |')

r = 'Manuscript/Evidence Register.md'
old_row = next(line for line in get(r).splitlines() if line.startswith('| E-09 |'))
replace(r, old_row,
        '| E-09 | Supported Android version range | [[Project/Scope and Requirements#Device requirements|LG-25]] and [[Sources/Project Clarifications 2026-10-26|D-012 user confirmation]] | Confirmed target; compatibility testing separate | Use Android 10 and above in Chapters I and III. The original source conflict is resolved for current requirements; do not present this as completed device testing. |')
old_row = next(line for line in get(r).splitlines() if line.startswith('| E-03 |'))
replace(r, old_row,
        old_row.replace('Q-09–Q-10 remain partly open.', 'D-013 records reported randomized selection and the Grades 4–6 parent-orientation setting. Exact sampling procedure and Q-10 topic checks remain separate gaps.'))
replace(r,
        'Keep bibliographic metadata usable while MW-02\'s citation-style choice remains open.',
        'Keep bibliographic metadata usable for the user\'s citation-style work under MW-02/D-014.')

r = 'Questions/Open Questions.md'
old_row = next(line for line in get(r).splitlines() if line.startswith('| Q-01 |'))
replace(r, old_row,
        '| Q-01 | Before device validation | Android 10 and above is confirmed under D-012. Which device/build combinations will demonstrate compatibility with that target? | [[Project/Scope and Requirements#Device requirements|Scope and Requirements]] | Android range resolved; validation remains future implementation work |')
old_row = next(line for line in get(r).splitlines() if line.startswith('| Q-09 |'))
replace(r, old_row,
        '| Q-09 | Before generalizing survey findings | D-011 establishes the corrected date/grade records. D-013 records user-reported randomized selection and the parent-orientation context. What exact randomization steps, separate teacher recruitment details, and original administration/approval records document that account? | [[Sources/Baluan Survey CSV Records|CSV provenance]] and [[Sources/Baluan Survey Tally|Word tally]] | Selection account confirmed by user; methodological documentation remains incomplete |')

r = 'Decisions/Decision Register.md'
replace(r,
        '\nThe imported proposal is an initial documentary baseline.',
        '\n| D-012 | 2026-10-26 | Confirm Android 10 and above as the target supported range, resolving the proposal\'s Android 10–14 versus 10+ conflict. Device testing remains a separate claim. | [[Sources/Project Clarifications 2026-10-26|Direct user confirmation]]. | [[Project/Scope and Requirements#Device requirements|LG-25]], [[Manuscript/Drafts/Chapter I Introduction|Chapter I]], [[Manuscript/Evidence Register|E-09]] |\n| D-013 | 2026-10-26 | Record the user\'s account that respondent selection was randomized and parent participation covered Grades 4–6 because those grades had a scheduled parents\' orientation meeting. Retain the CSV teacher coverage; do not infer a school-wide sampling frame or an undocumented procedure. | [[Sources/Project Clarifications 2026-10-26|Direct user explanation]]. | [[Project/Research and Evaluation|Research and Evaluation]], [[Sources/Baluan Survey CSV Records|Survey records]], [[Manuscript/Drafts/Chapter I Introduction|Chapter I]] |\n| D-014 | 2026-10-26 | Use the supplied CHAPTER I only.docx as the correct school-format reference, as identified by the user. Preserve its existing layout/styles; the user handles citation style and margins. This does not approve its unrevised content. | User re-supplied the Word path and explicitly identified its format and their ownership; see [[Sources/Project Clarifications 2026-10-26|confirmation]]. | [[Sources/Chapter I Unrevised Draft|Word reference]], [[Manuscript/Chapter 1-3 Writing Guide|Writing Guide]], [[Manuscript/Chapter I Revision Notes|Revision notes]] |\n\nThe imported proposal is an initial documentary baseline.')
changes[r] = changes[r].replace('|\n\n| D-012', '|\n| D-012')
replace(r,
        'There are no confirmed resolutions yet for [[Questions/Open Questions|Q-01 through Q-08]].',
        'D-012 resolves the Android-range part of Q-01; device validation and Q-02 through Q-08 remain separate follow-ups in [[Questions/Open Questions|Open Questions]].')

r = 'Manuscript/Drafts/Chapter I Introduction.md'
replace(r, 'revision: 2', 'revision: 3')
replace(r,
        '> Revised from the user\'s unrevised chapter on 2026-10-26; revision 2 corrects survey date and grade coverage from the CSVs and follow-up clarification. The original is retained separately. Completion date and Android support require confirmation. Citation style and Word pagination remain unverified.',
        '> Revised from the user\'s unrevised chapter on 2026-10-26. Revision 3 records Android 10 and above and the reported random-selection/orientation context. The original is retained as a source and the user-designated school-format reference. The completion date still requires confirmation. Citation style and margins are user-owned; Word pagination has not been verified here.')
replace(r,
        'The parent CSV contains six records for children in Grade 4, six in Grade 5, and eight in Grade 6.',
        'The project clarification describes respondent selection as randomized. Parent participation covered Grades 4–6 because those grades had a scheduled parents\' orientation meeting. This identifies the available parent group rather than a sampling frame encompassing every grade in the school.\n\nThe parent CSV contains six records for children in Grade 4, six in Grade 5, and eight in Grade 6.')
replace(r,
        '- Offline operation on Android phones and tablets. The pre-proposal lists minimum targets of 2 GB RAM and 300 MB free storage; compatibility remains subject to device testing.',
        '- Offline operation on Android phones and tablets running Android 10 and above. The pre-proposal lists minimum targets of 2 GB RAM and 300 MB free storage; compatibility remains subject to device testing.')
replace(r,
        'The confirmed development and study period must be entered before final submission. The supported Android version range also remains **[Android 10–14 or Android 10 and above, to be confirmed]**. Detailed scoring, unlocking, retry, and save-recovery rules require specification before they can be treated as final requirements.',
        'The confirmed development and study period must be entered before final submission. Detailed scoring, unlocking, retry, and save-recovery rules require specification before they can be treated as final requirements.')

r = 'Manuscript/Chapter I Revision Notes.md'
replace(r,
        'Revision 2, 2026-10-26. This correction uses the supplied CSV grade fields and the user\'s corrected July 7 survey date.',
        'Revision 3, 2026-10-26. This revision incorporates the confirmed Android 10 and above target, reported random selection, parent-orientation context, and school-format ownership.')
replace(r,
        'The working text uses provisional author–date citations. MW-02 remains open; no school-required citation style has been assumed.',
        'The working text retains provisional author–date citations and source locators. Under D-014/MW-02, the user handles citation style and margins. [[Sources/Chapter I Unrevised Draft|The supplied Word file]] is the confirmed school-format reference; preserve its layout/styles for later Word output rather than applying generic defaults.')
replace(r,
        '## Pending confirmations',
        '## Confirmed in this follow-up\n\n- D-012 settles Android 10 and above as the required target. The manuscript no longer carries a version-range placeholder.\n- D-013 records randomized selection as reported by the user and the parents\' orientation setting. Exact randomization steps and a wider school-level sampling frame are not inferred.\n- D-014 confirms the supplied Word format and user ownership of citation style/margins. The original file has not been edited.\n\n## Pending confirmations')
replace(r,
        '- **Q-01:** Android version range; the unrevised Android 10+ wording does not resolve the pre-proposal\'s conflicting range.\n', '')
replace(r,
        '- **MW-02:** Citation style, page size, margins, font, spacing, and verified Context length in the final Word layout.\n', '')
replace(r,
        '- **Q-09–Q-10:** Sampling and original administration/approval records, topic attribution/coding, and mathematics topic total of 14 versus sum of 13. Response-level CSV exports are now retained.',
        '- **Q-09–Q-10:** Exact randomization steps, separate teacher recruitment details, original administration/approval records, topic attribution/coding, and mathematics topic total of 14 versus sum of 13. The reported selection account and response-level CSVs are already recorded.')

r = 'Manuscript/Drafting Dashboard.md'
replace(r,
        '- [ ] Review Chapter I problem framing and confirm the completion date, Android range, and remaining writing requirements.',
        '- [ ] Review Chapter I problem framing and confirm the completion date. Android 10 and above is settled under D-012.')
replace(r,
        '- [ ] Record the intended citation style and page formatting when confirmed; see MW-02 in [[Manuscript/Chapter 1-3 Writing Guide#Clarifications to retain|writing clarifications]].',
        '- [x] Record the supplied Word school-format reference and the user\'s ownership of citation style/margins under D-014; see MW-02 in [[Manuscript/Chapter 1-3 Writing Guide#Clarifications to retain|writing clarifications]].')
replace(r, 'Needs evidence; revision 2 saved 2026-10-26', 'Needs evidence; revision 3 saved 2026-10-26')
old_row = next(line for line in get(r).splitlines() if line.startswith('| I — Scope and Limitations |'))
replace(r,old_row,
        '| I — Scope and Limitations | [[Manuscript/Drafts/Chapter I Introduction#Scope and Limitations of the Project|Open section]] | Drafting; revision 3 saved 2026-10-26 | Android 10 and above confirmed. Enter the study period; preserve unresolved detailed game rules. |')
replace(r,
        'Sampling, topic coding, and one topic-total discrepancy remain unresolved.',
        'The user reports random selection and explains the parent orientation context. Exact procedure documentation, topic coding, and one topic-total discrepancy remain unresolved.')
replace(r,
        'MW-01 and MW-02 affect final presentation; retain them while drafting other sections. Q-01 affects the final device-support wording.',
        'MW-01 remains open. MW-02 records the confirmed Word format and user ownership of citation style/margins. D-012 settles Android wording; Q-01 now concerns future device validation.')

r = 'Current Focus.md'
replace(r, 'Chapter I revision 2 is saved in the working draft;', 'Chapter I revision 3 is saved in the working draft;')
replace(r,
        '2. Resolve [[Questions/Open Questions|Q-01–Q-03]] for Android support, scoring, completion, and progression before implementing dependent systems.',
        '2. Resolve [[Questions/Open Questions|Q-02–Q-03]] for scoring, completion, and progression before implementing dependent systems. Android 10 and above is confirmed under D-012; validate target devices during implementation.')

r = 'Maintenance/Vault Guide.md'
replace(r,
        'These writing references do not themselves amend feature requirements or prove research outcomes.',
        'D-014 designates [[Sources/Chapter I Unrevised Draft|the supplied Chapter I Word file]] as the school-format reference; the user handles citation style and margins. Preserve its layout/styles for later Word output. These writing references do not themselves amend feature requirements or prove research outcomes.')

r = 'Maintenance/Change Log.md'
changes[r] = get(r) + '''
### Android, respondent selection, and school-format confirmation

- Recorded D-012: Android 10 and above is the confirmed target. Updated LG-25, E-09, the technical baseline, original-conflict follow-up, and Chapter I wording. Device testing remains separate from the target requirement.
- Recorded D-013: the user describes respondent selection as randomized; the parent Grades 4–6 coverage reflects the scheduled parents' orientation meeting. Preserved CSV teacher coverage and avoided inventing a school-wide sampling frame or exact procedure.
- Recorded D-014: the supplied CHAPTER I only.docx is the user-designated school-format reference. Citation style and margins are user-owned; no Word formatting, source bytes, or citation styles were changed.
- Saved Chapter I revision 3, updated the dashboard and remaining questions, and removed resolved Android/format choices from the drafting prerequisites. Project completion date and problem-framing clarification remain open.
'''

# Keep current text counts accurate; historical change-log counts remain historical.
chapter=changes['Manuscript/Drafts/Chapter I Introduction.md']
def wc(text):return len(re.findall(r"\b[\w]+(?:['’\-][\w]+)*\b",text))
main='This chapter presents'+chapter.split('This chapter presents',1)[1]
context=chapter.split('## Project Context\n\n',1)[1].split('\n## Purpose and Description',1)[0]
r='Manuscript/Chapter I Revision Notes.md'
changes[r]=re.sub(r'revised main text approximately [\d,]+; revised Project Context approximately [\d,]+',
                  f'revised main text approximately {wc(main):,}; revised Project Context approximately {wc(context):,}',get(r))

backup=ROOT/'notes-before-confirmations.zip'
assert not backup.exists()
with ZipFile(backup,'w',ZIP_DEFLATED) as archive:
    for relative in changes:
        archive.write(VAULT/relative,'LandGrand/'+relative)
for relative,text in changes.items():
    (VAULT/relative).write_text(text,encoding='utf-8')
print(f'Updated {len(changes)} notes. Chapter I revision 3: {wc(main)} words; Context: {wc(context)} words. Original files unchanged.')
