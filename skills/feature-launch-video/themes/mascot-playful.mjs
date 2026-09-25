// Bright, rounded, mascot-driven theme — for consumer/SMB-friendly products that want warmth.
// This is the theme the Satva Ledger sizzle video used (pill shapes, bouncy character).
export default {
  name: "mascot-playful",
  useMascot: true,
  vars(brand) {
    return `--accent:${brand.accent};--ink:${brand.ink};--sub:#333333;--muted:#686868;--paper:${brand.paper};
--bub:#e4eff6;--ok:#2f7d4f;--warn:#b3261e;--font:${brand.font || "system-ui"}`;
  },
  css: `
.ch{background:radial-gradient(1400px 700px at 50% 118%,color-mix(in srgb,var(--accent) 20%,transparent),transparent 70%),var(--paper)}
.card{background:#fff;border-radius:32px;box-shadow:0 26px 70px rgba(20,60,90,.14);padding:44px 52px}
.chip{display:inline-flex;align-items:center;gap:16px;background:#fff;border-radius:999px;padding:12px 32px 12px 12px;box-shadow:0 10px 34px rgba(20,60,90,.12);font-size:32px;font-weight:600}
.ico{width:128px;height:128px;border-radius:50%;background:var(--accent);display:flex;align-items:center;justify-content:center;flex:none}
.ico svg{width:70px;height:70px;fill:none;stroke:#fff;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.btn{display:inline-flex;align-items:center;justify-content:center;height:96px;border-radius:999px;font-size:38px;font-weight:700}
.allow{background:var(--accent);color:#fff;width:300px}.deny{background:#eef2f5;color:var(--muted);width:240px}
.bub{color:var(--sub);background:var(--bub);border-radius:34px;padding:30px 40px;font-size:40px;line-height:1.28;font-weight:600}
.mas{z-index:5}
`,
};
