"""Generate the small, fixed SFX palette compose.mjs references (pop/swoosh/click) plus a sonic-logo
chime for the end card. Cached — reruns are free once generated once per project."""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import el

ap = argparse.ArgumentParser()
ap.add_argument("--dir", default=".")
args = ap.parse_args()
D = os.path.abspath(args.dir)
OUT = os.path.join(D, "assets", "sfx")
os.makedirs(OUT, exist_ok=True)

PALETTE = {
    "pop": ("soft UI pop, short and light, like a card appearing", 0.5),
    "swoosh": ("quick, clean whoosh transition, modern UI, no reverb tail", 0.6),
    "click": ("crisp UI tap/click, short, confident", 0.5),  # ElevenLabs sound-gen requires >= 0.5s
    "chime": ("short bright confirmation chime, two notes, pleasant", 1.2),
}
for name, (prompt, seconds) in PALETTE.items():
    out = os.path.join(OUT, f"{name}.mp3")
    if os.path.exists(out) and os.path.getsize(out) > 500:
        print(f"{name}: cached"); continue
    code, err = el.sfx(prompt, seconds, out)
    if code != 200:
        print(f"{name}: FAILED {code} {err}"); sys.exit(1)
    print(f"{name}: generated ({seconds}s)")
print("sfx palette ready:", ", ".join(PALETTE))
