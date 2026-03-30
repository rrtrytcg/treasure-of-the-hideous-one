#!/usr/bin/env python3
"""
tools/renpy_automation.py

Best-effort Ren'Py UI automation script.

Behavior:
 - Optionally launches a game executable.
 - Sends repeated `space` keypresses to advance dialog.
 - Periodically saves screenshots and writes a small log.

This script is intentionally simple; it is a starting point for more advanced
automation (image templates, OCR, menu mapping).
"""

import argparse
import subprocess
import time
import os
import sys

try:
    import pyautogui
except Exception:
    pyautogui = None

try:
    import pygetwindow as gw
except Exception:
    gw = None


def parse_args():
    p = argparse.ArgumentParser(description="Simple Ren'Py runtime automation (best-effort)")
    p.add_argument('--exe', '-e', help='Path to built game executable to launch (optional)')
    p.add_argument('--presses', '-n', type=int, default=2000, help='Number of key presses to send')
    p.add_argument('--delay', '-d', type=float, default=0.4, help='Delay between key presses in seconds')
    p.add_argument('--wait', type=float, default=6.0, help='Initial wait (seconds) after launching/attaching')
    p.add_argument('--screenshot-dir', default=os.path.join('tools', 'renpy_screens'), help='Directory to save screenshots')
    p.add_argument('--screenshot-interval', type=int, default=50, help='Save a screenshot every N presses')
    p.add_argument('--log', default=os.path.join('tools', 'renpy_automation.log'), help='Path to a small log file')
    p.add_argument('--window-title', default=None, help='Optional substring of the game window title to wait for')
    return p.parse_args()


def fail_dependency_message():
    print('This script requires `pyautogui` (and usually `pillow` and `pygetwindow`).')
    print('Install them with:')
    print('  pip install pyautogui pillow pygetwindow')


def try_activate_window(title_substring, wait_seconds=6.0):
    if not gw:
        return False
    end = time.time() + wait_seconds
    while time.time() < end:
        wins = gw.getWindowsWithTitle(title_substring)
        if wins:
            try:
                wins[0].activate()
                return True
            except Exception:
                return True
        time.sleep(0.5)
    return False


def main():
    args = parse_args()

    if pyautogui is None:
        fail_dependency_message()
        return

    proc = None
    if args.exe:
        if not os.path.exists(args.exe):
            print('Executable not found:', args.exe)
            return
        try:
            print('Launching:', args.exe)
            proc = subprocess.Popen([args.exe], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            print('Failed to launch executable:', e)
            return

    # If a window-title is provided and pygetwindow is available, try to activate it
    if args.window_title:
        activated = try_activate_window(args.window_title, args.wait)
        if not activated:
            print('Window with title containing "%s" not found; continuing after wait.' % args.window_title)
    else:
        time.sleep(args.wait)

    os.makedirs(args.screenshot_dir, exist_ok=True)

    print('Starting automation: presses=%d delay=%.2f (screen shots every %d presses)' % (args.presses, args.delay, args.screenshot_interval))
    with open(args.log, 'w', encoding='utf-8') as logf:
        logf.write('Renpy automation start\n')
        try:
            for i in range(args.presses):
                # Advance dialog
                pyautogui.press('space')
                if (i + 1) % args.screenshot_interval == 0:
                    fname = os.path.join(args.screenshot_dir, f'shot_{i+1:05d}.png')
                    try:
                        pyautogui.screenshot(fname)
                        logf.write(f'screenshot {fname}\n')
                    except Exception as e:
                        logf.write(f'screenshot-failed {i+1}: {e}\n')
                logf.write(f'press {i+1}\n')
                logf.flush()
                time.sleep(args.delay)
        except KeyboardInterrupt:
            print('\nAutomation interrupted by user (KeyboardInterrupt).')
            logf.write('interrupted\n')
        except Exception as e:
            print('Automation error:', e)
            logf.write('error: %s\n' % e)

    print('Automation run complete. Log:', args.log)
    if proc:
        print('Launched process PID:', proc.pid)


if __name__ == '__main__':
    main()
