---
type: design
status: active
updated: 2026-11-12
sources:
  - "[[Decisions/Decision Register#Confirmed decisions|D-028]]"
---

# Start-up Screen

The start-up screen is the first screen the player sees. It shows the explorer walking toward the four landforms, with the Land Grand title and a "Tap to Start" prompt. Tapping opens the Main Menu ([[Project/Scope and Requirements|LG-16]]). This note is the asset specification. It is not a record of implemented assets.

## Confirmed choices (D-028)

| Item | Choice |
| --- | --- |
| Art style | All pixel art, matching the Cainos props (32 pixels per unit, Point filtering) |
| Pixel tool | Aseprite, replacing Piskel from the pre-proposal's tool list. Clip Studio Paint remains available. |
| Landforms shown | All four in the distance: Mountains, Plateaus, Hills, Plains |
| Motion | The explorer walks in place in an endless loop while the background layers scroll. A blinking "Tap to Start" prompt waits for the player. |
| Explorer | Genderless field geologist in the "Cave Spelunker" style. A steel miner helmet, orange visor and black respirator cover the face. |
| Sprite size | 32×32 pixels per frame |

## Explorer design

The face is fully covered, so the character reads as neither boy nor girl. Every learner can see themselves in it.

| Part | Description | Palette colours |
| --- | --- | --- |
| Head | Dark steel miner helmet with a bright headlamp on the front | Mask shade, Strap, Headlamp |
| Eyes | Orange visor band with a light glint | Scarf, Headlamp, Strap |
| Face | Black close-fitting respirator, flush with the face, with a round grey side filter | Strap, Hammer head, Mask shade |
| Body | Slim field vest over a teal shirt, with a belt | Vest, Vest shade, Shirt, Shirt shade |
| Neck | Orange scarf whose tail waves behind while walking | Scarf, Scarf shade |
| Back | Small backpack for collected rocks and minerals, with a pickaxe strapped across it | Backpack, Backpack shade, Handle, Hammer head |
| Arms and legs | Thin limbs with gloves and dark trousers. Brown work boots with an ankle cuff, a lighter toe cap and a dark sole. Both arms swing opposite the legs. | Pants, Backpack, Backpack shade, Handle, Boots |

The character faces right, toward the landforms. It has a slim build with medium-length legs and stands about 27 pixels tall inside the 32×32 frame, with the feet near the bottom row. The user asked for a less bulky, cooler design after the first draft, then for shorter legs and a clearer forward walk after the second.

## Screen layout

![[landgrand-startup-layout-480x270.png]]

The game runs in landscape orientation only (user confirmed 2026-11-12, D-030). The canvas is 480×270 pixels, which scales exactly ×4 to 1920×1080 in landscape. The reference image above is a layout guide, not final art. Open it as a reference layer in Aseprite.

