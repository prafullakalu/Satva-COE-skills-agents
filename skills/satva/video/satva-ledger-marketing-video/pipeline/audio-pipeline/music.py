"""Original instrumental score, synthesised in numpy/scipy (ElevenLabs Music needs a paid plan).
Locked to the video's beat grid: 115 BPM, beat = 0.522 s, first beat at 0.22 s, so chapter cuts land on downbeats.
Key: A minor, resolving to A major at the logo. Sections follow the story: mysterious intro, groove, tension, discovery,
confident report, anticipation -> release at the Allow tap, build, resolution."""
import os, sys
import numpy as np
from scipy import signal
from scipy.signal import fftconvolve

sys.path.insert(0, os.path.dirname(__file__))
import el

SR = 48000
DUR = 82.566992
BEAT = 0.522
T0 = 0.22
BAR = BEAT * 4
N = int(DUR * SR)
rng = np.random.default_rng(7)
BASE = os.path.join(os.path.dirname(__file__), "..")

dry = np.zeros((N, 2), np.float32)   # drums + bass (no reverb)
wet = np.zeros((N, 2), np.float32)   # pads / plucks / bells (reverb bus)
gain_env = np.ones(N, np.float32)    # section dynamics


def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
def t_of(bar, beat=0.0): return T0 + BAR * bar + BEAT * beat
def add(buf, t, x, pan=0.0):
    i = int(t * SR)
    if i >= N or i < -len(x): return
    a = max(0, -i); x = x[a:]; i = max(0, i)
    j = min(N, i + len(x)); x = x[: j - i]
    if x.ndim == 2:  # already stereo (pads)
        buf[i:j] += x; return
    l, r = np.sqrt(0.5 * (1 - pan)), np.sqrt(0.5 * (1 + pan))
    buf[i:j, 0] += x * l; buf[i:j, 1] += x * r
def lp(x, f, order=2): return signal.sosfilt(signal.butter(order, f, "low", fs=SR, output="sos"), x)
def hp(x, f, order=2): return signal.sosfilt(signal.butter(order, f, "high", fs=SR, output="sos"), x)
def bp(x, lo, hi): return signal.sosfilt(signal.butter(2, [lo, hi], "band", fs=SR, output="sos"), x)
def tt(d): return np.arange(int(d * SR)) / SR


# ---------- instruments ----------
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
def keys(notes, dur=0.7, vel=0.3):
    t = tt(dur); x = sum(np.sin(2 * np.pi * hz(m) * t) * 0.6 + np.sin(2 * np.pi * 2 * hz(m) * t) * 0.15 for m in notes)
    return lp(x, 2600) * np.exp(-t / 0.28) * np.minimum(1, t / 0.004) * vel / len(notes)
def riser(dur, vel=0.5):
    t = tt(dur); n = rng.standard_normal(len(t))
    f = 400 + 6500 * (t / dur) ** 2
    ph = 2 * np.pi * np.cumsum(200 + 1400 * (t / dur) ** 2) / SR
    out = (hp(n, 900) * 0.6 + np.sin(ph) * 0.35) * (t / dur) ** 1.7 * vel
    return out * np.minimum(1, (dur - t) / 0.02)
def impact(vel=0.9):
    t = tt(1.4); f = 38 + 60 * np.exp(-t / 0.08)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.45) + lp(rng.standard_normal(len(t)), 2500) * np.exp(-t / 0.25) * 0.25) * vel


# ---------- chord vocabulary (MIDI) ----------
CH = {"Am": (45, (57, 60, 64)), "F": (41, (53, 57, 60)), "C": (48, (55, 60, 64)), "G": (43, (55, 59, 62)),
      "Dm": (38, (50, 53, 57)), "E": (40, (52, 56, 59)), "A": (45, (57, 61, 64)), "Em": (40, (52, 55, 59))}
def arp_notes(name, up=12): return [n + up for n in CH[name][1]]

