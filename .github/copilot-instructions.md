# fltouch — Copilot Instructions

Purpose: Make an AI coding agent productive quickly on the FL Studio X-Touch MCU scripts.

## Quick summary
- This repo implements an FL Studio MIDI Control Surface script (MCU protocol) for Behringer X-Touch and extenders.
- Scripts run inside FL Studio and depend on the FL Studio scripting API (modules like `device`, `mixer`, `ui`, `midi`, `transport`, `channels`).
- Editors: key entry points are `device_XTouch.py` (main controller) and `device_XTouch_Ext.py` (extender variant).

## Architecture & responsibilities
- `device_XTouch.py` — main controller class `TMackieCU` (handlers: `OnInit`, `OnDeInit`, `OnRefresh`, `OnMidiMsg`, `OnIdle`). Modify here for high-level behavior and binding of UI controls.
- `mcu_base_class.py` — shared controller logic: page management, `Tracks` mapping, `SetKnobValue`, `UpdateTrack` helpers.
- `mcu_device.py` — hardware abstraction for the X-Touch: sysex construction (`SetTextDisplay`, `SetScreenColors`), extenders (`SendMidiToExtenders`, `SetFirstTrackOnExtender`) and per-device track wrappers (`mcu_device_track_*`).
- `mcu_colors.py`, `mcu_constants.py`, `mcu_pages.py` — small, opinionated helpers for color mapping, constants and page enums.

## Key patterns & project specifics
- FL Studio runtime: many imports (e.g., `mixer`, `device`) are provided by FL Studio; unit tests use API stubs from `requirements.txt`.
- Handlers follow PascalCase naming (e.g., `OnMidiMsg`) while modules use snake_case.
- MIDI event model: inspect `event` fields inside `OnMidiMsg` (common fields: `midiId`, `midiChan`, `data1`, `data2`, `inEv`, `outEv`, `isIncrement`). CC and pitch-bend are handled differently — see `device_XTouch.OnMidiMsg`.
- Free mode: `mcu_pages.Free` uses virtual event IDs (see `mcu_constants.FreeEventID`) and virtual tracks (`FreeTrackCount = 64`). Free knobs/buttons map to `BaseEventID + offset` (use `mixer.remoteFindEventValue` to read saved positions).
- Faders: pitch-bend is used for faders (midi channels 0–8). Conversion to FL internal values is done in `mcu_device_fader_conversion.McuFaderToFlFader`.
- Extenders: `device.dispatchReceiverCount()` indicates how many extenders are connected. Use `McuDevice.SetFirstTrackOnExtender` and `SendMidiToExtenders` to coordinate assignment and LEDs.
- UI feedback: use `OnSendMsg` (console/FL message) and `McuDevice.SetTextDisplay` for hardware display updates. `debug.PrintMidiInfo` is available for dumping event details locally.

## Tests & local development
- Install stubs: `pip install -r requirements.txt` (contains `FL-Studio-API-Stubs`).
- Run tests: `python -m unittest discover -v` or run a specific test (e.g., `python -m unittest test_colormap.py`).
- Tests are focused on pure-Python utilities (color mapping, fader conversions); hardware behavior must be validated on a real X-Touch in MCU mode.

## Debugging & validation tips
- Use `debug.PrintMidiInfo(event)` in `OnMidiMsg` to print structured event info for investigation.
- For visual/hardware changes, prefer unit tests that assert computed outputs (e.g., `mcu_colors.GetMcuColor` returns expected indices or `mcu_device.SetTextDisplay` constructs the expected sysex bytes) instead of relying only on connected hardware.
- When changing screen/sysex behavior, verify bytes emitted by `mcu_device.SetTextDisplay` or `SetScreenColors` (they rely on `device.midiOutSysex`).

## Common edits & examples
- Change knob behaviour: edit `SetKnobValue` in `mcu_base_class.py`. Update corresponding LED behavior in `mcu_device_track_encoder_knob.py` and add a unit test for edge cases.
- Modify fader conversion: update `mcu_device_fader_conversion.McuFaderToFlFader` and add tests asserting round-trip or expected numeric ranges.
- Adjust extenders or first-track logic: inspect `device_XTouch.SetPage` and `mcu_device.SetFirstTrackOnExtender` for how first-track numbers are distributed to attached extenders.

## Where to look first
- `device_XTouch.py`, `device_XTouch_Ext.py` — entry points and main behavior
- `mcu_device.py` — hardware communication & sysex
- `mcu_base_class.py` and `mcu_track.py` — UI mapping and per-track state
- `mcu_colors.py` + `test_colormap.py` — color mapping logic and tests

---

## PR checklist ✅
- Run unit tests: `python -m unittest discover -v` and fix any regressions in utilities (`mcu_colors`, `mcu_device_fader_conversion`, etc.).
- Add a focused unit test for any logic you change (examples below). Prefer deterministic, pure-Python tests that run without FL Studio.
- For hardware-impacting changes (sysex, screen output, extenders): manually validate using an X-Touch in MCU mode (follow `README.md` Installation steps), verify screen/LED behavior and `debug.PrintMidiInfo(event)` outputs.
- Update `README.md` or this file when you change user-facing behavior (layout, install instructions, or wiring/ports).
- Add a short note to the PR description describing how the change was validated (unit tests + manual steps if required).

## Example unit test — color mapping 🧪
Add tests to `test_mcu_colors.py` to assert `GetMcuColor` returns expected screen codes. Example:

```python
import unittest
from mcu_colors import GetMcuColor, ScreenColorRed, ScreenColorWhite

class TestGetMcuColor(unittest.TestCase):
    def test_red(self):
        # red: RGB (255,0,0) => int 0xFF0000
        self.assertEqual(GetMcuColor(0xFF0000), ScreenColorRed)

    def test_white(self):
        self.assertEqual(GetMcuColor(0xFFFFFF), ScreenColorWhite)

if __name__ == '__main__':
    unittest.main()
```

If you'd like, I can add the test file and a short PR checklist entry as a commit — tell me whether to proceed. ✅
