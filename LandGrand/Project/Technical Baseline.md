---
type: technical
status: proposal-baseline
updated: 2026-10-26
sources:
  - "[[Sources/Pre-proposal]]"
---

# Technical Baseline

These are the pre-proposal's declared specifications. Installed versions, build configuration, performance, and implemented save behavior have not been audited.

## Proposed development environment

| Item | Proposal specification |
| --- | --- |
| Engine | Unity Engine; version unspecified |
| Language | C# |
| Graphics tools | Piskel and Clip Studio Paint |
| Development OS | Windows 11, 64-bit |
| Editor | Visual Studio Code |
| Developer CPU | 11th Gen Intel Core i7-1185G7 at 3.00 GHz |
| Developer RAM | 16 GB, 2400 MHz |
| Developer GPU | Intel Iris Xe Graphics |
| Developer storage | 256 GB SSD |

Evidence: [[Sources/Pre-proposal Extract#Software Specification|Software Specification]] and [[Sources/Pre-proposal Extract#Hardware Specification|Hardware Specification]].

## Target devices

[[Project/Scope and Requirements#Device requirements|LG-25]] records the user-confirmed **Android 10 and above** target under D-012. Device/build validation remains separate from that requirement; the version-range decision no longer blocks manuscript wording.

## Save data

[[Project/Scope and Requirements#Presentation and persistence|LG-19]] identifies the proposed saved fields. Save format, save timing, reset behavior, interrupted-write recovery, profile count, and replay merge rules are not specified. The player's name is local game data; it does not imply an online account.

## Implementation evidence

The Unity workspace is `D:\Projects\LandGrand`. When checking implementation, record the relevant revision, files, build, or test results separately from proposal intent. Use [[Decisions/Decision Register|Decision Register]] for confirmed changes and [[Questions/Open Questions|Open Questions]] for unresolved differences.
