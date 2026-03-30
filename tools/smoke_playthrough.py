#!/usr/bin/env python3
# Stateful Ren'Py branch explorer / smoke-playthrough simulator
# Writes a short coverage report to tools/smoke_report.txt

import re
import os
import sys
import ast

RPY_PATH = os.path.join('game', 'treasure_of_the_hideous_one.rpy')
OUT_PATH = os.path.join('tools', 'smoke_report.txt')

if not os.path.exists(RPY_PATH):
    print('ERROR: file not found:', RPY_PATH)
    sys.exit(2)

with open(RPY_PATH, 'r', encoding='utf-8') as fh:
    lines = fh.read().splitlines()

# Collect labels
label_re = re.compile(r'^\s*label\s+([A-Za-z_][A-Za-z0-9_]*):')
labels = []
for i, ln in enumerate(lines):
    m = label_re.match(ln)
    if m:
        labels.append((m.group(1), i))

if not labels:
    print('No labels found in', RPY_PATH)
    sys.exit(1)

labels_map = {}
for idx, (name, start) in enumerate(labels):
    end = labels[idx+1][1] if idx+1 < len(labels) else len(lines)
    body = lines[start+1:end]
    labels_map[name] = {'start': start, 'end': end, 'body': body}

# Safe evaluator for simple boolean expressions using current flags
def safe_eval(expr, flags):
    if expr is None:
        return True
    expr = expr.strip()
    if expr == '':
        return True
    try:
        node = ast.parse(expr, mode='eval').body
    except Exception:
        return False
    def _eval(n):
        if isinstance(n, ast.Name):
            if n.id == 'True':
                return True
            if n.id == 'False':
                return False
            return flags.get(n.id, False)
        if isinstance(n, ast.Constant):
            return n.value
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.Not):
            return not _eval(n.operand)
        if isinstance(n, ast.BoolOp):
            if isinstance(n.op, ast.And):
                return all(_eval(v) for v in n.values)
            if isinstance(n.op, ast.Or):
                return any(_eval(v) for v in n.values)
        if isinstance(n, ast.Compare):
            left = _eval(n.left)
            for op, comp in zip(n.ops, n.comparators):
                right = _eval(comp)
                if isinstance(op, ast.Eq):
                    if not (left == right):
                        return False
                elif isinstance(op, ast.NotEq):
                    if not (left != right):
                        return False
                else:
                    return False
            return True
        return False
    try:
        return _eval(node)
    except Exception:
        return False

assign_re = re.compile(r'^\s*\$\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)$')

def parse_label_info(body_lines):
    edges = []
    entry_assigns = []
    i = 0
    menu_found = False
    while i < len(body_lines):
        ln = body_lines[i]
        stripped = ln.strip()
        # assignment outside menu (before first menu) -> entry assign
        if not menu_found:
            am = assign_re.match(ln)
            if am:
                var = am.group(1)
                expr = am.group(2).split('#',1)[0].strip()
                entry_assigns.append((var, expr))
                i += 1
                continue
        # explicit jump outside menu
        mj = re.search(r'\bjump\s+([A-Za-z_][A-Za-z0-9_]*)', ln)
        if mj and not menu_found:
            edges.append(('__auto__', mj.group(1), None, []))
            break
        # return
        if re.search(r'\breturn\b', ln) and not menu_found:
            edges.append(('__auto__', '__RETURN__', None, []))
            break
        # menu start
        if re.match(r'^\s*menu\s*:', ln):
            menu_found = True
            menu_indent = len(ln) - len(ln.lstrip())
            i += 1
            # parse choices
            while i < len(body_lines):
                l2 = body_lines[i]
                if l2.strip() == '':
                    i += 1
                    continue
                indent2 = len(l2) - len(l2.lstrip())
                # menu end
                if indent2 <= menu_indent:
                    break
                # detect quoted choice text
                m_quote = re.search(r'["\'](.+?)["\']', l2)
                if m_quote and ':' in l2:
                    choice_text = m_quote.group(1)
                    # detect condition after choice (e.g. "..." if rosentos_slain:)
                    cond_match = re.search(r'if\s+([^:]+)\s*:', l2)
                    cond = cond_match.group(1).strip() if cond_match else None
                    choice_indent = indent2
                    i += 1
                    inner = []
                    while i < len(body_lines):
                        l3 = body_lines[i]
                        if l3.strip() == '':
                            i += 1
                            continue
                        indent3 = len(l3) - len(l3.lstrip())
                        # next choice at same indent or menu end
                        if indent3 == choice_indent and re.search(r'["\'](.+?)["\']', l3) and ':' in l3:
                            break
                        if indent3 <= menu_indent:
                            break
                        inner.append(l3)
                        i += 1
                    # find jump or return and assignments inside inner block
                    target = None
                    assigns = []
                    for il in inner:
                        am = assign_re.match(il)
                        if am:
                            var = am.group(1)
                            expr = am.group(2).split('#',1)[0].strip()
                            assigns.append((var, expr))
                        mj = re.search(r'\bjump\s+([A-Za-z_][A-Za-z0-9_]*)', il)
                        if mj:
                            target = mj.group(1)
                            break
                        if re.search(r'\breturn\b', il):
                            target = '__RETURN__'
                            break
                    edges.append((choice_text, target, cond, assigns))
                    continue
                else:
                    i += 1
                    continue
            continue
        i += 1
    return edges, entry_assigns