# chapters: (first bar, chords per bar, feel)
SECTIONS = {
    "intro": (0, ["Am", "Am", "F", "F"]),
    "A": (4, ["Am", "F", "C", "G", "Am"]),
    "B": (9, ["Am", "Dm", "Am", "E", "E"]),
    "C": (14, ["F", "G", "Am", "F", "G"]),
    "D": (19, ["C", "G", "Am", "F", "C"]),
    "E": (24, ["Am", "F", "C", "G", "Am"]),
    "F": (29, ["Dm", "Am", "C", "G", "Am"]),
    "G": (34, ["F", "G", "Am", "E"]),
}


def drums(bar, mode):
    """mode: none | heart | half | four | four_clap"""
    for b in range(4):
        t = t_of(bar, b)
        if mode == "heart" and b == 0: add(dry, t, kick(0.45))
        if mode == "half" and b in (0, 2): add(dry, t, kick(0.85))
        if mode in ("four", "four_clap"): add(dry, t, kick(0.9 if b else 1.0))
        if mode in ("four_clap", "half") and b in (1, 3): add(dry, t, clap(0.5))
def hats(bar, mode):
    if mode == "8th":
        for h in range(8): add(dry, t_of(bar, h * 0.5), hat(open_=(h % 2 == 1) and h == 7, vel=0.35 + 0.1 * (h % 2)), pan=0.2)
    if mode == "16th":
        for h in range(16): add(dry, t_of(bar, h * 0.25), hat(vel=0.22 + 0.16 * (h % 4 == 2)), pan=-0.2)
    if mode == "tick":
        for h in (1.5, 2.5, 3.5): add(dry, t_of(bar, h), hat(vel=0.22), pan=0.3)
def bassline(bar, chord, mode):
    root = CH[chord][0]
    if mode == "pulse":
        for h in range(8): add(dry, t_of(bar, h * 0.5), bass(root + (12 if h in (3, 7) else 0), BEAT * 0.45, 0.6))
    if mode == "long": add(dry, t_of(bar), bass(root, BAR * 0.95, 0.7))
    if mode == "sub": add(dry, t_of(bar), bass(root - 12 if root > 36 else root, BAR * 0.98, 0.5))
def arps(bar, chord, mode, up=12):
    n = arp_notes(chord, up)
    if mode == "8th":
        for h in range(8): add(wet, t_of(bar, h * 0.5), pluck(n[h % 3] + (12 if h % 4 == 3 else 0), vel=0.3), pan=(-0.4 if h % 2 else 0.4))
    if mode == "16th":
        for h in range(16): add(wet, t_of(bar, h * 0.25), pluck(n[h % 3] + (12 if h % 8 > 5 else 0), 0.2, 0.24, 4200), pan=(-0.5 if h % 2 else 0.5))
    if mode == "sparse":
        for h in (0, 2.5): add(wet, t_of(bar, h), pluck(n[int(h) % 3] + 12, 0.5, 0.26), pan=0.3)
    if mode == "bell":
        for h in (0, 1.5, 3): add(wet, t_of(bar, h), bell(n[int(h * 2) % 3] + 12, 0.3), pan=(-0.3 if h else 0.3))
    if mode == "keys":
        for h in (0, 2): add(wet, t_of(bar, h), keys([x - 0 for x in CH[chord][1]], 0.9, 0.55), pan=0.0)
def pad_bar(bar, chord, vel, bright=1500, bars=1):
    add(wet, t_of(bar), pad(list(CH[chord][1]), BAR * bars + 0.8, vel, bright))


def section(name, per_bar):
    first, chords = SECTIONS[name]
    for i, ch in enumerate(chords):
        bar = first + i; last = i == len(chords) - 1
        per_bar(i, bar, ch, last)


# intro: mysterious, sparse; riser into the first cut
def intro(i, bar, ch, last):
    pad_bar(bar, ch, 0.34 + 0.06 * i, 900 + 300 * i)
    bassline(bar, ch, "sub")
    if i >= 1: arps(bar, ch, "sparse")
    if i >= 2: hats(bar, "tick")
    if last:
        add(dry, t_of(bar, 0), riser(BAR - 0.02, 0.55))
        for b in (2, 2.5, 3, 3.5): add(dry, t_of(bar, b), hat(vel=0.28))
