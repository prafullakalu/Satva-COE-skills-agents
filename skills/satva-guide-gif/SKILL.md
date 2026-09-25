---
name: satva-guide-gif
description: Produce a Satva house-format setup/user guide for any web feature — annotated full-screen screenshots with numbered callout rings, a cursor-animated narrated GIF of the whole flow, and a branded A4 PDF (SATVA banner header, contact footer, Mulish, cover page + Version History) with the GIF storyboard embedded at the end. Use when asked for a user guide, setup guide, feature documentation, walkthrough or demo GIF, annotated screenshots for a doc, or "document this feature like the Xero/Shopify MCP guide". Captures a LOCALLY RUNNING app seeded with fake data, so use it after the feature works.
---

# Satva guide + GIF pipeline

Three artefacts from one run against a **locally running** app:

1. `shots/s<NN>-<slug>.png` — full-viewport screenshots with numbered callout rings
2. `<Name>-Demo.gif` — narrated, cursor-animated walkthrough, start to finish (+ `storyboard.png`)
3. `<Name>-Setup-Guide.pdf` — Satva house format, screenshots inline, GIF storyboard at the end

`SKILL` below means **the folder that contains this file** (usually `~/.claude/skills/satva-guide-gif`).
The scripts in `starter/` find it there automatically; set `SATVA_SKILL=/path/to/satva-guide-gif` if it lives
elsewhere.

## Which document skill am I?

| Skill | Produces | For whom |
|---|---|---|
| **`satva-guide-gif`** (this) | Guide `.pdf` + annotated shots + narrated GIF | End user operating a shipped feature |
| `satva-doc` | Brief all-black Word `.doc` | Internal team: handover, "how we built it" |
| `feature-launch-video` | Marketing / launch video (MP4) | Prospects and customers |

Rule of thumb: this skill documents what the software **does** (after it works). If the feature does not run
locally yet, you are in the wrong skill.

## Rules that matter

- **Never film a third party's UI.** OAuth consent screens, vendor dashboards, editors: ripple the cursor over
  the button, then cut to a neutral illustration page (`examples/approve.html`, `examples/editor.html`) that says
  it is an illustration.
- **Never put a real secret in a shot.** Use a seeded demo tenant with fake tokens — never production or a client
  account. Every key, token and account id in a frame is invented.
- **Never invent a URL.** If the GIF has no hosted link yet, name the file and say it ships alongside the PDF.
- Set the app's public-base-url env to the **production** hostname while capturing, so screenshots show the URL
  users will really paste.
- Error strings in the troubleshooting table are **read out of the source**, never paraphrased.

## Step 0 — set up a workspace (once)

Needs Node 18+, Python 3 with Pillow, and either Google Chrome or Playwright's Chromium.

```bash
cp -r "$SKILL/starter" my-guide && cd my-guide      # Windows: Copy-Item -Recurse
npm install
pip install pillow
npx playwright install chromium     # skip if Google Chrome is installed
npm run build                       # optional smoke test: runs the whole demo pipeline
```

`starter/` is a working end-to-end example against the skill's illustration pages. Edit it for your app.
The skill ships no `node_modules`: `build-pdf.mjs` resolves `playwright` from the directory you run it in.

## Step 1 — run the app locally with demo data