| Layer | Content | Scroll speed (pixels per frame at 10 fps) |
| --- | --- | --- |
| L0 | Sky gradient and sun with a soft glow | Static |
| L1 | Clouds of mixed sizes | 0.15 |
| L2 | Far mountain range in haze colours | 0.1 |
| L3 | Near mountains: varied heights, lit left slopes, shaded right slopes, jagged snow caps | 0.25 |
| L4 | Plateaus of varied width and height with uneven rock strata | 0.45 |
| L5 | Rolling hills with scattered trees | 0.8 |
| L6 | Plains with uneven grass tufts and small flowers | 1.4 |
| L7 | Ground with an uneven grass edge, pebbles and coloured minerals | 2.0 (matches the explorer's stride) |
| Sprite | Explorer, feet at y = 239 | Walks in place |
| Sprite | "LAND GRAND" title | Bobs 1 px; a shine sweeps across every 3.2 s |
| Sprite | Birds (flock of 5) | Fly across the sky |
| Sprite | Sparkles | Twinkle on the coloured minerals in L7 |
| Sprite | Dust | Puffs at the explorer's feet on each step |
| UI | "Tap to Start" | Blinks |

The background canvas is 960×270, two screens wide, so features don't repeat on every screen. Peaks, plateaus, trees, tufts and minerals are placed at irregular spacing. Each layer tiles horizontally: its left edge continues its right edge. Wider phones (up to 20:9) show more of each layer at the sides, which tiling also covers.

## Palette

![[landgrand-palette.png]]

The palette file is `Assets/Art/Palettes/landgrand.gpl` in the Unity project. In Aseprite, load it with **Palette > Load Palette**. It holds 40 colours: the explorer, sky, each landform, and the ground.

## Files and Aseprite setup

Save working files in `Assets/Art/StartScreen/` in the Unity project. Unity imports `.aseprite` files directly through `com.unity.2d.aseprite`, and each Aseprite tag becomes an animation clip.

| File | Canvas | Content |
| --- | --- | --- |
| `explorer.aseprite` | 32×32 | Tag `walk`: 8 frames at 100 ms each (10 frames per second) |
| `startup-background.aseprite` | 960×270 | One Aseprite layer per scroll layer, L0 to L7 |
| `title.aseprite` | About 300×70 | The "LAND GRAND" lettering |

The `walk` tag uses a standard 8-frame cycle: contact, down, passing, up, then the same four poses on the other leg.

Import settings in Unity: Pixels Per Unit 32, Filter Mode Point, Compression None. Use a Pixel Perfect Camera with reference resolution 480×270 and 32 pixels per unit.

## Asset status

| Asset | Status |
| --- | --- |
| `explorer.aseprite` | Sixth draft plus a `collect` tag (8 frames: stop, bend, crouch, grab, rise, hold up, stash, stand). Cave Spelunker head (chosen by the user from three variants; see [[explorer_head_variants.png]]), 2026-11-12, replacing the earlier bulky and long-legged drafts. Generated by Claude from this spec: 8 frames at 100 ms, tag `walk`, LandGrand palette. Not yet reviewed in Aseprite or Unity. |
| `startup-background.aseprite` | Second draft, 2026-11-12. Eight layers (L0–L7) at 960×270 with irregular, non-repeating features. The user asked for effects, less repetition and interactivity after the first draft. |
| `title.aseprite` | Second draft, 2026-11-12. 291×44. Tag `idle` (1 frame) and tag `shine` (12 frames at 60 ms). |
| `birds.aseprite`, `sparkle.aseprite`, `dust.aseprite` | First drafts, 2026-11-12. Tags `fly` (4 frames), `twinkle` (4 frames), `puff` (3 frames). |
| `minerals.aseprite` | First draft, 2026-11-12. 4 frames, 12×12: quartz, gold, jasper, grey rock. |
| `startup-background-points.json` | Peak, plateau, hill and mineral positions in the background, for interactive tap targets. |
| `tap-to-start.aseprite` | First draft, 2026-11-12. "TAP TO START" in white pixel letters, 138×19. Stands in until a pixel font is chosen. |

![[explorer_walk_preview.gif]]

The full screen with parallax scrolling, the walking explorer and the blinking prompt:

![[startup_preview.gif]]

The flat sprite sheet is [[explorer_walk_sheet.png]] (256×32, eight 32×32 frames). The second draft adds the scarf, the back-mounted pickaxe and the far-arm swing.

## Interactivity (D-031)

Rocks and minerals appear on the path ahead of the explorer and scroll with the ground. When the explorer reaches one, it stops and the world stops scrolling (the clouds keep drifting). The explorer crouches, grabs the mineral from the ground (chime), holds it up (sparkle), puts it in the backpack, and walks on; the world eases back to speed over 0.3 seconds. This uses the `collect` tag in `explorer.aseprite` (frames 9–16), added at the user's request so the explorer collects minerals from the ground.

![[explorer_collect_preview.gif]] Four kinds exist (quartz crystal, gold nugget, red jasper, grey rock) in `minerals.aseprite`, with three chime sounds in `Assets/Audio/`. A new mineral appears every 2.5 to 5 seconds. The minerals painted into the ground also twinkle now and then.

Tapping anywhere opens the Main Menu scene. That scene does not exist yet, so a tap only logs a message for now.

## Unity scene

Run **LandGrand > Build Start Screen Scene** in the Unity menu. It sets pixel-art import settings (32 pixels per unit, Point, uncompressed) on every PNG in `Assets/Art/StartScreen/Sprites/`, sets landscape-only orientation, builds `Assets/Scenes/StartScreen.unity`, and adds it first in the build list. Running it again rebuilds the scene. Scripts are in `Assets/Scripts/StartScreen/` and the builder is `Assets/Editor/StartScreenBuilder.cs`. The game uses PNG frames exported from the `.aseprite` files, one PNG per frame or layer, because the scene built from the `.aseprite` imports showed no sprites on 2026-11-12. The `.aseprite` files stay as the editable sources. As of 2026-11-12 the scripts compiled against stand-in Unity types only; they have not yet been compiled or run in the Unity Editor.

## Still open

- The "Tap to Start" prompt is a sprite for now. A pixel font for UI text has not been chosen.
- Music: an original "Quest" loop composed by Claude for this project, `Assets/Audio/bgm_startscreen.ogg` (29.1 s, 132 BPM, A minor, chords Am–F–C–G, building to E major; brass-like lead, driving arpeggio, tom fills). Ambience: wind gusts with a soft whistle, a flowing river, birds and a distant eagle cry, `amb_wind_birds.ogg` (32 s). Volumes are 55% for music and 35% for ambience; both fade in over 1.5 s and fade out over 0.6 s on tap. On 2026-11-13 the user chose this version over the first (sad), cheerful and adventure drafts. No third-party licence applies.
