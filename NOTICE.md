# Notice

## This repository

Code and documentation are released under the [MIT License](LICENSE).

## Branding

`skills/satva/docs/satva-guide-gif/assets/satva-header.png` and `satva-footer.png` carry the Satva Solutions name and
logo. They are included so the Satva house style can be reproduced (the official logo files under `skills/satva/video/satva-ledger-marketing-video/pipeline/video-build/satva-sizzle/assets/` are Satva's likewise) and are **not** licensed for use as the
branding of another organisation's documents. If you are not Satva, replace them with your own (see the README
section "Make it your own brand").

## Fonts (bundled)

| File | Font | Licence |
|---|---|---|
| `skills/satva/docs/satva-guide-gif/assets/Mulish-*.ttf` | Mulish, © The Mulish Project Authors | SIL Open Font License 1.1 — [`OFL-Mulish.txt`](skills/satva/docs/satva-guide-gif/assets/OFL-Mulish.txt) |
| `skills/satva/docs/satva-guide-gif/assets/RobotoMono.ttf` | Roboto Mono, © The Roboto Mono Project Authors | SIL Open Font License 1.1 — [`OFL-RobotoMono.txt`](skills/satva/docs/satva-guide-gif/assets/OFL-RobotoMono.txt) |
| `skills/satva/video/satva-ledger-marketing-video/pipeline/video-build/satva-sizzle/assets/fonts/` | Mulish (woff2) and Geist Mono, © Vercel / basement.studio | SIL Open Font License 1.1 — `OFL-Mulish.txt`, `OFL-GeistMono.txt` in the same folder |

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

## Third-party skill content

The skills under `skills/` are Satva-original unless a skill's own frontmatter says otherwise
(`metadata.license` and `metadata.source`). **113 skills are adapted from 29 third-party repositories**, all MIT or
Apache-2.0 licensed. Each adapted skill keeps an attribution comment under its frontmatter, its upstream URL in
`metadata.source`, and the upstream licence text is saved verbatim in
[`skills/accounting/LICENSES/`](skills/accounting/LICENSES/). Neither Anthropic Apache-2.0 repository ships a NOTICE file or a
copyright holder line; the attribution names the repository owner. Modifications are summarised in each skill's attribution
comment. Where a skill bundles scripts, only scripts that were read and found to be local computation were kept.

