"""Objective QA on the final mix — the agent can't listen, so every claim is measured, not asserted.
Checks: overall loudness/peak vs target, per-scene voice-vs-background margin, tail fade present."""
import json, os, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import el

D = os.path.abspath(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else os.path.abspath(".")
timing = json.load(open(os.path.join(D, "timing.json")))
P = lambda *a: os.path.join(D, *a)

fin = P("final", "audio_final.wav")
m = subprocess.run([el.FFMPEG, "-i", fin, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                    capture_output=True, text=True).stderr
j = json.loads(m[m.rindex("{"): m.rindex("}") + 1])
print(f"measured: I={j['input_i']} LUFS  TP={j['input_tp']} dBTP  LRA={j['input_lra']}  (target -14 / -1.5 / 11)")

voice = el.load(P("audio", "voiceStem.wav"), mono=True)
music = el.load(P("audio", "musicStem.wav"), mono=True)
rms_db = lambda x: 20 * np.log10(np.sqrt(np.mean(np.asarray(x) ** 2)) + 1e-12)

bounds = [("intro", timing["intro"])] + [(s["id"], s) for s in timing["scenes"]] + [("end", timing["end"])]
print("\nper-scene voice-vs-music margin (want voice louder, margin > 6 dB while speaking):")
worst = 99
for name, span in bounds:
    i, k = int(span["start"] * el.SR), int(span["end"] * el.SR)
    vseg, mseg = voice[i:k], music[i:k]
    if np.sqrt(np.mean(vseg ** 2)) < 0.003:  # no speech in this window
        continue
    margin = rms_db(vseg) - rms_db(mseg)
    worst = min(worst, margin)
    print(f"  {name:10s} voice {rms_db(vseg):6.1f} dB  music {rms_db(mseg):6.1f} dB  margin {margin:5.1f} dB")
print(f"worst margin: {worst:.1f} dB" + ("  [OK]" if worst > 6 else "  [WARN: raise MUSIC_REL_DB or lower DUCK_DEPTH_DB and remix]"))

full = el.load(fin, mono=True)
tail = full[-int(1.0 * el.SR):]
print(f"\ntail (last 1.0s) peak: {20*np.log10(np.max(np.abs(tail))+1e-12):.1f} dBFS — should fade toward silence")
