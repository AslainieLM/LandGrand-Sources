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
- **Easy pits (D-048, changes the rule above for pits on Easy only):** falling into a pit puts the explorer back a short way behind the last ground spot where it stood (about 24 px), not at the checkpoint. *Changed again 2026-11-15 (D-056):* spike traps on Easy now work the same way: the explorer comes back a short way behind the last safe ground spot, clear of the spikes. Normal and Hard keep the checkpoint rule for both traps and pits.
- **Timeout** shows Retry or Back to Main Menu (manuscript Fig. 4C). Retry starts the level again from its Lesson Screen.
- **Pause button** during a level: Resume, Retry, Back to Main Menu. *Shown as icons with a small name under each (D-057): a green play triangle, a circle arrow and a house; the Time's up panel uses the same Retry and house icons.*
- **Controls:** hold the left or right arrow to walk; tap jump to jump, and tap again in the air for a double jump (a little lower, with a dust puff). No running or attack. Collecting is automatic on touch.
- **Pick-ups:** the first time the player ever collects a kind of item, the game and timer pause and a "You found an item!" pop-up shows its picture, name and short description with OK. Later pick-ups of the same kind, in the same level or on replay, only play a chime and sparkle. Each found kind is saved on the device.

## Screens (D-041)

| Screen | Design |
| --- | --- |
| Start-up and Main Menu | As built (D-037, D-038, [[Project/Main Menu]]). |
| Name entry | The first time Play is tapped: one player profile per device, a name of 1–12 letters, numbers or spaces, typed with the phone's keyboard, saved at once, changeable later in the Profile (D-052; was Settings under D-041). |
| Landform Map | One connected pixel-art map on the 480×270 screen, in the user's 2×2 placement sketch: Mountains top left, Hills top right, Plains bottom left, Plateaus bottom right (the sketch colours only marked placement). Regions join at natural borders, linked by a trail in episode order. Unlocked regions animate: Mountains blowing snow, a drifting cloud and a circling eagle; Hills swaying trees and a stream; Plains rippling grass and butterflies; Plateaus blowing dust and a gliding hawk. Locked regions are grey with a padlock, no animation, and a guide text such as "Finish Mountains first"; tapping one stays on the map. Each region shows its star progress (for example 0/45). Back is in the top-left corner. *Changed by the user on 2026-11-13 after ticket 04: the player's name is no longer shown on the map, and Back is an arrow icon with no word, for a cleaner map.* |
| Difficulty selection | A separate screen titled with the landform: three large cards, Easy, Normal and Hard, each with its stars (0/9, 0/15, 0/21). Normal and Hard are grey with a padlock and "Clear all Easy levels" or "Clear all Normal levels" until unlocked. Back top left; the landform animates slowly behind. |
| Level selection | A trail with one stone per level showing its stars; levels after the next playable one show a padlock. Tapping a stone opens the Lesson Screen. |
| Lesson Screen | A cream panel with the landform name and picture, three or four short sentences, the level's item pictures with names, and the level's goals. Start begins the level; Back returns to level selection. The user asked for good placement. |
| In-level layout | Top left collectibles count with an icon (for example 2/5); top centre countdown (red, hopping and flashing each second in the last 20 s, with a soft tick in the last 10 s, D-058); top right pause; bottom left large left and right arrows; bottom right large jump button. |
| Result Screen | Stars pop in one by one with a chime; collected items in a row with missed ones as grey outlines; the goals with ticks; two or three review sentences. Buttons: Replay, Continue, Back to Map. *Changed 2026-11-15 (D-059): left to right Back to Map, Replay, Next, each with an icon; Next reads "Next Level" or, after the whole landform, "Next Episode".* |

## Audio and text (D-042)

- **Ambience** differs per landform and per difficulty (12 sets). For Mountains: Easy a light breeze, Normal stronger wind, Hard gusty, near-storm wind; Hills a stream and birds; Plains grass and crickets (D-069: Normal adds frogs and water birds, Hard is dry wind and far thunder); Plateaus dry wind and a hawk.
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

## Mountains Easy 2 and 3 (D-055)

Settled 2026-11-15 in a grilling interview; built the same day (uncommitted, not yet played by the user; see [[Sessions/2026-11-15 - Mountains Easy 2 and 3 Build Handoff]]). Build changes: lesson lines shortened to fit the 312 px line, vent launch about 128 px, Easy 3 wide pit 64 px, Profile shelves page 5 kinds at a time. Full content, layouts and tests: `D:\LandGrand\LandGrand\.scratch\mountains-easy-2-3\spec.md`.

