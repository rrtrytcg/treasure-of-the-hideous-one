#!/usr/bin/env python3
import re

RPY_PATH = "game\\treasure_of_the_hideous_one.rpy"
with open(RPY_PATH, "r", encoding="utf-8") as fh:
    lines = fh.read().splitlines()

labels = []
label_re = re.compile(r"^\s*label\s+([A-Za-z_][A-Za-z0-9_]*):")
for i, ln in enumerate(lines):
    m = label_re.match(ln)
    if m:
        labels.append((m.group(1), i))

labels_map = {}
for idx, (name, start) in enumerate(labels):
    end = labels[idx + 1][1] if idx + 1 < len(labels) else len(lines)
    body = lines[start + 1 : end]
    labels_map[name] = {"start": start, "end": end, "body": body}

menu_re = re.compile(r"^\s*menu\s*:")
choice_re = re.compile(r'^\s*["\'](.+?)["\']\s*:')
jump_re = re.compile(r"\bjump\s+([A-Za-z_][A-Za-z0-9_]*)")
return_re = re.compile(r"\breturn\b")

issues = []
for label, info in labels_map.items():
    in_menu = False
    menu_indent = 0
    choice_indent = 0
    for ln in info["body"]:
        stripped = ln.strip()
        if stripped.startswith("menu:"):
            in_menu = True
            menu_indent = len(ln) - len(ln.lstrip())
            continue
        if not in_menu:
            continue
        indent = len(ln) - len(ln.lstrip())
        if indent <= menu_indent and stripped:
            in_menu = False
            continue
        cm = choice_re.match(ln)
        if cm:
            choice_indent = indent
            found_jump = False
            for ln2 in info["body"][info["body"].index(ln) + 1 :]:
                ind2 = len(ln2) - len(ln2.lstrip())
                if ind2 == choice_indent and ln2.strip():
                    if jump_re.search(ln2) or return_re.search(ln2):
                        found_jump = True
                    break
                if ind2 <= menu_indent:
                    break
            if not found_jump:
                issues.append(
                    f'{label}: menu choice "{cm.group(1)}" has no explicit jump'
                )

if issues:
    print("Issues found:")
    for i in issues:
        print(" -", i)
else:
    print("No issues found - all menu choices have explicit jumps")
