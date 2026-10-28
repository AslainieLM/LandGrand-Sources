---
type: design
status: proposal-baseline
updated: 2026-10-24
sources:
  - "[[Sources/Pre-proposal]]"
---

# Game Flow

This diagram summarizes [[Project/Scope and Requirements|LG-06 through LG-17]]. It describes the proposed flow; it is not a record of implemented screens.

```mermaid
flowchart TD
    Menu[Main Menu] --> Play[Play]
    Menu --> Settings[Settings]
    Menu --> Tutorial[Tutorial]
    Menu --> Exit[Exit]
    Play --> Map[Landform Map]
    Map --> Episode[Select an unlocked episode]
    Episode --> Level[Select the next available level]
    Level --> Lesson[Lesson Screen]
    Lesson --> Explore[Explore and collect]
    Explore --> Popup[Item name and description pop-up]
    Popup --> Explore
    Explore --> Result[Result Screen on level completion]
    Result --> Replay[Replay]
    Replay --> Lesson
    Result --> Next[Continue to next available level]
    Next --> Lesson
    Result --> Summary[Landform Description Screen after required episode levels]
    Summary --> Unlock[Unlock the next episode]
    Unlock --> Map
    Summary --> Complete[Completion Screen after all four episodes]
```

Source: [[Sources/Pre-proposal Extract#Program Specification|Program Specification]]. Replay passes through the pre-level lesson because the proposal places a lesson before each level.

## Progression boundaries

The proposal lists Mountains, Hills, Plains, and Plateaus. It does not explicitly confirm that this list is the required episode order, which episode starts unlocked, or what counts as completing a level or an episode. Easy → Normal → Hard is explicit. The diagram's completion branches describe conditional paths; the exact guards remain Q-02 and Q-03 in [[Questions/Open Questions|Open Questions]].

Failure, retry, pause, returning to the map, and the behavior of a time limit are unspecified. Record decisions before treating any of those paths as requirements.