Point the data dir at a scratch folder, seed a tenant with plausible **fake** records (2 items, so "choose the
active one" has something to show), and turn OFF any local-dev-only login form — it must not appear in a
customer-facing shot. Authenticate the browser by setting the session cookie directly. Read credentials from
env vars by name; never hardcode one in a seed script.

## Step 2 — screenshots (`scripts/callouts.mjs`)

```js
import { chromium } from "playwright";
import { skillUrl } from "./paths.mjs";          // from starter/
const { inject, mark, show, clear, shot, report } = await import(skillUrl("scripts/callouts.mjs"));

const browser = await chromium.launch({ channel: "chrome" }).catch(() => chromium.launch());
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
await ctx.addCookies([{ name: "session", value: KEY, domain: "localhost", path: "/" }]);
const page = await ctx.newPage();
await page.goto(BASE, { waitUntil: "networkidle" });
await inject(page);
await mark(page, "#step-connect", "1");          // ring + numbered badge
await shot(page, "shots", "s02-dashboard");      // 3rd arg name; add `true` for fullPage (justify it)
await clear(page);
report();                                         // must print "no selector problems"
```

`mark(page, sel, num, nth)` — `nth = -1` rings the union of every match (a whole list).
`show(page, sel)` scrolls the target to the middle first. **A missed selector means a ring silently did not
render** and the numbered prose now points at nothing — do not trust the output until `report()` is clean.

## Step 3 — narrated GIF (`scripts/cursor-demo.mjs`, `scripts/build-gif.py`)

```js
const { Demo } = await import(skillUrl("scripts/cursor-demo.mjs"));
const d = new Demo("gif/frames", { captionBg: "#0080C6" });
await d.install(page, "Step 1: type your store address");
await d.hold(8);                                   // ~8 frames = 0.6 s of dwell
await d.moveTo("#shop"); await d.click("#shop");
await d.type("#shop", "your-store.example.com");
await d.caption("Click Connect — you approve access next");
await d.moveTo("#connect"); await d.click("#connect");            // ripple only, no real click
await d.click(tab, async () => { await page.click(tab); });       // real interaction, own UI only
```

```bash
python "$SKILL/scripts/build-gif.py" gif/frames My-Feature-Demo.gif storyboard.png
```

`build-gif.py` walks a size ladder, stops at the first result under 12 MB, then re-opens the file and asserts
what is on disk (animated, under the limit). If those assertions fail the GIF is not shippable. Caption every
segment: one clause, imperative, no jargon. Aim for about 30 s: sign in → configure → approve → choose → copy →
paste → done.

## Step 4 — the guide PDF (`scripts/build-pdf.mjs`)

Write **body-only** HTML (`<h2>` downward; no `<html>`, `<head>`, `<style>` or `<h1>` — the cover supplies the
title), then:

```bash
node "$SKILL/scripts/build-pdf.mjs" doc.json
```

```json
{"body":"guide-body.html","out":"Acme-Portal-Setup-Guide.pdf",
 "title":"Acme Portal","subtitle":"Setup Guide","project":"Satva Acme Portal",
 "created":"25 September 2026",
 "versionRows":[["25 September 2026","First release","Satva Solutions"]]}
```

Paths inside `doc.json` are relative to its own folder. Body classes: `.tip`, `.warn`, `.break` (page break
before), `.keep`, `figure`, `figure.wide`, `figure.narrow`, `figure.strip` (storyboard), `figcaption`, `table`,
`pre`, `code`.

Structure that works, 8–12 A4 pages: what this is · before you start (address table) · numbered steps 1..N with
one screenshot each · permissions · managing it · **if something goes wrong** (table of the app's real error
strings) · quick reference · watch the setup (storyboard). `examples/body-example.html` is a complete real
guide body — copy it and rewrite.

## The house standard (the numbers)

**Screenshots** — 1440 × 900 viewport, `deviceScaleFactor: 2` → 2880 × 1800 px. Full viewport by default;
`fullPage` only when the story needs content below the fold, justified per figure. No cropping, zooming or
upscaling — scroll the target into view with `show()` and re-shoot. Page content only (no browser chrome).
Same theme, seeded data and signed-in state across a set. Name files `s<NN>-<kebab-slug>.png`, two digits,
in reading order.

**Callout ring** (`callouts.mjs`) — `3px solid #111`, 10 px radius, a 3 px white halo plus soft shadow, 6 px
padding around the target. Numbered badge: 34 px black circle, white bold 19 px number, 3 px white outline,
placed *outside* the ring at the first position that covers no text.

**Image frame in the PDF** — every screenshot gets `1px solid #b9c7d4`.

**Page** — A4; margins top 30 mm, bottom 22 mm, left/right 18 mm. Header: `assets/satva-header.png` (blue
SATVA SOLUTIONS banner, flush to the top edge) on every page. Footer: `assets/satva-footer.png`
(`sales@satvasolutions.com` bar) plus `Project — Subtitle` left and `Page N of M` right in 7 pt slate.

**Type** — Mulish (regular, bold, italic embedded from `assets/`). Body 10.5 pt / 1.5 line height, `#1a1a1a`.
h1 22 pt, h2 14 pt, h3 11.5 pt; h1/h2 in Satva blue `#0080C6`. Code: Roboto Mono 9 pt on `#f7fafd` with a
`#cfd9e3` border. Tables: 9.5 pt cells, `#b9c7d4` borders, header row `#0080C6` with white bold text.
Captions 9 pt `#48606f`. `.tip` = 3 px `#0080C6` left border on `#f2f8fd`; `.warn` = 3 px `#d97706` left border
on `#fff8ee`.

**Figures** — 150 mm wide by default (two fit a page with text); `.wide` = full column; `.narrow` = 98 mm, for
tall `fullPage` captures that would otherwise strand the next paragraph. Never override per figure with inline
styles. The storyboard is a **2 × 3 grid**, never a vertical strip (a strip is 4× taller than an A4 column).

**Cover** — "SATVA SOLUTIONS" kicker, title 30 pt, subtitle, a project block (Name of the Project · For ·
Prepared By · Created On), then a **Version History** table (Revision Date · Description of Change · Author),
then a page break before the body.

**GIF** — 1000 × 700 viewport at 1×, 56 px caption bar (`#0080C6`, white 22 px semibold), eased cursor, click
ripple. Encoded at 900 px / 70 ms / 256 colours, stepping down until under 12 MB.

## Rebranding for another organisation

Replace `assets/satva-header.png` and `assets/satva-footer.png` with your own banner and footer bar (same
proportions), swap `#0080C6` in `scripts/build-pdf.mjs`, `scripts/callouts.mjs` badge colour if wanted, and the
"Satva Solutions" strings on the cover. Fonts are OFL: Mulish and Roboto Mono can stay or be replaced.

## Before you call it done

- [ ] `report()` printed "no selector problems"
- [ ] `build-gif.py`'s verification passed — animated, under 12 MB
- [ ] No third-party UI in any frame; hand-offs cut to an illustration page that says so
- [ ] No real token, key, client name or customer record in any shot or caption
- [ ] Every error string in the troubleshooting table was copied from the source
- [ ] PDF page count is sane (no figure stranding a page); storyboard is the 2 × 3 grid
- [ ] PDF and GIF delivered together, and the paths reported back