section("intro", intro)

def A(i, bar, ch, last):
    pad_bar(bar, ch, 0.34, 1600); bassline(bar, ch, "pulse")
    drums(bar, "half" if i < 2 else "four_clap")
    if i >= 1: hats(bar, "8th")
    arps(bar, ch, "8th")
    if i == 0: add(dry, t_of(bar), impact(0.35))
section("A", A)

def B(i, bar, ch, last):  # tension: minor, sparse, low; silence gap handled by the mix around the flag
    pad_bar(bar, ch, 0.40, 900); bassline(bar, ch, "long")
    drums(bar, "heart"); hats(bar, "tick")
    if i in (1, 3): arps(bar, ch, "sparse", 0)
section("B", B)

def C(i, bar, ch, last):
    pad_bar(bar, ch, 0.34, 1800); bassline(bar, ch, "pulse"); drums(bar, "four_clap"); hats(bar, "8th"); arps(bar, ch, "16th")
section("C", C)

def D(i, bar, ch, last):  # positive, brighter, bells
    pad_bar(bar, ch, 0.40, 2600); bassline(bar, ch, "pulse"); drums(bar, "half"); hats(bar, "8th"); arps(bar, ch, "bell", 24)
    arps(bar, ch, "8th", 12) if i % 2 else None
section("D", D)

def E(i, bar, ch, last):  # confident, keys comping
    pad_bar(bar, ch, 0.30, 1400); bassline(bar, ch, "pulse"); drums(bar, "four"); hats(bar, "8th"); arps(bar, ch, "keys")
section("E", E)

def F(i, bar, ch, last):  # anticipation (bars 0-1), release at the Allow tap (bar index 2 = t~64.94)
    if i < 2:
        pad_bar(bar, ch, 0.42, 800 + 300 * i); bassline(bar, ch, "sub"); drums(bar, "heart"); hats(bar, "tick")
        if i == 1: add(dry, t_of(bar, 0), riser(BAR - 0.02, 0.4))
    else:
        pad_bar(bar, ch, 0.36, 2000); bassline(bar, ch, "pulse"); drums(bar, "four_clap"); hats(bar, "8th"); arps(bar, ch, "8th")
        if i == 2: add(dry, t_of(bar), impact(0.7))
section("F", F)

def G(i, bar, ch, last):  # build to the crescendo
    pad_bar(bar, ch, 0.36 + 0.03 * i, 2200); bassline(bar, ch, "pulse"); drums(bar, "four_clap"); hats(bar, "16th"); arps(bar, ch, "16th")
    if i == 2: add(dry, t_of(bar, 0), riser(BAR * 1.5, 0.7))
    if i == 3:
        for h in range(8): add(dry, t_of(bar, 2 + h * 0.25), clap(0.25 + 0.05 * h))
section("G", G)

# end: resolution to A major at the logo (bar 37.5 = 78.52 s), long shimmering tail
tEnd = T0 + BEAT * 150
add(dry, tEnd, impact(0.85))
add(dry, tEnd, kick(1.0))
add(wet, tEnd, pad([57, 61, 64, 69, 73], DUR - tEnd + 0.5, 0.55, 3200))
add(dry, tEnd, bass(33, 3.6, 0.8))
for j, m in enumerate((81, 85, 88, 93)):
    add(wet, tEnd + 0.08 + j * 0.13, bell(m, 0.32, 2.0), pan=(-0.4 + 0.27 * j))
for h in range(4): add(dry, tEnd + 0.522 * (h + 2), kick(0.55))

