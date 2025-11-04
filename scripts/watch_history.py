#!/usr/bin/env python3
"""Continuously refresh Git-derived history data while Hugo dev server runs."""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path
from typing import Dict

ROOT = Path(__file__).resolve().parents[1]
CONTENT_ROOT = ROOT / "content"
HISTORY_SCRIPT = ROOT / "scripts" / "generate_history.py"
POLL_INTERVAL = 1.0  # seconds


def snapshot_markdown_mtimes() -> Dict[Path, float]:
    """Return a mapping of Markdown files to their last modified timestamps."""
    mtimes: Dict[Path, float] = {}
    for markdown in CONTENT_ROOT.rglob("*.md"):
        try:
            mtimes[markdown] = markdown.stat().st_mtime
        except FileNotFoundError:
            continue
    return mtimes


def regenerate_history() -> None:
    """Invoke the history generator script."""
    try:
        subprocess.run([sys.executable, str(HISTORY_SCRIPT)], check=True)
    except subprocess.CalledProcessError as exc:
        print(f"watch-history: history generation failed ({exc.returncode})", file=sys.stderr, flush=True)


def current_head() -> str:
    """Return the current Git HEAD hash, or an empty string if unavailable."""
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        return ""
    return result.stdout.strip()


def main() -> None:
    print("watch-history: generating history data…", flush=True)
    regenerate_history()
    prev_snapshot = snapshot_markdown_mtimes()
    prev_head = current_head()

    try:
        while True:
            time.sleep(POLL_INTERVAL)
            current_snapshot = snapshot_markdown_mtimes()
            head = current_head()
            has_content_change = current_snapshot != prev_snapshot
            has_head_change = head != prev_head
            if has_content_change or has_head_change:
                reason = "content update" if has_content_change else "new commit"
                print(f"watch-history: {reason} detected, rebuilding history…", flush=True)
                regenerate_history()
                prev_snapshot = current_snapshot
                prev_head = head
    except KeyboardInterrupt:
        print("watch-history: stopping watcher.", flush=True)


if __name__ == "__main__":
    main()
