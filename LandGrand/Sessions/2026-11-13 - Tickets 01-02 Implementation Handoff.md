---
type: session
status: active
updated: 2026-11-13
sources:
  - "[[Project/Gameplay Design]]"
  - "[[Decisions/Decision Register]]"
---

# Tickets 01–02 implementation handoff (2026-11-13)

Spec and tickets: `D:\LandGrand\LandGrand\.scratch\mountains-easy-1\` (spec.md, issues 01–12).

## Done

- **Ticket 01, rules core and star rule.** `StarRule` in the `LandGrand.Rules` assembly (no Unity types) plus the EditMode test assembly `LandGrand.Rules.Tests`.
- **Ticket 02, player progress and save/load** (commit `9edd313`):
  - `PlayerProgress`: Mountains is the only unlocked episode; levels play in order; Normal unlocks after all 3 Easy levels, Hard after all 5 Normal levels, never by stars; a worse replay keeps the best stars (D-045); found item kinds are never removed.
  - `ProgressStore`: saves to a `.tmp` file first, then swaps it in; a missing or corrupt file gives a fresh profile.
  - `GameProgress` (Unity side): loads `progress.json` from the persistent data folder before the first scene. Volume settings stay in `GameSettings`.
  - Tests: the Unity Test Runner (EditMode) shows 32 tests passing, 0 failed (user confirmed 2026-11-13).

## Not yet checked

- Launch load in Play mode, and the file swap (`File.Replace`) on an Android device.
- `GameProgress.Save()` has no caller yet. Name entry (ticket 03) and the Result Screen (ticket 11) must call it.

## Needs a user answer

- Hard has 7 levels per episode. This is inferred from the "0/21" card in the spec, not stated in the manuscript (D-036). Confirm or correct.
- Q-03 still open: Hills, Plains and Plateaus stay locked until it is answered.
- An unknown key in the save file counts as corrupt, so a future save-format change needs a migration step.

## Next

Ticket 03 (pixel font, name entry, Settings name field, Tutorial double-jump line). Confirm the Pixelify Sans licence first. Then ticket 04 (Landform Map); 05 to 07 follow in a chain; after 07, tickets 08, 09, 10 and 12 can go in any order.