| Upstream | Licence | Copyright | Skills | Licence text |
|---|---|---|---|---|
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | MIT | Copyright (c) 2025 Corey Haines | 13 | this file, below |
| [Receiptor-AI/bookkeeping-skills](https://github.com/Receiptor-AI/bookkeeping-skills) | MIT | Copyright (c) 2026 Receiptor AI | 12 | `skills/accounting/LICENSES/Receiptor-AI__bookkeeping-skills.LICENSE` |
| [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | Apache-2.0 | none in licence (attributed to repository owner) | 12 | `skills/accounting/LICENSES/anthropics__knowledge-work-plugins.LICENSE` |
| [anthropics/financial-services](https://github.com/anthropics/financial-services) | Apache-2.0 | none in licence (attributed to repository owner) | 9 | `skills/accounting/LICENSES/anthropics__financial-services.LICENSE` |
| [GAJETOso/financeskills](https://github.com/GAJETOso/financeskills) | MIT | Copyright (c) 2026 KOMVIA | 8 | `skills/accounting/LICENSES/GAJETOso__financeskills.LICENSE` |
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | MIT | Copyright (c) 2025 Alireza Rezvani | 8 | `skills/accounting/LICENSES/alirezarezvani__claude-skills.LICENSE` |
| [amit-voais/fortax-skills](https://github.com/amit-voais/fortax-skills) | Apache-2.0 | none in licence (attributed to repository owner) | 8 | `skills/accounting/LICENSES/amit-voais__fortax-skills.LICENSE` |
| [VincentChuWaiChow/vanguard-frontier-agentic](https://github.com/VincentChuWaiChow/vanguard-frontier-agentic) | Apache-2.0 | none in licence (attributed to repository owner) | 7 | `skills/accounting/LICENSES/VincentChuWaiChow__vanguard-frontier-agentic.LICENSE` |
| [adoptai/cpa-skills](https://github.com/adoptai/cpa-skills) | MIT | Copyright (c) 2026 AdoptAI | 6 | `skills/accounting/LICENSES/adoptai__cpa-skills.LICENSE` |
| [davidjelinekk/tax-skills-claude-code](https://github.com/davidjelinekk/tax-skills-claude-code) | MIT (standard MIT text plus an added tax-advice disclaimer) | Copyright (c) 2025-2026 | 5 | `skills/accounting/LICENSES/davidjelinekk__tax-skills-claude-code.LICENSE` |
| [hazlijohar95/skills](https://github.com/hazlijohar95/skills) | MIT | Copyright (c) 2026 Hazli Johar | 3 | `skills/accounting/LICENSES/hazlijohar95__skills.LICENSE` |
| [karbonhq/Public-Claude-Skills](https://github.com/karbonhq/Public-Claude-Skills) | MIT | Copyright (c) 2026 Karbon | 3 | `skills/accounting/LICENSES/karbonhq__Public-Claude-Skills.LICENSE` |
| [erp-mafia/accounted-skills](https://github.com/erp-mafia/accounted-skills) | MIT | Copyright (c) 2026 ERP MAFIA | 2 | `skills/accounting/LICENSES/erp-mafia__accounted-skills.LICENSE` |
| [ryanduguid/australian-accounting-skills](https://github.com/ryanduguid/australian-accounting-skills) | MIT | Copyright (c) 2026 Ryan Duguid | 2 | `skills/accounting/LICENSES/ryanduguid__australian-accounting-skills.LICENSE` |
| [AmolDerickSoans/gst-filing-india](https://github.com/AmolDerickSoans/gst-filing-india) | MIT | Copyright (c) 2026 Amol Derick Soans | 1 | `skills/accounting/LICENSES/AmolDerickSoans__gst-filing-india.LICENSE` |
| [ChipmunkRPA/bank-recon-skill](https://github.com/ChipmunkRPA/bank-recon-skill) | MIT | Copyright (c) 2026 ChipmunkRPA | 1 | `skills/accounting/LICENSES/ChipmunkRPA__bank-recon-skill.LICENSE` |
| [Denymbird/accounts-receivable-skills](https://github.com/Denymbird/accounts-receivable-skills) | MIT | Copyright (c) 2026 Paidnice | 1 | `skills/accounting/LICENSES/Denymbird__accounts-receivable-skills.LICENSE` |
| [EveryInc/charlie-cfo-skill](https://github.com/EveryInc/charlie-cfo-skill) | MIT | Copyright (c) 2026 Every | 1 | `skills/accounting/LICENSES/EveryInc__charlie-cfo-skill.LICENSE` |
| [NidheeshJain/itr-prep-skill](https://github.com/NidheeshJain/itr-prep-skill) | MIT | Copyright (c) 2026 Nidheesh Jain | 1 | `skills/accounting/LICENSES/NidheeshJain__itr-prep-skill.LICENSE` |
| [ajaysurie/tax-prep](https://github.com/ajaysurie/tax-prep) | MIT | Copyright (c) 2026 Ajay Surie | 1 | `skills/accounting/LICENSES/ajaysurie__tax-prep.LICENSE` |
| [anthropics/financial-services-plugins](https://github.com/anthropics/financial-services-plugins) | Apache-2.0 | none in licence (attributed to repository owner) | 1 | `skills/accounting/LICENSES/anthropics__financial-services-plugins.LICENSE` |
| [caseonix/canadian-regulatory-compliance](https://github.com/caseonix/canadian-regulatory-compliance) | MIT | Copyright (c) 2026 Srivatsa Kasagar | 1 | `skills/accounting/LICENSES/caseonix__canadian-regulatory-compliance.LICENSE` |
| [imadbadreddine7-bot/uae-vat-registration-skill](https://github.com/imadbadreddine7-bot/uae-vat-registration-skill) | MIT | Copyright (c) 2026 Squarezone Corporate Services LLC-FZ | 1 | `skills/accounting/LICENSES/imadbadreddine7-bot__uae-vat-registration-skill.LICENSE` |
| [joetobrien/irish-accounting-skill](https://github.com/joetobrien/irish-accounting-skill) | MIT | Copyright (c) 2026 Joe O'Brien / Web Digital Innovations | 1 | `skills/accounting/LICENSES/joetobrien__irish-accounting-skill.LICENSE` |
| [openaccountant/skills](https://github.com/openaccountant/skills) | MIT | Copyright (c) 2026 Open Accountant | 1 | `skills/accounting/LICENSES/openaccountant__skills.LICENSE` |
| [panaversity/agentfactory-business-plugins](https://github.com/panaversity/agentfactory-business-plugins) | Apache-2.0 | none in licence (attributed to repository owner) | 1 | `skills/accounting/LICENSES/panaversity__agentfactory-business-plugins.LICENSE` |
| [skills-il/accounting](https://github.com/skills-il/accounting) | MIT | Copyright (c) 2026 Skills IL (Yootech) | 1 | `skills/accounting/LICENSES/skills-il__accounting.LICENSE` |
| [skills-il/tax-and-finance](https://github.com/skills-il/tax-and-finance) | MIT | Copyright (c) 2026 Skills IL (Yootech) | 1 | `skills/accounting/LICENSES/skills-il__tax-and-finance.LICENSE` |
| [thriveventurelabs/accountsos-agent-plugin](https://github.com/thriveventurelabs/accountsos-agent-plugin) | MIT (standard MIT text plus an added UK tax-advice disclaimer) | Copyright (c) 2026 Thrive Venture Labs Limited | 1 | `skills/accounting/LICENSES/thriveventurelabs__accountsos-agent-plugin.LICENSE` |

### coreyhaines31/marketingskills (verbatim licence)

> MIT License
>
> Copyright (c) 2025 Corey Haines
>
> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all
> copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
> SOFTWARE.

Every other upstream repository reviewed, with its licence and why nothing was copied, is recorded in
[`docs/SOURCES.md`](docs/SOURCES.md). Repositories without a permissive licence are linked there and **not** copied.

## Illustrations and sample data

The screens in `skills/satva/docs/satva-guide-gif/examples/` and `examples/setup-guide-sample/` are neutral illustrations
with invented data. No real credentials, customers or third-party interfaces appear in them. Figures in the
example video briefs are labelled demo data. The figures in the Satva Ledger sizzle generator come from a
QuickBooks Online **sandbox** company and are labelled "Sandbox data" on screen; QuickBooks is a trademark of Intuit.
