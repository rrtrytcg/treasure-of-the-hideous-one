# Code Style — Treasure of the Hideous One

This document captures observed conventions from the current codebase.

## Naming Conventions
| Element | Convention | Examples | References |
|---|---|---|---|
| Labels | `snake_case` | `combat_hydra`, `luln_departure` | `game/treasure_of_the_hideous_one.rpy` |
| Characters | `snake_case` | `fondalus`, `rosentos_vamp` | `game/treasure_of_the_hideous_one.rpy` |
| Defaults/flags | `snake_case` | `party_carmelita`, `rosentos_slain` | `game/treasure_of_the_hideous_one.rpy`, `game/combat_system.rpy` |
| Functions | `snake_case` | `roll_d20`, `add_item` | `game/combat_system.rpy`, `game/treasure_of_the_hideous_one.rpy` |
| Screens | `snake_case` | `inventory_screen` | `game/treasure_of_the_hideous_one.rpy`, `game/screens.rpy` |
| Assets | `prefix_snake_case` | `bg_luln_tavern`, `char_fondalus` | `game/treasure_of_the_hideous_one.rpy` |
| Audio | `mus_*` | `audio/mus_luln_tavern.ogg` | `game/treasure_of_the_hideous_one.rpy`, `game/options.rpy` |

## File Organization
- **Main narrative + state helpers**: `game/treasure_of_the_hideous_one.rpy`.
- **Combat tables/roll logic + defaults**: `game/combat_system.rpy`.
- **Entry point**: `game/script.rpy` (`label start`).
- **UI screens**: `game/screens.rpy`.
- **GUI styling**: `game/gui.rpy`.
- **Game config**: `game/options.rpy`.

## Import / Init Style
- Python logic lives in `init python:` blocks.
- Imports appear at the top of `init python:` blocks (e.g., `import random` in `game/treasure_of_the_hideous_one.rpy`).

## Code Patterns
### Scene setup order (common pattern)
1. Music change (via `play_scene_music`).
2. `scene` background with `fade`.
3. `show` character sprites with `dissolve`.
4. Narration/dialogue.
5. `menu:` choices.

**Example** (`game/treasure_of_the_hideous_one.rpy`):
```renpy
$ play_scene_music("audio/mus_luln_tavern.ogg", fadein=1.5)
scene bg_luln_tavern with fade
show char_fondalus neutral with dissolve
narrator "..."
menu:
    "Ask about Rosentos himself":
        jump luln_departure
```

### Combat loop pattern
- Initialize per-encounter state variables at encounter label.
- Route to `*_round` label for repeated menu/roll loop.
- Compute bonus → call `roll_d20` → mutate stance/hits → win/lose branch.

**Example** (`game/treasure_of_the_hideous_one.rpy`):
```renpy
$ hydra_round = 1
$ hydra_hits = 0
...
jump combat_hydra_round

label combat_hydra_round:
    menu:
        "Strike at the heads":
            $ bonus = 0
            jump combat_hydra_attack
```

### State defaults and mutation
- **Defaults** use `default` for persistent game state.
- **Runtime changes** use `$` assignments.

**Example** (`game/treasure_of_the_hideous_one.rpy`):
```renpy
$ add_item("Hydra Eggs (10)")
$ grisbaldos_oath_taken = True
```

### Helper functions
- Small, focused helpers for inventory and party state.

**Example** (`game/treasure_of_the_hideous_one.rpy`):
```renpy
def add_item(item):
    if item not in inventory:
        inventory.append(item)
```

## Error Handling
- Minimal error handling; used primarily in helper utilities.
- `play_scene_music` uses `try/except TypeError` to handle channel differences.

**Example** (`game/treasure_of_the_hideous_one.rpy`):
```renpy
try:
    current = renpy.music.get_playing(channel="music")
except TypeError:
    current = renpy.music.get_playing()
```

## Logging
- No in-game logging conventions observed in `.rpy` files.
- Tooling scripts write to log files (e.g., `tools/renpy_automation.log`).

## Testing / Tooling Patterns
- **Branch coverage**: `tools/smoke_playthrough.py` scans labels/menus and writes `tools/smoke_report.txt`.
- **UI automation**: `tools/renpy_automation.py` simulates keypresses and saves screenshots.

## Do’s and Don’ts (observed)
- **Do** keep labels in `snake_case` and jump between labels.
- **Do** use `play_scene_music(...)` instead of raw `play music` for scene transitions (`game/treasure_of_the_hideous_one.rpy`).
- **Do** define characters at the top of the script file (see `game/treasure_of_the_hideous_one.rpy`).
- **Do** use `default` for initial game state, `$` for mutations.
- **Don’t** embed large logic outside `init python` blocks.
- **Don’t** rename asset prefixes; music uses `mus_*`, backgrounds `bg_*`, characters `char_*`.
