Ren'Py Runtime Automation — Checklist & Quick Start
===============================================

Purpose
-------
This document describes how to run a best-effort UI automation for the Ren'Py project "Treasure of the Hideous One". It includes prerequisites, a quick-start checklist, and usage notes for the accompanying script `tools/renpy_automation.py`.

Prerequisites
-------------
- Ren'Py SDK installed on your machine (Windows installer from renpy.org).
- A built Windows distribution of the game, or the ability to "Launch Project" from the Ren'Py launcher.
- Python 3.8+ installed (for the automation script).
- Automation Python packages: `pyautogui`, `pillow`, and `pygetwindow` (installation shown below).

Quick checklist
---------------
1. Install Python and pip if missing.
2. Install automation dependencies:

```powershell
pip install pyautogui pillow pygetwindow
```

3. Build the Windows distribution from the Ren'Py launcher (optional but recommended for stable execution).
   - Open the Ren'Py launcher, select the project `Treasure of the Hideous One`, choose "Build Distributions" → "Windows" and note the produced `exe` path.

4. Adjust in-game settings for reliable keyboard control:
   - Ensure dialog advance is bound to `Space` or `Enter` (default Ren'Py behavior).
   - Prefer using number/arrow keys for menu selections if possible.

5. Bring the built game executable or the running game window to the foreground when running automation.

Running the quick test (dependency check)
----------------------------------------
The accompanying script prints helpful messages when packages are missing. To run the basic dependency check, run:

```powershell
python tools\renpy_automation.py
```

If dependencies are missing, the script will show the `pip install` command to run.

Full run example (when ready)
----------------------------
Once the game `exe` is available, run a simple automated advance test:

```powershell
pip install pyautogui pillow pygetwindow
python tools\renpy_automation.py --exe "C:\path\to\Game\release\Treasure.exe" --presses 2000 --delay 0.4 --wait 6
```

Outputs
-------
- Log: `tools/renpy_automation.log`
- Screenshots (periodic): `tools/renpy_screens/` (created by the script)

Notes & Limitations
-------------------
- This is a best-effort UI automation. It advances the UI by pressing `Space` repeatedly and captures periodic screenshots.
- It does NOT (yet) implement robust menu-choice logic (image templates or OCR required for that). For reliable menu navigation, add image templates and use `pyautogui.locateOnScreen()` or integrate `pytesseract` for OCR.
- Resolution, UI scaling, and window position affect reliability. Run on a consistent display resolution and scale.
- Always be ready to interrupt the script with Ctrl+C.

Next steps (optional)
---------------------
- Add a JSON mapping of menu identifiers → choice indexes, then extend the script to detect menus and select mapped options.
- Add `pytesseract` OCR support for text-based menu recognition.

End of checklist
