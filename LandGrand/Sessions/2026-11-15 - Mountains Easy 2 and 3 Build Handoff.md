---
type: session
status: active
updated: 2026-11-15
sources:
  - "[[Decisions/Decision Register#D-055]]"
  - "[[Project/Gameplay Design#Mountains Easy 2 and 3 (D-055)]]"
---

# Mountains Easy 2 and 3 build handoff (2026-11-15)

Follows [[Sessions/2026-11-14 - Profile and Menu Panels Handoff]]. Spec and tickets 01–06: `D:\LandGrand\LandGrand\.scratch\mountains-easy-2-3\`. Glossary terms added to `CONTEXT.md`: Review pickup, Lesson topic, Level theme, Level layout.

## State

- **All six tickets are built. Nothing is committed** (the user makes the commits).
- **138 rules tests pass**, both outside Unity (dotnet) and in Unity 6000.6.8f1 EditMode (batch mode, 2026-11-15). The Unity scripts compile with no errors.
- **Scenes were built in batch mode:** `MountainsEasy1`, `MountainsEasy2`, `MountainsEasy3` (LandGrand > Build Mountains Levels), `Lesson` and `Profile`. Screenshots rendered from the built scenes showed the right themes, ledges, pits, spikes, goals and eagle.
- **Physics bot check (scratch, outside the project):** with the motor's own numbers, a walk-right-and-jump bot finishes Easy 1 in 66 s, Easy 2 in 73 s and Easy 3 in 73 s (limit 120 s). The pumice ledge is reached only with the vent. The wide pit needs the double jump. The garnet ledge, the climb and the marble spike gap are all reachable.
- **Not checked by a person in the Editor yet:** feel, the banner, vents, props, the Profile page arrows, and phone frame rate.

## Done

- **Ticket 01:** `LevelLayout` (width, theme, boulders, ledges, vents) and `BannerName` now live on `LevelData`. One menu item, **Build Mountains Levels**, builds every catalog level into its scene and sets each controller's level. The old "Build Mountains Easy 1 Level" item is gone. Easy 1's layout is unchanged; a test checks every boulder and ledge position.
- **Ticket 02:** six new kinds: andesite, obsidian and pumice from Easy 2, slate, marble and garnet from Easy 3. Each has home landform Mountains, giving 10 on the shelf. Their sprites are in `make_lesson_art.py`. **Profile shelves now page:** 5 slots per page with the existing Next and Prev arrow icons. Six slots could not fit 10 kinds.
- **Tickets 03 and 05:** Easy 2 "Volcano Trail" (Volcanic theme, lava-rock arch goal) and Easy 3 "Folded Peaks" (Folded rock theme, summit stone pile goal), with lessons, reviews and pickups. The lesson pictures are `lesson_volcano` and `lesson_folds`. The Lesson builder now takes its picture list from the catalog.
- **Ticket 04:** steam vent (`SteamVent` rules, `SteamVentView`, `ExplorerMotor.Launch`) with a 2 s cycle: rest, warning wisp, then puff. A puff while standing on the vent launches the explorer. The steam hiss is `sfx_steam.wav`, added to `make_mountains_audio.py`.
- **Ticket 06:** level start banner (`LevelBanner`, 1.5 s, clock held by `LevelRun.BeginIntro/EndIntro`). Living props are decoration only: lava cracks and faint fumarole wisps (Volcanic), and summit snow plus an eagle that flies off (Folded).

## Changed from the spec during the build (recorded in the spec)

1. **Lesson sentences were shortened.** Measured in Andika at UI size 15, the first wording was 308–387 px, wider than the 312 px line. The new lines are at most 298 px and keep the same facts. Marble's limestone origin stays in its pop-up text. All are still drafts (Q-04).
2. **Vent launch speed is 480 (about 128 px), not 440, and the secret ledge moved 12 px right.** At 440, an explorer holding right bumped its head under the ledge and topped out at 64 px.
3. **The Easy 3 wide pit is 64 px, not 72.** At 72 only a very late double jump crossed, which is too hard for Easy.
4. **The lesson heading stays in Andika (D-051).** The spec's "Micro 5" wording was a mistake.

## For the user in Unity

1. The scenes are already built. If the art changes, run `python Tools/Art/make_lesson_art.py` and `python Tools/Art/make_level_art.py`, then **Build Lesson Scene** and **Build Mountains Levels**.
2. Play Start Screen > Mountains > Easy > 1, 2, 3. Check the banner, the vents (Easy 2), the wide pit and garnet (Easy 3), and the Result.
3. Open the Profile and page the Mountains shelf.
4. Commit when happy.

## After the user's playtest (2026-11-15)

- The user tested Easy 1-3 and asked that spike traps work like the Easy pits (D-056). Built: on Easy, a trap sends the explorer back a short way behind its last safe ground spot, clear of the spikes; Normal and Hard keep the checkpoint. 140 rules tests pass outside Unity; the Unity batch test could not run because the Editor was open. No scene rebuild is needed.

## Open

- **D-036 / panel:** the steam vent is a level object the manuscript does not name.
- **Review notes not acted on (style only):** theme sprite names are strings in three switches. A per-theme record would remove that once a fourth theme exists.
- Content stays draft until a teacher reviews it (Q-04).
