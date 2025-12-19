# fltouch — Copilot Instructions

Purpose: Help an AI coding agent be productive quickly when working on the FL Studio X-Touch scripts in this repo.

## Quick summary
- This repo implements an FL Studio MIDI control script (MCU protocol) for Behringer X-Touch and extenders.
- Runtime: These scripts run inside FL Studio and use the FL Studio scripting API (modules like `device`, `mixer`, `ui`, `midi`, `transport`, `channels`).

## Architecture & responsibilities
- `device_XTouch.py` — Main controller logic; defines `TMackieCU` with `OnInit`, `OnMidiMsg`, and `OnRefresh` handlers.
- `device_XTouch_Ext.py` — Extender variant (`TMackieCU_Ext`), reuses common base behavior.
- `mcu_device.py` — Hardware abstraction: building sysex messages, screen text/colors, sending messages to extenders.
- `mcu_base_class.py` — Shared logic between main controller and extenders: page management, track mapping (`Tracks`), text updates, meter updates.
- `mcu_*` modules (`mcu_track.py`, `mcu_device_track_*.py`, `mcu_colors.py`, `mcu_constants.py`, etc.) — small, focused helpers for UI/LED/track/state handling.

## Runtime & entry points
- FL Studio discovers scripts from the file header comments (e.g. top of `device_XTouch.py` includes `name=` and `supportedDevices=`).
- Key handlers an agent may modify: `OnInit`, `OnDeInit`, `OnRefresh`, `OnMidiMsg` in `device_XTouch.py` and extender file.
- Low-level hardware messages are constructed in `mcu_device.py` (e.g. `SetTextDisplay`, `SetScreenColors`, product IDs: `0x14` main, `0x15` extender).

## Testing & local development
- Tests are small unit tests focused on utilities (e.g. `test_colormap.py`, `test_mcu_colors.py`).
- Use the provided API stubs for local testing: `pip install -r requirements.txt` (contains `FL-Studio-API-Stubs`).
- Run tests: `python -m unittest discover -v` or `python -m unittest test_colormap.py`.

## Project-specific conventions & pitfalls
- This code runs in FL Studio's environment — imports like `mixer`, `device`, `ui` are provided by FL Studio; don't assume standard Python runtime behavior.
- Naming: class methods often use PascalCase (e.g. `OnInit`, `SetTextDisplay`), modules use snake_case. Follow the existing casing for consistency.
- Track mapping: `McuBaseClass.Tracks` maps UI slots to FL Studio track numbers; many page-specific behaviors depend on `mcu_pages` and `FirstTrack`.
- "Free" mode: `mcu_pages.Free` uses virtual event IDs (`mcu_constants.FreeEventID`) and virtual tracks (`FreeTrackCount = 64`).
- When changing visual behavior, see `mcu_colors.GetMcuColor` and tests in `test_colormap.py` to validate color mapping.

## Common change patterns (examples)
- Add or change knob behavior: edit `SetKnobValue` in `mcu_base_class.py` and LED behavior in `mcu_device_track_encoder_knob.py`.
- Modify fader mapping: inspect `device_XTouch.OnMidiMsg` (pitch-bend handling) and `mcu_device_fader_conversion.McuFaderToFlFader`.
- Update screen text or sysex formatting: modify `McuDevice.SetTextDisplay`/`SetScreenColors` and test that the sysex byte arrays conform to the MCU protocol used elsewhere in the repo.

## Integration & testing notes
- Hardware testing requires an actual X-Touch in MCU mode (see `README.md` installation steps). Unit tests only cover CPU-side logic (colors, conversions).
- When adding tests, prefer simple deterministic unit tests that exercise utility functions (color mappings, fader conversions) — these run in CI without FL Studio.

## Where to look next (important files)
- `device_XTouch.py`, `device_XTouch_Ext.py` (entry & event handlers)
- `mcu_device.py` (sysex, screen, device-level send/dispatch)
- `mcu_base_class.py` and `mcu_track.py` (mapping logic)
- `mcu_colors.py` + tests (`test_colormap.py`, `test_mcu_colors.py`)
- `requirements.txt` (developer dependency: FL Studio API stubs)

---
If anything here is unclear or you'd like more details (e.g., example PR template changes, suggested test cases, or an issue checklist for hardware changes), tell me what to expand. ✅
