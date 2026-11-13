---
type: session-handoff
status: active
updated: 2026-11-13
focus: Game development, start-up screen
---

# Start-up Screen Build Handoff

## Stopping point

On 2026-11-13 the user asked to save what was accomplished. The start-up screen runs in the Unity Editor: the user confirmed that the scene works, that the explorer and minerals appear, and that the "Quest" music is the chosen background. Game development is the active priority under [[Decisions/Decision Register|D-027]]. The user will upload the final Chapters I–III later.

## Accomplishments saved

### Project setup

- Working copies confirmed: `D:\LandGrand\LandGrand` (Unity) and `D:\LandGrand\LandGrand-Sources` (this vault). The `D:\Projects` copies are outdated (D-027). Live path references in the vault were updated.
- Unity upgraded from `6000.5.6f1` to `6000.6.8f1` and committed by the user. The Cainos `PolygonCollider2D` serialization warnings and a duplicate `using` in `Elevator.cs` were fixed. A merge-conflict marker left in `Assets/Editor/ReserializeCainos.cs` after the two-laptop merge was removed.
- Landscape-only orientation recorded (D-030); the scene builder sets it in Player Settings.

### Start-up screen design decisions

| Decision | Record |
| --- | --- |
| All pixel art in Aseprite (replacing Piskel), four landforms in the distance, endless walk with "Tap to Start", genderless masked field geologist at 32×32 | D-028 |
| "Cave Spelunker" explorer head (steel helmet, headlamp, orange visor, black respirator) | D-029 |
| Landscape only | D-030 |
| Rocks and minerals along the path; touching one plays a sound | D-031 |

The user also asked, in turn, for a slimmer cooler body, shorter legs and a forward-reading walk, visible boots, a mask without the "duck" snout, effects with less repetition, a ground pickup animation, closer minerals, a fixed footstep dust, and cheerful then adventurous then more intense music. Each request is reflected in [[Project/Start-up Screen]].

### Built assets (Unity project)

- **Art**: `Assets/Art/StartScreen/*.aseprite` are the editable sources. The game uses 53 PNG frames exported from them in `Assets/Art/StartScreen/Sprites/` (Background L0–L7 at 960×270, Explorer 16 frames = walk + collect, Title 13 frames with a shine, Birds, Sparkle, Dust, Minerals, UI). The palette is `Assets/Art/Palettes/landgrand.gpl` (40 colours).
- **Audio**: `Assets/Audio/bgm_startscreen.ogg` ("Quest", 29.1 s, 132 BPM, A minor), `amb_wind_birds.ogg` (wind gusts, river, birds, eagle; 32 s), three mineral chimes. All are original, generated for the project; no third-party licence applies.
- **Scripts** in `Assets/Scripts/StartScreen/`: parallax scrolling with a shared walk-speed scale, a sprite flipbook, the explorer collect controller, mineral spawner and pickup, footstep dust that drifts with the ground, birds, ground sparkles, the blinking prompt, the title bob, music with fades, and the tap-to-continue controller.
- **Scene builder**: `Assets/Editor/StartScreenBuilder.cs`, menu **LandGrand > Build Start Screen Scene**, creates `Assets/Scenes/StartScreen.unity` and adds it first in the build list. A rebuild replaces the scene, so it is needed only when the builder or the art changes, not for script-only changes.

### Lessons

- The `.aseprite` files written by Claude did not yield sprites through the Unity Aseprite importer on this project; the cause is unconfirmed. PNG frames with the standard texture importer work and are the current route.
- Preview GIFs with a separate palette per frame displayed with wrong colours in Claude's viewer. Previews now use one shared palette. The game art itself was never affected.
- Building with **Build And Run** needs a phone connected with USB debugging. **Build** alone makes an APK on the laptop.
- When the claude.ai chat replaced files already on the laptop, the copy reported success but kept the old contents. This hit both music files, `StartScreenMusic.cs` and `StartScreenBuilder.cs`, so the Quest music did not play until they were copied again by another route and all 71 start-screen files were checked against the intended versions. Verify a replaced file by its content, not by the tool's success message. Repository and vault work now runs in Claude Code on the laptop (user in chat, 2026-11-13: "should I use the Code version?").

## Not done yet

- The **Main Menu** was built in code later on 2026-11-13 (D-032; see [[Project/Main Menu]]). It still needs **LandGrand > Build Main Menu Scene** and an Editor test by the user.
- No Android device test has been recorded yet.
- `/setup-matt-pocock-skills` has not been run for the Unity project.
- Game-rule questions Q-02, Q-03, Q-06 and Q-07 remain open in [[Questions/Open Questions]].
- A pixel font for UI text has not been chosen; "Tap to Start" is a sprite.
- The final Chapters I–III are still to be uploaded.

## Suggested next step

Build the Main Menu from [[Project/Scope and Requirements|LG-16]] (Play, Settings, Tutorial, Exit), so the start screen has somewhere to go. Settings and Tutorial contents are unspecified in the requirements and need the user's decisions first.
