---
type: design
status: confirmed
updated: 2026-11-13
sources:
  - "[[Sources/Final Manuscript Chapters I-III 2026-11-13]]"
  - "[[Decisions/Decision Register#Confirmed decisions|D-039 to D-044]]"
---

# Gameplay Design

This note holds the gameplay the user settled on 2026-11-13 in a grilling interview, building on the final manuscript (D-036) and its procedure (LG-26 to LG-32). Each section names its decision. None of it is built yet; the first build target is **Mountains, Easy, level 1**. Answers are summarized from the chat; quoted wording is the user's.

## Progression and scoring (D-039)

| Rule | Decision |
| --- | --- |
| Episode order | Mountains → Hills → Plains → Plateaus, the manuscript's listed order. Mountains starts unlocked. |
| What counts | "Collectibles" are rocks and minerals alike. |
| Stars | Clearing a level gives 1 star for 0–40% of its collectibles, 2 stars for 41–99%, 3 stars for 100%. The user changed the top band from 81–100% to "collected all / 100%". |
| Clearing | Reaching the end goal clears the level, whatever the stars. Unlocking depends on clearing, not on stars (manuscript Fig. 4D). |
| Level size | Easy levels have 5 collectibles (0–2 = 1 star, 3–4 = 2 stars, 5 = 3 stars) and one checkpoint. Normal and Hard get more later. |
| Goals shown | Each level shows its goals as a guide on the Lesson and Result screens, for example "Collect 5/5" and "Finish before time runs out". Only collectibles decide the stars. |
| Time limit | Easy 2 minutes, Normal 3 minutes, Hard 4 minutes. |

## Hazards, controls and pick-ups (D-040)

- **No health bar.** Touching a trap or falling into a pit sends the explorer back to the last checkpoint; the timer keeps running and collected items stay collected. A health bar is added only if the panelists ask for one.
- **Easy pits (D-048, changes the rule above for pits on Easy only):** falling into a pit puts the explorer back a short way behind the last ground spot where it stood (about 24 px), not at the checkpoint. Spikes still use the checkpoint rule; Normal and Hard keep the checkpoint rule for pits too.
- **Timeout** shows Retry or Back to Main Menu (manuscript Fig. 4C). Retry starts the level again from its Lesson Screen.
- **Pause button** during a level: Resume, Retry, Back to Main Menu.
- **Controls:** hold the left or right arrow to walk; tap jump to jump, and tap again in the air for a double jump (a little lower, with a dust puff). No running or attack. Collecting is automatic on touch.
- **Pick-ups:** the first time the player ever collects a kind of item, the game and timer pause and a "You found an item!" pop-up shows its picture, name and short description with OK. Later pick-ups of the same kind, in the same level or on replay, only play a chime and sparkle. Each found kind is saved on the device.

## Screens (D-041)

| Screen | Design |
| --- | --- |
| Start-up and Main Menu | As built (D-037, D-038, [[Project/Main Menu]]). |
| Name entry | The first time Play is tapped: one player profile per device, a name of 1–12 letters, numbers or spaces, typed with the phone's keyboard, saved at once, changeable later in Settings. |
| Landform Map | One connected pixel-art map on the 480×270 screen, in the user's 2×2 placement sketch: Mountains top left, Hills top right, Plains bottom left, Plateaus bottom right (the sketch colours only marked placement). Regions join at natural borders, linked by a trail in episode order. Unlocked regions animate: Mountains blowing snow, a drifting cloud and a circling eagle; Hills swaying trees and a stream; Plains rippling grass and butterflies; Plateaus blowing dust and a gliding hawk. Locked regions are grey with a padlock, no animation, and a guide text such as "Finish Mountains first"; tapping one stays on the map. Each region shows its star progress (for example 0/45). Back is in the top-left corner. *Changed by the user on 2026-11-13 after ticket 04: the player's name is no longer shown on the map, and Back is an arrow icon with no word, for a cleaner map.* |
| Difficulty selection | A separate screen titled with the landform: three large cards, Easy, Normal and Hard, each with its stars (0/9, 0/15, 0/21). Normal and Hard are grey with a padlock and "Clear all Easy levels" or "Clear all Normal levels" until unlocked. Back top left; the landform animates slowly behind. |
| Level selection | A trail with one stone per level showing its stars; levels after the next playable one show a padlock. Tapping a stone opens the Lesson Screen. |
| Lesson Screen | A cream panel with the landform name and picture, three or four short sentences, the level's item pictures with names, and the level's goals. Start begins the level; Back returns to level selection. The user asked for good placement. |
| In-level layout | Top left collectibles count with an icon (for example 2/5); top centre countdown; top right pause; bottom left large left and right arrows; bottom right large jump button. |
| Result Screen | Stars pop in one by one with a chime; collected items in a row with missed ones as grey outlines; the goals with ticks; two or three review sentences. Buttons: Replay, Continue, Back to Map. |

