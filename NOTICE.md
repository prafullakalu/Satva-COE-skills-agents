# Notice

## This repository

Code and documentation are released under the [MIT License](LICENSE).

## Branding

`skills/satva-guide-gif/assets/satva-header.png` and `satva-footer.png` carry the Satva Solutions name and
logo. They are included so the Satva house style can be reproduced and are **not** licensed for use as the
branding of another organisation's documents. If you are not Satva, replace them with your own (see the README
section "Make it your own brand").

## Fonts (bundled)

| File | Font | Licence |
|---|---|---|
| `skills/satva-guide-gif/assets/Mulish-*.ttf` | Mulish, © The Mulish Project Authors | SIL Open Font License 1.1 — [`OFL-Mulish.txt`](skills/satva-guide-gif/assets/OFL-Mulish.txt) |
| `skills/satva-guide-gif/assets/RobotoMono.ttf` | Roboto Mono, © The Roboto Mono Project Authors | SIL Open Font License 1.1 — [`OFL-RobotoMono.txt`](skills/satva-guide-gif/assets/OFL-RobotoMono.txt) |

## Third-party software (not bundled)

| Project | Use | Licence / terms |
|---|---|---|
| [Playwright](https://github.com/microsoft/playwright) | screenshots, PDF | Apache-2.0 — installed by `npm install` |
| [Pillow](https://github.com/python-pillow/Pillow) | GIF encoding | MIT-CMU (HPND) — installed by `pip` |
| [HyperFrames](https://github.com/heygen-com/hyperframes) | video composition and render | see the project — fetched by `npx hyperframes` |
| [GSAP](https://gsap.com) | video animation | [GreenSock Standard License](https://gsap.com/standard-license) — downloaded on first `compose.mjs` run and cached locally; **not redistributed in this repository** |
| [ElevenLabs](https://elevenlabs.io) API | voice and sound effects | service terms apply; free-plan output is non-commercial and requires attribution |

## Illustrations and sample data

The screens in `skills/satva-guide-gif/examples/` and `examples/setup-guide-sample/` are neutral illustrations
with invented data. No real credentials, customers or third-party interfaces appear in them. Figures in the
example video briefs are labelled demo data.
