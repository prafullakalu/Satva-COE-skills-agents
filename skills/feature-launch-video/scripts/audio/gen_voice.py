"""Generate one voice line per scene (intro / each flow step / end card), trimmed and placed against
timing.json — no hardcoded script, no hand-tuned sync. Run from the composed project's output dir
(the folder that has brief.json, timing.json, and index.html), or pass --dir.
"""
import argparse, json, os, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import el

ap = argparse.ArgumentParser()
ap.add_argument("--dir", default=".")
args = ap.parse_args()
D = os.path.abspath(args.dir)
brief = json.load(open(os.path.join(D, "brief.json")))
timing = json.load(open(os.path.join(D, "timing.json")))

RAW, TRIM = os.path.join(D, "audio", "voice_raw"), os.path.join(D, "audio", "voice_trimmed")
os.makedirs(RAW, exist_ok=True); os.makedirs(TRIM, exist_ok=True)
VOICE_ID = (brief.get("voice") or {}).get("voiceId", "nPczCjzI2devNBz1zQrb")
PRONOUNCE = (brief.get("voice") or {}).get("pronounce", {})  # {"Satva": "SAHT-vah"} — screen text stays as-is

# Optional multi-character cast: brief.characters = {id: {voiceId, ...}}, brief.flow[].character = id.
# Mirrors compose.mjs's own introCharId/endCharId choice (first character opens, whoever's in the
# last flow step closes) so the voice cast always matches who's actually on screen.
CHARACTERS = brief.get("characters") or {}
CHAR_IDS = list(CHARACTERS.keys())
FLOW = brief.get("flow", [])
INTRO_CHAR = CHAR_IDS[0] if CHAR_IDS else None
END_CHAR = FLOW[-1].get("character") if FLOW and FLOW[-1].get("character") in CHARACTERS else INTRO_CHAR


def voice_for(char_id):
    return CHARACTERS.get(char_id, {}).get("voiceId", VOICE_ID)


def speak(text):
    """Swap in phonetic respellings for TTS only — never changes what's shown on screen."""
    import re
    for word, phon in PRONOUNCE.items():
        text = re.sub(rf"\b{re.escape(word)}\b", phon, text)
    return text

# one segment per scene: (id, text, startAt, voiceId) — startAt is a small, fixed offset into the
# scene so the line begins right as the visual appears, matching compose.mjs's own animation-in timing.
SEGS = [("V-intro", brief["message"], timing["intro"]["start"] + 0.35, voice_for(INTRO_CHAR))]
for sc in timing["scenes"]:
    SEGS.append((f"V-{sc['id']}", sc["line"], sc["start"] + 0.5, voice_for(sc.get("character"))))
# voice only the tagline, never the CTA — a URL or "sign up at ..." reads badly aloud and
# is already shown on screen (compose.mjs's e3 element); this also keeps the end line short
# enough to fit inside endDur instead of overrunning the video's total duration.
end_line = brief.get("endCard", {}).get("tagline")
if end_line:
    SEGS.append(("V-end", end_line, timing["end"]["start"] + 0.6, voice_for(END_CHAR)))


def trim(x, thr_db=-42.0, pre=0.02, post=0.06):
    a = np.abs(x)
    thr = 10 ** (thr_db / 20)
    idx = np.where(a > thr)[0]
    if len(idx) == 0:
        return x
    s = max(0, idx[0] - int(pre * el.SR)); e = min(len(x), idx[-1] + int(post * el.SR))
    return x[s:e]


rows = []
for sid, text, start_at, voice_id in SEGS:
    raw = os.path.join(RAW, f"{sid}.mp3")
    wav = os.path.join(TRIM, f"{sid}.wav")
    if os.path.exists(wav) and os.path.getsize(wav) > 1000:  # reuse the take; only placement recomputes
        x = el.load(wav, mono=True)
    else:
        code, err = el.tts(voice_id, speak(text), raw)
        if code != 200:
            code, err = el.tts(voice_id, speak(text), raw)  # one retry
        if code != 200:
            print(f"{sid} FAILED {code} {err}"); sys.exit(1)
        x = trim(el.load(raw, mono=True))
        subprocess.run([el.FFMPEG, "-v", "error", "-y", "-f", "f32le", "-ar", str(el.SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s24le", wav],
                       input=x.astype(np.float32).tobytes(), check=True)
    dur = len(x) / el.SR
    rows.append({"id": sid, "text": text, "start": round(start_at, 3), "end": round(start_at + dur, 3), "dur": round(dur, 3),
                 "voice_id": voice_id, "file": os.path.relpath(wav, D).replace("\\", "/")})
    print(f"{sid:10s} {start_at:7.2f} -> {start_at + dur:7.2f}  ({dur:4.2f}s)  [{voice_id}]  {text}")

rows.sort(key=lambda r: r["start"])
issues = [(a["id"], b["id"], round(a["end"] - b["start"], 2)) for a, b in zip(rows, rows[1:]) if a["end"] > b["start"] - 0.10]
print(f"\nvoices: {sorted(set(r['voice_id'] for r in rows))} | segments {len(rows)} | total speech {sum(r['dur'] for r in rows):.1f}s")
print("overlap/too-tight pairs (id,id,overlap_s):", issues or "none")
overrun = [r for r in rows if r["end"] > timing["durationSec"]]
if overrun:
    print(f"WARN: {len(overrun)} segment(s) run past the video's total duration ({timing['durationSec']}s) and will be cut off in mix.py: "
          + ", ".join(f"{r['id']} ends {r['end']}s" for r in overrun) + " — shorten the line in brief.json and rerun.")
os.makedirs(os.path.join(D, "audio"), exist_ok=True)
json.dump({"default_voice_id": VOICE_ID, "model": "eleven_v3", "segments": rows}, open(os.path.join(D, "audio", "voice_segments.json"), "w"), indent=1)
