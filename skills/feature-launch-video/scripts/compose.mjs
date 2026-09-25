#!/usr/bin/env node
// Generic HyperFrames composer: brief.json + a theme -> a renderable index.html + timing.json.
// This is the reusable "skill" itself — nothing in here is specific to any one product.
//
// Usage: node compose.mjs <path-to-brief.json> <output-dir>
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { ICON, VISUAL_ICON } from "./icons.mjs";
import { makeMascot } from "./mascot.mjs";

const briefPath = process.argv[2];
const outDir = process.argv[3];
if (!briefPath || !outDir) {
  console.error("usage: node compose.mjs <brief.json> <output-dir>");
  process.exit(1);
}
const brief = JSON.parse(fs.readFileSync(briefPath, "utf8"));
const themePath = path.join(import.meta.dirname, "..", "themes", `${brief.theme || "ledger-clean"}.mjs`);
const themeMod = await import(pathToFileURL(themePath).href);
const theme = themeMod.default;

// ---------- compliance gate: never let a restricted claim reach the page ----------
const neverWords = (brief.claims?.never || ["autonomous", "100% accurate", "zero errors", "replaces"]).map((w) => w.toLowerCase());
const allText = [brief.message, brief.endCard?.tagline, brief.endCard?.cta, ...(brief.flow || []).map((f) => f.line)].join(" \n ").toLowerCase();
const hits = neverWords.filter((w) => allText.includes(w));
if (hits.length) {
  console.error(`compose.mjs: brief.json contains a restricted claim (${hits.join(", ")}). Edit the copy in brief.json and rerun — this is a hard gate, not a warning.`);
  process.exit(1);
}
const grounded = (brief.groundedFactsSource || "").toLowerCase();
const isDemo = !grounded || grounded.includes("demo") || grounded.includes("not real") || grounded.includes("example");

// ---------- geometry ----------
const DIMS = { "16:9": [1920, 1080], "9:16": [1080, 1920], "1:1": [1080, 1080] };
const [W, H] = DIMS[brief.aspect] || DIMS["16:9"];
const portrait = W < H;
const fs_ = portrait ? 0.82 : 1; // font-scale for tighter vertical layouts

// ---------- beat grid (for satisfying, rhythmic cuts — not tied to any specific track) ----------
const bpm = brief.music?.bpm || 112;
const beatSec = 60 / bpm;
const snap = (t) => Math.round(t / beatSec) * beatSec;

const DUR = brief.durationTarget || 40;
const introDur = snap(Math.max(3, DUR * 0.12));
const endDur = snap(Math.max(4, DUR * 0.13));
const steps = brief.flow || [];
const bodyDur = Math.max(1, DUR - introDur - endDur);
const perStep = snap(Math.max(3.5, bodyDur / Math.max(1, steps.length)));
let cursor = introDur;
const sceneWindows = steps.map((_, i) => {
  const start = cursor, end = i === steps.length - 1 ? DUR - endDur : cursor + perStep;
  cursor = end;
  return { start: +start.toFixed(3), end: +end.toFixed(3) };
});
const totalDur = +(cursor + endDur).toFixed(3); // may drift slightly from DUR after snapping — that's fine

