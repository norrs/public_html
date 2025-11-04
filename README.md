# Simple Markdown Blog

This repository contains a Hugo-powered blog that converts Markdown into clean, minimal HTML. It delivers a fast local writing workflow, live reload, and Git-aware metadata without any heavy theming.

## Prerequisites

- [Hugo Extended](https://gohugo.io/getting-started/installing/) v0.123 or newer on your PATH
- Python 3.10+ (used for deriving Git history during the build)
- Optional: Node.js if you prefer `npm` scripts

## Local development

1. Install Hugo and ensure the `hugo` binary is available.
2. Clone this repository.
3. Generate Git history data and start the live reload server:

   ```bash
   npm run dev
   # or, manually
   python scripts/generate_history.py && hugo server -D --disableFastRender
   ```

4. Open <http://localhost:1313>. Saving Markdown files inside `content/` triggers an automatic browser refresh.

The default theme is inspired by the Amstrad CPC6128 palette but tuned for modern readability with generous white space and high-contrast typography.

## Creating new posts

Use Hugo’s archetype to scaffold a draft:

```bash
hugo new posts/my-new-post.md
```

Update the front matter as desired. Remove `draft: true` when you are ready to publish. The `.Date` field controls the “Created” timestamp; `.Lastmod` is pulled from Git automatically.

Each post shows a revision timeline sourced from Git at the bottom of the page. The history includes every commit that touched that Markdown file (following renames).

## Deployment (GitHub Pages)

A GitHub Actions workflow can build and publish the static site to the `gh-pages` branch:

```yaml
name: Deploy Hugo site
on:
  push:
    branches: [main]
permissions:
  contents: read
  pages: write
  id-token: write
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-hugo@v4
        with:
          hugo-version: 'latest'
          extended: true
      - name: Build Git-aware data
        run: python scripts/generate_history.py
      - name: Build site
        run: hugo --minify
      - uses: actions/upload-pages-artifact@v3
        with:
          path: public
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

Place your custom domain in `static/CNAME` and configure your DNS records to point at GitHub Pages.

## Repository history view

Visit `/history/` in the generated site to browse commits. The data is created automatically by the same script that powers per-post timelines.
