"""Objective QA of the final mix against the checklist (I cannot listen, so every check is measured)."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import el

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SR = el.SR
fin = el.load(os.path.join(BASE, "08_final", "satvaLedger_final_audio.wav"))
vo = el.load(os.path.join(BASE, "06_stems", "voiceStem.wav"), mono=True)
mu = el.load(os.path.join(BASE, "06_stems", "musicStem.wav"), mono=True)
sf = el.load(os.path.join(BASE, "06_stems", "sfxStem.wav"), mono=True)
n = min(len(fin), len(vo)); f = fin.mean(1)[:n]
rms = lambda x: 20 * np.log10(np.sqrt(np.mean(np.square(x))) + 1e-12)
seg = lambda x, a, b: x[int(a * SR):int(b * SR)]

print("== length / silence at the end ==")
print(f"samples {len(fin)} = {len(fin) / SR:.3f}s | last 100 ms RMS {rms(seg(f, len(f) / SR - 0.1, len(f) / SR)):.1f} dB (should fade to near silence, not cut)")

print("\n== hook ==")
vs = json.load(open(os.path.join(BASE, "03_voice", "voice_segments.json")))["segments"]
print(f"first spoken word at {vs[0]['start']:.2f}s  ('{vs[0]['text']}')")

print("\n== per-section loudness (final mix, RMS dBFS) -> energy arc ==")
secs = [("intro", 0, 8.6), ("A post", 8.6, 19.0), ("B anomaly", 19.0, 29.5), ("C owed", 29.5, 39.9), ("D credits", 39.9, 50.3),
        ("E report", 50.3, 60.8), ("F approve", 60.8, 71.2), ("G systems", 71.2, 78.5), ("end/logo", 78.5, 82.5)]
for name, a, b in secs:
    print(f"  {name:10s} {a:5.1f}-{b:5.1f}s  mix {rms(seg(f, a, b)):6.1f} | music {rms(seg(mu, a, b)):6.1f} | voice {rms(seg(vo, a, b)):6.1f}")

print("\n== voice intelligibility: voice vs everything else, during each spoken segment ==")
worst = []
for s in vs:
    a, b = s["start"], s["end"]
    v = seg(vo, a, b); other = seg(mu, a, b) + seg(sf, a, b)
    worst.append((rms(v) - rms(other), s["id"]))
worst.sort()
print("  lowest voice-over-background margins (dB):", ", ".join(f"{i} {m:.1f}" for m, i in worst[:5]))
print(f"  median margin {np.median([m for m, _ in worst]):.1f} dB (want >= ~12 dB for clear speech)")

print("\n== deliberate silence before the two key moments (music dropped) ==")
for a, b, why in [(22.70, 23.15, "before the flag / stamp (23.19s)"), (64.45, 64.90, "before Allow (64.9s)")]:
    print(f"  {a:.2f}-{b:.2f}s  mix {rms(seg(f, a, b)):6.1f} dB   ({why})   vs surrounding {rms(seg(f, a - 2, a - 0.5)):.1f} dB")

print("\n== sfx never louder than the voice ==")
sv = []
for e in json.load(open(os.path.join(BASE, "07_mix", "mix_report.json")))["sfx_events"]:
    a = e["t"]; sv.append((rms(seg(sf, a, a + 0.6)) , e["sfx"], a))
sv.sort(reverse=True)
print("  loudest sfx windows (dBFS):", ", ".join(f"{n}@{a:.1f}s {v:.1f}" for v, n, a in sv[:4]), "| voice speech RMS", round(rms(vo[np.abs(vo) > 0.02]), 1))
