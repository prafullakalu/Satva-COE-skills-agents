import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import el

OUT = os.path.join(os.path.dirname(__file__), "..", "03_voice", "auditions")
os.makedirs(OUT, exist_ok=True)
LINE = "Your books aren't just being recorded anymore."
CANDIDATES = {  # ElevenLabs premade American male voices
    "brian": "nPczCjzI2devNBz1zQrb",
    "adam": "pNInz6obpgDQGcFmaJgB",
    "chris": "iP95p4xoKVk53GoZ742B",
    "eric": "cjVigY5qzO86Huf0OWal",
    "josh": "TxGEqnHWrfWFTfGW9XjX",
}
for name, vid in CANDIDATES.items():
    p = os.path.join(OUT, f"{name}.mp3")
    code, err = el.tts(vid, LINE, p)
    if code != 200:
        print(f"{name:6s} FAILED {code} {err[:110]}")
        continue
    x = el.load(p, mono=True)
    print(f"{name:6s} OK   {len(x)/el.SR:4.2f}s  median F0 {el.median_f0(p):5.0f} Hz")
