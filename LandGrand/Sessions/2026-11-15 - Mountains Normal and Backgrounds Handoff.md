---
type: session
status: active
updated: 2026-11-15
sources:
  - "[[Decisions/Decision Register#D-061]]"
  - "[[Decisions/Decision Register#D-062]]"
  - "[[Decisions/Decision Register#D-063]]"
  - "[[Decisions/Decision Register#D-064]]"
  - "[[Project/Gameplay Design#Mountains Normal 1–5 (D-062)]]"
---

# Mountains Normal and backgrounds handoff (2026-11-15)

Follows [[Sessions/2026-11-15 - Mountains Easy 2 and 3 Build Handoff]]. Spec, tickets and Codex's handover: `D:\LandGrand\LandGrand\.scratch\mountains-normal\` (`spec.md`, `issues/01`–`07`, `HANDOVER.md`).

## State

- **Mountains Normal 1–5 are built, played by the user and committed** in the Unity project as `aaa3bef` (2026-11-15). Codex (ChatGPT) wrote the code from Claude's spec, art, audio and tickets; Claude reviewed it and fixed the findings.
- **198 rules tests pass** (dotnet, and Unity EditMode in Codex's run).
- **After `aaa3bef`, not committed yet:** the theme background rule in `LevelThemes.cs`, and the Hills, Plains and Plateaus menu pictures with `LandformBackdrop.cs`. The user still has to rebuild and check them in the Editor.
- **Vault:** D-061 to D-064 and this note are not committed yet (the user makes the commits).

## Done

1. **Code tidy-up (D-061):** `LevelController` split into parts with `Begin(LevelController)` and `IsBuilt`; theme art is one entry per theme in `LevelThemes.cs`. Rules recorded in [[Project/Technical Baseline]].
2. **Mountains Normal 1–5 (D-062):** Pulag, Pinatubo, Matutum, Apo and Everest; crumbling ledges, falling rocks, moving platforms and wind gusts; two checkpoints; ten new kinds (Mountains now has 20); Collection pages; three new badges in a 4×3 grid; stronger Normal wind.
3. **Review of Codex's work (`/code-review`)**, then six fixes:
   - crumbling ledges and moving platforms act like ledges, so the explorer can jump up through them;
   - `WindWatcher` became a proper part;
   - the checkpoint flag list is bounds-checked;
   - the ambience is chosen from one table by difficulty;
   - stale comments were fixed;
   - Codex's two Play Mode validation scripts were moved out of the project.
4. **Playtest fixes:**
   - the top-left level name panel is wider (156 px), so "Mountains Normal 3" fits;
   - a new `LevelClock` stops every moving object (platforms, rocks, wind, crumbling ledges, vents, falling chips) while the game is paused: the start banner, the pause menu and the "You found an item!" pop-up.
5. **Backgrounds (D-063):**
   - every level theme has its own six-layer background (`Tools/Art/make_normal_backdrops.py`); Easy 1 keeps the alpine one;
   - the builder stops with a clear error for a theme with no background, so Hills, Plains and Plateaus themes must get their own;
   - the difficulty, level and lesson screens show the picked landform's picture (`Tools/Art/make_selection_art.py`, `LandformBackdrop.cs`).
6. **Pause and Time's up (D-064):** the Main Menu button is now **Levels** (a grid icon) and opens the level selection; Android Back after time up also goes there.

## For the user in Unity

Run **Build Mountains Levels**, **Build Selection Scenes**, then **Build Lesson Scene**. Check:
- Easy 1 still builds;
- the menu screens still show Mountains;
- once another landform is open, its picture appears.

## Open

- **Next feature (recommended, not yet agreed):** Mountains Hard 1–7 plus the Landform Description Screen (LG-05, LG-14, LG-31, LG-32), so the first episode is complete end to end. Design it with `/grilling`, then assets, spec and Codex tickets, as for Normal.
- Hard ambience still uses the Easy breeze (a stand-in).
- The crumbling ledges, falling rocks, moving platforms and wind gusts are manuscript additions (D-036, Q-13 d); the adviser and panel should hear about them.
- All lesson, review and item text stays draft until a teacher reviews it (Q-04).
