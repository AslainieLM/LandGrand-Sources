---
type: session
status: active
updated: 2026-11-15
sources:
  - "[[Decisions/Decision Register#D-065]]"
  - "[[Project/Gameplay Design#Mountains Hard 1–7 (D-065)]]"
---

# Mountains Hard plan handoff (2026-11-15)

Follows [[Sessions/2026-11-15 - Mountains Normal and Backgrounds Handoff]]. Spec, tickets and bot files: `D:\LandGrand\LandGrand\.scratch\mountains-hard\` (`spec.md`, `CODEX-START.md`, `issues/01`–`09`, `bot-check-*.txt`, `backdrop-preview.png`).

## State

- **Designed with `/grilling`** (Q1–Q14, every answer the recommended one) and recorded as D-065. Q-03's "required episode levels" is answered: all 15 levels.
- **Made, not committed (the user makes the commits):**
  - new scripts `Tools/Art/make_hard_art.py`, `Tools/Art/make_hard_backdrops.py` and `Tools/Audio/make_hard_audio.py`;
  - four badge symbols added to `Tools/Art/make_profile_art.py`;
  - all their PNG, OGG and WAV outputs under `Assets/Art` and `Assets/Audio`.
  - The art was checked by viewing preview sheets. After the first look, these were fixed: the Sierra Madre clouds, the tanzanite colour, the watch station dish, the glacier soil tile, and the Mayon, Matterhorn, Kilimanjaro and Mauna Kea backgrounds.
- **Bot check:** all seven layouts reach the goal in 131–156 s of 240 s; all 63 pickups are reachable; the layout checks pass. The bot gained the rolling boulder and icy ground. One fairness rule came out of it: a boulder skips its roll when the explorer is within 48 px of its start.
- **Code:** not started. Codex builds it from the tickets.
- **Vault:** D-065, the Gameplay Design section, Open Questions Q-03 and Q-13 (d), Current Focus and this note are not committed yet.

## Not checked yet

- Unity has not imported the new assets; no scene has been built.
- The audio was generated but not listened to.
- The rolling boulder and ice numbers are checked by the bot only; tune them after the first play if they feel wrong.

## Next

1. Paste the Codex prompt (given in chat on 2026-11-15) into Codex and let it work through tickets 01–09.
2. Review Codex's work (`/code-review`), then play Hard 1–7 and the Description Screen with the ticket 09 checklist.
3. Tell the adviser and panel about the Q-13 (d) additions.
4. Plan Hills when ready; its levels, lessons, kinds and backgrounds do not exist yet.

**Unity builders after Codex is done:** **Build Mountains Levels**, **Build Lesson Scene**, **Build Selection Scenes**, **Build Landform Map Scene**, **Build Landform Description Scene** (new), **Build Profile Scene**.
