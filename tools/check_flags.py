#!/usr/bin/env python3
"""Check for undefined flag variables in conditions."""

import re
import os

# Read all rpy files
files = [
    "game/treasure_of_the_hideous_one.rpy",
    "game/combat_system.rpy",
    "game/screens.rpy",
]

defined_flags = set()
used_flags = set()

# Known Ren'Py/Python keywords to exclude
keywords = {
    "True",
    "False",
    "None",
    "and",
    "or",
    "not",
    "if",
    "elif",
    "else",
    "in",
    "is",
}

for filepath in files:
    if not os.path.exists(filepath):
        continue
    content = open(filepath, encoding="utf-8").read()

    # Find default statements (flag definitions)
    for m in re.findall(r"default\s+(\w+)\s*=", content):
        defined_flags.add(m)

    # Find $ assignments at start of line
    for m in re.findall(r"^\s*\$\s*(\w+)\s*=", content, re.M):
        defined_flags.add(m)

    # Find inline $ assignments
    for m in re.findall(r"\$\s*(\w+)\s*=", content):
        defined_flags.add(m)

    # Find conditions (if/elif with variables)
    for m in re.findall(r"\bif\s+([^:]+):", content):
        # Extract variable names from condition
        vars = re.findall(r"\b([a-z_][a-z0-9_]*)\b", m)
        for v in vars:
            if v not in keywords and not v.isdigit():
                used_flags.add(v)

    # Find 'if in_party' conditions
    for m in re.findall(r"\bif\s+([a-z_][a-z0-9_]*)\b", content):
        if m not in keywords:
            used_flags.add(m)

# Flags used but not defined
undefined = used_flags - defined_flags - keywords

# Filter to likely game flags (not function calls, not python builtins)
builtin_funcs = {
    "print",
    "len",
    "range",
    "str",
    "int",
    "float",
    "list",
    "dict",
    "set",
    "open",
    "input",
    "abs",
    "min",
    "max",
    "sum",
    "zip",
    "map",
    "filter",
    "sorted",
    "reversed",
    "enumerate",
    "type",
    "isinstance",
    "hasattr",
    "getattr",
    "setattr",
    "bool",
    "bytes",
    "chr",
    "ord",
    "jump",
    "show",
    "hide",
    "scene",
    "play",
    "stop",
    "pause",
    "renpy",
    "pyautogui",
    "narrator",
    "define",
    "init",
    "menu",
    "return",
}

suspicious = (
    undefined
    - builtin_funcs
    - {
        "in_party",
        "has_item",
        "get_companion_bonus",
        "get_combat_stance",
        "roll_d20",
        "outcome",
        "total",
        "raw",
        "bonus",
        "i",
        "m",
        "v",
        "n",
        "content",
        "result",
        "target",
        "choice_text",
        "cond",
        "assigns",
        "stack",
        "seen",
        "flags",
        "curr",
        "edges",
        "edge",
        "label",
        "info",
        "ch",
        "tgt",
        "assign",
        "ok",
        "val",
        "var",
        "expr",
        "am",
        "mj",
        "l2",
        "l3",
        "il",
        "ln",
        "am",
        "fh",
        "pi",
        "p",
        "step",
        "u",
        "all_labels",
        "visited_labels",
        "start_label",
        "graph",
        "labels_map",
        "labels",
        "idx",
        "name",
        "start",
        "end",
        "body",
        "lines",
        "line",
        "label_re",
        "out",
        "label_name",
        "start_line",
        "end_line",
        "label_lines",
        "menu_re",
        "choice_re",
        "jump_re",
        "assign_re",
        "flag_assigns",
        "flag_name",
        "flag_value",
        "label_data",
        "menu_data",
        "choice_data",
        "jump_target",
        "assign_data",
        "menu_indent",
        "choice_indent",
        "choice_line",
        "inner_lines",
        "inner",
        "found",
        "target_label",
        "choice_label",
        "assign_var",
        "assign_expr",
        "flag_conditions",
        "flag_name",
        "flag_expr",
        "flags_dict",
        "result_flags",
        "check_flags",
        "test_flags",
        "flag_list",
        "flag_set",
        "flag_dict",
        "flag_keys",
        "flag_values",
        "flag_items",
        "flag_count",
        "flag_index",
        "flag_key",
        "flag_type",
        "flag_types",
        "flag_names",
        "flag_defs",
        "flag_def",
        "flag_use",
        "flag_uses",
        "flag_ref",
        "flag_refs",
        "flag_ref",
    }
)

print(f"Defined flags: {len(defined_flags)}")
print(f"Used flags: {len(used_flags)}")
print(f"Undefined but used: {len(undefined)}")
print(f"Suspicious (not builtins): {len(suspicious)}")

if suspicious:
    print("\nSuspicious flags (used but may not be defined):")
    for s in sorted(suspicious)[:30]:
        print(f"  - {s}")
