---
type: requirements
status: proposal-baseline
updated: 2026-10-26
sources:
  - "[[Sources/Pre-proposal]]"
---

# Scope and Requirements

Every requirement below is a statement in the pre-proposal, normalized for reference. These IDs identify proposed requirements; they do not certify approval or working software. Confirmed changes are recorded in [[Decisions/Decision Register|Decision Register]].

## Audience and delivery

Source: [[Sources/Pre-proposal Extract#Scope of the Study|Scope]] and [[Sources/Pre-proposal Extract#Limitations of the Study|Limitations]].

| ID | Proposed requirement |
| --- | --- |
| LG-01 | Serve Grade 5 learners at Baluan Elementary School. |
| LG-02 | Provide a single-player Android educational game, usable offline at home alongside printed learning materials. |
| LG-03 | Cover Mountains, Hills, Plains, and Plateaus, with selected rocks and minerals associated with each landform. |
| LG-04 | Provide four episodes, one for each listed landform. |
| LG-05 | Give each episode Easy with 3 levels, Normal with 5 levels, and Hard with 7 levels. |
| LG-06 | Complete levels in order; unlock Normal after Easy and Hard after Normal. Unlock later episodes after completing the previous episode. Exact completion criteria remain open. |

## Learning and play

Source: [[Sources/Pre-proposal Extract#Scope of the Study|Scope]] and [[Sources/Pre-proposal Extract#Program Specification|Program Specification]].

| ID | Proposed requirement |
| --- | --- |
| LG-07 | Present a short lesson before each level about its landform and rocks or minerals. |
| LG-08 | Let an explorer character move and jump using simple touch controls. |
| LG-09 | Let the learner explore and collect rocks and minerals. |
| LG-10 | Show a collected item's name and short description in a pop-up. |
| LG-11 | Include challenges such as obstacles, traps, pitfalls, and time limits. The source gives no level-by-level distribution. |
| LG-12 | After each level, show collected items, a short review, and up to three performance-based stars. Scoring rules remain open. |
| LG-13 | Allow replay or continuation to the next available level. |
| LG-14 | Show a landform summary after all required levels in an episode, then unlock the next episode. |
| LG-15 | After all four episodes, show total stars, collected rocks and minerals, and a congratulatory message. |

## Presentation and persistence

Source: [[Sources/Pre-proposal Extract#Program Specification|Program Specification]].

| ID | Proposed requirement |
| --- | --- |
| LG-16 | Main Menu offers Play, Settings, Tutorial, and Exit. Settings controls and tutorial contents are unspecified. |
| LG-17 | Provide a Landform Map where only unlocked episodes can be selected. |
| LG-18 | Use simple 2D graphics, large touch buttons, background music, and sound effects. |
| LG-19 | Automatically save the player's name, unlocked episodes, completed levels, earned stars, and collected rocks and minerals on the device; load them on the next play session. |

## Explicit boundaries

Source: [[Sources/Pre-proposal Extract#Limitations of the Study|Limitations]].

| ID | Proposed boundary |
| --- | --- |
| LG-20 | Limit the study population to Grade 5 learners at Baluan Elementary School. |
| LG-21 | Limit coverage to the four listed landforms and selected related rocks and minerals, rather than all types. |
| LG-22 | Exclude multiplayer, online features, online accounts, cloud storage, websites, and an administrator panel. |
| LG-23 | Exclude separate quiz screens, GPS, and real-world scanning. |
| LG-24 | Save progress only on the device being used. |

## Device requirements

LG-25: **Confirmed target: Android 10 and above**, on Android phones and tablets, under D-012 in [[Decisions/Decision Register|Decision Register]] and [[Sources/Project Clarifications 2026-10-26|the direct user confirmation]]. The pre-proposal's **2 GB RAM minimum** and **300 MB free space** remain declared minimum targets. This records the required Android range, not a claim that every version/device has been tested. Q-01 now retains only device-validation follow-up.

The original source conflict is retained for history: its limitations say Android 10–14, while its hardware section says Android 10 and above. D-012 resolves the project target without modifying either original passage.

Evidence: [[Sources/Pre-proposal Extract#Limitations of the Study|Limitations]] and [[Sources/Pre-proposal Extract#Hardware Specification|Hardware Specification]].

[[Project/Game Flow|Game Flow]] visualizes the proposed sequence. [[Project/Technical Baseline|Technical Baseline]] records the proposed development environment. [[Research/Proposal Review|Proposal Review]] explains the 60-level workload inference.
