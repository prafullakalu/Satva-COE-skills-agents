"""Generate the custom SFX set with the ElevenLabs sound-effects API; reuse the seven earlier effects."""
import os, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
import el

BASE = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(BASE, "05_sfx"); os.makedirs(OUT, exist_ok=True)
EARLIER = os.path.join(BASE, "..", "satva-sizzle", "assets", "sfx")

NEW = {  # name: (prompt, seconds) - each has a specific visual reason in the mix
    "activate": ("futuristic digital activation, soft power-up of an intelligent system, clean and subtle", 1.6),
    "anomaly": ("subtle anomaly detection alert, one soft dissonant electronic blip, restrained, not alarming", 1.0),
    "scan": ("digital scanning data processing sweep, subtle, clean, short", 1.6),
    "match": ("subtle matching verification, two clean electronic blips, satisfying", 0.9),
    "discover": ("satisfying discovery chime, bright, gently rising two notes, premium", 1.6),
    "report": ("clean report generation, soft electronic data blips resolving, modern", 1.4),
    "permission": ("subtle notification anticipation, single soft tone with light shimmer, modern UI", 1.2),
    "approve": ("clean positive confirmation click and soft chime, premium UI", 1.2),
    "tick": ("tiny precise verification tick, crisp single click, very short", 0.5),
    "logo": ("short memorable premium sonic logo, three soft ascending synth notes with warm shimmer that resolves, 3 seconds", 3.0),
}
for name, (prompt, sec) in NEW.items():
    p = os.path.join(OUT, f"{name}.mp3")
    code, err = el.sfx(prompt, sec, p)
    if code != 200:
        code, err = el.sfx(prompt, sec, p)
    print(f"{name:10s}", "OK" if code == 200 else f"FAILED {code} {err[:100]}")

# The seven effects the original release reused from an earlier run. Reused if a copy is found; otherwise
# regenerated from these prompts (written for this release - the original prompts were not recorded, so the
# results are close in purpose, not identical in sound).
EARLIER_SET = {
    "el-swoosh.mp3": ("swoosh", "soft clean UI swoosh transition, short whoosh, modern, subtle", 0.8),
    "el-coin.mp3": ("coin", "bright satisfying coin ding, short, positive reward", 0.8),
    "el-type.mp3": ("type", "soft keyboard typing burst, a few gentle key clicks, subtle", 1.2),
    "el-stamp.mp3": ("stamp", "firm rubber stamp thud, short, restrained, not loud", 0.6),
    "el-ding.mp3": ("ding", "clean single bell ding, bright, premium notification", 1.0),
    "el-boing.mp3": ("hop", "cute soft boing, small rubbery bounce, playful, short", 0.6),
    "el-sparkle.mp3": ("sparkle", "gentle magical sparkle shimmer, short, twinkling, subtle", 1.0),
}
for f, (name, prompt, sec) in EARLIER_SET.items():
    src, dst = os.path.join(EARLIER, f), os.path.join(OUT, f"{name}.mp3")
    if os.path.exists(src):
        shutil.copy(src, dst); print(f"{name:10s} reused (generated earlier)")
    else:
        code, err = el.sfx(prompt, sec, dst)
        print(f"{name:10s}", "OK (regenerated)" if code == 200 else f"FAILED {code} {err[:100]}")