# ---------- sonic logo (synth): rising A major arpeggio + shimmer; delivered separately for the SFX stem ----------
logo = np.zeros((int(3.6 * SR), 2), np.float32)
for j, m in enumerate((69, 73, 76, 81)):
    t = tt(2.6); f = hz(m)
    x = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) + 0.12 * np.sin(2 * np.pi * 3 * f * t)) * np.exp(-t / 0.9) * np.minimum(1, t / 0.004) * 0.4
    i0 = int((0.10 * j) * SR); logo[i0:i0 + len(x), 0] += x[: len(logo) - i0] * (0.8 - 0.1 * j); logo[i0:i0 + len(x), 1] += x[: len(logo) - i0] * (0.5 + 0.1 * j)
sh = pad([81, 85, 88], 3.6, 0.5, 5000)[: len(logo)]
logo[: len(sh)] += sh * 0.6

# ---------- reverb on the wet bus, then combine ----------
ir_t = tt(1.8)
ir = (rng.standard_normal((len(ir_t), 2)) * np.exp(-ir_t / 0.55)[:, None]).astype(np.float32); ir[:int(0.012 * SR)] *= 0.2
tail = np.stack([fftconvolve(wet[:, c], ir[:, c])[:N] for c in (0, 1)], axis=1).astype(np.float32)
mix = dry + wet * 0.75 + tail * 0.11 * np.float32(len(ir_t) ** -0.5 * 60)

# section dynamics
def seg_gain(a, b, g0, g1=None):
    i, j = int(a * SR), min(N, int(b * SR)); g1 = g0 if g1 is None else g1
    gain_env[i:j] = np.linspace(g0, g1, j - i)
bounds = {n: (t_of(v[0]), t_of(v[0] + len(v[1]))) for n, v in SECTIONS.items()}
seg_gain(0, bounds["intro"][1], 0.55, 0.8)
seg_gain(*bounds["A"], 0.82); seg_gain(*bounds["B"], 0.62); seg_gain(*bounds["C"], 0.9)
seg_gain(*bounds["D"], 0.85); seg_gain(*bounds["E"], 0.88)
seg_gain(bounds["F"][0], t_of(31), 0.55); seg_gain(t_of(31), bounds["F"][1], 0.92)
seg_gain(bounds["G"][0], tEnd, 0.92, 1.0); seg_gain(tEnd, DUR, 1.0, 0.9)
mix = mix * gain_env[:, None]
# gentle fade-in at 0 and out over the last 1.4 s (tail rings naturally before that)
mix[:int(0.05 * SR)] *= np.linspace(0, 1, int(0.05 * SR))[:, None]
mix[-int(1.4 * SR):] *= np.linspace(1, 0, int(1.4 * SR))[:, None]
peak = float(np.max(np.abs(mix)))
mix = (mix / peak * 0.708).astype(np.float32)          # -3 dBFS peak stem
logo = (logo / max(1e-6, np.max(np.abs(logo))) * 0.7).astype(np.float32)

import subprocess
def write(path, a):
    subprocess.run([el.FFMPEG, "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s24le", path],
                   input=a.astype(np.float32).tobytes(), check=True)
os.makedirs(os.path.join(BASE, "04_music"), exist_ok=True)
os.makedirs(os.path.join(BASE, "05_sfx"), exist_ok=True)
write(os.path.join(BASE, "04_music", "music_original_synth.wav"), mix)
write(os.path.join(BASE, "05_sfx", "logo_synth.wav"), logo)
open(os.path.join(BASE, "04_music", "music_prompt.txt"), "w").write(
    "Original score synthesised in code (ElevenLabs Music requires a paid plan). 115 BPM, A minor to A major.\n"
    "If regenerating with ElevenLabs Music (paid plan), use: 'Premium futuristic fintech underscore, cinematic electronic, 115 BPM, "
    "instrumental only, deep warm bass, crisp electronic percussion, subtle synth pulses, digital plucks, atmospheric pads, minimal piano accents; "
    "mysterious opening, building momentum, tense middle, satisfying discovery, confident reporting, anticipation then release, "
    "strong premium resolution in A major at 78.5 seconds; 82.6 seconds; must leave space for a male voiceover.'\n")
print("music done: %.1fs, peak -3 dBFS" % (N / SR))
