#!/usr/bin/env python3
"""Check for missing assets and broken references."""

import re
import os

content = open("game/treasure_of_the_hideous_one.rpy", encoding="utf-8").read()

# Extract audio references
audio = []
audio.extend(re.findall(r'play\s+music\s+"([^"]+)"', content))
audio.extend(re.findall(r'play\s+sound\s+"([^"]+)"', content))
audio.extend(re.findall(r'play_scene_music\("([^"]+)"', content))

# Unique audio files
audio = list(set(audio))
print(f"Audio references: {len(audio)}")

# Check which audio files exist
missing_audio = []
for a in audio:
    path = os.path.join("game", a)
    if not os.path.exists(path):
        missing_audio.append(a)

print(f"Missing audio files: {len(missing_audio)}")
for a in missing_audio[:10]:
    print(f"  - {a}")

# Check image directories
for dir_name in ["images", "audio"]:
    path = os.path.join("game", dir_name)
    if os.path.exists(path):
        files = os.listdir(path)
        print(f"{dir_name}/ has {len(files)} files")
    else:
        print(f"{dir_name}/ does not exist")
