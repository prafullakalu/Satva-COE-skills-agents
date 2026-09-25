"""Generate every voice segment separately (Brian, eleven_v3), trim silence, and compute exact placement on the video timeline.
Segments carry startAt (word begins here) or endAt (last word ends here) so key words land on visual events."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import el

BASE = os.path.join(os.path.dirname(__file__), "..")
RAW, TRIM = os.path.join(BASE, "03_voice", "raw"), os.path.join(BASE, "03_voice", "trimmed")
os.makedirs(RAW, exist_ok=True); os.makedirs(TRIM, exist_ok=True)
VOICE_ID, VOICE_NAME = "nPczCjzI2devNBz1zQrb", "Brian"

# id, spoken text (clean, no tags), placement, the visual event it is cued to
SEGS = [
    ("V01", "Your books aren't just being recorded anymore.", {"startAt": 0.55}, "icon wall builds"),
    ("V02", "Meet Satva. It's working on them.", {"startAt": 4.45}, "text: Satva is your own trusted, smart bookkeeping agent (4.4s)"),
    ("V03", "One agent. For everything.", {"startAt": 6.80}, "text: One agent for everything (6.48s)"),
    ("A01", "It spots what's off.", {"startAt": 10.90}, "A: Tania's Nursery bubble (11.18s)"),
    ("A02", "And before it changes anything... it asks.", {"endAt": 15.75}, "A: approval card 13.27s, Allow tap 15.36s"),
    ("A03", "Then it checks its own work.", {"startAt": 16.35}, "A: Posted and verified (15.67s), CSV/OFX/QIF line 16.9s"),
    ("B01", "Then it hits something that doesn't add up.", {"endAt": 22.85}, "B: $900 card 21.6s; silence before the flag"),
    ("B02", "And it doesn't guess.", {"startAt": 23.75}, "B: flag stamp 23.2s, bubble 23.7s"),
    ("B03", "It flags it. And waits for you.", {"startAt": 26.00}, "B: reply chips 25.8s, Left flagged 27.4s"),
    ("C01", "It knows who owes you.", {"startAt": 31.90}, "C: aging card 32.06s"),
    ("C02", "And who's already late.", {"startAt": 34.20}, "C: bubble 34.15s"),
    ("C03", "You decide who to chase.", {"startAt": 36.80}, "C: read-only note 36.76s"),
    ("D01", "It finds what you forgot.", {"startAt": 42.60}, "D: credits card 42.5s"),
    ("D02", "Six thousand three hundred dollars... sitting unused.", {"startAt": 44.65}, "D: bubble 44.6s, total 45.6s"),
    ("E01", "It turns the numbers into answers.", {"startAt": 53.05}, "E: P&L card 52.9s"),
    ("E02", "Like the nearly three thousand dollars sitting in Miscellaneous.", {"startAt": 55.55}, "E: Miscellaneous bubble 55.0s"),
    ("F01", "Every change needs your yes.", {"endAt": 64.80}, "F: approval card 62.86s, Allow tap 64.9s"),
    ("F02", "Read it.", {"startAt": 65.70}, "F: audit check 1 (65.7s)"),
    ("F03", "Change it.", {"startAt": 66.50}, "F: audit check 2 (66.5s)"),
    ("F04", "Check it.", {"startAt": 67.30}, "F: audit check 3 (67.3s)"),
    ("F05", "Log it.", {"startAt": 68.10}, "F: audit check 4 (68.1s)"),
    ("F06", "Nothing happens without you.", {"startAt": 68.95}, "F: line 68.9s"),
    ("G01", "It works where your books already live.", {"startAt": 71.75}, "G: title 71.26s, chips from 72.26s"),
    ("G02", "Every system. One agent.", {"startAt": 75.00}, "G: chips complete 75.9s"),
    ("Z01", "Satva Ledger. One agent for everything.", {"startAt": 79.28}, "End card: logo 78.6s, Satva Ledger 79.0s"),
]


def trim(x, thr_db=-42.0, pre=0.02, post=0.06):
    a = np.abs(x)
    thr = 10 ** (thr_db / 20)
    idx = np.where(a > thr)[0]
    if len(idx) == 0:
        return x
    s = max(0, idx[0] - int(pre * el.SR)); e = min(len(x), idx[-1] + int(post * el.SR))
    return x[s:e]


import subprocess
rows = []
for sid, text, place, cue in SEGS:
    raw = os.path.join(RAW, f"{sid}.mp3")
    wav = os.path.join(TRIM, f"{sid}.wav")
    if os.path.exists(wav) and os.path.getsize(wav) > 1000:  # reuse the take; only placement changes
        x = el.load(wav, mono=True)
    else:
        code, err = el.tts(VOICE_ID, text, raw)
        if code != 200:
            code, err = el.tts(VOICE_ID, text, raw)  # one retry
        if code != 200:
            print(f"{sid} FAILED {code} {err}"); sys.exit(1)
        x = trim(el.load(raw, mono=True))
        subprocess.run([el.FFMPEG, "-v", "error", "-y", "-f", "f32le", "-ar", str(el.SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s24le", wav],
                       input=x.astype(np.float32).tobytes(), check=True)
    dur = len(x) / el.SR
    start = place["startAt"] if "startAt" in place else place["endAt"] - dur
    rows.append({"id": sid, "text": text, "start": round(start, 3), "end": round(start + dur, 3), "dur": round(dur, 3), "cue": cue,
                 "file": f"03_voice/trimmed/{sid}.wav"})
    print(f"{sid} {start:6.2f} -> {start + dur:6.2f}  ({dur:4.2f}s)  {text}")

# overlap / spacing check
rows.sort(key=lambda r: r["start"])
issues = [(a["id"], b["id"], round(a["end"] - b["start"], 2)) for a, b in zip(rows, rows[1:]) if a["end"] > b["start"] - 0.10]
print("\nvoice:", VOICE_NAME, VOICE_ID, "eleven_v3 | segments:", len(rows), "| total speech %.1fs" % sum(r["dur"] for r in rows))
print("overlap/too-tight pairs (id,id,overlap_s):", issues or "none")
json.dump({"voice": VOICE_NAME, "voice_id": VOICE_ID, "model": "eleven_v3", "segments": rows}, open(os.path.join(BASE, "03_voice", "voice_segments.json"), "w"), indent=1)
