"""Small ElevenLabs helper: key is read from a .env near the project (never printed or written to output).
Generic — no product-specific paths. Every other audio script imports this."""
import json, os, shutil, subprocess, urllib.request, urllib.error
import numpy as np

SR = 48000


def _find_env():
    d = os.getcwd()
    for _ in range(6):
        p = os.path.join(d, ".env")
        if os.path.exists(p):
            return p
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return None


def key():
    p = _find_env() or os.environ.get("DOTENV_PATH")
    if p and os.path.exists(p):
        for line in open(p, encoding="utf8"):
            if line.startswith("ELEVENLABS_API_KEY="):
                return line.split("=", 1)[1].strip()
    if os.environ.get("ELEVENLABS_API_KEY"):
        return os.environ["ELEVENLABS_API_KEY"]
    raise SystemExit("ELEVENLABS_API_KEY missing: put it in a .env next to your project (ELEVENLABS_API_KEY=...) "
                      "or export it as an env var. Never paste the key value into a prompt or a committed file.")


def _ffmpeg():
    found = shutil.which("ffmpeg") or shutil.which("ffmpeg.exe")
    if found:
        return found
    raise SystemExit("ffmpeg not found on PATH. Install it, or `npm i ffmpeg-static` and set FFMPEG_PATH.")


FFMPEG = os.environ.get("FFMPEG_PATH") or _ffmpeg()


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
