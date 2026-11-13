---
type: design
status: active
updated: 2026-11-13
sources:
  - "[[Decisions/Decision Register#Confirmed decisions|D-032]]"
  - "[[Project/Scope and Requirements|LG-16]]"
---

# Main Menu

The Main Menu is the screen that opens when the player taps the [[Project/Start-up Screen|start-up screen]]. It offers Play, Settings, Tutorial and Exit ([[Project/Scope and Requirements|LG-16]]). The contents below were confirmed by the user on 2026-11-13 under [[Decisions/Decision Register|D-032]]. As of 2026-11-13 the scripts compile against the project's Unity assemblies, but the scene has not yet been run in the Unity Editor or on a device.

![[mainmenu_preview.png]]

## Confirmed contents (D-032)

| Button | What it does |
| --- | --- |
| Play | Loads the `LandformMap` scene ([[Project/Scope and Requirements|LG-17]]) once that scene is in the build list. Until then it shows a "Landform Map — Coming soon" panel with Back. Episode order and unlocking stay open under Q-03. |
| Settings | A Music volume slider and a Sound Effects volume slider, with Back. Both values are saved on the device with PlayerPrefs and apply to every scene, including the start-up screen music and mineral chimes. They are device preferences, not player progress, so Q-07 is unaffected. |
| Tutorial | Four picture pages with Prev, Next and Back: 1 move and jump, 2 collect rocks and minerals, 3 earn stars, 4 watch out for pits, traps and the timer. Each page carries the note "DRAFT: GAME RULES ARE NOT FINAL YET" until Q-02 (stars, completion) and Q-06 (hazards, timeout) are answered. |
| Exit | Asks "Exit game?" with Yes and No (kept under D-038, although Chapter III Figure 4A closes directly). Yes fades the music and closes the app on Android; in the Unity Editor it stops Play mode. |

The Android Back button closes an open panel; with no panel open, it opens "Exit game?". Every button plays a short click (`Assets/Audio/sfx_ui_click.wav`, original, generated for the project).

![[mainmenu_panels_preview.png]]

## Transition (D-034)

A tap on the start-up screen darkens the screen in six steps while the music fades (0.6 s), loads the Main Menu, and fades it back in (0.5 s). The four buttons then rise 16 pixels into place one after another, so the player can see a new screen has opened; taps wait until they arrive. Play (once the Landform Map exists) uses the same transition, and Exit darkens the screen before the game closes. The fader is `Assets/Scripts/Common/ScreenFader.cs`.

## Look

The start-up screen's eight landform layers scroll slowly behind the LAND GRAND title (same shine and bob) and four large buttons, 120×26 pixels on the 480×270 screen. Birds fly by now and then. The menu has its own calm music loop (D-035): `Assets/Audio/bgm_mainmenu.ogg`, 30 s at 96 BPM in A minor on Quest's chords, with a soft pad, a music-box arpeggio and a flute-like melody, and no drums. It fades in with the wind ambience. Not yet heard in the Editor by the user. Play is green, Settings and Tutorial are brown, and Exit is red. Panels are cream paper with a tan frame over a dark see-through layer. All colours come from `Assets/Art/Palettes/landgrand.gpl`.

The text is drawn into the sprites from a 5×7 pixel font defined in the art script. I and 1 are 3 columns wide so words keep even spacing, and button labels sit exactly in the middle of the button face (D-034). A UI font for the game has still not been chosen; changing a word means editing the script and running it again.

## Files (Unity project)

| Item | Path |
| --- | --- |
| Music script | `Tools/Audio/make_menu_music.py` composes the menu loop and saves `Assets/Audio/bgm_mainmenu.ogg`. Run `python Tools/Audio/make_menu_music.py` (needs ffmpeg). |
| Art script | `Tools/Art/make_mainmenu_art.py` draws every Main Menu PNG and the click sound. Run `python Tools/Art/make_mainmenu_art.py` from the project folder (needs Pillow). |
| Sprites | `Assets/Art/MainMenu/Sprites/` with `Buttons/` (normal and pressed), `Panels/` (9-slice panel, slider track, fill and knob), `Text/` and `Tutorial/` (page pictures and text) |
| Scripts | `Assets/Scripts/MainMenu/MainMenuController.cs`, `SettingsPanel.cs`, `TutorialPanel.cs`; shared volumes in `Assets/Scripts/Common/GameSettings.cs` |
| Builder | `Assets/Editor/MainMenuBuilder.cs`, menu **LandGrand > Build Main Menu Scene**. It sets pixel-art import settings, builds `Assets/Scenes/MainMenu.unity`, and puts it second in the build list after `StartScreen`. |

`StartScreenController` already loads the scene named `MainMenu` when it is in the build list, so building the Main Menu is enough to connect the tap. The UI is a uGUI canvas. `Assets/Scripts/Common/PixelPerfectUiScale.cs` scales it by the Pixel Perfect Camera's whole-number zoom (×4 on a 1920×1080 phone), so one UI pixel is always one art pixel. On 2026-11-13 the first version scaled the UI by screen height instead; in a 589×332 Game view that made letters uneven next to the art. The first version of the zoom script also read the camera's `pixelRatio` in `Awake`, before the camera had set itself up, and failed with a NullReferenceException; the UI then stayed at ×4 and filled small Game views. It now works the zoom out from the screen size with the camera's own formula.

## Code comments (D-033)

Every line in the Main Menu code, the art script, the start-screen scripts and both builders has a short comment in basic English that says what the line is for, as the user asked on 2026-11-13. Adding the start-screen comments changed no code; a line-by-line comparison with the last commit and a fresh compile confirmed this.

## Try it in the Editor

1. In the Game view, choose a fixed even size such as **Full HD (1920x1080)** instead of Free Aspect. At odd sizes the Pixel Perfect Camera shows a red "Rendering at an odd-numbered resolution" notice; it appears only in the Editor and development builds, and phone screens use even sizes.
2. Run **LandGrand > Build Main Menu Scene** (again after any builder change).
3. Open `Assets/Scenes/StartScreen.unity`, press Play, and tap the screen.
4. Check that each of the four buttons responds and that the Escape key (Android Back) closes panels.

## Still open

- The final tutorial wording depends on Q-02 and Q-06; the controls on page 1 are the planned touch controls (LG-08), not a built level.
- The Landform Map scene does not exist yet (LG-17, Q-03).
- No Android device test has been recorded.
- A pixel font for UI text has not been chosen.
