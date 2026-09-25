"""Original instrumental score, synthesised in numpy/scipy — no external samples, no copyrighted
reference track, so licensing is never a question. Section lengths and count come from timing.json
(the composer's own beat-grid + scene boundaries), so this fits ANY brief/duration/theme automatically.
The instrument functions below are generic DSP (kick/hat/bass/pad/pluck/bell/riser/impact) — reuse them
as-is; only the arrangement (which sections, how many bars) is driven by data.
"""
import argparse, json, os, sys
import numpy as np
from scipy import signal
from scipy.signal import fftconvolve

sys.path.insert(0, os.path.dirname(__file__))
import el

ap = argparse.ArgumentParser()
ap.add_argument("--dir", default=".")
args = ap.parse_args()
D = os.path.abspath(args.dir)
timing = json.load(open(os.path.join(D, "timing.json")))

SR = 48000
DUR = timing["durationSec"]
BEAT = timing["beatSec"]
BAR = BEAT * 4
N = int(DUR * SR)
rng = np.random.default_rng(7)

dry = np.zeros((N, 2), np.float32)   # drums + bass (no reverb)
wet = np.zeros((N, 2), np.float32)   # pads / plucks / bells (reverb bus)
gain_env = np.ones(N, np.float32)    # section dynamics


def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
def t_of(bar, beat=0.0): return BAR * bar + BEAT * beat
def add(buf, t, x, pan=0.0):
    i = int(t * SR)
    if i >= N or i < -len(x): return
    a = max(0, -i); x = x[a:]; i = max(0, i)
    j = min(N, i + len(x)); x = x[: j - i]
    if x.ndim == 2:
        buf[i:j] += x; return
    l, r = np.sqrt(0.5 * (1 - pan)), np.sqrt(0.5 * (1 + pan))
    buf[i:j, 0] += x * l; buf[i:j, 1] += x * r
def lp(x, f, order=2): return signal.sosfilt(signal.butter(order, f, "low", fs=SR, output="sos"), x)
def hp(x, f, order=2): return signal.sosfilt(signal.butter(order, f, "high", fs=SR, output="sos"), x)
def bp(x, lo, hi): return signal.sosfilt(signal.butter(2, [lo, hi], "band", fs=SR, output="sos"), x)
def tt(d): return np.arange(int(d * SR)) / SR


# ---------- instruments (generic — reuse for any project) ----------
def kick(vel=1.0):
    t = tt(0.45); f = 44 + 130 * np.exp(-t / 0.03); ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * np.exp(-t / 0.16) * 1.0 + rng.standard_normal(len(t)) * np.exp(-t / 0.004) * 0.18) * vel
def hat(open_=False, vel=0.5):
    t = tt(0.22 if open_ else 0.06); return hp(rng.standard_normal(len(t)), 7000) * np.exp(-t / (0.09 if open_ else 0.018)) * vel
def clap(vel=0.6):
    t = tt(0.3); n = bp(rng.standard_normal(len(t)), 1100, 3800)
    e = sum(np.exp(-np.clip(t - d, 0, None) / 0.035) * (t >= d) for d in (0, 0.011, 0.023)) * 0.45 + np.exp(-t / 0.12) * 0.5
    return n * e * vel
def bass(m, dur, vel=0.8):
    t = tt(dur); f = hz(m)
    x = 0.65 * signal.sawtooth(2 * np.pi * f * t) + 0.9 * np.sin(2 * np.pi * f * t)
    x = lp(x, 420) * np.minimum(1, t / 0.005) * np.minimum(1, (dur - t) / 0.04) * np.exp(-t / (dur * 1.6))
    return x * vel
def pad(notes, dur, vel=0.5, bright=1500):
    t = tt(dur); out = np.zeros((len(t), 2), np.float32)
    env = np.minimum(1, t / 0.9) * np.minimum(1, np.clip(dur - t, 0, None) / 1.2)
    for m in notes:
        for k, (det, pan) in enumerate(((-7, 0), (7, 1))):
            f = hz(m) * 2 ** (det / 1200)
            x = signal.sawtooth(2 * np.pi * f * t + rng.uniform(0, 6.28))
            out[:, pan] += lp(x, bright) * env * vel / len(notes)
    return out
def pluck(m, dur=0.32, vel=0.4, tone=3200):
    t = tt(dur); f = hz(m)
    x = 0.8 * signal.sawtooth(2 * np.pi * f * t, 0.5) + 0.35 * np.sin(2 * np.pi * 2 * f * t)
    return lp(x, tone) * np.exp(-t / 0.11) * np.minimum(1, t / 0.003) * vel
