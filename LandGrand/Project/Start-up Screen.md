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
| Explorer | Genderless field geologist. A helmet, goggles and dust mask cover the face. |
| Sprite size | 32×32 pixels per frame |

## Explorer design

The face is fully covered, so the character reads as neither boy nor girl. Every learner can see themselves in it.

| Part | Description | Palette colours |
| --- | --- | --- |
| Head | Miner hard hat with a headlamp on the front | Helmet, Helmet shade, Headlamp |
| Eyes | Round goggles with a dark strap | Goggle lens, Strap |
| Face | Dust mask with a small filter on the side | Mask, Mask shade |
| Body | Field vest with pockets over a teal shirt | Vest, Vest shade, Shirt |
| Back | Backpack for collected rocks and minerals | Backpack, Backpack shade |
| Hand | Rock hammer, carried head-down | Hammer head, Dark brown |
| Legs and feet | Dark trousers and work boots | Pants, Boots |

The character faces right, toward the landforms. It stands about 26 pixels tall inside the 32×32 frame, with the feet on the bottom row.

## Screen layout

![[landgrand-startup-layout-480x270.png]]

The canvas is 480×270 pixels, which scales exactly ×4 to 1920×1080 in landscape. The reference image above is a layout guide, not final art. Open it as a reference layer in Aseprite.

| Layer | Content | Scroll speed |
| --- | --- | --- |
| L0 | Sky and clouds | Static |
| L1 | Mountains | 0.1× |
| L2 | Plateau | 0.2× |
| L3 | Hills | 0.4× |
| L4 | Plains | 0.7× |
| L5 | Ground, where the explorer walks | 1.0× |
| Sprite | Explorer, feet at y = 238 | Walks in place |
| Sprite | "LAND GRAND" title, inside the top box | Static. A shine animation can come later. |
| UI | "Tap to Start" text | Blinks |

Layers L1 to L5 scroll, so each one must tile horizontally: its left edge must continue its right edge. Wider phones (up to 20:9) show more of each layer at the sides, which tiling also covers.

## Palette

![[landgrand-palette.png]]

The palette file is `Assets/Art/Palettes/landgrand.gpl` in the Unity project. In Aseprite, load it with **Palette > Load Palette**. It holds 31 colours: the explorer, sky, each landform, and the ground.

## Files and Aseprite setup

Save working files in `Assets/Art/StartScreen/` in the Unity project. Unity imports `.aseprite` files directly through `com.unity.2d.aseprite`, and each Aseprite tag becomes an animation clip.

| File | Canvas | Content |
| --- | --- | --- |
| `explorer.aseprite` | 32×32 | Tag `walk`: 8 frames at 100 ms each (10 frames per second) |
| `startup-background.aseprite` | 480×270 | One Aseprite layer per scroll layer, L0 to L5 |
| `title.aseprite` | About 300×70 | The "LAND GRAND" lettering |

The `walk` tag uses a standard 8-frame cycle: contact, down, passing, up, then the same four poses on the other leg.

Import settings in Unity: Pixels Per Unit 32, Filter Mode Point, Compression None. Use a Pixel Perfect Camera with reference resolution 480×270 and 32 pixels per unit.

## Still open

- The "Tap to Start" text needs a pixel font. No font has been chosen yet.
- Music and sound for this screen ([[Project/Scope and Requirements|LG-18]]) are not specified.
