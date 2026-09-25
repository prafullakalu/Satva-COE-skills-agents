---
name: feature-launch-video
description: Generate a marketing/launch video for any feature of any product — reads the real user flow, writes a grounded brief, picks a visual theme, composes and renders a HyperFrames video, produces fully original voice/music/SFX (no copyrighted audio, ever), and mixes to broadcast-ready audio. Use when someone asks for a promo/launch/demo/sizzle video for a feature, module, or product.
---

# feature-launch-video

Turns "make a launch video for [feature]" into a rendered video in one sitting, for **any**
project — not tied to any one product. Install it with the repo's `install.ps1` / `install.sh` (or copy this folder into `~/.claude/skills/` or a
project's `.claude/skills/`).

This is a **generator**, not a template with the blanks left in from a past project. Every fact
that reaches the screen comes from `brief.json`, which you build by actually reading the feature —
not by imagining a cool video and backfilling data to match.

## The non-negotiable rules (read before doing anything else)

1. **Ground every claim.** Every number, screen state, and line of copy in `brief.json` traces to
   something real: code you read, a running build, real sample data, or a fixture you explicitly
   label as one (`groundedFactsSource: "example/demo — ..."`). Never invent a stat to make a scene
   look better. If the feature doesn't exist yet, say so on screen — `compose.mjs` does this
   automatically via a "CONCEPT / NOT FINAL" stamp whenever `groundedFactsSource` reads like a demo.
2. **Never use a copyrighted reference track**, not even "slightly changed." If someone hands you a
   reference video for style, take the *structure* (pacing, shot types, energy arc) and match the
   picture — never reuse its audio, and never help disguise a copyrighted track as original. `music.py`
   in this skill always synthesizes fully original audio in code. See `references/no-copyrighted-audio.md`.
3. **Brand comes from the project, not your imagination.** Read the project's own brand guideline /
   `DESIGN.md` / style guide first; only fall back to a theme's defaults when nothing exists, and say
   so out loud. Never hand-redraw an official logo — use the real file or omit the logo.
4. **Restricted claims are enforced, not just remembered.** `brief.json`'s `claims.never` list is
   checked by `compose.mjs` before anything renders — it's a hard gate (exit 1), not a comment. Fill
   it from the product's own "what we don't claim" doc if one exists; otherwise default to: not
   "autonomous", not "100% accurate" / "zero errors", not "replaces a human", not letting "AI-powered"
   carry the whole pitch.
5. **Quality gate before rendering.** Always run `npx hyperframes check` on the composed output and
   fix every `error` (warnings about sub-composition structure are fine to leave — see below) before
   rendering. Verify audio with measurement (`analyze.py`), not by claiming to have listened to it.
6. **Be honest about what you actually tested.** If you compose a video but don't render/mux it, say
   that plainly. If you generate placeholder or silent audio to validate the pipeline, say that too —
   don't imply a finished, narrated video exists when it doesn't.

## Workflow

### 1. Think the real user flow (before writing anything)

Read the actual feature: the code, a running instance, or a spec. Walk it step by step the way a
user actually would. Write down 3–6 steps — screen by screen, not an imagined highlight reel. This
becomes `brief.json`'s `flow` array. See `references/brief-schema.md` for the full contract and
field-by-field rules.

Also gather, in this pass:
- The product's brand (accent color, ink, paper/background, font, logo file) — from a real brand
  doc or the live product, never guessed.
- What NOT to claim — from the product's own positioning docs if they exist.
- One message: the single thing this video should land. Not three things. One.

### 2. Write `brief.json`

Follow `references/brief-schema.md` exactly. Pick `aspect` (16:9 landscape / 9:16 vertical / 1:1
square) based on where this will run, and `durationTarget` (25–45s is the sweet spot for a feature
promo). Pick a `theme` — this is what gives different videos genuinely different looks, not just
different words on the same template:

| theme | feel | mascot | best for |
|---|---|---|---|
| `ledger-clean` | light, paper, straight lines, monospace numerals | no | finance/ops/B2B, trust-first products |
| `cinematic-dark` | dark, glass cards, accent glow | no | AI/platform/dev-tool products, premium feel |
| `mascot-playful` | bright, rounded, pill shapes, character | yes | consumer/SMB-friendly, warm brands |

Don't default to the same theme every time — pick the one that matches the product's actual brand
personality, and vary it run to run when the brief doesn't force a specific brand palette.

`mascot-playful` supports two distinct original character designs via `brand.character`: `"default"`
(antenna, no gender markers) or `"bow"` (bow + eyelashes, `brand.ribbon` sets its color). Pick a
different `voiceId` to go with a different character — see `references/brief-schema.md` for
`voice.pronounce`, which fixes TTS mispronouncing a brand name without touching on-screen text.

