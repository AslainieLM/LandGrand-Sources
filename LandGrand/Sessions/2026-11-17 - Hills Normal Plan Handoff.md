# 2026-11-17 - Hills Normal Plan Handoff

## State

- **Hills Easy 1–3:**
  - Built: Unity project `8d92fd5`, plus the Profile "Found here" count fix in `f4e293b`.
  - 296 EditMode tests pass.
  - The user played the whole checklist, and every item passed ("Yes all passed and good").
- **Hills Normal 1–5:** planned in grilling rounds Q1–Q21 ([[Decisions/Decision Register|D-067]]).
  - **Codex (ChatGPT):** draws the art and makes the sounds with Python scripts, and writes the code.
  - **Claude:** designed and bot-checked the layouts, and wrote the content and the tickets.

## Files (Unity project, `D:\LandGrand\LandGrand\.scratch\hills-normal\`)

- `spec.md`: decisions, content drafts, and every sprite name and size, the themes, props and audio.
- `layouts.md`: rule constants and the exact data for the five levels.
  - The bot reached every goal with all 7 pickups: N1 97.6 s, N2 99.9 s, N3 98.5 s, N4 101.0 s, N5 106.1 s. Mountains Normal ran 97.6–111.6 s.
- `kinds-research.md`: sources for the seven new kinds, with confidence.
- `CODEX-START.md`, `issues/01`–`07`, and `CODEX-PROMPT.md` (paste-ready).

## Not checked yet

- No Hills Normal code, art or audio exists yet.
- **Content needs the teacher (Q-04):**
  - Coquina and volcanic breccia rest on weak sources.
  - No source names the bedrock at Pagsanjan or Banaue.
- **Numbers the bot added (not decided in grilling):**
  - The float rises at 16 px/s.
  - The bat push is spread over 0.2 s.
  - N1's practice float sits over a shallow safe pool.

## Next

1. Paste `CODEX-PROMPT.md` into Codex. It builds tickets 01–07 and does not commit.
2. Claude reviews the build (`/code-review`), runs the tests and builders in batch mode, and looks at the three preview PNGs.
3. The user plays the ticket 07 checklist.
4. Tell the adviser and panel about the Q-13 (d) additions.
5. Plan Hills Hard 1–7.

## Builders after the Codex build

LandGrand > Build Levels, Build Lesson Scene, Build Selection Scenes, Build Landform Map Scene, Build Landform Description Scene, Build Profile Scene.