// ---------- css ----------
const css = `
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:${W}px;height:${H}px;overflow:hidden;background:var(--paper)}
body{font-family:var(--font),system-ui,sans-serif;color:var(--ink)}
.mono{font-variant-numeric:tabular-nums lining-nums}
.abs{position:absolute}
.tt{left:0;width:${W}px;text-align:center}
.tt .l1{font-size:${72 * fs_}px;font-weight:700;letter-spacing:-.03em;line-height:1.08}
.tt .l2{font-size:${52 * fs_}px;font-weight:600;color:var(--muted);margin-top:14px}
.row{display:flex;justify-content:space-between;align-items:baseline;gap:28px;padding:18px 0;border-top:2px solid rgba(0,0,0,.06);font-size:${34 * fs_}px}
.row .a{font-weight:600}.row .b{font-weight:700}
.k{font-size:${22 * fs_}px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.big{font-size:${118 * fs_}px;font-weight:700;letter-spacing:-.03em}
.label{font-size:${30 * fs_}px;color:var(--muted);font-weight:600;margin-top:8px}
.hide{opacity:0}
.note{position:absolute;left:${portrait ? 40 : 120}px;bottom:26px;font-size:${20 * fs_}px;color:var(--muted);font-weight:600;z-index:40;max-width:${W - (portrait ? 80 : 240)}px}
.note i{display:inline-block;width:10px;height:10px;border-radius:50%;background:var(--warn);margin-right:8px}
.chatRow{display:flex}.chatRow.you{justify-content:flex-end}
.chatBub{display:inline-block;background:#fff;border-radius:22px;padding:22px 30px;font-size:${32 * fs_}px;font-weight:600;color:var(--ink);box-shadow:0 14px 40px rgba(0,0,0,.10);max-width:80%}
.chatBub.you{background:var(--accent);color:#fff}
.cmp{flex:1;text-align:center;padding:32px 26px}
.cmpT{font-size:${34 * fs_}px;font-weight:700;margin:10px 0 6px}
.cmp.win{border:3px solid var(--accent)}
${theme.css}
`;

// ---------- helpers ----------
const html = [];
const tw = [];
const aud = [];

// One or more characters. `brief.characters` (optional): { id: {name, variant, ribbon, voiceId} }.
// Without it, falls back to a single mascot from brief.brand.character/ribbon (old, still-valid shape).
const charIds = brief.characters ? Object.keys(brief.characters) : ["_default"];
const chars = Object.fromEntries(charIds.map((id) => {
  const c = brief.characters ? brief.characters[id] : { variant: brief.brand.character, ribbon: brief.brand.ribbon };
  return [id, theme.useMascot ? makeMascot(tw, brief.brand.accent, brief.brand.ink, undefined, c.variant || "default", c.ribbon) : {}];
}));
const charFor = (step) => chars[step?.character && brief.characters?.[step.character] ? step.character : charIds[0]];
const introCharId = charIds[0];
const endCharId = steps.length && brief.characters?.[steps[steps.length - 1].character] ? steps[steps.length - 1].character : charIds[0];

// small deterministic VFX (no Math.random — HyperFrames compositions must render the same every time)
const burst = (id, x, y, t, color, n = 8) => {
  const parts = [];
  for (let i = 0; i < n; i++) {
    const ang = (i / n) * Math.PI * 2, dx = (Math.cos(ang) * 95).toFixed(1), dy = (Math.sin(ang) * 95).toFixed(1);
    const eid = `${id}-p${i}`;
    parts.push(`<div id="${eid}" class="abs" style="left:${x}px;top:${y}px;width:11px;height:11px;border-radius:50%;background:${color};opacity:0"></div>`);
    tw.push(`tl.fromTo("#${eid}",{opacity:1,x:0,y:0,scale:1},{opacity:0,x:${dx},y:${dy},scale:.3,duration:.65,ease:"power2.out"},${t.toFixed(3)});`);
  }
  return parts.join("");
};
const pulseRing = (id, x, y, t, color, size = 200) => {
  const el = `<div id="${id}" class="abs" style="left:${x - size / 2}px;top:${y - size / 2}px;width:${size}px;height:${size}px;border-radius:50%;border:4px solid ${color};opacity:0"></div>`;
  tw.push(`tl.fromTo("#${id}",{opacity:.75,scale:.3},{opacity:0,scale:1.5,duration:.9,ease:"power2.out"},${t.toFixed(3)});`);
  return el;
};