| Level | Lesson topic | New item kinds | Review pickup | Theme and goal | Hazards |
| --- | --- | --- | --- | --- | --- |
| Easy 2 "Volcano Trail" | Volcanic mountains (lava cools into new rock; Mayon and Apo) | Andesite, pumice, obsidian (rocks) | Quartz | Dark volcanic ground, lava cracks, steam vents; lava-rock arch | 2 pits, 2 spikes |
| Easy 3 "Folded Peaks" | Folded mountains (heat and squeezing change rock) | Slate, marble (rocks), garnet (mineral) | Mica | Grey folded rock, summit snow, eagle; summit stone pile | 3 pits (one needs the double jump), 3 spikes |

- Easy rules unchanged: 5 pickups (3 new kinds, 1 review pickup, 1 repeat), 1 checkpoint, 120 s, D-048 pit rule. All text is draft (Q-04). The Mountains shelf holds 10 kinds; basalt is kept for Plateaus.
- Popular-platformer touches with no rule change: teach-test-twist pacing, one secret-spot pickup per level, a 1.5 s level start banner (the timer starts after it), decorative living props.
- **Steam vent (Easy 2 only):** puffs about every 2 s and launches the explorer high; never harms and does not touch time, items or stars. **Manuscript (D-036):** a level object Chapter III does not name; tell the panel.
- One builder: level layout becomes level data and **LandGrand > Build Mountains Levels** builds every level.

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

## Profile tabs and achievements (D-060)

Settled 2026-11-15; built the same day, not yet checked in the Editor.

- Under the explorer strip: two section tabs, **Collection** and **Achievements**, over one cream page.
- **Collection:** one tab per landform. Only that landform's rocks and minerals show, in a 6 by 2 grid with names (no page arrows). Landforms not yet open on the map have a grey tab with a padlock; tapping it says "Finish <landform> first".
- **Achievements:** eight draft badges in a 4 by 2 grid: First Steps, Rock Hound, Crystal Finder (bronze); Star Explorer, Volcano Visitor, Summit Climber (silver); Perfect Trail, Mountain Collector (gold). Locked badges are dark with a padlock but keep their name; tapping any badge shows how to earn it. "Badges n/8" sits at the right of the tab row.
- Badges are worked out from saved progress only (LG-19), so the save file does not change.
- A badge earned in a level shows on the Result Screen: a red "NEW BADGE!" ribbon with the medal and its name, to the right of the stars, after they pop in.
- **Manuscript (D-036):** achievements are an addition; listed under Q-13 (d) for the adviser and panel.

## Mountains Normal 1–5 (D-062)

