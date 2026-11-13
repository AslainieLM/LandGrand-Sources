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
- **Timeout** shows Retry or Back to Main Menu (manuscript Fig. 4C). Retry starts the level again from its Lesson Screen.
- **Pause button** during a level: Resume, Retry, Back to Main Menu.
- **Controls:** hold the left or right arrow to walk; tap jump to jump, and tap again in the air for a double jump (a little lower, with a dust puff). No running or attack. Collecting is automatic on touch.
- **Pick-ups:** the first time the player ever collects a kind of item, the game and timer pause and a "You found an item!" pop-up shows its picture, name and short description with OK. Later pick-ups of the same kind, in the same level or on replay, only play a chime and sparkle. Each found kind is saved on the device.

## Screens (D-041)

| Screen | Design |
| --- | --- |
| Start-up and Main Menu | As built (D-037, D-038, [[Project/Main Menu]]). |
| Name entry | The first time Play is tapped: one player profile per device, a name of 1–12 letters, numbers or spaces, typed with the phone's keyboard, saved at once, changeable later in Settings. |
| Landform Map | One connected pixel-art map on the 480×270 screen, in the user's 2×2 placement sketch: Mountains top left, Hills top right, Plains bottom left, Plateaus bottom right (the sketch colours only marked placement). Regions join at natural borders, linked by a trail in episode order. Unlocked regions animate: Mountains blowing snow, a drifting cloud and a circling eagle; Hills swaying trees and a stream; Plains rippling grass and butterflies; Plateaus blowing dust and a gliding hawk. Locked regions are grey with a padlock, no animation, and a guide text such as "Finish Mountains first"; tapping one stays on the map. Each region shows its star progress (for example 0/45). Back is in the top-left corner; the player's name is at the top. |
| Difficulty selection | A separate screen titled with the landform: three large cards, Easy, Normal and Hard, each with its stars (0/9, 0/15, 0/21). Normal and Hard are grey with a padlock and "Clear all Easy levels" or "Clear all Normal levels" until unlocked. Back top left; the landform animates slowly behind. |
| Level selection | A trail with one stone per level showing its stars; levels after the next playable one show a padlock. Tapping a stone opens the Lesson Screen. |
| Lesson Screen | A cream panel with the landform name and picture, three or four short sentences, the level's item pictures with names, and the level's goals. Start begins the level; Back returns to level selection. The user asked for good placement. |
| In-level layout | Top left collectibles count with an icon (for example 2/5); top centre countdown; top right pause; bottom left large left and right arrows; bottom right large jump button. |
| Result Screen | Stars pop in one by one with a chime; collected items in a row with missed ones as grey outlines; the goals with ticks; two or three review sentences. Buttons: Replay, Continue, Back to Map. |

## Audio and text (D-042)

- **Ambience** differs per landform and per difficulty (12 sets). For Mountains: Easy a light breeze, Normal stronger wind, Hard gusty, near-storm wind; Hills a stream and birds; Plains grass and crickets; Plateaus dry wind and a hawk.
- **Music:** each landform has its own original loop (Mountains first), quieter than the menu so ambience and chimes come through. The Settings sliders control both.
- **Font:** a bundled Open Font License pixel font with TextMeshPro, proposed Pixelify Sans, so typed names and lesson text can be shown. Its licence is to be checked before it is added; sprite text stays for the existing buttons.

## Content and first level (D-043)

- Build **Mountains, Easy, level 1** first, then follow the episode order.
- Draft Mountains lesson and items: granite, quartz, feldspar and mica, each marked "draft — needs teacher review". Q-04 (curriculum content and who validates it) stays open.
- Level 1: a side-scrolling mountain trail of 2–3 screens, finishable in about 90 s; 5 collectibles; a mid-level checkpoint flag; one pit and one spike trap; boulders and ledges to jump; a cave entrance with a flag as the end goal. New pixel art in the LandGrand palette; the Cave Spelunker explorer.

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