let sfxN = 0;
const sfx = (file, t, vol, dur) => aud.push(`<audio id="sfx${++sfxN}" class="clip" src="assets/sfx/${file}" data-start="${+t.toFixed(3)}" data-duration="${dur}" data-track-index="${5 + (sfxN % 3)}" data-volume="${vol}"></audio>`);
const pop = (t) => sfx("pop.mp3", t, 0.22, 0.72);
const swoosh = (t) => sfx("swoosh.mp3", t, 0.3, 0.8);
const IN = (sel, t) => tw.push(`tl.from("${sel}",{opacity:0,y:26,duration:.45,ease:"power2.out"},${(+t).toFixed(3)});`);
const scene = (id, a, b, cls, body) => html.push(`<div class="clip ${cls} ch" id="${id}" data-start="${a}" data-duration="${+(b - a).toFixed(3)}" data-track-index="0">${body}</div>`);
const noteHtml = () => (isDemo ? `<div class="note"><i></i>CONCEPT / NOT FINAL — ${brief.groundedFactsSource || "example data, not from a real run"}</div>` : "");

function renderVisual(step, id) {
  const d = step.data || {};
  if (step.visual === "stat") {
    return `<div id="${id}" class="abs card" style="left:${portrait ? 90 : W / 2 - 380}px;top:${portrait ? 620 : 340}px;width:${portrait ? W - 180 : 760}px;text-align:center">
      <div class="big">${d.big}</div><div class="label">${d.label || ""}</div>${d.sub ? `<div class="label">${d.sub}</div>` : ""}</div>`;
  }
  if (step.visual === "approval") {
    return `<div id="${id}" class="abs card" style="left:${portrait ? 90 : W / 2 - 380}px;top:${portrait ? 620 : 340}px;width:${portrait ? W - 180 : 760}px">
      <div class="k">Asks first</div><div style="font-size:${38 * fs_}px;font-weight:700;margin:14px 0 28px">${d.prompt}</div>
      <div style="display:flex;gap:22px"><span class="btn deny">Deny</span><span id="${id}-allow" class="btn allow">${d.allow || "Allow"}</span></div></div>`;
  }
  if (step.visual === "chat") {
    // a two-line exchange: what someone asked, what it answered — {user, agent}
    return `<div id="${id}" class="abs" style="left:${portrait ? 60 : W / 2 - 420}px;top:${portrait ? 560 : 300}px;width:${portrait ? W - 120 : 840}px">
      <div class="chatRow you"><span class="chatBub you">${d.user}</span></div>
      <div class="chatRow" style="margin-top:22px"><span class="chatBub">${d.agent}</span></div></div>`;
  }
  if (step.visual === "compare") {
    // two mini-cards side by side — {before:[title,sub], after:[title,sub]}
    const [bt, bs] = d.before || [], [at, as_] = d.after || [];
    return `<div id="${id}" class="abs" style="left:${portrait ? 60 : W / 2 - 420}px;top:${portrait ? 600 : 320}px;width:${portrait ? W - 120 : 840}px;display:flex;gap:24px">
      <div class="card cmp"><div class="k">Before</div><div class="cmpT">${bt || ""}</div><div class="label">${bs || ""}</div></div>
      <div class="card cmp win"><div class="k">${brief.product}</div><div class="cmpT">${at || ""}</div><div class="label">${as_ || ""}</div></div></div>`;
  }
  // "card" / "list" / default — kicker + field rows, the most common shape
  const rows = (d.fields || []).map(([a, b]) => `<div class="row"><span class="a">${a}</span><span class="b mono">${b}</span></div>`).join("");
  return `<div id="${id}" class="abs card" style="left:${portrait ? 90 : W / 2 - 380}px;top:${portrait ? 620 : 300}px;width:${portrait ? W - 180 : 780}px">
    <div class="k">${d.kicker || ""}</div>${rows}</div>`;
}

