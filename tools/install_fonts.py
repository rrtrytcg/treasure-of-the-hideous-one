#!/usr/bin/env python3
"""
Download and install Google Fonts for Treasure of the Hideous One.
Run this script to download fonts, then edit gui.rpy to use them.
"""

import os
import urllib.request

FONTS = {
    "Cinzel": "https://github.com/google/fonts/raw/main/ofl/cinzel/Cinzel%5Bwght%5D.ttf",
    "Cardo": "https://github.com/google/fonts/raw/main/ofl/cardo/Cardo.ttf",
    "MedievalSharp": "https://github.com/google/fonts/raw/main/ofl/medievalsharp/MedievalSharp.ttf",
    "UnifrakturMaguntia": "https://github.com/google/fonts/raw/main/ofl/unifrakturmaguntia/UnifrakturMaguntia.ttf",
}

FONT_DIR = "game/fonts"

os.makedirs(FONT_DIR, exist_ok=True)

for name, url in FONTS.items():
    path = os.path.join(FONT_DIR, f"{name}.ttf")
    if os.path.exists(path):
        print(f"Skip: {name} (already exists)")
        continue
    try:
        print(f"Downloading: {name}")
        urllib.request.urlretrieve(url, path)
        print(f"  -> Saved to {path}")
    except Exception as e:
        print(f"  ERROR: {e}")

print(f"\nFonts downloaded to {FONT_DIR}/")
print("Now edit gui.rpy to use these fonts!")