# Build graph
graph = {}
for label, info in labels_map.items():
    edges, entry_assigns = parse_label_info(info['body'])
    graph[label] = {'edges': edges, 'entry_assigns': entry_assigns}

# Depth-first enumeration with flag state
MAX_PATHS = 2000
paths = []
start_label = 'veterans_tale' if 'veterans_tale' in graph else list(graph.keys())[0]

def state_key_for(flags):
    return tuple(sorted((k, str(v)) for k, v in flags.items()))

def dfs(curr, stack, seen, flags):
    if len(paths) >= MAX_PATHS:
        return
    # apply entry assigns for this label
    flags = dict(flags)  # copy
    for var, expr in graph.get(curr, {}).get('entry_assigns', []):
        val = safe_eval(expr, flags)
        flags[var] = val
    # mark visited label (name-based)
    visited_labels.add(curr)
    edges = graph.get(curr, {}).get('edges', [])
    if not edges:
        paths.append(stack + [(curr, '__END__', None, None)])
        return
    for choice_text, target, cond, assigns in edges:
        rec = (curr, choice_text, cond, target)
        # evaluate condition against current flags (menu visibility)
        if cond:
            ok = safe_eval(cond, flags)
            if not ok:
                continue
        # prepare flags after taking this choice (apply assigns)
        flags_after = dict(flags)
        for var, expr in assigns:
            val = safe_eval(expr, flags_after)
            flags_after[var] = val
        if target is None:
            paths.append(stack + [rec, ('__TERMINAL__', None, None, None)])
            continue
        if target == '__RETURN__':
            paths.append(stack + [rec, ('__RETURN__', None, None, None)])
            continue
        sig = (target, state_key_for(flags_after))
        if sig in seen:
            paths.append(stack + [rec, ('__LOOP__', target, None, None)])
            continue
        dfs(target, stack + [rec], seen | {sig}, flags_after)
        if len(paths) >= MAX_PATHS:
            return

# Run DFS from start
visited_labels = set()
initial_flags = {}
dfs(start_label, [], {(start_label, state_key_for(initial_flags))}, initial_flags)

# Coverage
all_labels = set(graph.keys())
unseen = sorted(list(all_labels - visited_labels))

# Write report
with open(OUT_PATH, 'w', encoding='utf-8') as out:
    out.write('Stateful Smoke Playthrough Report\\n')
    out.write('RPY: %s\\n' % RPY_PATH)
    out.write('Start label: %s\\n' % start_label)
    out.write('Total labels: %d\\n' % len(all_labels))
    out.write('Enumerated paths (cap %d): %d\\n' % (MAX_PATHS, len(paths)))
    out.write('Visited labels: %d\\n' % len(visited_labels))
    out.write('\\nUnseen labels (%d):\\n' % len(unseen))
    for u in unseen:
        out.write(' - %s\\n' % u)
    out.write('\\nSample paths:\\n')
    N = min(30, len(paths))
    for pi, p in enumerate(paths[:N]):
        out.write('Path %d:\\n' % (pi+1))
        for step in p:
            if step[0] in ('__TERMINAL__', '__RETURN__', '__LOOP__', '__END__'):
                out.write('  [%s]\\n' % step[0])
            else:
                label, choice_text, cond, target = step
                out.write('  %s --choice:"%s" cond:%s -> %s\\n' % (label, choice_text, str(cond), str(target)))
    out.write('\\nMenu choices with no explicit jump (manual check):\\n')
    for label, info in graph.items():
        for ch, tgt, cond, assigns in info.get('edges', []):
            if tgt is None:
                out.write(' - %s: "%s" cond:%s assigns:%s\\n' % (label, ch, str(cond), str(assigns)))
    out.write('\\nEnd of report\\n')

print('Report written to', OUT_PATH)
print('Labels total:', len(all_labels), 'paths enumerated:', len(paths))
print('Unseen labels:', len(unseen))
print('Sample output saved to', OUT_PATH)
