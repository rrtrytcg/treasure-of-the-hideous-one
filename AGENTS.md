# AGENTS.md - Treasure of the Hideous One

This file provides guidance for AI coding agents working in this Ren'Py visual novel codebase.

## Project Overview

This is a Ren'Py visual novel game: "Treasure of the Hideous One," a D&D-style adventure module. The game features:
- Branching narrative with multiple endings
- Combat system using D20 rolls
- Party system with companions (Carmelita, Thut)
- Inventory management
- State tracking via game flags

## Build/Test Commands

### Running the Game
Open the Ren'Py SDK launcher and select this project, then click "Launch Project".

### Building Distributions
From Ren'Py launcher: "Build Distributions" → select platform (Windows is primary).

### Smoke Test (Branch Coverage)
```powershell
python tools\smoke_playthrough.py
```
Outputs coverage report to `tools\smoke_report.txt`. Enumerates all labels and menu choices, tracking visited paths and flag states.

### UI Automation Test
```powershell
pip install pyautogui pillow pygetwindow
python tools\renpy_automation.py --exe "path\to\Game.exe" --presses 2000
```
See `tools/renpy_automation.md` for full documentation.

### Running a Single Test (Label)
No formal test framework. To test a specific label/scene:
1. Edit `game/script.rpy` to jump directly to your label:

```renpy
label start:
    jump your_label_name
```

2. Launch project in Ren'Py and play through.

## Code Style Guidelines

### Ren'Py Script (.rpy) Formatting

#### Labels andFlow
```renpy
# Use lowercase with underscores for label names
label combat_hydra:
    # Music/scene setup first
    $ play_scene_music("audio/mus_combat_mid.ogg", fadein=0.8)
    scene bg_riverbank_hydra with fade# Dialogue and narration
    narrator "The hydra surges from the shallows!"
    
    # Menu choices last
    menu:
        "Attack directly":
            jump combat_hydra_attack
        "Retreat":
            jump combat_hydra_retreat
```

#### Character Definitions
```renpy
# At top of file, define characters with colors
define narrator = Character(None, what_color="#d4cfc8")
define fondalus = Character("Fondalus the Soldier", color="#c8a84b")
define rosentos_vamp = Character("Rosentos the Vampire", color="#dc143c", what_italic=True)
```

#### Game State Flags
```renpy
# Use default for persistent game state
default inventory = []
default combat_bonus = 0
default rosentos_slain = False

# Use $ for runtime modifications
$ combat_bonus += 2
$ rosentos_slain = True
```

#### Python Blocks
```renpy
init python:
    # Import at top of init block
    import random
    
    # Function names use snake_case
    def roll_d20(bonus=0):
        raw = random.randint(1, 20)
        total = max(1, min(20, raw + bonus))
        # Return tuple of (raw, total, outcome_string)
        if raw == 20:
            return (raw, total, "critical_success")
        # ...elif outcome == "success":
            return (raw, total, "success")
        return (raw, total, "failure")
    
    # Helper functions for game state
    def add_item(item):
        if item not in inventory:
            inventory.append(item)
    
    def has_item(item):
        return item in inventory
```

#### Screens
```renpy
screen inventory_screen():
    frame:
        xalign 1.0
        yalign 0.0
        background Frame("#1a1a2ecc", 10, 10)
        vbox:
            spacing 4
            text "INVENTORY" size 18 color "#c8a84b" bold True
            if inventory:
                for item in inventory:
                    text "• [item]" size 16 color "#d4cfc8"
            else:
                text "— empty—" size 16 color "#6b6880" italic True
```

### Comment Conventions

```renpy
# ============================================================
# SECTION HEADER
# ============================================================

# --- SUBSECTION HEADER ---
# Music: description of emotional tone
$ play_scene_music("audio/mus_luln_tavern.ogg", fadein=1.5)

# ASSET: Detailed description for image generation prompts
# This is used when generating background/character art.
# Prompt: [detailed image prompt]
# Mood: [emotional descriptors]
# Lighting: [lighting description]
scene bg_luln_tavern with fade
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|----------|
| Labels | snake_case | `combat_hydra`, `luln_departure` |
| Characters | snake_case | `fondalus`, `rosentos_vamp` |
| Default variables | snake_case | `combat_bonus`, `rosentos_slain` |
| Functions | snake_case | `roll_d20()`, `add_item()` |
| Screens | snake_case | `inventory_screen` |
| Assets | snake_case withunderscores | `bg_luln_tavern.png`, `char_rosentos friendly.png` |
| Audio |mus_prefix + snake_case | `mus_combat_mid.ogg` |

### Error Handling in Python Blocks

```renpy
init python:
    defplay_scene_music(track, fadein=0.0):
        try:
            current = renpy.music.get_playing(channel="music")
        except TypeError:
            current = renpy.music.get_playing()
        
        # Avoid restarting same track
        if current == track or (current and current.rsplit("/", 1)[-1] == track.rsplit("/", 1)[-1]):
            return False
        
        renpy.music.play(track, channel="music", fadein=fadein)
        return True
```

### Conditional Logic

```renpy
# Useif/elif/else for branching
if in_party("carmelita"):
    carmelita "My grandmother was one of Rosentos' original soldiers."
    
if has_item("Essence-Orb of Trinkla"):
    narrator "The orb pulses coldly in your pack."

# Combine conditions with and/or
if grisbaldos_oath_taken and rosentos_slain:
    narrator "A soldier's ghost, finally at rest."
```

### File Organization

```
game/
├── script.rpy              # Entry point (just label start: jump veterans_tale)
├── treasure_of_the_hideous_one.rpy  # Main game script
├── options.rpy             # Game configuration (name, version, build settings)
├── screens.rpy             # UI screens (say,choice, menu, preferences)
├── gui.rpy                 # GUI styling and dimensions
├── images/                 # Background images (bg_*.png)
├── audio/                  # Music and sound (mus_*.ogg)
├── saves/                  # Save files (gitignored)
└── tl/                    # Translations
```

## Important Patterns

### D20 Combat Resolution
```renpy
$ combat_bonus = 0
# Player choices modify combat_bonus
menu:
    "Attack aggressively":
        $ combat_bonus += 2
    "Defend carefully":
        $ combat_bonus += 1
        
$ raw, total, outcome = roll_d20(combat_bonus)

if outcome == "critical_success":
    jump combat_enemy_critical_win
elif outcome == "success":
    jump combat_enemy_win
elif outcome == "partial":
    jump combat_enemy_partial
elif outcome == "failure":
    jump combat_enemy_lose
else:
    jump combat_enemy_critical_fail
```

### Flag Tracking
Track story state with boolean flags:
- `grisbaldos_oath_taken` - Player swore oath to ghost
- `grisbaldos_cursed` - Player refused ghost's oath
- `rosentos_slain` - Rosentos was defeated
- `party_carmelita` / `party_thut` - Companion joined party

Use suffix conventions:
- `_taken`, `_slain`, `_killed` - Positive action completed
- `_witnessed`, `_found`, `_betrayed` - Event occurred

### Music Transitions
Always use `$ play_scene_music()` helper instead of raw `play music`:
```renpy
$ play_scene_music("audio/mus_explore_swamp.ogg", fadein=2.0)
```

### Scene Transitions
```renpy
scene bg_new_location with fade  # Standard transition
show char_name expression with dissolve  # Character entrance
```

## Assets

### Image Naming
- Backgrounds: `bg_location_name.png` (1920x1080)
- Characters: `char_name expression.png` (~600px tall, transparent bg)

### Audio Naming
- Music: `mus_descriptive_name.ogg`
- Stingers: `mus_stinger_event.ogg`