---
name: satva-ppt
description: >-
  Create or edit PowerPoint decks (.pptx) in the Satva house style: 16:9, Mulish on the
  branded background, #1194D2 headings, point-to-point bullets, code boxes, card and step
  diagrams. Use when someone says "satva ppt", "make a deck", "training deck", "add slides",
  "edit this pptx", or names a .pptx to read, edit, build or trim in the Satva format.
metadata:
  department: "satva"
  domain: "presentations"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---


# Satva PPTX — build and edit

A `.pptx` is a ZIP of XML. Pick the approach by task:

| Task | Approach |
|---|---|
| **Build slides that look designed** | `scripts/satva_deck.py` — cards, badges, step flows, chevrons, chips, code panels |
| **Retext an existing slide** | `scripts/satva_pptx.py` — clone slides, swap text, keep every bit of formatting |
| **Read a deck** | `python scripts/satva_pptx.py deck.pptx` — dumps every slide's text and tables |
| **Animations + transitions** | `powershell -File scripts/animate.ps1 -Deck out.pptx` — one fade per component group |
| **Visual QA + validation** | `powershell -File scripts/render.ps1 -Deck out.pptx -Out shots` → view the PNGs |

Requires the `python-pptx` package to be already available. The scripts live in this
skill's `scripts/` folder (add it to `sys.path`). `render.ps1` and `animate.ps1` drive
desktop PowerPoint over COM (Windows only); that doubles as the file check: if
PowerPoint opens and exports it, the package is valid.

**Never build a Satva deck from scratch with pptxgenjs or an empty python-pptx
presentation.** The branded background image is not shipped in this repo: always start
from an existing Satva deck (ask the CoE team for the current template deck) and clone its slides — the background image, the master, the
fonts and the footer bars are the brand, and they only survive a clone.

## The house format (measured from the real training decks)

Canvas **10 × 5.625 in** (16:9). Every content slide is the same four shapes on a
full-bleed background picture:

| Shape name | Position (in) | Style |
|---|---|---|
| Background `PICTURE` | 0, 0 · 10 × 5.625 | branded jpg — never touch, never recolour |
| Title (`Google Shape;65;*`) | 0.35, 0.92 · 9.22 wide | **Muli 20pt bold, `#1194D2`** |
| Kicker (`;66;*`) | 0.35, ~1.40 · 9.22 wide | Muli 13pt *italic*, `#1194D2` — one line, sets up the slide |
| Body (`;67;*`) | 0.35, ~1.90 · 9.22 wide | Muli 14pt, `#212121`, bulleted, 115% line, 10pt after |
| Code box (`SkillExample`) | 5.12, 1.83 · 4.44 wide | header Muli 14pt bold `#1194D2`; lines **Consolas 11.5pt `#434343`** |
| Footer (`SkillsFooter` / `Footer`) | 0.35, ~4.85 · 9.22 wide | 12.5pt `#1194D2`, centred — one takeaway line |
| Table (`Table 2`) | 0.35, ~1.85 · 8.43 wide | header row filled `#1194D2`, white bold 13pt Muli; body 12pt |

Two-column slides split the body: left `0.35 → 4.44 wide`, right `5.12 → 4.44 wide`.

Colours: **`#1194D2` brand blue · `#212121` body · `#434343` code · `#FFFFFF` on blue.**
Nothing else. No accent stripes, no extra palette, no clip art.

## Components — build slides out of these, not paragraphs

A training slide is a *diagram of an idea*, not a page of prose. Every component
below draws real PowerPoint shapes, so the deck stays editable by hand afterwards.

```python
import sys; sys.path.insert(0, "<path-to-this-skill>/scripts")
from satva_pptx import *
from satva_deck import *

prs = Presentation("template-deck.pptx")      # an existing Satva deck
s = blank(prs, prs.slides[6], "Slide Title", "The one-line kicker.")   # slide 6 = a bullets slide of the template
```

