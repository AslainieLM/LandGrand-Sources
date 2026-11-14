---
type: session
status: active
updated: 2026-11-14
sources:
  - "[[Decisions/Decision Register]]"
  - "[[Project/Gameplay Design]]"
  - "[[Project/Game Font]]"
---

# Profile, Settings and Tutorial handoff (2026-11-14)

Follows [[Sessions/2026-11-14 - Mountains Easy 1 Polish Handoff]]. Spec and tickets: `D:\LandGrand\LandGrand\.scratch\profile-collection\` (spec.md, issues 01–05). Glossary: `D:\LandGrand\LandGrand\CONTEXT.md`.

## State

- **All work below is uncommitted.** The user makes the commits.
- **118 rules tests pass** outside Unity (9 new Collection tests). The Unity scripts compile outside the Editor.
- **Not checked in the Editor:** Unity had the project open, so no scene could be rebuilt from the command line. The Profile layout was checked with a drawn mock-up using the real sprites and fonts.

## Done this session

- **Reading font extended (D-051):** the Lesson heading ("Level 1: Mountains") and its draft note now use Andika.
- **Tutorial panel (D-053):** page text became real Andika text (it was baked pixel-font pictures); Prev/Next became arrow icons; Back is an arrow icon top-left; the panel covers the logo. `TutorialPanel.cs` holds titles and sentences.
- **Settings panel (D-053):** Back arrow icon top-left, green SAVE bottom-right; SAVE keeps the volumes, Back reverts them.
- **Profile and Collection (D-052, tickets 01–05 built and reviewed):**
  - Rules: `ItemKind` has `IsRock` and `HomeLandform`; `PlayerProgress` has `TotalStars` and `ClearedLevelCount`; new `Collection` (shelves, found count, total). Tests in `CollectionTests.cs`.
  - Main Menu: round explorer portrait (32x32) top-right with the name under it; opens the new Profile scene.
  - Profile scene (`ProfileBuilder`, `ProfileController`): explorer strip (portrait, "Explorer: name", pencil, Stars, Found n/total, Levels cleared), four landform shelves (found items in colour, unfound as flat dark shapes with "?", "Coming soon" for Hills, Plains, Plateaus), item card (picture, name, Rock/Mineral, description, draft note), name panel prefilled with the saved name.
  - Name editing moved from Settings to the Profile (Gameplay Design updated).
  - The code review found the name panel opened empty and the silhouettes kept shading; both fixed.
- **New art** (`Tools/Art/make_mainmenu_art.py`): Back, Prev, Next and pencil icon buttons, SAVE button, explorer portrait.

- **Main Menu base camp (D-054, same day):** a new golden-afternoon camp background (`Tools/Art/make_menu_camp.py`: sky, clouds, peaks, pines, clearing with tent, map board, log and campfire; animated fire and sparks; the explorer is the start-screen explorer itself in its relaxed standing frame (`explorer_15`, legs together; the walking frame looked wrong when still), standing on the grass a little away from the fire and facing it (the log seat moved in front of the tent); adventure details added: a dirt trail winding from the bottom of the screen toward the mountains with footprints, a signpost at its start, a flag on the left peak, a flickering lantern by the tent, a coil of rope, boulders and mushrooms; drawn 1.5x (48x48) so it reads well; the near-white headlamp is amber here. (Sitting poses were tried and rejected by the user on 2026-11-14.) Pixel-perfect pass: every camp sprite has even sizes, cameras turn off MSAA and HDR, and the one quality level with 2x anti-aliasing is now 0. The badge and Profile totals use one font (Andika) so the text lines up; a waving tent pennant, two butterflies, an eagle circling the peak, a rock crate whose quartz twinkles, flowers and a backpack). The title is gone from the menu. Player badge top-left (portrait, name, stars, found items; opens the Profile), Settings/Tutorial/Exit as named icon buttons top-right, a big bobbing PLAY at the bottom. The Profile uses the same camp. Checked with a drawn mock-up; compiles.

- **Later fixes (same day):** the Main Menu badge name was hidden (its Ellipsis box was shorter than an Andika line, so TextMeshPro dropped the line); the box is now 30 px and the scene saves "Explorer" as a placeholder. The badge no longer greys out (no colour tint). Profile: each total is one label ("Stars 3", word in clay) on even 120 px columns; the strip is y 6–54; shelves are 50 px with a 1 px gap so frames and names clear the borders. The Profile scene must be rebuilt, or the old labels show "Stars Stars 3".
- **Not kept:** `ProjectSettings/QualitySettings.asset` level 3 anti-aliasing was set to 0, but the open Editor wrote it back to 2. Set it in Edit > Project Settings > Quality if wanted; the menu cameras already turn MSAA off.
- **Committed 2026-11-14** at the user's request (Unity project and vault).

## For the user to do in Unity

1. Run **LandGrand > Build Main Menu Scene**, then **LandGrand > Build Profile Scene**.
2. Play from the Start Screen: Main Menu portrait → Profile → tap a found item → card → Back; pencil → change name → OK; Settings → move a slider → Back (volume reverts) and SAVE; Tutorial pages with the arrows.
3. Commit when happy.

## Open

- Check the new Main Menu (D-054) in the Editor: run `python Tools/Art/make_menu_camp.py` (already run once), then **Build Main Menu Scene** and **Build Profile Scene**.
- Badges/achievements wait for the adviser (D-052). Progress reset stays open (Q-07).
- Items for Hills, Plains and Plateaus wait on Q-04.
- Earlier open items from [[Sessions/2026-11-14 - Mountains Easy 1 Polish Handoff]] still apply (`__pycache__` in git, Result best stars, Result goal row room).
