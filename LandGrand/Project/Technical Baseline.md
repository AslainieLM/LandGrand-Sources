---
type: technical
status: proposal-baseline
updated: 2026-11-12
sources:
  - "[[Sources/Pre-proposal]]"
---

# Technical Baseline

These are the pre-proposal's declared specifications. The limited file-level configuration inspection below is separate from those declarations. Installed dependencies, build output, performance, and implemented save behavior have not been audited.

## Proposed development environment

| Item | Proposal specification |
| --- | --- |
| Engine | Unity Engine; version unspecified |
| Language | C# |
| Graphics tools | Piskel and Clip Studio Paint (proposal). Aseprite replaces Piskel for pixel art under [[Decisions/Decision Register#Confirmed decisions|D-028]]. |
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

The Unity workspace is `D:\LandGrand\LandGrand`. When checking implementation, record the relevant revision, files, build, or test results separately from proposal intent. Use [[Decisions/Decision Register|Decision Register]] for confirmed changes and [[Questions/Open Questions|Open Questions]] for unresolved differences.

## Configuration inspection, 2026-11-01

Direct file reads during the [[Sources/Chapter III Unrevised Draft 2026-11-01#Limited Unity configuration inspection|Chapter III review]] recorded Unity editor version `6000.5.6f1` (revision `0e0577a1a2ac`) in `ProjectSettings/ProjectVersion.txt`, and `AndroidMinSdkVersion: 26` with `AndroidTargetSdkVersion: 0` in `ProjectSettings/ProjectSettings.asset` lines 180–181. These are dated configuration values, not proof of installed build dependencies or a working Android build. Recheck the files before making current implementation claims.

The minimum value does not enforce the confirmed Android 10+ floor: Android 10 is API 29 and API 26 corresponds to Android 8.0, as documented by [Android Developers](https://developer.android.com/guide/topics/manifest/uses-sdk-element). Keep the requirement unchanged and track configuration reconciliation/device validation under Q-01. No project settings were changed, and no earlier-Android support or successful device test is established.