Settled 2026-11-15. Built by Codex and committed on 2026-11-16 (`5a453e5` to `5940ec7`; 234 EditMode tests and 19 focused Play Mode checks pass; Codex's handover is `.scratch/mountains-hard/HANDOVER.md`). A Claude review found no spec gaps; the user's play check is still open. Spec and tickets are in `D:\LandGrand\LandGrand\.scratch\mountains-normal\` (`CODEX-START.md`, `spec.md`, `issues/01`–`07`).

| Level | Mountain (banner) | Topic | Theme | New object | New kinds |
| --- | --- | --- | --- | --- | --- |
| N1 | Mount Pulag | Weathering | Pine Forest, ranger hut goal | Crumbling ledges: they break 0.5 s after you stand on them and come back after 3 s; bridges across pits make you keep walking | sandstone, clay |
| N2 | Mount Pinatubo | Erosion (lahar) | Ash Gorge, stone bridge goal | Falling rocks: a 1.2 s shadow-and-pebbles warning, then a rock drops | conglomerate, shale |
| N3 | Mount Matutum | Mountains and water | Mossy Forest, trail sign goal | Moving platforms that carry the explorer across wide pits (the first one is over safe ground) | basalt, magnetite |
| N4 | Mount Apo | Minerals from mountains | Mossy Forest with sulfur at the vent | Mix of N1–N3, plus the Easy 2 steam vent | sulfur, pyrite |
| N5 | Mount Everest | The highest mountain | Snow Peak, summit prayer flags goal | Wind gusts: 2 s calm, 0.6 s warning, 1.4 s push back at 40 px/s | limestone, gneiss |

- **Size:** 7 pickups and 2 checkpoints (x 2400 and 4800) per level, 7200 px wide with the goal at 7040. A physics bot reached each goal in 98–112 s of the 180 s limit, and all 35 pickups can be reached.
- **Hazards:** Normal keeps the checkpoint rule for every hazard (D-040); the Easy short-return rules do not apply.
- **Profile:** the Collection pages within a landform tab (12 per page); the Achievements grid becomes 4×3 with Philippine Peaks (clear Normal 1–4), Top of the World (clear Everest) and Rock Scholar (find 15 kinds).
- **Audio:** stronger Normal wind, plus gust, crumble and rockfall sounds (`Tools/Audio/make_normal_audio.py`).
- **Art:** `Tools/Art/make_normal_art.py` (themes, level objects, 10 items, 5 lesson pictures of the real mountains); badges in `make_profile_art.py`.
- **Content:** lesson sentences, reviews and item descriptions are in the spec, all draft until a teacher reviews them (Q-04). Mountain facts were checked on 2026-11-15:
  - Pulag: 3rd highest, frost from November to February (Wikipedia, Inquirer).
  - Pinatubo: lahars carried away about half of its 1991 ash (USGS).
  - Matutum: a watershed for South Cotabato, General Santos and Sarangani (FPE, MindaNews).
  - Apo: sulfur at its solfataras (Inquirer, VolcanoDiscovery).
  - Everest: its summit is seafloor limestone with fossils (Montana State University, IUGS).
- **Backgrounds (D-063):** each level theme has its own six-layer background drawn for its mountain (`Tools/Art/make_normal_backdrops.py`); Easy 1 keeps the shared alpine Mountains background. Every future landform theme (Hills, Plains, Plateaus) gets its own background too.
- **Pause and Time's up (D-064):** Resume, Retry and Levels, and Retry and Levels; Levels opens the level selection instead of the Main Menu.
- **Manuscript (D-036):** crumbling ledges, falling rocks, moving platforms and wind gusts are additions, listed under Q-13 (d).

## Mountains Hard 1–7 (D-065)

Settled 2026-11-15. The art, audio and the level layouts are made and bot-checked. The code is to be built by Codex from the spec and tickets in `D:\LandGrand\LandGrand\.scratch\mountains-hard\` (`CODEX-START.md`, `spec.md`, `issues/01`–`09`).

| Level | Mountain (banner) | Topic | Theme and goal | Level objects | New kinds |
| --- | --- | --- | --- | --- | --- |
| H1 | Mount Mayon | Volcano safety | Lava Slope, watch station | **Rolling boulders** (new), falling rocks | scoria, hornblende |
| H2 | Sierra Madre | Mountain ranges and typhoons | Storm Ridge, lookout tower | Wind gusts, crumbling bridges, rolling boulders | diorite, gold |
| H3 | Kitanglad Range | Mountains are homes (Philippine eagle) | Eagle Forest, eagle nest | Moving platforms, crumbling steps, rolling boulders | tuff, hematite |
| H4 | Mount Hamiguitan | Caring for mountains, landslides | Bonsai Forest, sanctuary sign | Crumbling bridges, falling rocks, rolling boulders | serpentinite, chromite |
| H5 | Matterhorn | Glaciers shape mountains | Glacier Horn, alpine hut | **Icy ground** (new), wind gusts, bridges, rolling boulders | schist, calcite |
| H6 | Mount Kilimanjaro | Climbing changes weather | Equator Summit, summit board | Vents, platforms, rocks, rolling boulders, ice | trachyte, tanzanite |
| H7 | Mauna Kea | Mountains under the sea | Sea Peak, telescope dome | Everything | gabbro, olivine |

- **Size:** 9600 px wide, goal at 9440; 9 pickups (2 new kinds × 4 and 1 review pickup, one in a secret spot) and 3 checkpoints (x 2400, 4800, 7200); 240 s (D-039). A physics bot reached each goal in 131–156 s, and all 63 pickups can be reached.
- **Hazards:** the checkpoint rule for every hazard (D-040), including rolling boulders.
- **Rolling boulder:** a 0.8 s rumble and dust warning, then it rolls left at 90 px/s along the ground and vanishes at its end point; 3.5 s cycle; 14×14; it skips its roll if the explorer stands within 48 px of its start, so it never appears on top of the explorer.
- **Icy ground:** while standing on ice, walking speeds up at 160 px/s² and slows down at 100 px/s², so the explorer slides about 26 px; the wind still pushes.
- **Collection:** Mountains has 34 kinds, 3 pages. **Badges:** Brave Hiker (any Hard level), World Peaks (Hard 5–7), Hard Star (3 stars on all Hard), Mountain Master (all 15 Mountains levels); the grid becomes 5×3.
- **Audio:** near-storm Hard wind (D-042), boulder rumble and roll, ice slide, a fanfare and an unlock sound (`Tools/Audio/make_hard_audio.py`).
- **Art:** `Tools/Art/make_hard_art.py` (themes, objects, 14 items, 7 lesson pictures, Description Screen art), `Tools/Art/make_hard_backdrops.py` (seven six-layer backgrounds, D-063), badges in `make_profile_art.py`.
- **Content:** lesson sentences, reviews and item descriptions are in the spec, all draft until a teacher reviews them (Q-04). Facts checked on 2026-11-15; the spec lists the sources. Two wording cautions from the sources: the Sierra Madre "helps weaken" typhoons (DOST: it cannot fully protect Luzon), and the green olivine beach is on Mauna Loa, so the olivine text says "a Hawaii beach".

### Landform Description Screen and unlocking (D-065)

- **When:** "required episode levels" means all 15 levels of the landform (answers part of Q-03). After the landform is complete, the Result Screen's Next Episode opens the Landform Description Screen; a book button on the difficulty screen reopens it later.
- **What:** the landform's picture with falling snow, a scroll panel with "Mountains" and five short summary sentences (draft), the trip totals (stars n/45, kinds n/34, badges n/15), "Hills is now open!" with a padlock opening, a fanfare, and To the Map.
- **Unlock:** a landform is open when the landform before it is complete, worked out from saved clears, so the save file does not change and the unlock is saved with the Hard 7 clear (LG-32). Hills has no levels yet, so the map shows it open and tapping it says "Coming soon". The first map visit after an unlock plays a one-time padlock-break animation; the "seen" mark is a device setting.
- **Not in scope:** the Completion Screen after all four landforms.
- **Manuscript (D-036):** the rolling boulder, icy ground, the four badges and 5×3 grid, the unlock animation, the book button and the Hard sizes are additions, listed under Q-13 (d).

## Hills (D-066)

Settled 2026-11-16. Hills Easy 1–3 is fully specified. Its art, audio and layouts are made and bot-checked, and Codex builds the code from `D:\LandGrand\LandGrand\.scratch\hills\` (`CODEX-START.md`, `spec.md`, `issues/01`–`07`). Normal and Hard are outlined only; each gets its own spec after the user plays Easy.

| Level | Hill (banner) | Topic | Theme and goal | New object | Kinds |
| --- | --- | --- | --- | --- | --- |
| E1 | Chocolate Hills, Bohol | What a hill is | Chocolate Hills, viewing deck | none | limestone\*, calcite\*, clay\*, coral stone |
| E2 | Vayang Rolling Hills, Batanes ("Batanes Hills") | Grass holds soil; grazing | Rolling Pasture, Ivatan stone house | none (grazing goats and cows) | andesite\*, limonite, kaolinite, coral stone review |
| E3 | La Paz Sand Dunes, Ilocos Norte ("La Paz Dunes") | Wind makes dunes | Sand Dunes, dune marker | **soft sand** | quartz\*, magnetite\*, feldspar\*, limonite review |
| N1 | Hundred Islands, Pangasinan | Hills from old coral reefs | Island Hills | sinking float | later |
| N2 | Callao Cave, Cagayan | Caves in limestone hills | Limestone Cave | gentle bats (push back 24 px only) | later |
| N3 | Pagsanjan Gorge, Laguna | Rivers wear valleys | River Gorge | river current | later |
| N4 | Banaue Rice Terraces, Ifugao | Farming on slopes | Rice Terraces | mix | later |
| N5 | Cappadocia, Türkiye | Wind and rain carve rock | Fairy Chimneys | hot-air balloons | later |
| H1 | Tarsier forest, Corella, Bohol | Homes for animals | Tarsier Forest | slippery mud | later |
| H2 | Hills of Antipolo, Rizal (source to check) | Landslide warning signs | Rainy Slope | rolling log | later |
| H3 | Masungi Georeserve, Rizal | Rain shapes limestone; protecting hills | Karst Ridge | mix | later |
| H4 | Pililla Wind Farm, Rizal | Wind power | Wind Hills | mix | later |
| H5 | Clew Bay drumlins, Ireland | Glaciers leave hills | Drumlin Bay | mix | later |
| H6 | Seven Hills of Rome, Italy | Cities on hills | City Hills | mix | later |
| H7 | Guilin karst hills, China | Tower limestone hills | Karst Towers | mix | later |

\* Shared kind, already on the Mountains shelf.

- **Easy sizes:**
  - E1: 4800 px, checkpoint at 2400. E2 and E3: 5400 px, checkpoints at 2700 and 2500.
  - 5 pickups each, one of them in a secret spot. 120 s limit.
  - Pits and spikes send the explorer a short way back.
  - The bot reached the goals in 66.0, 72.7 and 81.1 s, and every pickup can be reached.
- **Soft sand:** walking speed drops to 60% on the flat ground inside a zone. Jumps and speed in the air are unchanged, and sand never hurts the explorer. A step crunch and a sand puff come every 0.3 s. The first patch is on safe ground.
- **Shared kinds:** a kind can sit on more than one shelf. It is saved and counted once. The Hills shelf has 10 kinds now (one Collection page).
- **Badges:** one 5×3 page per landform. Hills adds Pasture Pal, Dune Surfer, Rolling Star, Hill Collector, Philippine Hills, Balloon Rider, Slope Ranger, World Hills, Steady Star and Hill Master. The `world_peaks` level numbers become data.
- **Map and menus:**
  - The open Hills region shows swaying trees, a shining stream and two birds; the cloud the Mountains Hard build added is removed.
  - Plains stays locked ("Finish Hills first") until Hills is complete.
  - Menu screens show the life of the chosen landform (Hills: birds and grass).
- **Audio** (`Tools/Audio/make_hills_audio.py`):
  - `bgm_hills`: G major, three beats to a bar, 108 BPM, a 40 s loop.
  - Easy ambience: a stream, songbirds and a far cow bell.
  - Normal ambience: adds cicadas and grass wind.
  - Hard ambience: rain, a louder stream and far thunder.
  - `sfx_sand_step`.
- **Art:** `Tools/Art/make_hills_easy_art.py` (themes, soft sand, props, three items, three lesson pictures, map and menu life), `Tools/Art/make_hills_easy_backdrops.py` (three six-layer backgrounds, D-063), and the ten badges in `make_profile_art.py`.
- **Flow:**
  - An open difficulty with no levels says "Coming soon".
  - The Result Screen hides Next when the next level has no data.
  - The Hills Description Screen data is ready: 5 draft summary sentences, stars n/45, kinds n/(Hills shelf), badges n/10, "Plains is now open!".
- **Content:** every lesson, review, kind and summary text is a draft for teacher review (Q-04). The spec lists the sources checked on 2026-11-16. Ilmenite was dropped because no source confirmed it in Ilocos sand; E3 uses feldspar instead.
- **Manuscript (D-036):** the Hills content and the new objects are additions, listed under Q-13 (d).

## Hills Normal (D-067)

| Level | Place | New object | New kinds | Goal |
|---|---|---|---|---|
| N1 | Hundred Islands, Pangasinan | 4 sinking floats | aragonite, coquina | Boat Dock |
| N2 | Callao Cave, Cagayan | 3 gentle bat loops; cave-drip ambience | flowstone, dripstone | Cave Mouth |
| N3 | Pagsanjan Gorge, Laguna | 3 river-current strips (one pushes the other way) | volcanic breccia | Falls Landing |
| N4 | Banaue Rice Terraces, Ifugao | 1 float, 1 bat loop, 1 current | none (clay and kaolinite reviews) | Ifugao House |
| N5 | Cappadocia, Türkiye | 4 hot-air balloons (vertical platforms) | ignimbrite, zeolite | Balloon Field |

- Normal sizes as Mountains Normal: 7200 px, 2 checkpoints, 180 s.
- The first object of each kind is on a safe practice spot.
- Hills shelf: 17 kinds after Normal.
- Art and sound are made by Codex with Python scripts; layouts are designed and bot-checked by Claude.
- Full spec: `D:\LandGrand\LandGrand\.scratch\hills-normal\spec.md`.

## Hills Hard (D-068)

| Level | Place | Objects | New kinds | Goal |
|---|---|---|---|---|
| H1 | Tarsier forest, Corella, Bohol | slippery mud | peridotite | Tarsier Lookout |
| H2 | Antipolo slopes, Rizal | rolling logs | chlorite | Barangay Hall |
| H3 | Masungi Georeserve, Rizal | mud, bats, crumbling ledges | none | Spider-Web Bridge |
| H4 | Pililla Wind Farm, Rizal | wind, logs, balloons | dacite | Turbine Base |
| H5 | Clew Bay, Ireland | mud, current, logs | quartzite | Stone Pier |
| H6 | Seven Hills of Rome, Italy | logs, platforms, floats | travertine, leucite | Temple Ruins |
| H7 | Guilin karst, China | everything | none | Raft Dock |

- Hard sizes as Mountains Hard; walk 84 px/s; Hills shelf 23 kinds after Hard.
- Full spec: `D:\LandGrand\LandGrand\.scratch\hills-hard\spec.md`.

## Plains (D-069)

Planned 2026-11-21. Plains Easy 1–3 is fully specified; its art, backgrounds, badges, sounds and bot-checked layouts are made, and Codex builds the code from `D:\LandGrand\LandGrand\.scratch\plains-easy\` (`CODEX-START.md`, `CODEX-PROMPT.md`, `spec.md`, `layouts.md`, `issues/01`–`04`). Normal and Hard are an outline only; each gets its own spec after the user plays Easy.

| Level | Place (banner) | Topic | Theme and goal | New object | Kinds |
| --- | --- | --- | --- | --- | --- |
| E1 | Central Luzon Plain, Nueva Ecija | What a plain is | RicePlain, Rice Granary | none | clay\*, sandstone\*, shale\*, siltstone |
| E2 | Pangasinan Salt Beds | Plains by the sea; salt from seawater | SaltBeds, Salt Hut | none | halite, gypsum, quartz\*, siltstone review |
| E3 | Isabela River Plain, Cagayan Valley | Rivers spread soil and make farm plains | RiverPlain, Farm Shed | **straw bounce pile** | conglomerate\*, limestone\*, mudstone, halite review |
| N1–N5 | Candaba Swamp; Pinatubo lahar plain; Agno River delta; Agusan Marsh; Mekong Delta (Vietnam) | wetlands, volcanic plains, deltas, wetland living, floating markets | outline | float; sand and vents; current; mix; market boats | later |
| H1–H7 | Great Plains (USA); Serengeti; Pampas; West Siberian Plain; Nullarbor; Indo-Gangetic Plain; finale | grassland, migration, ranching, cold plains, limestone plains, river floods | outline | hay bales (log rule); herd push (bat rule); mix; ice; crumbles and bats; floats and current; everything | later |

\* Shared kind.

- **Easy sizes:** E1 4800 px (checkpoint 2400), E2 and E3 5400 px (checkpoints 2700 and 2500); 5 pickups with one secret; 120 s. The bot reached the goals in 56.8, 62.4 and 62.2 s at walk 84, and every pickup can be reached.
- **Straw bounce pile:** 48×16, solid like a boulder; landing on its top launches the explorer at 400 px/s (feet to about 104 px; with the double jump about 128 px); its side is a wall; it never hurts; squash picture, straw bits and `sfx_straw_bounce`. A 32 px pile was too narrow to land on from a walking jump.
- **Plains shelf:** 10 kinds; total kinds 54.
- **Badges:** Salt Maker, Straw Jumper, Flat Star, Plain Collector, Philippine Plains, Delta Boater, Prairie Ranger, World Plains, Steady Plains, Plain Master (the Hills rules on the Plains page).
- **Audio** (`Tools/Audio/make_plains_audio.py`): `bgm_plains` (D major, 4/4, 96 BPM, 40 s loop); `amb_grass_easy`, `amb_wetland_normal`, `amb_dry_hard`; `sfx_straw_bounce`.
- **Art:** `Tools/Art/make_plains_easy_art.py`, `Tools/Art/make_plains_easy_backdrops.py`, and the ten badges in `make_profile_art.py`.
- **Map and menus:** the open Plains region shows rice, two egrets and a carabao; menu screens show egrets and grass. Plateaus stays locked with "Finish Plains first".
- **Description Screen data:** 5 draft summary lines, `bg_plains`, "Plateaus is now open!".
- **Content:** every lesson, review, kind and summary text is a draft for teacher review (Q-04). Not confirmed: that Isabela mostly grows corn (the lesson says only "crops").
- **Manuscript (D-036):** the Plains content and the straw bounce pile are additions, listed under Q-13 (d).

## Plains Normal (D-070)

Planned 2026-11-22 from the D-069 outline. Art, backgrounds, sound and bot-checked layouts are made; Codex builds the code from `D:\LandGrand\LandGrand\.scratch\plains-normal\` (`CODEX-PROMPT.md`, `CODEX-START.md`, `spec.md`, `layouts.md`, `issues/01`–`04`). Built by Codex and reviewed by Claude on 2026-11-22 (440 EditMode tests pass); the user played all five levels and every checklist item passed.

| Level | Place | Topic | Objects (reused rules) | Kinds |
| --- | --- | --- | --- | --- |
| N1 | Candaba Swamp, Pampanga | Wetland plains | sinking floats | **peat**, clay, siltstone, mudstone |
| N2 | Pinatubo Lahar Plain | Volcanoes can bury and build plains | soft sand, crumbling bridges | pumice, dacite, andesite |
| N3 | Agno River Delta | Deltas; the Pangasinan Plain | river currents | gold, quartz, siltstone, mudstone |
| N4 | Agusan Marsh | Living on wetlands | float, sand, current | peat, clay, mudstone |
| N5 | Mekong Delta, Vietnam | Floating markets on a delta | market boats (moving platforms with boat art) | **laterite**, clay, siltstone, mudstone |

- Normal sizes as Hills Normal; bot 83.8–98.4 s at walk 84. Plains shelf 16 kinds after Normal; total 56.
- A theme can name its own moving-platform sprite and landing sound (`market_boat`, `sfx_boat_bump`); old platforms are unchanged.
- Not confirmed (teacher check): Pinatubo rock types (summary only), peat at Candaba and Agusan, laterite in the Mekong Delta itself.

## Plains Hard (D-071)

Planned 2026-11-22 from the D-069 outline; the finale is the Mongolian Steppe. Art, backgrounds, sound and bot-checked layouts are made; a Claude Code session builds the code, one ticket per session, from `D:\LandGrand\LandGrand\.scratch\plains-hard\` (`SESSION-PROMPT.md`, `BUILD-START.md`, `spec.md`, `layouts.md`, `issues/01`–`04`).

| Level | Place | Topic | Objects (reused rules) | Kinds |
| --- | --- | --- | --- | --- |
| H1 | Great Plains, USA | Grassland plains; an old sea left chalk | hay bales (rolling log), straw piles | **chalk**, calcite, limestone, shale, sandstone |
| H2 | Serengeti, Tanzania | Plains of animals; migration | wildebeest herds (bat on the ground) | granite, tuff, sandstone, siltstone, shale |
| H3 | Pampas, Argentina | Farm and ranch plains | hay bales, cattle herds | **loess**, mica, feldspar, quartz, clay |
| H4 | West Siberian Plain, Russia | Cold plains; bogs | frozen ground (ice), bog floats | peat, clay, siltstone, mudstone, sandstone |
| H5 | Nullarbor Plain, Australia | A limestone plain; flint mining | crumbling ledges, bats | **flint**, limestone, calcite, chalk |
| H6 | Indo-Gangetic Plain | River flood plains | floats, currents | laterite, clay, siltstone, sandstone, mudstone |
| H7 | Mongolian Steppe | Plains of the world (finale) | hay, horse herds, ice, crumbles, currents | reviews |

- Hard sizes as Hills Hard; bot 112.6–123.8 s at walk 84. Plains shelf 24 kinds after Hard; total 59.
- A theme can name its own rolling-log frames and sound, bat frames, sound and art lift, and ice top tile; old logs, bats and ice are unchanged.
- Sound: `sfx_hay_roll`, `sfx_herd_hooves`; H4 ambience `amb_cold_plain`, the rest `amb_dry_hard`.
- Not confirmed (teacher check): Mongolian herders, gers and winters (summary only); "loess makes rich farm soil"; peat in the West Siberian bogs; lignite was dropped for lack of a source.
