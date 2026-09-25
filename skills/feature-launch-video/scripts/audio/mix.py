"""Assemble stems (voice / music / sfx), duck the music under the voice, master to -14 LUFS / -1.5 dBTP
at the exact video length. Scene-cut SFX and duration all come from timing.json — nothing hardcoded."""
import argparse, json, os, subprocess, sys
import numpy as np
from scipy import signal
from scipy.ndimage import maximum_filter1d
sys.path.insert(0, os.path.dirname(__file__))
import el

ap = argparse.ArgumentParser()
ap.add_argument("--dir", default=".")
args = ap.parse_args()
D = os.path.abspath(args.dir)
timing = json.load(open(os.path.join(D, "timing.json")))
SR = el.SR
DUR = timing["durationSec"]
N = int(round(DUR * SR))
FF = el.FFMPEG
P = lambda *a: os.path.join(D, *a)
db = lambda x: 10 ** (x / 20)
MUSIC_REL_DB = float(os.environ.get("MUSIC_REL_DB", -19))
DUCK_DEPTH_DB = float(os.environ.get("DUCK_DEPTH_DB", -12))


def write(path, a, ch=2):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    subprocess.run([FF, "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", str(ch), "-i", "-", "-c:a", "pcm_s24le", path],
                   input=a.astype(np.float32).tobytes(), check=True)


def ffmpeg_filter(path_in, path_out, af):
    subprocess.run([FF, "-v", "error", "-y", "-i", path_in, "-af", af, "-c:a", "pcm_s24le", path_out], check=True)


# ---------- 1. voice stem ----------
vs = json.load(open(P("audio", "voice_segments.json")))["segments"]
voice = np.zeros(N, np.float32)
for s in vs:
    x = el.load(P(s["file"]), mono=True).copy()
    f = int(0.012 * SR); x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    i = int(round(s["start"] * SR)); voice[i:i + len(x)] += x[: max(0, N - i)]
raw_v = P("audio", "_voice_raw.wav"); write(raw_v, voice, 1)
ffmpeg_filter(raw_v, P("audio", "_voice_proc.wav"),
              "highpass=f=80,equalizer=f=220:t=q:w=1:g=1.5,equalizer=f=3200:t=q:w=1.2:g=1.8,equalizer=f=7200:t=q:w=2:g=-3.5,"
              "acompressor=threshold=-24dB:ratio=3:attack=8:release=140:makeup=5")
voice_p = el.load(P("audio", "_voice_proc.wav"), mono=True)[:N]
voice_p = np.pad(voice_p, (0, N - len(voice_p)))
voice_st = np.stack([voice_p, voice_p], 1)

# ---------- 2. sfx stem — one swoosh per scene cut (matches compose.mjs's own cue placement) ----------
cuts = [timing["intro"]["end"]] + [s["end"] for s in timing["scenes"][:-1]] + [timing["end"]["start"]]
EV = [(t - 0.05, "swoosh", -17, "scene cut") for t in cuts]
EV += [(timing["intro"]["start"] + 0.05, "pop", -13, "intro text in")]
for s in timing["scenes"]:
    EV.append((s["start"] + 0.5, "pop", -15, f"{s['id']} visual in"))
    if s.get("visual") == "approval":
        EV.append((s["start"] + 1.4, "click", -12, f"{s['id']} allow tap"))
EV.append((timing["end"]["start"] + 0.3, "pop", -16, "end card"))

sfx = np.zeros((N, 2), np.float32)
cache = {}
def sfx_audio(name):
    if name not in cache:
        path = P("assets", "sfx", name + ".mp3")
        if not os.path.exists(path):
            cache[name] = None
        else:
            x = el.load(path, mono=True)
            x = x / max(1e-6, np.max(np.abs(x))) * 0.5
            f = int(0.004 * SR); x[:f] *= np.linspace(0, 1, f); x[-3 * f:] *= np.linspace(1, 0, 3 * f)
            cache[name] = x.astype(np.float32)
    return cache[name]
for t, name, g, why in EV:
    x = sfx_audio(name)
    if x is None or t < 0: continue
    xg = x * db(g + 6); i = int(round(t * SR))
    sfx[i:i + len(xg), :] += xg[: max(0, N - i), None]
lg_path = P("assets", "sfx", "logo.wav")
if os.path.exists(lg_path):
    lg = el.load(lg_path); i = int(round(timing["end"]["start"] * SR))
    sfx[i:i + len(lg)] += lg[: max(0, N - i)] * db(-14)
write(P("audio", "sfxStem_raw.wav"), sfx)

# ---------- 3. music: duck under voice ----------
music = el.load(P("assets", "music.wav"))[:N]
music = np.pad(music, ((0, N - len(music)), (0, 0)))
frame = int(0.010 * SR)
env = np.sqrt(np.convolve(voice_p ** 2, np.ones(frame) / frame, "same"))
active = (env > 0.012).astype(np.float32)
active = maximum_filter1d(active, size=int(0.30 * SR))
a = np.exp(-1 / (0.10 * SR))
duck = signal.lfilter([1 - a], [1, -a], active).astype(np.float32)
speech = duck > 0.7
duck_gain = 1 - duck * (1 - db(DUCK_DEPTH_DB))
music_d = music * duck_gain[:, None]
rms = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
v_db = rms(voice_p[speech]) if speech.any() else -30.0
m_db = rms(music_d[speech, 0]) if speech.any() else rms(music_d[:, 0])
gain_m = db(v_db + MUSIC_REL_DB - m_db)
music_d *= gain_m
sfx_duck = (1 - 0.30 * duck)[:, None]
sfx_d = sfx * sfx_duck
write(P("audio", "voiceStem.wav"), voice_st)
write(P("audio", "musicStem.wav"), music_d)
write(P("audio", "sfxStem.wav"), sfx_d)

pre = voice_st + music_d + sfx_d
pre_path = P("audio", "premaster_float.wav"); write(pre_path, pre)

# ---------- 4. master: two-pass loudnorm to -14 LUFS / -1.5 dBTP, exact length, 24-bit WAV ----------
m1 = subprocess.run([FF, "-hide_banner", "-i", pre_path, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
j = json.loads(m1[m1.rindex("{"): m1.rindex("}") + 1])
ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:"
      f"measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
os.makedirs(P("final"), exist_ok=True)
fin_wav = P("final", "audio_final.wav")
# duration-based apad/atrim, not sample-count-based: loudnorm's internal true-peak oversampling
# (ITU-R BS.1770, ~4x) shifts what "N samples" means to a downstream filter, so end_sample=N
# silently trims to ~1/4 the intended length. end=/whole_dur= are in seconds and immune to that.
subprocess.run([FF, "-v", "error", "-y", "-i", pre_path, "-af", f"{ln},alimiter=limit=0.891:level=false,apad=whole_dur={DUR},atrim=end={DUR}",
                "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s24le", fin_wav], check=True)
subprocess.run([FF, "-v", "error", "-y", "-i", fin_wav, "-c:a", "libmp3lame", "-b:a", "192k", P("final", "audio_final.mp3")], check=True)

json.dump({"voice_vs_music_db_target": MUSIC_REL_DB, "voice_speech_rms_db": round(float(v_db), 1),
           "music_gain_applied_db": round(float(20 * np.log10(gain_m)), 1), "sfx_events": len(EV), "duration_sec": DUR},
          open(P("audio", "mix_report.json"), "w"), indent=1)
print(f"voice speech RMS {v_db:.1f} dB | music gain {20 * np.log10(gain_m):.1f} dB | sfx events {len(EV)} | duration {DUR:.1f}s")
