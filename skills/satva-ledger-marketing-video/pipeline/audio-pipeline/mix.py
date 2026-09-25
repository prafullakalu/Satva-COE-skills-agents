"""Assemble stems (voice / music / sfx), duck the music under the voice, master to -14 LUFS / -1 dBTP at the exact video length."""
import json, os, subprocess, sys
import numpy as np
from scipy import signal
from scipy.ndimage import maximum_filter1d

sys.path.insert(0, os.path.dirname(__file__))
import el

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SR = el.SR
DUR = 82.566992
N = int(round(DUR * SR))
FF = el.FFMPEG
P = lambda *a: os.path.join(BASE, *a)
for _d in ("06_stems", "07_mix", "08_final"):
    os.makedirs(P(_d), exist_ok=True)
db = lambda x: 10 ** (x / 20)
MUSIC_REL_DB = float(os.environ.get("MUSIC_REL_DB", -19))     # music level vs voice while speaking
DUCK_DEPTH_DB = float(os.environ.get("DUCK_DEPTH_DB", -12))   # extra dip on speech


def write(path, a, ch=2):
    subprocess.run([FF, "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", str(ch), "-i", "-", "-c:a", "pcm_s24le", path],
                   input=a.astype(np.float32).tobytes(), check=True)


def ffmpeg_filter(path_in, path_out, af):
    subprocess.run([FF, "-v", "error", "-y", "-i", path_in, "-af", af, "-c:a", "pcm_s24le", path_out], check=True)


# ---------- 1. voice stem ----------
vs = json.load(open(P("03_voice", "voice_segments.json")))["segments"]
voice = np.zeros(N, np.float32)
for s in vs:
    x = el.load(P(s["file"]), mono=True).copy()
    f = int(0.012 * SR); x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    i = int(round(s["start"] * SR)); voice[i:i + len(x)] += x[: N - i]
raw_v = P("06_stems", "_voice_raw.wav"); write(raw_v, voice, 1)
# EQ + compression: low cut, warmth, presence, gentle de-ess, 3:1 compression
ffmpeg_filter(raw_v, P("06_stems", "_voice_proc.wav"),
              "highpass=f=80,equalizer=f=220:t=q:w=1:g=1.5,equalizer=f=3200:t=q:w=1.2:g=1.8,equalizer=f=7200:t=q:w=2:g=-3.5,"
              "acompressor=threshold=-24dB:ratio=3:attack=8:release=140:makeup=5")
voice_p = el.load(P("06_stems", "_voice_proc.wav"), mono=True)[:N]
voice_p = np.pad(voice_p, (0, N - len(voice_p)))
voice_st = np.stack([voice_p, voice_p], 1)

# ---------- 2. sfx stem (each effect has a visual reason; times come from the video analysis) ----------
def T(k): return 0.22 + 0.522 * k
EV = [  # (time s, file, gain dB, why)
    (2.31, "activate", -13, "mascot appears / agent activates"),
    (6.55, "sparkle", -22, "One agent for everything"),
    (T(16) - 0.05, "swoosh", -17, "cut into chapter A"),
    (13.27, "permission", -15, "A: approval card asks permission"),
    (15.36, "approve", -12, "A: Allow tap"),
    (15.70, "ding", -16, "A: Posted and verified"),
    (15.75, "hop", -20, "A: mascot happy hop"),
    (16.90, "tick", -22, "A: CSV/OFX/QIF line"),
    (T(36) - 0.05, "swoosh", -17, "cut into chapter B"),
    (21.10, "scan", -17, "B: reconciling scan"),
    (23.19, "anomaly", -14, "B: something does not add up"),
    (23.19, "stamp", -12, "B: DOESN'T MATCH stamp"),
    (T(56) - 0.05, "swoosh", -17, "cut into chapter C"),
    (32.06, "report", -18, "C: aging card"),
    (T(76) - 0.05, "swoosh", -17, "cut into chapter D"),
    (44.60, "coin", -15, "D: credits found"),
    (45.60, "discover", -12, "D: unused credit total"),
    (45.65, "hop", -20, "D: mascot happy hop"),
    (T(96) - 0.05, "swoosh", -17, "cut into chapter E"),
    (52.90, "report", -17, "E: P&L card"),
    (55.00, "anomaly", -20, "E: Miscellaneous highlighted"),
    (T(116) - 0.05, "swoosh", -17, "cut into chapter F"),
    (62.86, "permission", -15, "F: Satva asks permission"),
    (64.90, "approve", -12, "F: Allow tap"),
    (65.00, "hop", -20, "F: mascot happy hop"),
    (65.70, "tick", -15, "F: audit check 1"),
    (66.50, "tick", -15, "F: audit check 2"),
    (67.30, "tick", -15, "F: audit check 3"),
    (68.10, "tick", -15, "F: audit check 4"),
    (T(136) - 0.05, "swoosh", -17, "cut into all-systems chapter"),
    (71.74, "sparkle", -20, "G: mascot in"),
] + [(72.26 + 0.522 * i, "tick", -21, f"G: system {i + 1}/8 appears") for i in range(8)] + [
    (T(150) - 0.05, "swoosh", -16, "cut to end card"),
    (78.62, "logo", -11, "sonic logo (ElevenLabs layer)"),
    (79.55, "sparkle", -19, "end card: tagline"),
    (80.80, "hop", -20, "end card: mascot waves"),
]
sfx = np.zeros((N, 2), np.float32)
cache = {}
def sfx_audio(name):
    if name not in cache:
        x = el.load(P("05_sfx", name + ".mp3"), mono=True)
        x = x / max(1e-6, np.max(np.abs(x))) * 0.5            # normalise to -6 dBFS peak
        f = int(0.004 * SR); x[:f] *= np.linspace(0, 1, f); x[-3 * f:] *= np.linspace(1, 0, 3 * f)
        cache[name] = x.astype(np.float32)
    return cache[name]
