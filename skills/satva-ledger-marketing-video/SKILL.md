---
name: satva-ledger-marketing-video
description: Reference pipeline to FORK for a longer "sizzle" / hero marketing video — the Satva Ledger (AI accounting agent) 82-second promo. A generator script builds the HyperFrames composition from data, an original SVG mascot animates it, and a Python audio pipeline makes the ElevenLabs voice + SFX, an original synthesised score, the ducked mix and measured QA. Use when asked to rebuild, re-render or adapt the Satva Ledger / accounting-agent marketing video, or to make a multi-chapter promo with a mascot and beat-synced sound design. For a quick launch video of ANY single feature, use feature-launch-video instead.
---

# Satva Ledger marketing video — the reference pipeline

This is the **real, hand-built pipeline** behind the Satva Ledger promo, kept readable so the team can
rerun it or fork it for the next product. It is **not** a portable template: the chapters, the 25 voice
lines and the 82.567 s length are written into the scripts on purpose.

## Which video skill do I use?

| | `feature-launch-video` | **`satva-ledger-marketing-video`** (this) |
|---|---|---|
| Length / shape | 25–45 s, one feature | ~80 s, intro → 6 chapters → all-in-one → end card |
| Input | a `brief.json` — no code edits | you edit the generator and the voice script |
| Sound | generic, timing-driven | hand-cued so key words land on visual beats |
| Portable | yes — any product | no — a worked reference to fork |

If you only need "a launch video for feature X", stop and use `feature-launch-video`.

## What is in the folder

```
pipeline/
  video-build/
    build-sizzle.mjs        generates satva-sizzle/index.html from data (chapters, timings, cues)
    sizzle-mascot.mjs       the original SVG mascot + mood/bob/blink/wave/hop helpers (brand palette only)
    satva-sizzle/           composition scaffold: fonts (OFL), official Satva logo, hyperframes config
  audio-pipeline/
    el.py                   ElevenLabs helper (key from env or .env, never logged) + ffmpeg decode
    gen_voice.py            25 voice lines, silence-trimmed, placed by startAt/endAt on the visual beats
    gen_sfx.py              10 custom sound effects (+7 more, regenerated if no earlier copy exists)
    music.py                ORIGINAL instrumental score synthesised in code (115 BPM) + a sonic logo
    mix.py                  three stems, music ducked under voice, mastered to -14 LUFS / -1.5 dBTP
    analyze.py              measured QA (loudness per section, voice-vs-music margin, silences)
    test_voices.py          voice auditions
docs/
  marketing-copy.md         the approved claims and the explicit "what we do not claim" list
  VIDEO-SCRIPT-V3.md        the beat sheet, hook and positioning notes
```

Not included on purpose: the rendered MP4s and the audio. The voice and sound effects were generated on a
**free ElevenLabs plan, so that audio is non-commercial** and must not be redistributed under this repo's
licence. Regenerate it with your own (paid) key.

## Set up a workspace (do not run from `~/.claude/skills`)

The scripts write their output folders (`03_voice/`, `04_music/`, …) **next to themselves**, so work on a copy:

```bash
cp -r ~/.claude/skills/satva-ledger-marketing-video/pipeline my-video && cd my-video
```

You need Node 18+, Python 3.11+ with `numpy scipy`, and `ffmpeg` on `PATH` (or set `FFMPEG_PATH`).
Voice and SFX need `ELEVENLABS_API_KEY` (export it, or a git-ignored `.env` in the working folder).
`music.py` needs no key.

## Steps

### 1. Build the picture composition

```bash
cd video-build && node build-sizzle.mjs                # writes satva-sizzle/index.html (about 80 KB)
curl -L https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js -o satva-sizzle/assets/gsap.min.js
cd satva-sizzle && npx hyperframes@0.8.58 check         # must show 0 errors
```

GSAP carries GreenSock's own licence, so it is downloaded rather than shipped. The checker will report
`audio_src_not_found` for the in-composition sound-effect clips — expected: the finished soundtrack comes from
step 3 and is muxed on afterwards, not from those clips.

### 2. Render the picture

```bash
npx hyperframes@0.8.58 render -o renders/picture.mp4 -f 30 -q looks -w 2
```

### 3. Make the audio (order matters)

```bash
cd ../../audio-pipeline
python gen_voice.py     # ElevenLabs "Brian", eleven_v3 → ../03_voice/
python gen_sfx.py       # → ../05_sfx/
python music.py         # original score → ../04_music/  (no API)
python mix.py           # duck + master → ../08_final/
python analyze.py       # read it: voice must clear the music by a healthy margin
```

### 4. Mux

```bash
cd ..                                              # back to the workspace root (my-video/)
ffmpeg -i video-build/satva-sizzle/renders/picture.mp4 -i 08_final/satvaLedger_final_audio.wav \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k final.mp4
```

## Forking it for the next video

1. **Facts first.** Replace every figure in `build-sizzle.mjs` with real, sourced data. The originals are
   *QuickBooks Online sandbox demo data* and are labelled as such on screen — keep an equivalent label
   whenever the data is not from a live customer.
2. **Copy** in `docs/marketing-copy.md`: write your own claims list and your own "what we do not claim".
3. **Story:** edit `chapters`, `SYS` and the scene HTML in `build-sizzle.mjs`; the beat grid is
   `0.22 + 0.522·k` seconds at 115 BPM — change `DUR` and `T()` together if the tempo changes.
4. **Voice:** edit `SEGS` in `gen_voice.py` (each line carries `startAt` or `endAt` tied to a visual event) and
   `DUR` in `mix.py` to the new length.
5. Re-run steps 1–4 and read `analyze.py`'s output before you call it finished.

## Rules that carry over

- **Never use a copyrighted reference track**, not even for timing, and never disguise one. The original
  project started from one, and it was removed; this generator no longer emits any reference-audio tag.
- **Claims are restricted** to what `docs/marketing-copy.md` allows: not "autonomous", not "zero errors",
  not "replaces accountants".
- **Logo:** official files only, on a light background, never recoloured, redrawn or stretched.
- **Systems shown:** the demo lists eight accounting systems but only some have real connectors. Confirm with
  product before publishing and drop or reword any that are not supported.
- **Licences:** ElevenLabs free-plan output is non-commercial and needs an "elevenlabs.io" credit — upgrade the
  account before any paid or public campaign.
- **Say plainly what was tested.** Do not claim a finished, narrated video exists if only the composition ran.

## Verified in this repo, and what is not

- ✅ `node build-sizzle.mjs` regenerates the original composition exactly, apart from the intended
  on-screen-label fix (checked by diff against the original build).
- ✅ `music.py` produces the 82.57 s, 48 kHz stereo original score (run with a throwaway `ffmpeg`).
- ✅ `mix.py` creates its output folders and stops only at the expected missing voice input.
- ✅ `hyperframes check` passes (0 errors) and `hyperframes render` completes all 2,477 frames; muxing the original
  final audio gives the 82.57 s video in `examples/satva-ledger-video/` (picture within 42 dB PSNR of the original).
- ⚠️ **Not run:** `gen_voice.py`, `gen_sfx.py`, `mix.py` past that point and `analyze.py` — they need an ElevenLabs key
  and credits. Treat them as the original working scripts, lightly ported (paths, `ffmpeg` lookup, missing folder
  creation), and not re-verified end to end here.
