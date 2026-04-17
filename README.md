# arienkock.github.io

A Jekyll-based GitHub Pages blog. Clean, markdown-authored, with a warm
paper-and-teal design.

## Writing

New posts go in `_posts/` as `YYYY-MM-DD-slug.md`:

```markdown
---
title: My post title
subtitle: Optional one-liner
date: 2026-04-17
tags: [optional, tags]
---

Body text in **Markdown**. Fenced code blocks, tables, images, and
blockquotes are all styled.
```

Commit, push — GitHub Pages builds and serves it.

## Pages

- `index.html` — home, lists `_posts/`
- `about.md` — about page
- `archive.html` — lists `_archive/` grouped by year
- `_archive/` — posts from 2013–2018, preserved and converted to markdown

## Local development

```bash
bundle install
bundle exec jekyll serve
```

Then open <http://localhost:4000>.

## Design

A light, editorial style:

- **Fonts**: Fraunces (display), Manrope (body), JetBrains Mono (code)
- **Palette**: warm paper surfaces, teal primary, rich contrast in both light
  and dark mode
- Dark mode follows OS preference and can be toggled (stored in localStorage)

Styles live in `assets/css/main.css`.

## Legacy

The original 2013–2018 site and old index live under `legacy/` for reference.
They're excluded from the Jekyll build. The old post URLs
(`/YYYY/MM/DD/slug.html`) now redirect to the archive versions at
`/archive/YYYY-MM-DD-slug/` — internal cross-links between old posts were
rewritten automatically during conversion. Note: anyone linking to the _old_
URLs externally will hit 404 unless you add redirect rules; consider the
[jekyll-redirect-from](https://github.com/jekyll/jekyll-redirect-from) plugin
if you want to preserve them.

## Re-running the archive conversion

The conversion script is at `_tools/convert_archive.py` — only needed if you
ever want to regenerate the archive from the original HTML sources:

```bash
python3 _tools/convert_archive.py
```
