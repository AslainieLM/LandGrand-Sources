---
type: review
status: reviewed
updated: 2026-10-26
sources:
  - "[[Sources/Pre-proposal]]"
---

# Pre-proposal Review

The pre-proposal gives a coherent initial audience, platform, subject boundary, and learning loop. It leaves several rules too open to serve as a complete implementation specification or research protocol.

## Findings

| Finding | Evidence and implication | Follow-up |
| --- | --- | --- |
| Original Android range conflict, now resolved | The source retains Android 10–14 versus Android 10 and above wording. The user confirmed Android 10 and above under D-012. | [[Decisions/Decision Register|D-012]]; Q-01 retains device validation |
| Undefined performance awards | Up to three stars are specified without metrics or thresholds. A star requirement for unlocking is not stated. | Q-02 |
| Undefined completion and unlocking | Easy → Normal → Hard and episode unlocking are specified, but level success, required episode levels, and episode order are not explicit. | Q-03 |
| Missing content inventory | Landforms are named, but individual rocks/minerals, competencies, references, and lesson texts are absent. | Q-04 |
| Missing evaluation design | The title states an intended knowledge benefit, but the source supplies no method or results establishing it. | Q-05 |
| Incomplete play and persistence rules | Time limits, failure, retries, replay effects, settings, and profile/reset behavior are not defined. | Q-06 and Q-07 |

Sources: [[Sources/Pre-proposal Extract#Scope of the Study|Scope]], [[Sources/Pre-proposal Extract#Limitations of the Study|Limitations]], [[Sources/Pre-proposal Extract#Program Specification|Program Specification]], and [[Sources/Pre-proposal Extract#Hardware Specification|Hardware Specification]]. Full prompts are in [[Questions/Open Questions|Open Questions]].

## Workload inference

The stated counts imply **15 levels per episode** and **60 levels overall**: `4 × (3 + 5 + 7) = 60`. This is arithmetic derived from the proposal, not an explicit statement of 60 unique scenes or 60 distinct maps. Reuse and level variation are not specified.

An upper bound of **180 stars** follows only if all 60 levels award three stars and the final total counts one best award per level. The proposal does not define replay aggregation, so 180 is conditional, not an accepted rule.

## Evidence limits

The filename “Final,” the institutional form, and its effective date do not establish adviser approval. No approval evidence was supplied. The Word package's metadata reports two pages, but page layout was not visually verified; citations use source sections and extracted paragraph anchors instead of page numbers. The original document is preserved unchanged.

## Suggested order of clarification

The Android target is settled by D-012. Resolve success/scoring and progression before implementing those rules, then validate builds against the confirmed Android target. Confirm educational content and evaluation design before making a learning-effectiveness claim. This ordering is a recommendation, not a project decision.
