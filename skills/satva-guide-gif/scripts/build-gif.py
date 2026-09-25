"""Assemble a demo GIF + a 2x3 storyboard contact sheet from cursor-demo frames.

    python build-gif.py <frames-dir> <out.gif> [storyboard.png]

Size ladder, in order, stopping at the first result under HARD_LIMIT_MB:
  900px @70ms 256c -> 900px @70ms 192c -> 800px @70ms 256c -> 800px every 2nd
  frame @140ms (same wall-clock length, half the data). Flat UI art loses nothing
  visible at 192 colours, and full framerate matters more than palette depth for
  a demo whose whole point is a smoothly gliding cursor.
"""
import glob
import os
import sys
from PIL import Image, ImageOps

SRC = sys.argv[1]
GIF = sys.argv[2]
STRIP = sys.argv[3] if len(sys.argv) > 3 else None

HARD_LIMIT_MB = 12.0
MB = 1024 * 1024
LADDER = ((900, 1, 70, 256), (900, 1, 70, 192), (800, 1, 70, 256), (800, 2, 140, 256))
CELL_W, GAP, COLS, STILLS = 780, 18, 2, 6

FRAMES = sorted(glob.glob(os.path.join(SRC, "f*.png")))
assert FRAMES, "no frames in " + SRC


def scaled(path, width):
    im = Image.open(path).convert("RGB")
    return im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)


def build_gif():
    for width, step, duration, colors in LADDER:
        frames = [scaled(f, width).quantize(colors=colors, method=Image.MEDIANCUT)
                  for f in FRAMES[::step]]
        frames[0].save(GIF, save_all=True, append_images=frames[1:],
                       duration=duration, loop=0, optimize=True)
        mb = os.path.getsize(GIF) / MB
        print(f"  {width}px step={step} {duration}ms {colors}c -> {mb:.2f} MB")
        if mb <= HARD_LIMIT_MB:
            return mb
    return mb  # best effort; verify() will fail loudly


def signature(path):
    """Tiny grayscale fingerprint for cheap frame-difference comparison."""
    return list(Image.open(path).convert("L").resize((32, 32), Image.LANCZOS).tobytes())


def dist(a, b):
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)


def pick_distinct(sigs, n=STILLS, window=14):
    """Evenly spaced anchors, each nudged within +/-window to the most distinct frame."""
    anchors = [round(i * (len(sigs) - 1) / (n - 1)) for i in range(n)]
    picked = []
    for a in anchors:
        lo, hi = max(0, a - window), min(len(sigs), a + window + 1)
        cands = [i for i in range(lo, hi) if i not in picked] or [a]
        picked.append(a if not picked else max(
            cands, key=lambda i: min(dist(sigs[i], sigs[p]) for p in picked)))
    return sorted(picked)


def build_strip(idxs):
    """2 x 3 grid — a vertical strip is 4x taller than an A4 column can hold."""
    ims = [ImageOps.expand(scaled(FRAMES[i], CELL_W), border=1, fill="#111") for i in idxs]
    cw, ch = ims[0].size
    rows = (len(ims) + COLS - 1) // COLS
    sheet = Image.new("RGB",
                      (cw * COLS + GAP * (COLS - 1), ch * rows + GAP * (rows - 1)), "white")
    for k, im in enumerate(ims):
        sheet.paste(im, ((k % COLS) * (cw + GAP), (k // COLS) * (ch + GAP)))
    sheet.save(STRIP)
    return sheet.size


def verify():
    """Re-open the outputs and report what is actually on disk."""
    g = Image.open(GIF)
    count = getattr(g, "n_frames", 1)
    total = 0
    for i in range(count):
        g.seek(i)
        total += g.info.get("duration", 0)
    print(f"\nGIF   {GIF}\n      {g.size[0]}x{g.size[1]}  {count} stored frames  "
          f"{total / 1000:.1f}s  loop={g.info.get('loop')}  "
          f"{os.path.getsize(GIF) / MB:.2f} MB")
    assert os.path.getsize(GIF) / MB <= HARD_LIMIT_MB, "GIF exceeds the 12 MB limit"
    assert count > 1, "GIF is not animated"


if __name__ == "__main__":
    print(f"{len(FRAMES)} source frames")
    build_gif()
    if STRIP:
        idxs = pick_distinct([signature(f) for f in FRAMES])
        print("storyboard:", [os.path.basename(FRAMES[i]) for i in idxs],
              build_strip(idxs))
    verify()
