---
type: session
status: active
updated: 2026-11-14
sources:
  - "[[Project/Gameplay Design]]"
  - "[[Project/Game Font]]"
  - "[[Decisions/Decision Register]]"
---

# Mountains Easy 1 polish handoff (2026-11-13 to 14)

Follows [[Sessions/2026-11-13 - Tickets 06-07 Implementation Handoff]]. Spec and tickets: `D:\LandGrand\LandGrand\.scratch\mountains-easy-1\`.

## State

- **All 12 tickets of the Mountains Easy 1 slice are built and committed by the user**: ticket 07 `0b6f5d2`, D-046 and font files `c5d87ce`, ticket 08 `35c7ace`, tickets 09–12 with the Easy pit rule `d6a8cfe`, and the backdrop, HUD and font work below `21c4498`.
- **109 rules tests pass** outside Unity (dotnet with NUnit). The Unity scripts compile outside the Editor with no errors and no CS0618 warnings.
- **Not yet played through in the Editor** as a whole slice. The user tested parts (font, backdrop, HUD, ledges) and reported the problems fixed below.

## Done this session

- **Tickets 08–12** (collectibles and first-find pop-up; pit, spikes and checkpoint; timer, pause and Time up; Result Screen and progress; Mountains music, ambience and sound effects). Each got a review with no blocking defects.
- **Easy pit rule (D-048):** on Easy, a fall into a pit puts the explorer back about 24 px behind the last ground spot. Spikes and Normal/Hard pits still use the checkpoint.
- **Solid ledges:** the explorer walked through the sides of ledges, because they were one-way platforms. Ledges are now solid 10 px stone slabs (`LevelBuilder.cs`, the `Ledges` loop adds them to `solids`).
- **Mountains-only backdrop and organized HUD (D-049):** the level used the start-screen layers, which mix all landforms. `Tools/Art/make_mountains_backdrop.py` draws six new layers (sky, clouds, far snowy range, middle rocky range, pine forest, alpine meadow) into `Assets/Art/Level/Sprites/Backdrop/Mountains/`, with balanced colours that keep the play area readable. The HUD is one top strip: the level name over the gem count on the left, the timer with a new trail progress bar (start, checkpoint flag that turns green, goal flag, explorer marker) in the centre, and pause on the right.
- **Font fix (D-047, D-050):**
  - The level scene had saved TextMeshPro's smooth default font. The builder loaded the font, then an asset refresh made the reference stale. Every builder now calls `PixelSceneKit.FixFonts()` just before saving, which reloads Micro 5 and puts it on every text.
  - 15 px was 1.5x of Micro 5's pixel grid and bent the letters ("so hard to read"). An 11 px/22 px mix was "so small". **All text is now 22 px (2x)**, and the Lesson, item pop-up, Result, HUD, guide, lock-hint and name-panel layouts were widened to fit. Details: [[Project/Game Font]].
- **Unused fonts deleted (2026-11-14, at the user's request):** `Micro5 Raster.asset` (15 px), `Micro5 1x.asset` (11 px), and the Pixelify Sans files (`PixelifySans.ttf`, `PixelifySans Raster.asset`, `OFL.txt`). Only `Micro5.ttf`, `OFL-Micro5.txt` and `Micro5 2x.asset` remain. Not committed.

## For the user to do in Unity

1. Rebuild every scene. The committed scenes come from the 11/22 px mix build, and some labels pointed to the now-deleted `Micro5 1x.asset`; the rebuild puts 22 px Micro 5 on all of them. Run **Build Main Menu Scene**, **Build Landform Map Scene**, **Build Selection Scenes**, **Build Lesson Scene**, **Build Mountains Easy 1 Level**.
2. Play the whole slice from the Start Screen: Main Menu → Map → Mountains → Easy → 1 → Lesson → level → Result. Check: text size and fit on every screen, parallax and backdrop, somersault, all 5 pickups reachable with the solid ledges, pit and spikes, Easy pit return, checkpoint, timer, pause, Time up, Result, music and sounds.
3. Commit the rebuilt scenes and the font deletions.

## Open

- `21c4498` committed `Tools/Art/__pycache__/*.pyc`. The repository has no ignore rule for them; add `__pycache__/` to `.gitignore` and remove them from git.
- The Result Screen shows this attempt's stars, not the best stars (judgement call, not yet decided by the user).
- No test covers the Unity-side spot picking of the Easy pit rule.
- A level with a third goal would break the Result goal row (it has room for two).
- The Lesson Screen no longer shows "You will find:" and "Goals:" headings (no room at 22 px).
- Q-03 (episode order and unlocking) and Q-04 (curriculum content and who validates it) are still open and block the next levels.

## Next feature: draft prompt

Recommended next step after the Editor check: **Mountains Easy 2 and 3**, so the player can finish Easy and see Normal unlock. Their lessons and item sets wait on Q-04, so start with a grilling session rather than code. Prompt to paste into a fresh session:

> /grill-with-docs Plan Mountains Easy 2 and Easy 3 for LandGrand. Read `Current Focus.md`, `Sessions/2026-11-14 - Mountains Easy 1 Polish Handoff.md`, `Project/Gameplay Design.md`, `Project/Learning Content.md`, the Decision Register and Open Questions (Q-03, Q-04) in the vault, and `.scratch/mountains-easy-1/spec.md` in the Unity project. Mountains Easy 1 is built (`LevelData.cs`, `LevelBuilder.cs`). Settle for each new level: the lesson topic and its 3–4 draft sentences (still marked "Draft — needs teacher review" until Q-04 is answered), which rocks or minerals are collected and any new item kinds, layout length and difficulty step from Easy 1 (pits, spikes, ledges, boulders, checkpoint), the review sentences, and whether `LevelBuilder` should become data-driven so one builder makes every level. Check every choice against the final manuscript (D-036) and keep 22 px text layouts (D-050). Do not write code; end with a spec I can turn into tickets.
