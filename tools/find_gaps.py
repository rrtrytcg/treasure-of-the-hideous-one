#!/usr/bin/env python3
"""Find potential story gaps and loose ends."""

import re
import os

content = open("game/treasure_of_the_hideous_one.rpy", encoding="utf-8").read()

print("=" * 60)
print("STORY GAP ANALYSIS - Treasure of the Hideous One")
print("=" * 60)

# 1. Check for jumps to labels that might not exist
all_content = content
for extra_file in ["game/game_over.rpy", "game/combat_system.rpy"]:
    if os.path.exists(extra_file):
        all_content += "\n" + open(extra_file, encoding="utf-8").read()

all_labels = set(re.findall(r"^label\s+(\w+):", all_content, re.M))
jumps = set(re.findall(r"jump\s+(\w+)", content))
missing_labels = jumps - all_labels

print(f"\n1. BROKEN JUMPS (jump to undefined label)")
if missing_labels:
    for l in sorted(missing_labels):
        print(f"   MISSING: jump {l}")
else:
    print("   None found - all jumps resolve to labels")

# 2. Check for labels that are never jumped to (orphaned)
# (excluding start label and common patterns)
start_label = "veterans_tale"
jumped_to = set(jumps)
orphaned = all_labels - jumped_to - {start_label}
# Filter out labels that are entry points (e.g., game_over_*, combat_*)
orphaned = {
    l
    for l in orphaned
    if not l.startswith("game_over_") and not l.startswith("combat_")
}

print(f"\n2. ORPHANED LABELS (never jumped to, excluding entry points)")
print(f"   Total labels: {len(all_labels)}")
print(f"   Labels jumped to: {len(jumped_to)}")
print(f"   Potentially orphaned: {len(orphaned)}")
if orphaned and len(orphaned) < 20:
    for l in sorted(orphaned):
        print(f"   ORPHAN: {l}")
elif len(orphaned) > 20:
    print(f"   (Too many to list - likely normal entry points)")

# 3. Check for incomplete conditionals (if without else where it matters)
print(f"\n3. CRITICAL PATH CHECKS")

# Check if key story flags are used
key_flags = [
    "grisbaldos_oath_taken",
    "grisbaldos_cursed",
    "rosentos_slain",
    "slave_farm_betrayed",
    "slave_farm_mercy_killed",
    "party_carmelita",
    "party_thut",
]

for flag in key_flags:
    count = content.count(flag)
    status = "[OK]" if count > 0 else "[MISSING]"
    print(f"   {status} {flag}: referenced {count} times")

# 4. Check menu choices
menus = re.findall(r"menu\s*:", content)
menu_count = len(menus)
print(f"\n4. MENU STATISTICS")
print(f"   Total menus: {menu_count}")

# 5. Check for TODO/FIXME comments
todos = re.findall(r"#\s*(TODO|FIXME|XXX|HACK)[:\s]*(.+)", content, re.I)
print(f"\n5. CODE COMMENTS (TODO/FIXME)")
if todos:
    for todo, text in todos[:10]:
        print(f"   {todo}: {text.strip()[:60]}")
else:
    print("   None found")

# 6. Check for placeholder text
placeholders = re.findall(r"(XXX|PLACEHOLDER|INSERT|TODO)", content, re.I)
print(f"\n6. PLACEHOLDER TEXT")
print(f"   Found: {len(placeholders)} instances")

print("\n" + "=" * 60)
print("Analysis complete")
print("=" * 60)
