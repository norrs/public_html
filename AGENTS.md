# Repository Guidelines

## Project Structure & Module Organization
Snippets live under `content/posts/`, while page templates and partials are in `layouts/`. Palette and typography tweaks sit in `assets/`, and the Git-derived timeline JSON is generated into `data/post-history/`. Deployment-ready HTML lands in `public/`. Utility scripts sit in `scripts/`, while `static/` holds unprocessed files such as `CNAME`. Hugo archetypes are under `archetypes/`; avoid editing `node_modules/` directly.

## Build, Test, and Development Commands
- `npm run dev` — watches snippet content and HEAD changes, regenerates timelines, then launches `hugo server -D --disableFastRender` on port 1313 with live reload.
- `npm run build` — rebuilds history data and produces a minified static site inside `public/`.
- `npm run prepare-history` — runs `python scripts/generate_history.py` to refresh per-snippet timelines before building or committing.

## Coding Style & Naming Conventions
Markdown front matter should include `title`, `date`, and `draft` flags; use kebab-case filenames inside `content/posts/` (e.g., `retro-gfx-notes.md`). The Python helper uses standard library only—keep type hints, 4-space indentation, and docstrings consistent with `scripts/generate_history.py`. Favor descriptive template partial names (`layouts/partials/...`) and snake_case for Python variables.

## Testing Guidelines
No formal test suite exists, so treat `npm run build` as your regression check. Inspect the generated site by opening `public/index.html` or running `hugo server` in production mode. Confirm that the JSON files under `data/post-history/` update when snippets change; stale files indicate a missing history refresh.

## Commit & Pull Request Guidelines
Existing commits are terse and sometimes informal; please normalize on short, imperative summaries such as `add timeline badge spacing`. Group related edits and include context in the body if needed. PRs should describe the user-facing impact, list affected directories, and link issues when available. Attach before/after screenshots for visual changes and note any manual history regeneration steps executed.
