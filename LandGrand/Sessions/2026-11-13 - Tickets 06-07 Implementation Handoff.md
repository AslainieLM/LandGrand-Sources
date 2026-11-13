---
type: session
status: active
updated: 2026-11-13
sources:
  - "[[Project/Gameplay Design]]"
  - "[[Decisions/Decision Register]]"
---

# Tickets 06–07 implementation handoff (2026-11-13)

Spec and tickets: `D:\LandGrand\LandGrand\.scratch\mountains-easy-1\` (spec.md, issues 01–12). Follows [[Sessions/2026-11-13 - Tickets 01-02 Implementation Handoff]].

## Done

- **Ticket 06, Lesson Screen with draft content** (commit `af063d0`):
  - `LevelData.cs` in the rules core: levels are data (episode, difficulty, number, time limit from the difficulty, lesson, pickups, start, checkpoint, hazards, goal). Item kinds (`ItemCatalog`: granite, quartz, feldspar, mica) are shared by every level. `LevelCatalog` holds Mountains Easy 1 only. Lesson and item texts are drafts marked "Draft — needs teacher review" (D-043, Q-04 open).
  - `LessonController` and `LessonBuilder` (menu **LandGrand > Build Lesson Scene**); art from `python Tools/Art/make_lesson_art.py` (lesson picture, item pictures, Start button, goal icons).
  - Start opens the level scene; Back returns to the level trail.
- **Ticket 07, Mountains Easy 1 playable from start to goal** (**not committed**; the user said "don't commit it okay"):
  - `LevelRun.cs` in the rules core: an attempt starts at the start, clears once at the goal, gives stars by the star rule, and saves the clear. Tests in `LevelRunTests.cs`.
  - `Assets/Scripts/Play/`: `ExplorerMotor` (walk while held; jump about 47 px; one lower double jump about 29 px with a dust puff; short edge grace and jump buffer; whole-pixel positions), `HoldButton` and `LevelInput` (touch buttons plus keyboard), `LevelGeometry`, `CameraFollow`, `LevelController` (goal check, save, basic "Level cleared!" panel with Continue).
  - `LevelBuilder` (menu **LandGrand > Build Mountains Easy 1 Level**); art from `python Tools/Art/make_level_art.py`.
  - Placeholders until later tickets: menu music (ticket 12); Android Back leaves to the level trail (ticket 10); no pit or spikes yet (ticket 09); no collectibles yet, so every clear gives 1 star (ticket 08).
- **Tests:** 72 rules tests pass outside Unity (dotnet with NUnit). The Unity scripts compile outside the Editor.
- **Font on the Lesson Screen:** the user found Pixelify Sans hard to read. VT323 was tried and rejected ("it was so very bad") and rewound. The user then asked to "just improvise the spacing": Lesson text now has 3 px more between words and lines (`Spaced` in `LessonBuilder`); the item and goal columns moved to fit. Not committed. See [[Project/Gameplay Design#Audio and text (D-042)|Gameplay Design]].

## Not yet checked

- Ticket 07 in the Unity Editor: movement feel, camera, result panel and save.
- The Lesson Screen with the new spacing.
- Scenes rebuilt while VT323 was in use point at a deleted font asset; rebuild Main Menu, Landform Map, Selection, Lesson and the level.

## Open

- Mountains Easy 1 takes about 25–30 s to walk; the spec says "finishable in about 90 s". The user has not chosen between keeping it short and making it longer.
- "5" can look like "S" in Pixelify Sans at 12 px.
- The user wants **gameplay design changes** (2026-11-13), described as "the background mountain was not moving if the character runs, and also the double jump is very boring, I want that character to flip". Do not build them yet (user: "don't implement it right now"). Settled as **D-046** (see [[Project/Gameplay Design#Level look and feel (D-046)|Gameplay Design]]): reuse the start-screen layers for the parallax, draw 4–6 somersault frames, and lengthen the level to about 60–90 s. The user chose to fold them into the still-uncommitted ticket 07 (its checklist now lists them); build them before ticket 07 is committed. Requests:
  1. **Moving background:** the mountains behind the level should scroll (parallax) as the explorer walks. Today the backdrop is fixed to the camera.
  2. **Double-jump flip:** the explorer should flip (somersault) on the double jump instead of only a dust puff.

## D-046 built (2026-11-13, after ticket 07 was committed by the user as `0b6f5d2`)

- `BackdropLayer` (camera-driven parallax, layers L0–L5), 4 somersault frames in `Assets/Art/Level/Sprites/Flip`, level 4800 px wide with new boulders and ledges; pickup, checkpoint, pit, spike and goal places in `LevelData.cs` moved to match. 72 rules tests pass; scripts compile outside Unity. Not committed, not yet checked in the Editor: run `python Tools/Art/make_level_art.py`, then **LandGrand > Build Mountains Easy 1 Level**.

## Ticket 08 built (2026-11-13, not committed, not yet checked in the Editor)

- Rules: `LevelRun.Collect` / `DismissFind` / `PendingFind` / `IsPaused` and `CollectResult` (None, FirstFind, Repeat). A first find saves the kind in `PlayerProgress` at once; the goal waits while the pop-up is open. 81 rules tests pass (9 new).
- Unity: `PickupSpot` (bobbing collectible), `LevelController` collects on touch, updates the 0/5 counter, plays a chime and sparkle, and opens the "You found an item!" pop-up (picture, name, description, OK) that freezes the explorer and blocks taps. Found kinds are saved with `GameProgress.Save`. Stars at the goal follow the collected count.
- Art: `icon_gem.png`, `btn_ok.png` from `make_level_art.py`. To test: run `python Tools/Art/make_level_art.py`, then **LandGrand > Build Mountains Easy 1 Level**. Delete `progress.json` (Application.persistentDataPath) to see the first-find pop-ups again.

## Ticket 09 built (2026-11-13, not committed, not yet checked in the Editor)

- Rules: `LevelRun.ReachCheckpoint`, `CheckpointReached`, `HitHazard` (returns the respawn spot), `Respawns`; `RespawnPoint` is the last checkpoint or the start. Items stay collected (D-040). 87 rules tests pass.
- Unity: the ground now has a real gap at the pit (dark fill inside); spike trap drawn and checked by area; falling below -40 px counts as the pit. A hazard freezes the explorer 0.35 s with a red flash and the message "Oops! Back to the checkpoint" (or "start"). The checkpoint flag changes from a grey rag to a raised green flag with "Checkpoint reached!".
- Art: `checkpoint_off/on.png`, `spikes.png`, `pit_fill.png` from `make_level_art.py`. To test: run `python Tools/Art/make_level_art.py`, then **LandGrand > Build Mountains Easy 1 Level**.

## Ticket 10 built (2026-11-13, not committed, not yet checked in the Editor)

- Rules: `LevelRun.RemainingSeconds`, `Tick`, `Pause`, `Resume`, `IsMenuOpen`, `IsTimeUp`, `RunOutcome.TimeUp`. The clock stops while the pause menu or the first-find pop-up is open, keeps running through a hazard respawn, and stops at the goal. 98 rules tests pass.
- Unity: countdown top centre (red in the last 10 s), pause button top right, pause menu (Resume, Retry, Main Menu), Time up panel (Retry, Main Menu). Retry goes to the Lesson Screen (D-040). Android Back or Escape opens the pause menu during play and closes it again; after Time up it goes to the Main Menu, after the goal to the level trail.
- Art: `btn_pause`, `btn_resume`, `btn_retry`, `btn_menu` (and pressed) from `make_level_art.py`. To test: run `python Tools/Art/make_level_art.py`, then **LandGrand > Build Mountains Easy 1 Level**. Tip: temporarily lower the time limit in `LevelData.cs` to see Time up quickly.

## Ticket 11 built (2026-11-13, not committed, not yet checked in the Editor)

- Rules: `LevelRun.TakenFlags`, `GoalResults` (Collect 5/5 and Finish before time runs out, each with Met), `LevelData.Review` (three draft sentences), `PlayerProgress.NextLevelAfter`. 104 rules tests pass.
- Unity: the result panel in the level scene is now the Result Screen: stars pop in one by one with a rising chime, the item row (missed items as grey outlines), goals with tick or cross, review sentences with the draft note, and Replay, Continue, Back to Map. Replay goes to the Lesson Screen; Continue sets `GameSession.Level` to the next available level and opens its lesson (Easy 2 shows Coming soon); Back to Map opens the Landform Map. The map, cards and trail already read the saved best stars.
- Art: `icon_tick`, `icon_cross`, `btn_replay`, `btn_map` from `make_level_art.py`. Only audio (ticket 12) is left in this slice.

## Easy pit rule and ticket 12 built (2026-11-13, not committed, not yet checked in the Editor)

- **Easy pit rule (D-048):** on Easy, falling into a pit returns the explorer about 24 px behind the last ground spot where it stood (`LevelRun.FallIntoPit`, `LevelController.SafeSpotNearThePit`); spikes still use the checkpoint; Normal and Hard keep the checkpoint rule for pits. 109 rules tests pass.
- **Ticket 12 audio:** `python Tools/Audio/make_mountains_audio.py` makes `bgm_mountains.ogg` (D minor, 84 BPM, 16 bars, 45.7 s), `amb_breeze_easy.ogg` (24 s), `sfx_hit.wav` and `sfx_checkpoint.wav`; already generated into `Assets/Audio`. The level uses `K.LevelMusic` (music 0.28, quieter than the menu 0.40). Settings sliders already drive music and breeze (music slider) and the effects (sound slider); chimes, hits, the flag and every level button use the sound-effects slider. While paused or after Time up the music and breeze duck to 30% (`StartScreenMusic.DuckTo`). Screen changes fade the music out as before.
- All 12 tickets of the Mountains Easy 1 slice are now built. Still to do: the user checks everything in the Editor, then commits.

## Next tickets

Ticket 08 (collectibles and first-find pop-up), 09 (hazards and checkpoint), 10 (timer, pause, time's up) and 12 (audio) are unblocked now and can go in any order. Ticket 11 (Result Screen) waits for 08 and 10.
