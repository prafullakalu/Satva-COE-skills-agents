// Light, paper/ledger theme — for finance/ops/B2B features. No mascot; straight lines, generous
// whitespace, monospace numerals. Closest to the Satva Ledger V3 hero build.
export default {
  name: "ledger-clean",
  useMascot: false,
  vars(brand) {
    return `--accent:${brand.accent};--ink:${brand.ink};--sub:#333333;--muted:#686868;--paper:${brand.paper};
--bub:#eef2f5;--ok:#2f7d4f;--warn:#b3261e;--font:${brand.font || "system-ui"}`;
  },
  css: `
.ch{background:radial-gradient(1200px 640px at 50% 116%,color-mix(in srgb,var(--accent) 14%,transparent),transparent 70%),var(--paper)}
.card{background:#fff;border-radius:20px;box-shadow:0 20px 56px rgba(20,40,60,.10);padding:44px 52px;border:1px solid rgba(0,0,0,.04)}
.chip{display:inline-flex;align-items:center;gap:16px;background:#fff;border-radius:999px;padding:12px 32px 12px 12px;box-shadow:0 10px 30px rgba(20,40,60,.10);font-size:32px;font-weight:600}
.ico{width:120px;height:120px;border-radius:50%;background:var(--accent);display:flex;align-items:center;justify-content:center;flex:none}
.ico svg{width:64px;height:64px;fill:none;stroke:#fff;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.btn{display:inline-flex;align-items:center;justify-content:center;height:92px;border-radius:12px;font-size:36px;font-weight:700}
.allow{background:var(--accent);color:#fff;width:300px}.deny{background:#eef2f5;color:var(--muted);width:240px}
.bub{color:var(--sub);background:var(--bub);border-radius:16px;padding:28px 38px;font-size:38px;line-height:1.28;font-weight:600}
`,
};
