---
name: satva-doc
description: Write a brief INTERNAL Word document (.doc) in the Satva house style — Mulish body, Roboto Mono code, pure black, no colour anywhere — that explains in plain language how something was built or how a mechanism works. Use for implementation write-ups, handover notes, "explain what we did and where it lives", or when asked for a "satva doc" / a brief Word document. NOT for client-facing setup guides (use satva-guide-gif) and NOT for marketing video (use feature-launch-video).
---

# Satva doc (internal house style)

Produce a Microsoft Word–compatible `.doc` written as a single HTML file. Word opens HTML-based `.doc`
natively — **no pandoc, no docx library, no dependency at all.** One file, written directly, opens in Word.

## Which document skill am I?

| Skill | Produces | For whom |
|---|---|---|
| **`satva-doc`** (this) | Brief `.doc`, plain black house style | **Internal** — the team, a handover, a reviewer |
| `satva-guide-gif` | Branded guide `.pdf` + annotated screenshots + narrated GIF | **End users / clients** of a shipped feature |
| `feature-launch-video` | Launch video | Prospects and customers |

If someone needs to *operate* a feature step by step with pictures, or the document goes to a client, use
`satva-guide-gif` instead — a client document must carry the Satva banner and footer, which this format
deliberately does not.

## Non-negotiable formatting rules

These *are* the house style. Do not tune them per document. The pure-black, colourless look is an intentional
choice for internal notes, not something to "fix".

- **All text pure black (`#000000`). No colours anywhere** — not in headings, links, borders or tables.
- **Body + headings font:** `"Mulish", "Segoe UI", sans-serif`.
- **Code font:** `"Roboto Mono", "Roboto", Consolas, monospace`.
- **Sizes:** title 20 pt · h2 15 pt · h3 12.5 pt · body/list 11 pt · table cells 10.5 pt · code 9.5 pt.
- Code blocks: `<pre>` with a plain 1 pt black border, 8 pt / 10 pt padding, `white-space: pre-wrap`.
- Tables: collapsed 1 pt black borders, bold header row, left-aligned, full width.
- A4 page, 2.2 cm margins, line height 1.55.
- Simple language throughout — short sentences, explain jargon inline, bold the key phrase of each point.

## File skeleton

```html
<html xmlns:o="urn:schemas-microsoft-com:office:office"
      xmlns:w="urn:schemas-microsoft-com:office:word"
      xmlns="http://www.w3.org/TR/REC-html40">
<head>
<meta charset="utf-8">
<title>DOC TITLE</title>
<!--[if gte mso 9]><xml><w:WordDocument><w:View>Print</w:View><w:Zoom>100</w:Zoom></w:WordDocument></xml><![endif]-->
<style>
  @page { size: A4; margin: 2.2cm; }
  body { font-family: "Mulish", "Segoe UI", sans-serif; color: #000; font-size: 11pt; line-height: 1.55; }
  h1 { font-size: 20pt; font-weight: bold; margin: 0 0 4pt 0; }
  h2 { font-size: 15pt; font-weight: bold; margin: 18pt 0 6pt 0; }
  h3 { font-size: 12.5pt; font-weight: bold; margin: 14pt 0 4pt 0; }
  p, li { font-size: 11pt; }
  pre, code { font-family: "Roboto Mono", "Roboto", Consolas, monospace; font-size: 9.5pt; color: #000; }
  pre { border: 1pt solid #000; padding: 8pt 10pt; margin: 6pt 0 10pt 0; white-space: pre-wrap; }
  table { border-collapse: collapse; margin: 6pt 0 10pt 0; width: 100%; }
  th, td { border: 1pt solid #000; padding: 4pt 8pt; font-size: 10.5pt; text-align: left; vertical-align: top; }
  th { font-weight: bold; }
  hr { border: none; border-top: 1pt solid #000; margin: 14pt 0; }
</style>
</head>
<body>
  <h1>Title</h1>
  <p class="subtitle">One-line subtitle</p>
  <hr>
  <!-- numbered h2 sections -->
</body>
</html>
```

## Content structure (adapt the topic, keep the order)

1. **What is X, in simple words?** — plain-language definition; a 3-column table if there are phases or modes.
2. **What we built / what this covers.**
3. **Step-by-step flow** — one `h3` per step, with real examples and **real code snippets read out of the
   actual repo**. Never invent a snippet and never paraphrase an error string — open the file and quote it.
4. **How it works end to end** — a table tracing one action through every layer, naming what guards each step.
5. **What this gave us** — bullet list of concrete benefits.
6. **Where everything lives** — file/purpose table, paths relative to the repo root.
7. Close with **"In one sentence:"** — a single bold summary sentence.

## Delivery

- Save as `docs/<Topic>-Guide.doc` in the consuming project's repo (create `docs/` if missing).
- Report the absolute path back to the user. If the host can attach files, attach it too; if not, say so and
  give the path — never claim a file was sent when it was not.

## Fonts

Mulish and Roboto Mono are the house fonts and must be installed on the machine that *opens* the file; the
`.doc` references them by name and does not embed them. Without them Word falls back to Segoe UI / Consolas —
the document still opens and stays all-black, just off-brand. This repo ships them in
`../satva-guide-gif/assets/` (`Mulish-*.ttf`, `RobotoMono.ttf`); on Windows, right-click → *Install for all
users*. Both are free from Google Fonts (`ofl/mulish`, `ofl/robotomono`).

## Before you call it done

- [ ] Every code snippet and file path was read out of the repo, not recalled or invented
- [ ] No colour anywhere — grep the file for `color:` and confirm every value is `#000`
- [ ] No credential, token, connection string or real customer record in the prose
- [ ] Opens in Word (a `.doc` that only renders in a browser has a broken `<!--[if gte mso 9]-->` block or
      namespace declarations)
- [ ] The absolute output path was reported back
