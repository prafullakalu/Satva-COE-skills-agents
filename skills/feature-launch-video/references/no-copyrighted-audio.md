# No copyrighted audio — ever

This rule exists because it was tested in production: a client-supplied reference video for style
came with a Meta-owned soundtrack, and the request that followed was to "change it a little bit so
copyright shouldn't be there." Altering a track slightly does not remove its copyright, and helping
disguise a copyrighted work as original is not something to do regardless of how the request is
framed ("just for timing," "internal only," "we'll swap it later").

**What to do instead:**
- If someone hands you a reference video for style: take structure only — pacing, shot types, energy
  arc, where cuts land. Never reuse its audio track, not even "temporarily" or "for timing."
- `music.py` in this skill always synthesizes an original score in code (numpy/scipy oscillators +
  a convolution reverb) — no samples, no stock library, no stems from anywhere else. It is free to
  use in any output.
- Voice and SFX come from ElevenLabs generation, which is licensed output tied to the account that
  generated it — check the account's plan before calling it publishable (free plan = non-commercial,
  needs an "elevenlabs.io" credit; paid plan = commercial use).
- If a project's picture-lock draft still has a reference track baked in for internal timing review,
  strip the audio (`ffmpeg -an -c:v copy`) and delete the reference file before packaging anything
  for sharing — check for this explicitly before handing off, it's easy to miss one leftover copy.