// ---------- intro ----------
{
  const cols = portrait ? 5 : 9, rows = portrait ? 6 : 5, iconKeys = Object.keys(ICON);
  const icons = [];
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
    const n = r * cols + c, size = portrait ? 78 : 96, gap = portrait ? 170 : 200;
    const x = 70 + c * gap + (r % 2) * (gap / 2), y = 60 + r * (portrait ? 150 : 190);
    icons.push(`<div class="abs wi" style="left:${x}px;top:${y}px;width:${size}px;height:${size}px;border-radius:22px;background:#fff;box-shadow:0 10px 30px rgba(0,0,0,.10);display:flex;align-items:center;justify-content:center;opacity:.9"><div class="ico" style="width:${size * 0.6}px;height:${size * 0.6}px;background:${n % 3 === 0 ? "var(--accent)" : "color-mix(in srgb,var(--accent) 22%,#fff)"}">${ICON[iconKeys[n % iconKeys.length]].replace("<svg", `<svg style="width:${size * 0.34}px;height:${size * 0.34}px;${n % 3 === 0 ? "" : "stroke:var(--accent)"}"`)}</div></div>`);
  }
  const introMx = portrait ? W / 2 - 100 : W * 0.42, introMy = portrait ? 60 : 100, introMw = portrait ? 190 : 230;
  const { mascot: iMascot, mMood: iMood, mIn: iIn, mBob: iBob, mBlink: iBlink } = chars[introCharId];
  const mascotTag = theme.useMascot ? iMascot("mI", introMx, introMy, introMw) : "";
  scene("intro", 0, introDur, "", `
    ${mascotTag}<div id="wall" class="abs" style="left:0;top:0;width:${W}px;height:${H}px">${icons.join("")}</div>
    <div id="veil" class="abs" style="left:0;top:0;width:${W}px;height:${H}px;background:var(--paper);opacity:0"></div>
    <div id="i1" class="abs tt" style="top:${H * 0.42}px"><div class="l1" style="font-size:${(portrait ? 58 : 86) * fs_}px">${brief.product}</div></div>
    <div id="i2" class="abs tt" style="top:${H * 0.4}px;padding:0 ${portrait ? 60 : 240}px"><div class="l1" style="font-size:${(portrait ? 50 : 78) * fs_}px;line-height:1.12">${brief.message}</div></div>
    ${theme.useMascot ? burst("iBurst", introMx + introMw / 2, introMy + introMw / 2, snap(introDur * 0.28), "var(--accent)") : ""}`);
  const t1 = snap(introDur * 0.28), t2 = snap(introDur * 0.62);
  tw.push(`tl.from(".wi",{opacity:0,scale:.6,duration:.5,stagger:{each:.025,from:"center"},ease:"back.out(1.6)"},0.05);`);
  tw.push(`tl.to("#wall",{y:-30,duration:${introDur},ease:"none"},0);`);
  tw.push(`tl.to("#veil",{opacity:.9,duration:.4},${t1});`);
  tw.push(`tl.from("#i1",{opacity:0,scale:.9,duration:.5,ease:"power2.out"},${t1 + 0.05});`);
  tw.push(`tl.to("#i1",{opacity:0,duration:.25},${t2 - 0.05});`);
  tw.push(`tl.from("#i2",{opacity:0,y:26,duration:.5,ease:"power2.out"},${t2});`);
  tw.push(`tl.fromTo("#i2",{scale:1},{scale:1.045,duration:.16,yoyo:true,repeat:1,ease:"power2.out"},${(t2 + 0.35).toFixed(3)});`); // hook punch
  pop(t1); pop(t2); sfx("chime.mp3", t2 + 0.35, 0.25, 1.2);
  if (theme.useMascot) { iIn("mI", t1); iBob("mI", t1, introDur); iMood("mI", t2, "happy"); iBlink("mI", [t1 + 1.2]); }
}