### 3. Compose

```bash
node scripts/compose.mjs path/to/brief.json path/to/output-dir
```

Writes `output-dir/index.html` (the HyperFrames composition), `output-dir/timing.json` (the scene
beat-grid every audio script reads — never hand-edit timings elsewhere), and copies `brief.json` +
`assets/gsap.min.js` into the output dir. **This is the step that enforces rule 4** — it exits
non-zero and refuses to write anything if a restricted claim is present.

### 4. Check before rendering

```bash
cd path/to/output-dir
npx hyperframes@0.8.58 check
```

Fix every `error`. `nested_structure_needs_subcomposition` / `timeline_track_too_dense` warnings are
expected (this generator intentionally keeps one scene per file for simplicity) and can be ignored.
`audio_src_not_found` is expected until step 5 has run — that's the correct order, not a bug.

### 5. Generate audio (all original, no exceptions)

Needs `ELEVENLABS_API_KEY` in a `.env` near the project (or exported) for voice + SFX; music and
mixing need no external API (synthesized/processed locally). Needs Python 3.11+ (`numpy`, `scipy`)
and `ffmpeg`/`ffprobe` on PATH.

```bash
cd path/to/output-dir
python ../../scripts/audio/gen_sfx.py --dir .     # small SFX palette + sonic logo, cached after first run
python ../../scripts/audio/gen_voice.py --dir .   # one voice line per scene, auto-placed from timing.json
python ../../scripts/audio/music.py --dir .       # original synth score, length/sections from timing.json
python ../../scripts/audio/mix.py --dir .         # duck, master to -14 LUFS/-1.5 dBTP, exact length
python ../../scripts/audio/analyze.py --dir .     # measured QA — read this, don't skip it
```

Check `analyze.py`'s "worst margin" line is above 6 dB (voice audible over music). If not, remix
with a louder voice bed: `MUSIC_REL_DB=-22 python ../../scripts/audio/mix.py --dir .`

Before treating the output as publishable, check the ElevenLabs account's plan — free-plan audio is
non-commercial and needs an "elevenlabs.io" credit; say this explicitly if you can't verify the plan.

### 6. Render and mux

```bash
cd path/to/output-dir
npx hyperframes@0.8.58 render -o renders/picture.mp4 -f 30 -q looks -w 1
ffmpeg -i renders/picture.mp4 -i final/audio_final.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k renders/final.mp4
```

Use `-w 1` (single worker) if render fails with a low-disk-capture error — it streams instead of
buffering to disk.

### 7. Hand back

State plainly: what was grounded vs. demo data, which theme and why, whether audio was generated or
is still a placeholder, whether `hyperframes check` passed clean, and whether render+mux actually
ran. Don't claim a finished video exists if only the composition step ran.

## Files in this skill

```
SKILL.md                    <- this file
references/
  brief-schema.md            <- the brief.json contract, field by field
  no-copyrighted-audio.md    <- why, and what to do when someone hands you a reference track
scripts/
  compose.mjs                <- the generator: brief.json + theme -> index.html + timing.json
  icons.mjs                  <- generic outline icon set (shared across themes)
  mascot.mjs                 <- original SVG mascot, brand-color-parameterized
  shared-assets/gsap.min.js  <- GSAP, downloaded on first compose (GreenSock licence) and cached here
  audio/
    el.py                    <- shared ElevenLabs helper (reads key from .env, never logs it)
    gen_sfx.py                <- small SFX palette + sonic logo
    gen_voice.py               <- one voice line per scene, placement from timing.json
    music.py                   <- original synth score, arrangement driven by timing.json
    mix.py                     <- duck + master to broadcast loudness
    analyze.py                  <- measured QA (loudness, voice-vs-music margin, tail fade)
themes/
  ledger-clean.mjs, cinematic-dark.mjs, mascot-playful.mjs
examples/
  bank-import/brief.json       <- ledger-clean, 16:9   (compose it to get out/)
  smart-nudges/brief.json      <- cinematic-dark, 9:16 (compose it to get out/)
```

## Known limitations (upgrade paths, not blockers)

- **Fonts**: themes use `var(--font), system-ui, sans-serif` with no bundled webfont files — a
  project's real brand font won't render unless you add `@font-face` rules + font files to the
  theme yourself. Upgrade when a project's exact typeface matters.
- **Music key**: `music.py` always composes in a generic minor-key progression regardless of
  `brief.music.key`. Upgrade: transpose the `CH` chord table by the requested root.
- **Two themes have no mascot** by design (`ledger-clean`, `cinematic-dark`) — this is deliberate
  variety, not a gap.
- The example briefs are compose-ready but ship **without** rendered output or audio (no API calls are
  spent on a demo nobody asked for) — run steps 3–6 yourself to get a finished file.
