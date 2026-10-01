# skills/satva: Satva house skills

Skills about **how Satva itself works and what Satva-branded output looks like**. They are
useful to anyone at Satva, whatever their department.

| Group | What lives here |
|---|---|
| `docs/` | Satva-format documents and setup guides (`satva-doc`, `satva-guide-gif`) |
| `video/` | Satva product videos |
| `practice/` | How Satva runs accounting work: practice vs controller, the context interview before answering from a live ledger |
| `presentations/` | The Satva PowerPoint house style, with its helper scripts |

## Rule for adding a house skill

A skill belongs here only if it is **Satva-specific and reusable across the org**. Generic
domain skills go in their own department (accounting, marketing, seo).

1. License is `Satva-original` (or an allowed permissive licence with attribution).
2. The repo is public. No secrets, tokens, private hostnames or IDs, internal URLs, personal
   contact details, client names or client data. If it cannot be made safe, do not publish it.
3. It must stand alone: no paths on one person's machine, no reliance on files that are not
   in the repo. Reference internal assets by name and say who to ask for them.
4. Folder name equals frontmatter `name`, unique across the repo; `metadata.department` is
   `satva`; run `python scripts/validate.py skills/satva` before opening the PR.
5. Record anything you evaluated but withheld in `SOURCES-<tag>.md` with the reason.
