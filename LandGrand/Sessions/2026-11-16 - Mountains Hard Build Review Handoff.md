---
type: session
status: active
updated: 2026-11-16
sources:
  - "[[Decisions/Decision Register#D-065]]"
  - "[[Project/Gameplay Design#Mountains Hard 1–7 (D-065)]]"
---

# Mountains Hard build review handoff (2026-11-16)

Follows [[Sessions/2026-11-15 - Mountains Hard Plan Handoff]].

## State

- **Built and committed by the user:** Codex built tickets 01–09 from `.scratch/mountains-hard/`. Commits `5a453e5` (art and audio), `d26f12d` (code), `db29c30` (spec, tickets, bot) and `5940ec7` (verification notes). Codex reports 234 EditMode tests and 19 focused Play Mode checks passing, and all six builders working. Its handover is `.scratch/mountains-hard/HANDOVER.md`.
- **Claude review (`/code-review`, 2026-11-16, against `08ce224`):**
  - Spec axis: all seven Hard layouts, the text, the rolling boulder and ice rules, the unlock flow, the badges and grid, the Hard wind and the theme offsets match the spec. Small additions nobody asked for: a drifting Hills cloud on the map, a 20 px/s slide-sound threshold, smaller medals (26 px) with two-line names in the badge grid, and a level-clock mode for the Glacier snow.
  - Standards axis: no hard violations; every new line is commented; no Unity types in Rules. Judgement calls: `IceWatcher` and `RollingBoulderWatcher` connect themselves in `Start()` instead of being started by `LevelController` like the other parts (D-061); `world_peaks` hard-codes Hard levels 5–7; `MaxStarsFor` returns a fixed 45.
- **Two small fixes by Claude, not committed:**
  - `IceWatcher`: the ice check now accepts feet within 0.01 px of the ground instead of exactly 0.
  - `ResultScreen`: Next Episode falls back to the map if the `LandformDescription` scene is missing from the build list.
  - They were not compiled or tested, because the Unity Editor was open. Unity recompiles them on focus; run the EditMode tests once.

## Open for the user

1. Rebuild **Build Mountains Levels** (the Result Screen lives in the level scenes), let Unity compile, and run the EditMode tests.
2. Play the checklist in `.scratch/mountains-hard/issues/09-final-check-and-handover.md`, and listen to the new sounds.
3. Commit the two fixes and these vault notes.
4. Tell the adviser and panel about the Q-13 (d) additions.
5. Optional clean-up: start the two watchers from `LevelController` like the other parts.
6. Next feature: plan Hills.