def bell(m, vel=0.35, dur=1.4):
    t = tt(dur); f = hz(m)
    x = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t / d) for r, a, d in ((1, 1.0, 0.7), (2.76, 0.45, 0.35), (5.4, 0.2, 0.18)))
    return x * vel * np.minimum(1, t / 0.002)
def riser(dur, vel=0.5):
    t = tt(dur); n = rng.standard_normal(len(t))
    ph = 2 * np.pi * np.cumsum(200 + 1400 * (t / dur) ** 2) / SR
    out = (hp(n, 900) * 0.6 + np.sin(ph) * 0.35) * (t / dur) ** 1.7 * vel
    return out * np.minimum(1, (dur - t) / 0.02)
def impact(vel=0.9):
    t = tt(1.4); f = 38 + 60 * np.exp(-t / 0.08)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.45) + lp(rng.standard_normal(len(t)), 2500) * np.exp(-t / 0.25) * 0.25) * vel


CH = {"Am": (45, (57, 60, 64)), "F": (41, (53, 57, 60)), "C": (48, (55, 60, 64)), "G": (43, (55, 59, 62)),
      "Dm": (38, (50, 53, 57)), "E": (40, (52, 56, 59)), "A": (45, (57, 61, 64)), "Em": (40, (52, 55, 59))}
def arp_notes(name, up=12): return [n + up for n in CH[name][1]]
LOOP = ["Am", "F", "C", "G", "Dm", "Em"]  # generic minor-key progression; cycles for however many bars a section needs


def drums(bar, mode):
    for b in range(4):
        t = t_of(bar, b)
        if mode == "heart" and b == 0: add(dry, t, kick(0.45))
        if mode == "half" and b in (0, 2): add(dry, t, kick(0.85))
        if mode in ("four", "four_clap"): add(dry, t, kick(0.9 if b else 1.0))
        if mode in ("four_clap", "half") and b in (1, 3): add(dry, t, clap(0.5))
def hats(bar, mode):
    if mode == "8th":
        for h in range(8): add(dry, t_of(bar, h * 0.5), hat(open_=(h % 2 == 1) and h == 7, vel=0.35 + 0.1 * (h % 2)), pan=0.2)
    if mode == "tick":
        for h in (1.5, 2.5, 3.5): add(dry, t_of(bar, h), hat(vel=0.22), pan=0.3)
def bassline(bar, chord, mode):
    root = CH[chord][0]
    if mode == "pulse":
        for h in range(8): add(dry, t_of(bar, h * 0.5), bass(root + (12 if h in (3, 7) else 0), BEAT * 0.45, 0.6))
    if mode == "sub": add(dry, t_of(bar), bass(root - 12 if root > 36 else root, BAR * 0.98, 0.5))
def arps(bar, chord, mode, up=12):
    n = arp_notes(chord, up)
    if mode == "8th":
        for h in range(8): add(wet, t_of(bar, h * 0.5), pluck(n[h % 3] + (12 if h % 4 == 3 else 0), vel=0.3), pan=(-0.4 if h % 2 else 0.4))
    if mode == "sparse":
        for h in (0, 2.5): add(wet, t_of(bar, h), pluck(n[int(h) % 3] + 12, 0.5, 0.26), pan=0.3)
    if mode == "bell":
        for h in (0, 1.5, 3): add(wet, t_of(bar, h), bell(n[int(h * 2) % 3] + 12, 0.3), pan=(-0.3 if h else 0.3))
def pad_bar(bar, chord, vel, bright=1500):
    add(wet, t_of(bar), pad(list(CH[chord][1]), BAR + 0.8, vel, bright))


# ---------- arrangement: sections from timing.json, feels cycle by scene index ----------
def bars_for(span):
    return max(2, round((span["end"] - span["start"]) / BAR))

