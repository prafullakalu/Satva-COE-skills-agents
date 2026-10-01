"""Small ElevenLabs helper: the key comes from ELEVENLABS_API_KEY or a git-ignored .env, never printed or written to output files."""
import json, os, shutil, subprocess, urllib.request, urllib.error, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
# ffmpeg: FFMPEG_PATH, else whatever is on PATH.  Key: env var, else a .env in the working dir or next to the pipeline.
FFMPEG = os.environ.get("FFMPEG_PATH") or shutil.which("ffmpeg") or "ffmpeg"
ENV_FILES = [os.path.join(d, ".env") for d in (os.getcwd(), os.path.join(HERE, ".."), os.path.join(HERE, "..", ".."))]
SR = 48000


def key():
    if os.environ.get("ELEVENLABS_API_KEY"):
        return os.environ["ELEVENLABS_API_KEY"]
    for path in ENV_FILES:
        if os.path.exists(path):
            for line in open(path, encoding="utf8"):
                if line.startswith("ELEVENLABS_API_KEY="):
                    return line.split("=", 1)[1].strip()
    raise SystemExit("ELEVENLABS_API_KEY missing: export it, or put ELEVENLABS_API_KEY=... in a .env in the working folder")


def post(path, body, out_path):
    req = urllib.request.Request(
        "https://api.elevenlabs.io" + path, data=json.dumps(body).encode(),
        headers={"xi-api-key": key(), "Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            open(out_path, "wb").write(r.read())
        return 200, ""
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf8", "ignore")[:200]


def tts(voice_id, text, out_mp3, model="eleven_v3", stability=0.5, similarity=0.75, style=0.25):
    return post(f"/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128",
                {"text": text, "model_id": model,
                 "voice_settings": {"stability": stability, "similarity_boost": similarity, "style": style, "use_speaker_boost": True}},
                out_mp3)


def sfx(prompt, seconds, out_mp3, influence=0.6):
    return post("/v1/sound-generation?output_format=mp3_44100_128",
                {"text": prompt, "duration_seconds": seconds, "prompt_influence": influence}, out_mp3)


def load(path, sr=SR, mono=False):
    """Decode any audio file to float32 numpy [n] (mono) or [n,2] (stereo) at sr via ffmpeg."""
    ch = 1 if mono else 2
    raw = subprocess.run([FFMPEG, "-v", "error", "-i", path, "-f", "f32le", "-ac", str(ch), "-ar", str(sr), "-"],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(raw, dtype=np.float32)
    return a if mono else a.reshape(-1, 2)


def median_f0(path):
    """Rough median fundamental frequency (Hz) of voiced frames, via autocorrelation."""
    x = load(path, 16000, mono=True)
    fl, hop = 640, 320
    f0s = []
    for i in range(0, len(x) - fl, hop):
        f = x[i:i + fl]
        if np.sqrt(np.mean(f ** 2)) < 0.02:
            continue
        f = f - f.mean()
        ac = np.correlate(f, f, "full")[fl - 1:]
        lo, hi = 16000 // 300, 16000 // 70
        seg = ac[lo:hi]
        if len(seg) == 0 or ac[0] <= 0:
            continue
        k = int(np.argmax(seg)) + lo
        if ac[k] / ac[0] > 0.4:
            f0s.append(16000 / k)
    return float(np.median(f0s)) if f0s else 0.0
