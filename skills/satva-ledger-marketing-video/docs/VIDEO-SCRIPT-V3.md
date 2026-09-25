# Satva Ledger — Video Script V3 (Satva Solutions brand, 45s hero)

Drafted 2026-09-21. Builds on V2 (`VIDEO-SCRIPT-V2.md`, rendered). Brand source: satvasolutions.com pages fetched 2026-09-21 (fetch returned partial pages; re-verify against the live site before publishing). Nothing here is rendered yet.

## Brand truth (quote only these)

From satvasolutions.com (verbatim):
- "Satva Solutions is a globally recognized Fintech Software Development Company and premier Custom Accounting, and ERP Integration Company for CPAs, SaaS companies" (home / about-us; meta says "Since 2013").
- "Your finance team should spend its time on decisions, not data entry." (accounting-integration page)
- "A misclassified transaction creates a compliance problem with real consequences: fines, audit findings, and harm to reputation." (same page)
- Mission (search summary, verify on `/vision-values`): "provide value-added services to their clients globally". Core value: customer centricity.
- House colours: blue `#1194D2`, font Muli/Mulish (from the `satva-ppt` skill). Logo: white "SATVA SOLUTIONS" on blue (banner at `skills/satva-guide-gif/assets/satva-header.png` in this repo; a clean SVG/transparent PNG is still needed).

Do NOT use named client testimonials without written permission. Do NOT put "since 2013" on screen until confirmed.

## Positioning (agreed direction)

Not "replaces your accountant" (FTC substantiation risk; your own copy says it does not). Use:
**"Your books, kept intact. Agents do the bookkeeping. You approve."**
Bridge to Satva Solutions' own line: decisions, not data entry.

## Hero beats (45s, 16:9 first, 9:16 cutdowns after)

| Time | Beat | Visual | VO (ElevenLabs v3 tags) | Caption |
|---|---|---|---|---|
| 0–5 | Stakes | Licensed stock: accountant late at a desk, then push into a QuickBooks Online transaction list | [calm, serious] "One misclassified transaction can mean fines, audit findings, and a damaged reputation." | "Real consequences." |
| 5–12 | Solution | Satva Solutions logo lockup, Satva Ledger UI (own app recording), QuickBooks® Online named in text | "So we built agents that read your QuickBooks Online books. One analyzes. One reviews, without seeing the first one's work." | "Two agents. Never compared notes." |
| 12–22 | Proof 1 | The $900 "Monthly Payment" card, NEEDS INFORMATION stamp | [pause] "They found a nine hundred dollar payment nobody could explain. And refused to guess." | "It won't guess." |
| 22–32 | Proof 2 | Txn 89 recode, 55% confidence, Approve, read-back (SyncToken 1 to 2) | "The rest, they propose, with how sure they are. You approve. Then they read the record back." | "You approve. It verifies." |
| 32–40 | Payoff | Split: finance team in a meeting, licensed stock, over the Ledger UI | [warm] "Your finance team gets its time back for decisions, not data entry." | "Decisions, not data entry." |
| 40–45 | CTA | Satva Solutions logo, blue end card | "Satva Ledger. Your books, kept intact." | "It asks before it touches your books." |

Only list agent tasks on screen that are verified as wired into the live app (categorize, aging review, bank sync, year-end). Unverified ones stay off screen.

## Voice, music, SFX (ElevenLabs skills, installed)

- Voice: `eleven_v3`, start with Daniel (`onwK4e9ZLuTAKqWW03F9`, authoritative) or George (`JBFqnCBsd6RMkjVDRZzb`, narrative); audition 3 and pick. Best option for trust: a real Satva voice via consented voice clone (needs a plan that includes it).
- Direction: calm, credible, unhurried; stability around 0.5; no hype.
- Music: ElevenLabs `music` skill, prompt "restrained corporate technology underscore, no vocals, 45s, soft build, warm, confident". Duck 12 dB under VO, fade out over the last 0.8s.
- SFX: keep the bundled Pixabay set for clicks/whooshes/impact; add via `sound-effects` only if a moment needs more.
- Licence: ElevenLabs free plan is non-commercial and needs attribution; a paid plan is required for this video.

## Build route

- Renderer: keep HyperFrames (Apache-2.0, already built). Remotion is free only up to 3 people; Satva Solutions would need the $25/seat/month Company licence. The Remotion skills are installed and their patterns (captions, SaaS-video pacing) are reusable either way.
- Assets to add: clean Satva logo; own-app screen recording (Playwright); 3 to 5 licensed Pexels/Pixabay clips; QuickBooks® mention as text unless Intuit grants screenshot permission ("Reprinted with permission © Intuit Inc." is required on any Intuit screenshot).

## Blockers (need the user)

1. ElevenLabs paid account and `ELEVENLABS_API_KEY` saved in a local `.env` (never pasted in chat).
2. Clean Satva logo file.
3. Confirm the safer positioning line.
4. Optional: Intuit permission for real QBO screenshots; Remotion licence if Remotion is required.
