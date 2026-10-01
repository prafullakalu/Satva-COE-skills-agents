// Dark, glow-accented theme — for AI/platform/developer-tool features that want to feel premium
// and high-tech. No mascot; glass cards, soft accent glow, tighter tracking.
export default {
  name: "cinematic-dark",
  useMascot: false,
  vars(brand) {
    return `--accent:${brand.accent};--ink:#f2f4f7;--sub:#c7cdd6;--muted:#8992a1;--paper:#0b0e14;
--bub:#161b26;--ok:#3ddc84;--warn:#ff6b6b;--font:${brand.font || "system-ui"}`;
  },
  css: `
.ch{background:radial-gradient(1200px 700px at 50% 110%,color-mix(in srgb,var(--accent) 30%,transparent),transparent 70%),var(--paper)}
.card{background:rgba(255,255,255,.045);border:1px solid rgba(255,255,255,.09);border-radius:22px;box-shadow:0 0 60px color-mix(in srgb,var(--accent) 20%,transparent);padding:44px 52px;backdrop-filter:blur(6px)}
.chip{display:inline-flex;align-items:center;gap:16px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);border-radius:999px;padding:12px 32px 12px 12px;font-size:32px;font-weight:600;color:var(--ink)}
.ico{width:120px;height:120px;border-radius:26px;background:color-mix(in srgb,var(--accent) 85%,#000);display:flex;align-items:center;justify-content:center;flex:none;box-shadow:0 0 40px color-mix(in srgb,var(--accent) 45%,transparent)}
.ico svg{width:64px;height:64px;fill:none;stroke:#fff;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.btn{display:inline-flex;align-items:center;justify-content:center;height:92px;border-radius:14px;font-size:36px;font-weight:700}
.allow{background:var(--accent);color:#0b0e14;width:300px}.deny{background:rgba(255,255,255,.08);color:var(--muted);width:240px}
.bub{color:var(--sub);background:var(--bub);border-radius:18px;padding:28px 38px;font-size:38px;line-height:1.28;font-weight:600;border:1px solid rgba(255,255,255,.06)}
`,
};