## Audio and text (D-042)

- **Ambience** differs per landform and per difficulty (12 sets). For Mountains: Easy a light breeze, Normal stronger wind, Hard gusty, near-storm wind; Hills a stream and birds; Plains grass and crickets; Plateaus dry wind and a hawk.
- **Music:** each landform has its own original loop (Mountains first), quieter than the menu so ambience and chimes come through. The Settings sliders control both.
- **Font:** a bundled Open Font License pixel font with TextMeshPro, proposed Pixelify Sans, so typed names and lesson text can be shown. Its licence is to be checked before it is added; sprite text stays for the existing buttons. *Changed on 2026-11-13:* the user found Pixelify Sans hard to read on the Lesson Screen ("it was not easy to read, find a good fonts please"). Pixelify Sans and four other OFL fonts were compared (VT323, DotGothic16, Tiny5, Silkscreen; all from github.com/google/fonts, downloaded with the user's approval). VT323 at 16 px was tried and then rejected by the user the same day ("it was so very bad"); the change was rewound, so the game still uses Pixelify Sans at 12 px. The user then asked to "just improvise the spacing": the Lesson Screen text now has 3 more pixels between words and between lines, and the item and goal columns moved slightly so the wider text fits. *Changed again on 2026-11-13:* Pixelify drew "5" like "S" and crowded its letters, so the user asked for a better font. DotGothic16 was tried and lost thin letters at 12 px (its grid is 16 px). Fonts must be drawn at a whole multiple of their own pixel grid. The user then chose the best fit from a mock-up: **Micro 5** (OFL, github.com/google/fonts; Jersey 10, Jersey 15 and Press Start 2P were the other candidates) at 15 px for all text, with 3 px extra word spacing and about 2 px extra line spacing on the Lesson Screen. Pixelify Sans is no longer used.

## Content and first level (D-043)

- Build **Mountains, Easy, level 1** first, then follow the episode order.
- Draft Mountains lesson and items: granite, quartz, feldspar and mica, each marked "draft — needs teacher review". Q-04 (curriculum content and who validates it) stays open.
- Level 1: a side-scrolling mountain trail of 2–3 screens, finishable in about 90 s; 5 collectibles; a mid-level checkpoint flag; one pit and one spike trap; boulders and ledges to jump; a cave entrance with a flag as the end goal. New pixel art in the LandGrand palette; the Cave Spelunker explorer.

## Level look and feel (D-046)

Settled 2026-11-13 after the user played ticket 07's first build. Built 2026-11-13 after the user asked for it; not yet checked in the Editor. Built as: layers L0–L5 slide with the camera (`BackdropLayer`; L6 and L7 are ground strips and are left out); a 4-frame somersault made from quarter turns of a tucked explorer (`make_level_art.py`; can be redrawn by hand later); the level is 4800 px wide (about 65 s of walking).

- **Moving background:** the mountains behind the level scroll in layers (parallax) as the explorer walks, far layers slower than near ones. Reuse the start screen's 8-layer mountain background and its layer-scrolling script (the reused art was replaced by Mountains-only layers in D-049; the scrolling stays). Today's level backdrop is fixed to the camera.
- **Double-jump flip:** the double jump becomes a full forward somersault, about 0.3 s, then a normal landing. It uses 4–6 new hand-drawn curled-up frames, not a rotated sprite, so the pixel art stays sharp. The dust puff stays.
- **Level length:** Mountains Easy 1 grows from about 25–30 s to about 60–90 s to finish (the earlier "about 90 s" target), so the 2-minute timer matters. The item places in `LevelData.cs` move with the new layout.
- **Manuscript (D-036):** none of these changes a game rule in the final manuscript; they are presentation and level layout.

## Mountains backdrop and level HUD (D-049)

Asked 2026-11-13 after the user saw that the level background was the same as the Start Screen's. Built 2026-11-13; not yet checked in the Editor. This replaces the "reuse the start screen's background" part of D-046; the parallax itself stays.

- **Why:** the start-screen layers mix every landform (plateaus and green rolling hills appear behind a Mountains level) and make the level look like the Start Screen.
- **Mountains-only background:** six new layers drawn by `Tools/Art/make_mountains_backdrop.py` into `Assets/Art/Level/Sprites/Backdrop/Mountains/`: L0 sky (deeper blue high up, pale at the horizon, soft sun), L1 long flat clouds and two far eagles, L2 a far pale snowy range with valley mist, L3 a middle blue-grey rocky range with small snow caps, L4 a soft blue-green pine forest, L5 an alpine meadow with a few pines and rocks. Same scroll speeds as before.
- **Colour balance:** palette colours plus even mixes of two palette colours. Far layers are lightest and palest; nearer layers get a little darker and greener; the layers behind the explorer (screen rows 100–220) stay mid-toned so the explorer, pickups, ledges and boulders stand out. Sunlight comes from the upper right on every layer.
- **HUD layout:** one top strip, 6 px from the edges. Left: a panel with the level name ("Mountains Easy 1") over the gem count. Centre: the countdown with a new trail progress bar under it (start on the left, the checkpoint flag that turns green when reached, the red goal flag on the right, and an explorer marker that moves with the explorer). Right: the pause button. Touch controls stay in the bottom corners.
- **Manuscript (D-036):** presentation only; no game rule changes.

## Flowchart redesign (D-044)

The redesigned procedure is [[Manuscript/Drafts/Land Grand - Chapter III - Game Procedure Flowchart - v2.drawio|the draw.io file, version 2]], five pages that replace Figures 4A–4E. It differs from the final manuscript's figures in these places, each a decision above:

| Part | Change from the manuscript figure | Decision |
| --- | --- | --- |
| 1 Launch and Main Menu | Start-up "Tap to Start" screen; name entry on first Play; "Exit game?" confirmation; Settings lists the volume controls | D-037, D-038, D-041, D-032 |
| 2 Episode and level | Locked episodes show a guide text; separate difficulty selection screen; Back buttons | D-041 |
| 3 Lesson and level | Timer per difficulty; double jump; trap or pit → checkpoint; first-find pop-up pauses the timer; pause menu | D-039, D-040 |
| 4 Score, save, unlock | Star thresholds 0–40% / 41–99% / 100% of collectibles; found items saved; Back to Map on the Result Screen | D-039, D-041 |
| 5 Continue or complete | Unchanged, except "required episode levels" stays open (Q-03) | — |

## Build spec

The first playable slice (Mountains, Easy 1) is specified in `D:\LandGrand\LandGrand\.scratch\mountains-easy-1\spec.md` (2026-11-13, written with `/to-spec`; local files chosen as the tracker). It tests one seam: a plain C# rules core (stars, level run, player progress) with Unity EditMode tests; screens, art and feel are checked by playing in the Editor. Replays keep the best stars and every found item (D-045).

The user approved its split into 12 tickets on 2026-11-13: `.scratch\mountains-easy-1\issues` to `12` in the Unity repo.

## Still open

- What "required episode levels" means (Q-03), and progress reset and reinstall behaviour (Q-07).
- Final tutorial wording, after these rules (Q-06).
- Curriculum content and its validator (Q-04).
- Chapter III's graphics-tool list (Q-13 c).
