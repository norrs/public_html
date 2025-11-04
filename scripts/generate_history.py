#!/usr/bin/env python3
"""Generate repository and per-post git history data for Hugo."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Iterable, List

ROOT = Path(__file__).resolve().parents[1]
CONTENT_ROOT = ROOT / "content" / "posts"
DATA_ROOT = ROOT / "data"
POST_HISTORY_ROOT = DATA_ROOT / "post-history"


def run_git(args: Iterable[str]) -> str:
    """Run a git command in the repository and return stdout."""
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def parse_log_lines(lines: Iterable[str]) -> List[dict]:
    entries: List[dict] = []
    for raw_line in lines:
        if not raw_line:
            continue
        parts: List[str] = raw_line.split("\x1f")
        if len(parts) != 3:
            continue
        commit, date, subject = parts
        entries.append(
            {
                "hash": commit,
                "short": commit[:7],
                "date": date,
                "subject": subject,
            }
        )
    return entries


def collect_post_history(markdown: Path) -> List[dict]:
    rel_path = markdown.relative_to(ROOT)
    output = run_git([
        "log",
        "--follow",
        "--date=iso-strict",
        "--pretty=format:%H%x1f%ad%x1f%s",
        "--",
        str(rel_path),
    ])
    return parse_log_lines(output.splitlines())


def write_json(path: Path, payload: List[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")


def generate_post_histories() -> None:
    if POST_HISTORY_ROOT.exists():
        for json_file in POST_HISTORY_ROOT.glob("**/*.json"):
            json_file.unlink()
    for markdown in sorted(CONTENT_ROOT.rglob("*.md")):
        history = collect_post_history(markdown)
        rel = markdown.relative_to(ROOT / "content")
        target = POST_HISTORY_ROOT / rel.with_suffix(".json")
        write_json(target, history)


def main() -> None:
    generate_post_histories()


if __name__ == "__main__":
    main()