// ---------- one scene per real user-flow step ----------
steps.forEach((step, i) => {
  const { start: a, end: b } = sceneWindows[i];
  const id = `s${i}`;
  const icon = ICON[step.icon] ? step.icon : (VISUAL_ICON[step.visual] || "tray");
  const { mascot: sMascot, mMood: sMood, mIn: sIn, mBob: sBob, mBlink: sBlink, mHop: sHop } = charFor(step);
  const mx = portrait ? 60 : 160, my = portrait ? 120 : 180, mw = portrait ? 150 : 170;
  const mascotTag = theme.useMascot ? sMascot(`m${i}`, mx, my, mw) : "";
  const vx = portrait ? 90 + (W - 180) / 2 : W / 2 - 380 + 390, vy = (portrait ? 620 : 340) + 130; // visual-card center, approx
  scene(id, a, b, "", `
    <div id="${id}-t" class="abs tt" style="top:${portrait ? 170 : 130}px;padding:0 ${portrait ? 60 : 240}px">
      <span class="ico" style="display:inline-flex;vertical-align:middle;margin-right:18px">${ICON[icon]}</span>
      <span class="l1" style="display:inline-block;vertical-align:middle;font-size:${(portrait ? 44 : 60) * fs_}px">${step.step}</span>
    </div>
    ${mascotTag}
    ${renderVisual(step, `${id}-v`)}
    <div id="${id}-line" class="abs tt" style="top:${portrait ? 1180 : 900}px;padding:0 ${portrait ? 60 : 300}px;font-size:${(portrait ? 34 : 40) * fs_}px;font-weight:600;color:var(--sub)">${step.line}</div>
    ${step.visual === "stat" ? pulseRing(`${id}-ring`, vx, vy, a + 1.2, "var(--accent)") : ""}
    ${step.visual === "approval" ? burst(`${id}-burst`, vx, vy, a + 1.48, "var(--ok)") : ""}
    ${noteHtml()}`);
  const tIn = a + 0.15;
  swoosh(a - 0.05);
  IN(`#${id}-t`, tIn);
  IN(`#${id}-v`, tIn + 0.35);
  IN(`#${id}-line`, tIn + 0.7);
  pop(tIn + 0.35);
  if (theme.useMascot) {
    sIn(`m${i}`, tIn); sBob(`m${i}`, tIn, b); sMood(`m${i}`, tIn, "work"); sBlink(`m${i}`, [tIn + 1.5]);
    if (step.visual === "stat" || step.visual === "approval") { sMood(`m${i}`, tIn + 1.2, "happy"); sHop(`m${i}`, tIn + 1.2); }
  }
  if (step.visual === "approval") {
    const tapT = a + 1.4;
    tw.push(`tl.to("#${id}-v-allow",{scale:.94,duration:.08},${tapT.toFixed(3)});tl.to("#${id}-v-allow",{scale:1,duration:.15},${(tapT + 0.08).toFixed(3)});`);
    sfx("click.mp3", tapT, 0.35, 0.36);
  }
});

// ---------- end card ----------
{
  const a = totalDur - endDur;
  const logo = brief.brand.logo ? `<img id="lg" class="abs" src="${brief.brand.logo}" alt="${brief.product}" style="left:${W / 2 - 260}px;top:${portrait ? 500 : 170}px;width:520px" />` : "";
  const { mascot: eMascot, mIn: eIn, mBob: eBob, mMood: eMood, mWave: eWave } = chars[endCharId];
  const mascotTag = theme.useMascot ? eMascot("mX", W / 2 - 90, portrait ? 900 : 560, portrait ? 170 : 220) : "";
  scene("end", a, totalDur, "", `
    ${logo}
    <div id="e1" class="abs tt" style="top:${portrait ? 640 : 500}px"><div class="l1" style="font-size:${(portrait ? 62 : 90) * fs_}px">${brief.product}</div></div>
    <div id="e2" class="abs tt" style="top:${portrait ? 760 : 650}px"><div class="l1" style="font-size:${(portrait ? 38 : 56) * fs_}px;color:var(--accent)">${brief.endCard?.tagline || ""}</div></div>
    ${mascotTag}
    <div id="e3" class="abs tt" style="top:${portrait ? 860 : 760}px"><div class="l2" style="font-size:${(portrait ? 26 : 34) * fs_}px">${brief.endCard?.cta || ""}</div></div>
    ${noteHtml()}`);
  tw.push(`tl.from("#e1",{opacity:0,y:24,duration:.5,ease:"power2.out"},${(a + 0.3).toFixed(3)});`);
  tw.push(`tl.from("#e2",{opacity:0,y:20,duration:.5,ease:"power2.out"},${(a + 1.0).toFixed(3)});`);
  tw.push(`tl.from("#e3",{opacity:0,duration:.6},${(a + 1.8).toFixed(3)});`);
  tw.push(`tl.to("#end",{opacity:0,duration:.8},${(totalDur - 0.8).toFixed(3)});`);
  swoosh(a - 0.05);
  if (theme.useMascot) { eIn("mX", a + 0.4); eBob("mX", a + 0.4, totalDur); eMood("mX", a + 0.4, "happy"); eWave("mX", a + 1.2); }
}

