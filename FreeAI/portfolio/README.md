# Mayank Aggarwal — Portfolio (v2)

A single-file, static portfolio site. No build step, no dependencies.

## Contents

| File | Purpose |
|------|---------|
| `index.html` | The entire site — HTML, CSS and JS inline. Fonts load from Google Fonts. |
| `Mayank_Aggarwal_Resume.pdf` | Linked from the "Download CV" buttons. |
| `robots.txt` | Allows all crawlers. |

## Design

Engineering-datasheet treatment: monospace throughout, a faint drafting grid,
crop marks, numbered sections (§0–§4), a `TABLE 0` parameter table, and a
line-printer-style history log.

- **Type:** Space Mono (display), IBM Plex Mono (body, data, labels)
- **Theme:** light = printed manual, dark = amber terminal. Follows the OS by
  default, manual toggle (◐, top-right) remembered per browser.
- Dense, no scroll animations, keyboard-accessible, respects reduced-motion,
  prints cleanly.

## Editing

Everything is in `index.html`:

- **Contact address** — search for `mayank953ai@gmail.com` (appears in the hero button and the Contact section).
- **Metrics** — the `TABLE 0` rows in §0.
- **History / Builds / Stack** — plain HTML sections, each marked with a `<!-- §N -->` comment.
- **Colours** — the `:root` CSS custom properties at the top of the `<style>` block.

## Deploy to Hostinger

This is a static site, so any of these work:

**A. hPanel file manager**
1. Zip the *contents* of this folder (not the folder itself) so `index.html` is at the archive root.
2. hPanel → Websites → your site → File Manager → `public_html`.
3. Upload the zip, extract it, delete the zip.

**B. Deploy from an archive (what was used here)**
1. `cd` into this folder and run:
   `zip -r ../portfolio_$(date +%Y%m%d_%H%M%S).zip .`
2. Deploy that archive to the target domain's `public_html` (Hostinger "deploy static website" flow).

**C. Drag-and-drop hosts** (Netlify, Cloudflare Pages, GitHub Pages)
Point the host at this folder; publish directory is the folder root.

No environment variables, no server config required.