| Component | Use it for | Call |
|---|---|---|
| `cards` | **The default.** Definition sets — What it is / Why it exists / When to use it | `cards(s, [(title, [lines], badge?), ...], h=2.18, cols=COL3)` |
| `steps` | An ordered process where each step needs a sentence | `steps(s, [(label, detail), ...], y=1.88, row=0.58)` |
| `chevrons` | A short pipeline of single words — Discuss → Plan → Verify | `chevrons(s, ["Discuss", "Plan", "Verify"])` |
| `chips` | An inventory: tools, servers, integrations | `chips(s, [(name, sub), ...], cols=COL5)` |
| `code` | Install / CLI blocks, Consolas on a tinted panel | `code(s, x, y, w, h, "gstack — terminal", [lines])` |
| `callout` | One contrast block — the pain vs the fix | `callout(s, x, y, w, h, [lines])` |
| `footer` | The one line to remember. Auto-hugs the row above it | `footer(s, "…")` |

Layout constants: `COL2 / COL3 / COL4 / COL5` give `(x_positions, width)` for an
n-across row; `BAND` is the vertical content band. Colors: `BLUE INK GREY WHITE
LINE TINT`, plus `RED`/`GREEN` for badge fills where the semantics are universal
(a TDD red-green-refactor cycle, pass/fail) — never for decoration.

**Sizing cards is the one thing to get right.** Height = `0.66` (title row)
`+ 0.20 × wrapped body lines + 0.18` padding. Pass `y=None` (the default) and the
row centres itself in the band; `footer()` then sits 0.32in under it. Guessing
too tall leaves dead space, and it is the most common defect in a first render.

**Do not** put a table on a slide where three cards would say the same thing.
Tables are for a genuine matrix — the side-by-side comparison — nothing else.

## Font — check this before anything else

The Satva template asks for **`Muli`**. That family was renamed **`Mulish`** in
2020 and `Muli` is installed nowhere, so PowerPoint silently substitutes a
fallback on every run — which reads as uneven weight and loose spacing, never as
a missing-font warning. `satva_deck` writes `Mulish`; run `set_font_family(prs)`
once before saving to repoint the template's own runs too (it fixed hundreds of runs
in one real deck).

```powershell
# confirm what is actually installed before trusting a render
Add-Type -AssemblyName System.Drawing
[System.Drawing.FontFamily]::Families | Where-Object { $_.Name -match "Mulish" }
```

Office 2013 COM does **not** expose `EmbedTrueTypeFonts`, so the deck cannot
embed the font programmatically. Either install Mulish on the presenting machine
(per-user fonts folder), or embed by hand via
File → Options → Save → *Embed fonts in the file*.

## Animation

`animate.ps1` drives PowerPoint over COM — python-pptx cannot write animations,
and hand-authoring `<p:timing>` XML is the quickest way to make PowerPoint
declare a deck corrupt. Every component built by `satva_deck` is named
`A<group>_<n>`; the script fades in one group per click, so a three-card slide
reveals card by card while you talk. Untagged shapes (background, title, kicker)
are on screen from the start. Slide transitions are plain OOXML —
`set_transition(prs, "fade")` in Python, no COM needed.

Run order matters: **build in Python → save → animate.ps1 → render.ps1.**
Rebuilding overwrites the file and drops the animations, so re-run `animate.ps1`
after every rebuild.

## Language

Training decks get read aloud to people who do not know the vocabulary. Write
the way you would explain it standing at a whiteboard:

- No unexplained jargon. "context rot" → "in a long chat the AI slowly gets worse".
- No consultant register: "opinionated bundle", "polyglot", "product judgement", "orchestrate" — all out.
- Prefer a concrete example over an abstraction: an actual question someone would type beats a description of a capability.
- Spell an acronym out the first time, then use it.

## Content rules

- **One idea per slide.** Title says the idea, kicker says why it matters, body proves it in 4–6 bullets, footer gives the one line to remember.
- **Point to point.** A bullet is one sentence. Lead with a bolded phrase and an em-dash: `**The problem:** …`. In `set_bullets()` write it as `**The problem:** …`.
- **Max 6 bullets** per body box, **max 6 rows** per table — past that the text overflows 5.625in and gets clipped.
- Training decks are read aloud: the deck carries the skeleton, the speaker carries the detail. If a bullet needs a second sentence, it is a footer line or a new slide.
- Real commands, real URLs, real project names. Never invented examples.
- Every deck ends with the existing "Thanks for Listening" slide — clone, never rebuild.

## Editing recipe