for t, name, g, why in EV:
    x = sfx_audio(name) * db(g + 6); i = int(round(t * SR))
    sfx[i:i + len(x), :] += x[: max(0, N - i), None]
lg = el.load(P("05_sfx", "logo_synth.wav"))          # synthesised A-major sonic logo, layered under the ElevenLabs one
i = int(round(78.62 * SR)); sfx[i:i + len(lg)] += lg[: max(0, N - i)] * db(-16)
write(P("06_stems", "sfxStem_raw.wav"), sfx)

# ---------- 3. music: duck under voice + manual drops ----------
music = el.load(P("04_music", "music_original_synth.wav"))[:N]
music = np.pad(music, ((0, N - len(music)), (0, 0)))
frame = int(0.010 * SR)
env = np.sqrt(np.convolve(voice_p ** 2, np.ones(frame) / frame, "same"))
active = (env > 0.012).astype(np.float32)
active = maximum_filter1d(active, size=int(0.30 * SR))                    # hold across word gaps, look ahead
a = np.exp(-1 / (0.10 * SR))
duck = signal.lfilter([1 - a], [1, -a], active).astype(np.float32)        # ~100 ms attack/release smoothing
speech = duck > 0.7
duck_gain = 1 - duck * (1 - db(DUCK_DEPTH_DB))
drops = np.ones(N, np.float32)
for t0, t1, g in [(22.60, 23.18, -28), (64.35, 64.92, -18)]:              # silence before the flag; held breath before Allow
    i0, i1 = int(t0 * SR), int(t1 * SR); r = int(0.12 * SR)
    drops[i0:i1] = db(g); drops[i0 - r:i0] = np.linspace(1, db(g), r); drops[i1:i1 + r] = np.linspace(db(g), 1, r)
music_d = music * (duck_gain * drops)[:, None]
rms = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
v_db = rms(voice_p[speech]); m_db = rms(music_d[speech, 0])
gain_m = db(v_db + MUSIC_REL_DB - m_db)
music_d *= gain_m
sfx_duck = (1 - 0.30 * duck)[:, None]
sfx_d = sfx * sfx_duck
write(P("06_stems", "voiceStem.wav"), voice_st)
write(P("06_stems", "musicStem.wav"), music_d)
write(P("06_stems", "sfxStem.wav"), sfx_d)

pre = voice_st + music_d + sfx_d
pre_path = P("07_mix", "premaster_float.wav"); write(pre_path, pre)

# ---------- 4. master: two-pass loudnorm to -14 LUFS / -1 dBTP, exact length, 24-bit WAV ----------
m1 = subprocess.run([FF, "-hide_banner", "-i", pre_path, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
j = json.loads(m1[m1.rindex("{"): m1.rindex("}") + 1])
ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:"
      f"measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
fin_wav = P("08_final", "satvaLedger_final_audio.wav")
# duration-based apad/atrim, not sample-count-based — see satvaLedgerAudio/tools/mix.py's copy of
# this fix for why: loudnorm's dynamic-mode fallback can silently truncate a sample-count-based trim.
subprocess.run([FF, "-v", "error", "-y", "-i", pre_path, "-af", f"{ln},alimiter=limit=0.891:level=false,apad=whole_dur={DUR},atrim=end={DUR}",
                "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s24le", fin_wav], check=True)
subprocess.run([FF, "-v", "error", "-y", "-i", fin_wav, "-c:a", "libmp3lame", "-b:a", "192k", P("08_final", "satvaLedger_final_audio.mp3")], check=True)

json.dump({"voice_vs_music_db_target": MUSIC_REL_DB, "voice_speech_rms_db": round(float(v_db), 1), "music_in_speech_rms_db": round(float(rms(music_d[speech, 0])), 1),
           "music_gain_applied": round(float(20 * np.log10(gain_m)), 1), "sfx_events": [{"t": round(t, 3), "sfx": n, "gain_db": g, "why": w} for t, n, g, w in EV]},
          open(P("07_mix", "mix_report.json"), "w"), indent=1)
print(f"voice speech RMS {v_db:.1f} dB | music while speaking {rms(music_d[speech, 0]):.1f} dB "
      f"(target {MUSIC_REL_DB} dB below voice; achieved {rms(music_d[speech, 0]) - v_db:.1f}) | music gain {20 * np.log10(gain_m):.1f} dB | sfx events {len(EV)}")
