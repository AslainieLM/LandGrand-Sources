---
type: design
status: confirmed
updated: 2026-11-13
sources:
  - "[[Decisions/Decision Register]]"
  - "[[Project/Gameplay Design]]"
---

# Game Font

**Chosen (D-047): Micro 5 for all game text, at 22 px (D-050).** 22 px is 2x Micro 5's pixel grid: every stroke is exactly 2 px wide and capitals are 10 px tall. Files: `Assets/Fonts/Micro5.ttf` and `OFL-Micro5.txt` (SIL Open Font License, source github.com/google/fonts). The font asset `Micro5 2x.asset` is made by `MainMenuBuilder.EnsureFont` (constants `FontAssetPath`, `FontSize`). Every builder calls `PixelSceneKit.FixFonts` just before saving; it reloads the font and puts it, at 22 px, on every text, so a stale font reference can never save TextMeshPro's smooth default font. The old `Micro5 Raster.asset` (15 px), `Micro5 1x.asset` (11 px) and the Pixelify Sans files were deleted on 2026-11-14 at the user's request. Rebuild all scenes after changing the font, because scenes store the font asset's id.

## Size history (2026-11-13 to 14)

- 15 px: 1.5x of the grid; some strokes 1 px, others 2 px, letters bent. User: "it is so hard to read right now".
- Mix of 11 px (1x) for sentences and 22 px (2x) for the rest: user: "it is so bad btw, make it more visually appealing and easy to read, that's so small btw".
- **22 px for all text (current).** Layouts were widened so it fits: Lesson panel 464 px wide with sentences beside the picture and no "You will find:" or "Goals:" headings; item pop-up 360x176; Result panel 456x250 with both goals on one row; HUD panel 136x46; guide panel 240x26; lock guides on two lines; name panel 300 px wide. Extra word and line spacing is 0 (Micro 5 spaces are 6 px and lines 24 px at 22 px).

## Lesson Screen spacing

At 22 px no extra spacing is added (`LessonBuilder.Spaced` sets both to 0). The longest lesson line is 310 px in a 312 px box.

## Rules for choosing a font later

1. **Draw it at a whole multiple of its own pixel grid.** Measure it: render the font at many sizes and find where every stroke is the same width. Micro 5's grid fits about 10.5 px (a 5-pixel tall H), so 11 px is 1x and 22 px is 2x. The earlier note said 15 px was 3x; that was wrong. 15 px is 1.5x, and it drew some strokes 1 px and others 2 px wide, which made the text hard to read (user, 2026-11-13). Off-grid sizes bend letters or lose 1-pixel strokes.
2. **Check before building:** a sample of a–z, A–Z, 0–9 and the real lesson text, drawn without smoothing. Look for "5" against "S", "i", "l" and "t".
3. **Check the fit:** the longest lesson sentence must fit the 292 px column and goal text the 178 px column.
4. **Licence:** only fonts under the SIL Open Font License. Keep the licence text beside the font file. Download only with the user's approval.

## What was tried (all 2026-11-13)

| Font | Result |
| --- | --- |
| Pixelify Sans, 12 px | Crowded letters; "5" drawn like "S". Replaced. |
| VT323, 16 px | Rejected by the user ("so very bad"). |
| DotGothic16, 12 px | Its grid is 16 px; thin strokes vanished (i, t, s, w lost). Rejected. |
| Silkscreen | Capitals only; too wide for sentences. Could suit short labels. |
| Tiny5 | Compact and bold; small at its 8 px grid. |
| Jersey 10, Jersey 15 | Jersey 10 crowded; Jersey 15 bold and readable but "5" looks a little like "S". |
| Press Start 2P, 8 px | Clearest letters, but 352 px for the longest line, too wide for the lesson column. Possible for titles. |
| **Micro 5, 15 px** | **Chosen.** Thin, clean, clear "5", fits every box. |