// ---------- write page ----------
const page = `<!doctype html>
<html lang="en" data-resolution="${portrait ? "portrait" : "landscape"}"><head><meta charset="UTF-8"/><meta name="viewport" content="width=${W}, height=${H}"/>
<script src="assets/gsap.min.js"></script><style>:root{${theme.vars(brief.brand)}}${css}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="${totalDur}" data-width="${W}" data-height="${H}">
${html.join("\n")}
<audio id="music" class="clip" src="assets/music.wav" data-start="0" data-duration="${totalDur}" data-track-index="4" data-volume="1" data-timeline-role="music"></audio>
${aud.join("\n")}
</div>
<script>
window.__timelines = window.__timelines || {};
const tl = gsap.timeline({ paused: true });
${tw.join("\n")}
window.__timelines["main"] = tl;
tl.seek(0);
</script></body></html>
`;
fs.mkdirSync(outDir, { recursive: true });
fs.mkdirSync(path.join(outDir, "assets", "sfx"), { recursive: true });
// GSAP carries GreenSock's own licence, so it is fetched once (and cached) instead of being shipped in this repo.
const gsapCache = path.join(import.meta.dirname, "shared-assets", "gsap.min.js");
if (!fs.existsSync(gsapCache)) {
  const res = await fetch("https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js");
  if (!res.ok) { console.error(`compose.mjs: could not download GSAP (HTTP ${res.status}). Check your network and rerun.`); process.exit(1); }
  fs.mkdirSync(path.dirname(gsapCache), { recursive: true });
  fs.writeFileSync(gsapCache, Buffer.from(await res.arrayBuffer()));
}
fs.copyFileSync(gsapCache, path.join(outDir, "assets", "gsap.min.js"));
fs.writeFileSync(path.join(outDir, "index.html"), page);
fs.copyFileSync(briefPath, path.join(outDir, "brief.json"));

// ---------- timing.json: the only thing the audio pipeline is allowed to read ----------
const timing = {
  durationSec: totalDur, bpm, beatSec, aspect: brief.aspect || "16:9", width: W, height: H,
  intro: { start: 0, end: introDur },
  scenes: steps.map((s, i) => ({ id: `s${i}`, step: s.step, line: s.line, visual: s.visual, character: s.character || null, ...sceneWindows[i] })),
  end: { start: totalDur - endDur, end: totalDur },
  demo: isDemo,
};
fs.writeFileSync(path.join(outDir, "timing.json"), JSON.stringify(timing, null, 1));
console.log(`wrote ${outDir}/index.html (${(page.length / 1024).toFixed(0)} KB) + timing.json — ${totalDur.toFixed(1)}s, theme ${theme.name}, ${steps.length} flow steps, sfx ${sfxN}${isDemo ? " [CONCEPT/DEMO DATA]" : ""}`);
