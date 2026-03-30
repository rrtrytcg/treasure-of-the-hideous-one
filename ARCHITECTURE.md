# Architecture — Treasure of the Hideous One

## Overview
- Ren’Py visual novel game with branching narrative, combat encounters, and multiple endings.
- Entry label starts in `game/script.rpy` and routes into the main story script `game/treasure_of_the_hideous_one.rpy`.

## Tech Stack
- **Engine**: Ren’Py (Ren’Py script + Python blocks)
- **Languages**: Ren’Py script (`.rpy`), Python (`tools/*.py`)
- **Automation tooling**: `pyautogui`, `pillow`, `pygetwindow` (see `tools/requirements.txt`)

## Directory Structure (key paths)
```
game/                             # Ren’Py game content
├── script.rpy                     # Entry label start -> jump veterans_tale
├── treasure_of_the_hideous_one.rpy# Main narrative + combat labels + helpers
├── combat_system.rpy              # Combat tables + roll_d20 + default combat state
├── game_over.rpy                  # Game over labels and restart flow
├── options.rpy                    # Ren’Py config + build settings
├── screens.rpy                    # UI screens (say, menu, save/load, etc.)
├── gui.rpy                        # GUI sizing/colors/fonts/layout variables
├── images/                        # Backgrounds (bg_*.png)
├── audio/                         # Music/SFX (mus_*.ogg)
└── tl/                            # Translations

tools/                            # Test/automation utilities
├── smoke_playthrough.py           # Stateful branch explorer -> tools/smoke_report.txt
├── renpy_automation.py            # UI automation via keypresses/screenshots
└── renpy_automation.md            # Automation checklist and usage

project.json                      # Ren’Py build settings
.vscode/settings.json             # Editor exclusions
AGENTS.md                         # Project-specific agent guidance
```

## Core Components
- **Story & branching labels** (`game/treasure_of_the_hideous_one.rpy`)
  - Main narrative labels and menus (e.g., `label veterans_tale`, `label luln_departure`).
  - Controls branching with `menu:` blocks and `jump` targets.
- **Combat system** (`game/combat_system.rpy`)
  - Tables: `ENEMIES`, `STANCE_EFFECTS`, `COMPANION_BONUSES`, `PASSIVE_ITEMS`.
  - Helpers: `get_enemy`, `get_companion_bonus`, `roll_d20`.
  - Default combat flags (e.g., `hydra_*`, `bandit_*`, `ghoul_*`, `rosentos_*`).
- **Inventory + party state** (`game/treasure_of_the_hideous_one.rpy`)
  - `default inventory = []` with `add_item`, `remove_item`, `has_item`.
  - Party flags: `party_carmelita`, `party_thut`, `in_party()` helper.
- **Game over handling** (`game/game_over.rpy`)
  - Per-defeat labels (e.g., `game_over_hydra`, `game_over_rosentos`).
  - Central `game_over_screen` menu with restart/main menu/quit.
- **UI & GUI** (`game/screens.rpy`, `game/gui.rpy`)
  - Dialogue, choice menus, save/load, preferences, game over screen.
  - GUI colors/fonts/layout set in `gui.rpy`.
- **Configuration & build** (`game/options.rpy`, `project.json`)
  - Game name/version, menu transitions, build include/exclude rules.

## Data Flow (high level)
1. **Entry**: `game/script.rpy` → `label start` → `jump veterans_tale`.
2. **Narrative branching**: `menu:` choices in `game/treasure_of_the_hideous_one.rpy` → `jump` to next label.
3. **Combat loops**:
   - Encounter label initializes state (e.g., `hydra_*` variables), then loops a `*_round` label.
   - Each round collects player choice → computes bonuses → `roll_d20` → updates stance/hits → win/lose branch.
4. **State tracking**:
   - Story flags set via `$ flag = True` (e.g., `grisbaldos_oath_taken`, `rosentos_slain`).
   - Inventory updates via `add_item` and conditional checks via `has_item`.
5. **Endings**:
   - End labels hide inventory and either go to `game_over_screen` or epilogues.

## External Integrations
- **Ren’Py engine APIs**: `renpy.music.play`, `renpy.show_screen`, `renpy.full_restart`, `renpy.quit`.
- **Automation/test tooling**:
  - `tools/smoke_playthrough.py` uses Python standard library to scan labels/menus.
  - `tools/renpy_automation.py` uses `pyautogui` + `pygetwindow` to simulate input.

## Configuration
- **Game configuration**: `game/options.rpy` (name/version, transitions, save dir, build rules).
- **GUI layout & styles**: `game/gui.rpy` (fonts, colors, sizes, layout constants).
- **Screens/UI behavior**: `game/screens.rpy` (say/menu/save/load/preferences/confirm/game over).
- **Build/package metadata**: `project.json`.
- **Editor excludes**: `.vscode/settings.json`.

## Build & Deploy
- **Run locally**: Ren’Py Launcher → “Launch Project”.
- **Build distributions**: Ren’Py Launcher → “Build Distributions” (Windows primary).
- **Smoke test (branch coverage)**:
  - `python tools/smoke_playthrough.py` → outputs `tools/smoke_report.txt`.
- **UI automation**:
  - Install deps: `pip install pyautogui pillow pygetwindow`
  - Run: `python tools/renpy_automation.py --exe "path\to\Game.exe" --presses 2000`