```python
import sys; sys.path.insert(0, "<path-to-this-skill>/scripts")
from satva_pptx import *

prs = Presentation("deck.pptx")
s = prs.slides[6]

set_text(shape_by_name(s, "Google Shape;65;p14"), "Slide Title")
set_text(shape_by_name(s, "Google Shape;66;p14"), "The one-line kicker.")
set_bullets(shape_by_name(s, "Google Shape;67;p14"), [
    "**The problem:** what hurts today.",
    "**The fix:** what this changes.",
])

new = clone_slide(prs, prs.slides[6])          # exact copy incl. background
set_table(shape_by_name(s2, "Table 2"), [["h1","h2"], ["a","b"]])
reorder_slides(prs, [0, 1, 27, 2, 3])          # also DELETES anything omitted
prs.save("deck.pptx")
```

Order of operations, always: **clone every new slide first → then fill text → then
reorder/delete → then save.** Cloning after editing clones the edits.

## Gotchas

- `text_frame.text = "..."` **collapses the paragraph to one unstyled run** and loses Muli/blue/bullets. Use `set_text` / `set_bullets` / `set_steps`, which swap only the string inside the existing run.
- `reorder_slides` drops any index you leave out — that is how you delete slides. The dropped slide *parts* stay inside the zip (harmless, a few KB each) — PowerPoint ignores anything missing from `<p:sldIdLst>`.
- **Deleting a shape off an animated slide breaks the whole file.** `animate.ps1` leaves a `<p:timing>` block naming each shape by `spid`; delete the shape and PowerPoint refuses to open the deck — no repair prompt, just `Presentations.Open` throwing `E_FAIL`. Strip `<p:timing>` from every slide you rebuild, then re-run `animate.ps1`.
- Same silent `E_FAIL`, two more causes: a `"\n"` inside a run is invalid DrawingML (`_write` now splits on it), and several slides sharing one `notesSlide` part (`clone_slide` no longer copies that relationship). None of the three shows up in a python-pptx round-trip — `render.ps1` is the only test that catches them.
- `clone_slide` copies relationships, so background images survive; a cloned chart still *points at* the original's chart part — edit one and you edit both.
- Bullets are inherited from `<a:pPr marL="200025" indent="-200025">`. Never type a literal `•`.
- Round-tripping OOXML through `xml.etree.ElementTree` rewrites namespaces and corrupts the deck. python-pptx (lxml) is safe.
- The template says Muli, we write Mulish; PowerPoint substitutes if it is missing, which changes wrapping. Check overflow in the render, not in the XML.

## Updating a deck the user has edited by hand

**Once you have delivered a deck, never re-run its build script.** It regenerates
every slide from the original and destroys every hand edit — deleted slides come
back, retyped lines revert. Open the delivered file and patch it in place:

```python
prs = Presentation("Delivered Deck.pptx")
assert len(prs.slides._sldIdLst) == 21, "not the deck I expected"   # fail loud
```

Before touching it, diff the current file against what the script would produce
(build into a scratch directory, dump both, compare) so you know exactly what the
user changed and can preserve it. Copy the file to `*-handedited-backup.pptx`
first — the update is destructive and you will want to re-run it after a fix.

Component shape names embed `id(shape) % 100000`, a Python memory address, so
**they are not stable across runs.** Never target a shape by an `A<group>_<n>`
name written in an earlier session. To rewrite a component slide, delete its
`A*` shapes wholesale and redraw with the component library — the template chrome
(`Google Shape;64/65/66;p14`) is what stays. `reorder_slides` still works: read
the live order first, then map indices.

`prs.save()` preserves the `<p:timing>` animation blocks PowerPoint wrote, so an
in-place text edit does not cost you the animations. Adding or reordering slides
does — re-run `animate.ps1` after those.

## QA before delivering (required)

1. Copy the source to `*-original.pptx` **before** the first edit, and make the script read the original and write the live filename — then every rebuild is idempotent instead of editing its own output.
2. `python scripts/satva_pptx.py out.pptx` — content, order, no leftover placeholder text.
3. `powershell -File scripts/render.ps1 -Deck out.pptx -Out shots` — then **look at every PNG**. Text spilling past 5.4in vertically is the #1 defect; two-column slides and 6+ bullet bodies are where it happens. A left column of 4.44in fits ~48 characters per line and 7 lines total.
4. Deliver the file and say which slides you checked.

## Companion

For Word documents use the `satva-doc` skill (Mulish, black, no colour). Decks and docs are deliberately different; do not copy doc rules into slides.
