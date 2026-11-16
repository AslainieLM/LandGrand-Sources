---
type: session
status: active
updated: 2026-11-17
sources:
  - "[[Decisions/Decision Register#D-066]]"
  - "[[Project/Gameplay Design#Hills (D-066)]]"
---

# Hills plan handoff (2026-11-17)

Follows [[Sessions/2026-11-16 - Mountains Hard Build Review Handoff]]. Spec, tickets and bot files: `D:\LandGrand\LandGrand\.scratch\hills\` (`spec.md`, `CODEX-START.md`, `issues/01`–`07`, `bot-check-*.cs.txt`, and the previews `art-preview.png`, `backdrop-preview.png`, `badge-preview.png` and `audio-preview.png`).

## State

- **Mountains Hard play check:** the user played the whole D-065 checklist on 2026-11-16, and every item passed (fixes in `0726daf`). Ticket 09, D-065 and Current Focus record it.
- **Grilling (Q1–Q10):** the user took every recommendation. The result is D-066 and [[Project/Gameplay Design#Hills (D-066)|the Hills section]].
- **Made by Claude, not committed:**
  - `Tools/Art/make_hills_easy_art.py`
  - `Tools/Art/make_hills_easy_backdrops.py`
  - `Tools/Audio/make_hills_audio.py`
  - the ten Hills badges added to `Tools/Art/make_profile_art.py`
  - every PNG, OGG and WAV those scripts write
  - the `.scratch/hills/` files

  Each was checked on its preview image. The audio was checked by length, loudness and a spectrum picture; it has not been listened to.
- **Bot check:** E1 66.0 s, E2 72.7 s and E3 81.1 s to the goal; 15 of 15 pickups can be reached; no lint warnings.
- **Code:** not started. Codex builds tickets 01–07.
- **Vault:** D-066, the Gameplay Design Hills section, notes on Q-03, Q-04 and Q-13, and Current Focus are updated (not committed).

## Not checked yet

- How the music and ambience sound (listen during the play check).
- The H2 landslide location (Antipolo) has no source yet. The Batanes facts rest on travel guides only.
- Ilmenite was dropped from E3 because no source confirmed it in Ilocos sand; feldspar replaces it.

## Next

1. Paste the Codex prompt (below) to start the build from `CODEX-START.md`.
2. Claude reviews the build (`/code-review`).
3. The user plays the ticket 07 checklist.
4. Plan Hills Normal 1–5.
5. Tell the adviser and panel about the Q-13 (d) additions.

## Codex prompt

> Read `D:\LandGrand\LandGrand\.scratch\hills\CODEX-START.md` and follow it. Build tickets 01 to 07 in `.scratch/hills/issues/` in the order and with the blocking edges given there. Use `.scratch/hills/spec.md` for every number and text. Do not commit, do not edit art or audio files, and end each ticket by naming the Unity builder to run. Finish with ticket 07's handover.

## Builders to run after the build

**LandGrand > Build Levels**, **Build Lesson Scene**, **Build Selection Scenes**, **Build Landform Map Scene**, **Build Landform Description Scene** and **Build Profile Scene**.
