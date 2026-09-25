# Notice

## This repository

Code and documentation are released under the [MIT License](LICENSE).

## Branding

`skills/satva-guide-gif/assets/satva-header.png` and `satva-footer.png` carry the Satva Solutions name and
logo. They are included so the Satva house style can be reproduced (the official logo files under `skills/satva-ledger-marketing-video/pipeline/video-build/satva-sizzle/assets/` are Satva's likewise) and are **not** licensed for use as the
branding of another organisation's documents. If you are not Satva, replace them with your own (see the README
section "Make it your own brand").

## Fonts (bundled)

| File | Font | Licence |
|---|---|---|
| `skills/satva-guide-gif/assets/Mulish-*.ttf` | Mulish, © The Mulish Project Authors | SIL Open Font License 1.1 — [`OFL-Mulish.txt`](skills/satva-guide-gif/assets/OFL-Mulish.txt) |
| `skills/satva-guide-gif/assets/RobotoMono.ttf` | Roboto Mono, © The Roboto Mono Project Authors | SIL Open Font License 1.1 — [`OFL-RobotoMono.txt`](skills/satva-guide-gif/assets/OFL-RobotoMono.txt) |
| `skills/satva-ledger-marketing-video/pipeline/video-build/satva-sizzle/assets/fonts/` | Mulish (woff2) and Geist Mono, © Vercel / basement.studio | SIL Open Font License 1.1 — `OFL-Mulish.txt`, `OFL-GeistMono.txt` in the same folder |

## Third-party software (not bundled)

| Project | Use | Licence / terms |
|---|---|---|
| [Playwright](https://github.com/microsoft/playwright) | screenshots, PDF | Apache-2.0 — installed by `npm install` |
| [Pillow](https://github.com/python-pillow/Pillow) | GIF encoding | MIT-CMU (HPND) — installed by `pip` |
| [HyperFrames](https://github.com/heygen-com/hyperframes) | video composition and render | see the project — fetched by `npx hyperframes` |
| [GSAP](https://gsap.com) | video animation | [GreenSock Standard License](https://gsap.com/standard-license) — downloaded on first `compose.mjs` run and cached locally; **not redistributed in this repository** |
| [ElevenLabs](https://elevenlabs.io) API | voice and sound effects | service terms apply; free-plan output is non-commercial and requires attribution — which is why no generated audio or rendered video is shipped |
| NumPy, SciPy, FFmpeg | audio synthesis and mastering (sizzle pipeline) | BSD-3-Clause / BSD-3-Clause / LGPL-2.1+ or GPL — installed by you, not bundled |

## The example video

`examples/satva-ledger-video/Satva-Ledger-Sizzle-82s.mp4` is the Satva Ledger promo. Its voice and sound effects
were generated with the ElevenLabs API on a **free plan**: that output is non-commercial and requires an
"elevenlabs.io" credit, which the video shows on its end card. Do not reuse the audio commercially unless you
have generated your own on a paid plan. The score is original (synthesised in code). Figures are QuickBooks
Online sandbox data. The video is Satva Solutions' own marketing content and is not covered by the MIT licence.

## Illustrations and sample data

The screens in `skills/satva-guide-gif/examples/` and `examples/setup-guide-sample/` are neutral illustrations
with invented data. No real credentials, customers or third-party interfaces appear in them. Figures in the
example video briefs are labelled demo data. The figures in the Satva Ledger sizzle generator come from a
QuickBooks Online **sandbox** company and are labelled "Sandbox data" on screen; QuickBooks is a trademark of Intuit.