bar_cursor = 0
def emit(span, feel, is_intro=False, is_end=False):
    global bar_cursor
    n_bars = bars_for(span)
    for i in range(n_bars):
        bar = bar_cursor + i
        chord = LOOP[bar % len(LOOP)]
        last = i == n_bars - 1
        if is_intro:
            pad_bar(bar, chord, 0.34 + 0.05 * i, 900 + 250 * i); bassline(bar, chord, "sub")
            if i >= 1: arps(bar, chord, "sparse")
            if i >= 2: hats(bar, "tick")
            if last: add(dry, t_of(bar, 0), riser(BAR - 0.02, 0.55))
        elif feel == "groove":
            pad_bar(bar, chord, 0.34, 1700); bassline(bar, chord, "pulse"); drums(bar, "four_clap"); hats(bar, "8th"); arps(bar, chord, "8th")
        elif feel == "tension":
            pad_bar(bar, chord, 0.42, 900); bassline(bar, chord, "sub"); drums(bar, "heart"); hats(bar, "tick")
            if i in (1, 3): arps(bar, chord, "sparse")
        elif feel == "bright":
            pad_bar(bar, chord, 0.36, 2400); bassline(bar, chord, "pulse"); drums(bar, "half"); hats(bar, "8th"); arps(bar, chord, "bell")
        if is_end and last:
            add(dry, t_of(bar, 0), impact(0.85)); add(dry, t_of(bar, 0), kick(1.0))
            add(wet, t_of(bar, 0), pad([57, 61, 64, 69, 73], BAR * 2, 0.55, 3200))
            add(dry, t_of(bar, 0), bass(33, 3.6, 0.8))
            for j, m in enumerate((81, 85, 88, 93)):
                add(wet, t_of(bar, 0) + 0.08 + j * 0.13, bell(m, 0.32, 2.0), pan=(-0.4 + 0.27 * j))
    bar_cursor += n_bars
    return t_of(bar_cursor)


bounds = {}
b0 = emit(timing["intro"], None, is_intro=True); bounds["intro"] = (0, b0)
FEELS = ["groove", "tension", "bright"]
for i, sc in enumerate(timing["scenes"]):
    feel = FEELS[i % len(FEELS)]
    b1 = emit(sc, feel); bounds[sc["id"]] = (b0, b1); b0 = b1
bEnd = emit(timing["end"], "groove", is_end=True); bounds["end"] = (b0, bEnd)

# ---------- reverb + master ----------
ir_t = tt(1.8)
ir = (rng.standard_normal((len(ir_t), 2)) * np.exp(-ir_t / 0.55)[:, None]).astype(np.float32); ir[:int(0.012 * SR)] *= 0.2
tail = np.stack([fftconvolve(wet[:, c], ir[:, c])[:N] for c in (0, 1)], axis=1).astype(np.float32)
mix = dry + wet * 0.75 + tail * 0.11 * np.float32(len(ir_t) ** -0.5 * 60)

def seg_gain(a, b, g0, g1=None):
    i, j = int(a * SR), min(N, int(b * SR)); g1 = g0 if g1 is None else g1
    if j > i: gain_env[i:j] = np.linspace(g0, g1, j - i)
seg_gain(*bounds["intro"], 0.55, 0.8)
for i, sc in enumerate(timing["scenes"]):
    g = {"groove": 0.85, "tension": 0.6, "bright": 0.85}[FEELS[i % len(FEELS)]]
    seg_gain(*bounds[sc["id"]], g)
seg_gain(*bounds["end"], 0.9, 0.95)
mix = mix * gain_env[:, None]
mix[:int(0.05 * SR)] *= np.linspace(0, 1, int(0.05 * SR))[:, None]
mix[-int(1.4 * SR):] *= np.linspace(1, 0, int(1.4 * SR))[:, None]
peak = float(np.max(np.abs(mix))) or 1.0
mix = (mix / peak * 0.708).astype(np.float32)

logo = np.zeros((int(3.0 * SR), 2), np.float32)
for j, m in enumerate((69, 73, 76, 81)):
    t = tt(2.4); f = hz(m)
    x = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t)) * np.exp(-t / 0.9) * np.minimum(1, t / 0.004) * 0.4
    i0 = int((0.10 * j) * SR); logo[i0:i0 + len(x), 0] += x[: len(logo) - i0] * (0.8 - 0.1 * j); logo[i0:i0 + len(x), 1] += x[: len(logo) - i0] * (0.5 + 0.1 * j)
logo_peak = float(np.max(np.abs(logo))) or 1.0
logo = (logo / logo_peak * 0.7).astype(np.float32)

import subprocess
def write(path, a):
    subprocess.run([el.FFMPEG, "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s24le", path],
                   input=a.astype(np.float32).tobytes(), check=True)
os.makedirs(os.path.join(D, "assets"), exist_ok=True)
os.makedirs(os.path.join(D, "assets", "sfx"), exist_ok=True)
write(os.path.join(D, "assets", "music.wav"), mix)
write(os.path.join(D, "assets", "sfx", "logo.wav"), logo)
print(f"music done: {N / SR:.1f}s, {bar_cursor} bars, peak -3 dBFS — original synth, no external samples")
