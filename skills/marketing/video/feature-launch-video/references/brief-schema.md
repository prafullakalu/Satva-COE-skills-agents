# brief.json — the one contract between research and rendering

Every run produces exactly one `brief.json`. Nothing downstream (composer, audio pipeline,
renderer) reads anything else about the feature — if a fact isn't in here, it can't appear in the
video. This is what makes claims auditable: `grep` the brief against the video's on-screen text
and VO, they must match 1:1.

```jsonc
{
  "product": "Satva Ledger",                    // the product/site this feature belongs to
  "feature": "Bank statement import",             // the module/feature being launched
  "message": "It reads your statement so you don't have to type it in.", // the ONE thing to land
  "audience": "practice owners already on QuickBooks",
  "aspect": "16:9",                                // 16:9 | 9:16 | 1:1
  "durationTarget": 45,                            // seconds; the composer fits beats to this
  "theme": "ledger-clean",                         // see themes/ — or "auto" to pick from brand
  "brand": {
    "accent": "#1d83b8",                           // pulled from the project's own brand guide;
    "ink": "#111111",                              // never invented — ask for the guide/tokens
    "paper": "#f7fafd",
    "font": "Mulish",
    "logo": "brand-assets/logo/satva-logo.svg",    // official file path, never hand-redrawn
    "character": "bow",                            // mascot-playful theme only: "default" | "bow" | "spark"
    "ribbon": "#ef5da8"                            // "bow"/"spark" variant's accent color; optional, has a default
  },
  "flow": [                                        // the REAL user flow, step by step —
    {                                               // this is what "think the user flow" means:
      "step": "Upload the statement",               // walk the actual feature, screen by screen,
      "visual": "card",                             // before writing a single line of script
      "data": { "kicker": "Vault", "fields": [["File", "statement-sept.csv"], ["Rows found", "142"]] },
      "line": "Drop in the file. It reads every row."
    },
    {
      "step": "It matches what it can",
      "visual": "stat",
      "data": { "big": "138 / 142", "label": "matched automatically" },
      "line": "One hundred thirty eight matched on the first pass."
    },
    {
      "step": "It asks about the rest",
      "visual": "approval",
      "data": { "prompt": "4 rows need a category", "allow": "Review them" },
      "line": "Four it isn't sure about. You decide, not it."
    }
  ],
  "endCard": { "tagline": "Fewer rows to type. Same books.", "cta": "See it on your data." },
  "groundedFactsSource": "path/to/where/these/numbers/came/from.md OR 'example/demo — not real data'",
  "claims": { "never": ["autonomous", "zero errors", "replaces your bookkeeper"] },
  "voice": { "provider": "elevenlabs", "voiceId": "nPczCjzI2devNBz1zQrb", "fallback": "kokoro",
    "pronounce": { "Satva": "SAHT-vah" }           // TTS-only phonetic respellings; screen text is untouched
  },
  "music": { "bpm": 112, "key": "auto" }
}
```

## `flow[].visual` types

`card`/`list` (kicker + field rows — the default, works for most data), `stat` (one big number/word
+ label, gets an automatic glow-pulse), `approval` (Allow/Deny prompt, gets an automatic particle
burst on tap), `chat` (a two-line exchange: `{user, agent}`), `compare` (two mini-cards side by
side: `{before:[title,sub], after:[title,sub]}` — for a workflow before/after, not a named
competitor comparison; see the claims rule below on why).

## Multiple characters (optional)

For a scenario with more than one persona — an admin connecting things, a teammate asking
questions — add `characters` and tag each flow step:

```jsonc
"characters": {
  "admin":    { "voiceId": "nPczCjzI2devNBz1zQrb", "variant": "default" },
  "teammate": { "voiceId": "EXAVITQu4vr4xnSDxMaL", "variant": "bow", "ribbon": "#ef5da8" }
},
"flow": [
  { "step": "...", "character": "admin", ... },
  { "step": "...", "character": "teammate", ... }
]
```

The character who opens the video is whichever key comes first in `characters`; the one who closes
it is whoever's in the last `flow` step. Without `characters`, a brief still works exactly as
before (`brand.character` / `brand.ribbon` pick the single mascot's look).

Voices must be real, callable ElevenLabs voice IDs you've actually verified respond 200 on this
account — free-plan accounts can't reach most library voices (402 `paid_plan_required`); check
before writing one into a brief. **Never** pick a voice to sound like a specific real, identifiable
person (an actor, a public figure) — that's impersonation for a commercial purpose regardless of
framing ("any famous X" still means a specific real person once a voice is chosen), and it's refused
categorically, not something a brief field can request around.

## Rules the brief must satisfy before it goes to the composer

1. **Every number, every screen state in `flow[].data` traces to something real** — a spec, a
   running build, real sample data, or a fixture explicitly labeled as one. If the feature doesn't
   exist yet and there's nothing to point at, set `groundedFactsSource` to
   `"example/demo — not real data"` and the composer stamps every scene with a visible "Concept /
   not final" tag. Never present a mockup as a real product screen.
2. **`brand` is read from the project, not invented.** Look for (in order): a `DESIGN.md` /
   `BRAND.md` / style guide in the repo, a brand guideline doc the user supplies, or existing
   product screenshots to sample colors/type from. Only fall back to a theme's own default palette
   when truly nothing exists, and say so.
3. **`claims.never`** is filled from whatever the product's own marketing-copy / positioning doc
   says not to claim (see `sat:accounting-fundamentals`-style "what we do not claim" sections when
   present). If no such doc exists, default to: not "autonomous", not "100% accurate", not
   "replaces a human", not "AI-powered" as the entire pitch (say what it does, not that it's AI).
4. **`flow` is the real flow**, in the real order, from actually reading the feature (code, a
   running instance, or a spec) — not an imagined "cool" sequence. 3–6 steps is the sweet spot for
   a 30–60s video; more than that, cut to the steps that carry the message.
5. **No market-uniqueness or competitor claims** ("nothing else like this exists," "no one else
   does this") unless you've actually verified them — most products in this space have prior art,
   and claiming otherwise is false advertising, not enthusiasm. If the real differentiator is
   genuinely strong (a real number, a real architecture choice), lead with that instead — it's more
   convincing than an unverifiable superlative anyway. Put the phrase in `claims.never` if there's
   any risk of it sneaking back into copy.
