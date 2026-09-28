# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Personal portfolio for Dinmuhammad, a static site served by GitHub Pages (`.nojekyll`, custom domain in `CNAME`). All user-facing text is in **Uzbek (Latin script)**, including commit messages and code comments — keep new content in the same language and use the typographic apostrophe `‘` / `’` as the existing text does (e.g. `Qo‘llab-quvvatlash`, `sun’iy`).

## Build

```sh
python3 build.py
```

No dependencies (standard library only), no tests, no linter. The script prints `tayyor: N sahifa` on success. There is no dev server; to preview, serve the repo root with any static server (e.g. `python3 -m http.server`) — pages use root-absolute paths (`/style.min.css`, `/assets/...`), so opening files directly from disk won't render correctly.

## Architecture

The site is generated, and **the generated output is committed** (GitHub Pages serves the repo root as-is):

- `data.py` — all content: `SITE` (name, URLs, contact handles, SEO `keywords`, search-console verification codes), `SERVICES`, `SUPPORT`, `SKILLS`/`SKILL_LEVELS` (the `/konikmalar/` page; also feeds `Person.knowsAbout`), `FAQ`, `PROJECTS`, `POSTS`.
- `build.py` — renders `data.py` into HTML with f-strings. `page()` is the shared layout (head/meta/OG tags, nav, footer, theme toggle, and the "nudge" contact popup JS); `build_index`, `build_project`, `build_blog_index`, `build_post`, `build_404` produce page bodies.
- `style.css` — the only hand-written stylesheet. `build.py` minifies it into `style.min.css`, which is what pages link.

Generated files — **never edit by hand**; change `data.py`/`build.py`/`style.css` and rebuild, then commit source and output together:
`index.html`, `404.html`, `konikmalar/index.html`, `loyihalar/<slug>/index.html`, `blog/index.html`, `blog/<slug>/index.html`, `sitemap.xml`, `robots.txt`, `llms.txt`, `llms-full.txt`, `style.min.css`.

Discoverability (search engines and AI assistants): every page gets schema.org JSON-LD via `ld()` (a shared `Person` node plus page-specific `WebSite`/`ProfilePage`, `CreativeWork`, `Blog`/`BlogPosting`, `BreadcrumbList`); `llms.txt`/`llms-full.txt` are markdown summaries built from `data.py`; `robots.txt` explicitly allows the AI crawlers in `AI_BOTS`.

Things to know when editing content:

- Most strings are HTML-escaped via `E()`, but project `summary` is inserted raw (it intentionally contains `<b>` tags); it's also stripped to plain text for the meta description.
- A project's `site` is either `(href, label)` or `None`; when `None`, `site_label` is shown as plain text instead.
- `SERVICES[*].examples` are project slugs and must exist in `PROJECTS`. `SERVICES[*].icon` must be a key in `SERVICE_ICONS` in `build.py`.
- Project pages link prev/next cyclically in `PROJECTS` order; the homepage shows the first 3 `POSTS`.
- Blog "posts" are summary pages; each links out via `url` to a separate course site hosted elsewhere under the same GitHub Pages account.
- If `SITE["whatsapp"]` is empty, WhatsApp buttons fall back to GitHub (`second_contact()`).
- Renaming or removing a slug leaves the old generated directory behind — delete it manually.
- Image variants in `assets/` (`-480`/`-760` JPG+WebP, `avatar-96.webp`) are pre-generated and committed; `build.py` does not produce them.
