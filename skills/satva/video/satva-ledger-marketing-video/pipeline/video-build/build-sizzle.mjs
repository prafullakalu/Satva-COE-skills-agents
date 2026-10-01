// Builds satva-sizzle/index.html: an 82.56s picture edit on a 115 bpm beat grid (beat k -> 0.22 + 0.522*k seconds).
// Structure: intro -> six "AI that ... for you" chapters -> all-in-one -> end card.
// Every figure on screen is DEMO DATA from a QuickBooks Online sandbox and is labelled as such. Replace them with your own real, sourced facts.
import fs from "node:fs";
import path from "node:path";
import { makeMascot } from "./sizzle-mascot.mjs";

const out = path.join(import.meta.dirname, "satva-sizzle", "index.html");
const DUR = 82.56;
const T = (k) => +(0.22 + 0.522 * k).toFixed(3); // musical beat k -> seconds (115 bpm grid from beat detection)

const ICON = {
  tray: '<svg viewBox="0 0 24 24"><path d="M12 3v11m0 0l-4-4m4 4l4-4M4 15v4h16v-4"/></svg>',
  scale: '<svg viewBox="0 0 24 24"><path d="M12 4v16M6 20h12M5 8h14M5 8l-3 7a3.5 3.5 0 007 0zM19 8l-3 7a3.5 3.5 0 007 0z"/></svg>',
  users: '<svg viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.6 3-6 6.5-6s6.5 2.4 6.5 6M16 5a3.5 3.5 0 010 7M18 14c2.5.6 4 2.6 4 6"/></svg>',
  tag: '<svg viewBox="0 0 24 24"><path d="M3 12V4h8l10 10-8 8zM7.5 8.5h.01"/></svg>',
  chart: '<svg viewBox="0 0 24 24"><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></svg>',
  shield: '<svg viewBox="0 0 24 24"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6zM8.5 12l2.5 2.5 4.5-5"/></svg>',
  link: '<svg viewBox="0 0 24 24"><path d="M10 14a4 4 0 005.7 0l3-3a4 4 0 00-5.7-5.7l-1 1M14 10a4 4 0 00-5.7 0l-3 3a4 4 0 005.7 5.7l1-1"/></svg>',
};
const WALL = ["tray", "scale", "users", "tag", "chart", "shield", "link"];

const chapters = [
  { id: "A", k: 16, icon: "tray", verb: "posts your entries" },
  { id: "B", k: 36, icon: "scale", verb: "catches what<br/>doesn't add up" },
  { id: "C", k: 56, icon: "users", verb: "tracks who owes you" },
  { id: "D", k: 76, icon: "tag", verb: "finds the credits<br/>you forgot" },
  { id: "E", k: 96, icon: "chart", verb: "reports on your business" },
  { id: "F", k: 116, icon: "shield", verb: "asks before it acts" },
];
const G = 136, END = 150;
const SYS = ["QuickBooks&reg; Online", "Xero", "Zoho Books", "Sage", "NetSuite", "SAP", "Business Central", "Acumatica"];

const css = `
@font-face{font-family:"Mulish";font-weight:400;src:url("assets/fonts/mulish-latin-400-normal.woff2") format("woff2")}
@font-face{font-family:"Mulish";font-weight:600;src:url("assets/fonts/mulish-latin-600-normal.woff2") format("woff2")}
@font-face{font-family:"Mulish";font-weight:700;src:url("assets/fonts/mulish-latin-700-normal.woff2") format("woff2")}
@font-face{font-family:"Geist Mono";font-weight:500;src:url("assets/fonts/GeistMono-Medium.woff2") format("woff2")}
:root{--blue:#1d83b8;--deep:#1d83b8;--ink:#111111;--sub:#333333;--muted:#686868;--grey:#6d6d6d;--bg:#f7fafd;--bub:#e4eff6;--ok:#2f7d4f;--warn:#b3261e;--amber:#1d83b8}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1920px;height:1080px;overflow:hidden;background:var(--bg)}
body{font-family:"Mulish",system-ui,sans-serif;color:var(--ink)}
.mono{font-family:"Geist Mono",monospace;font-variant-numeric:tabular-nums lining-nums}
.abs{position:absolute}
.ch{background:radial-gradient(1400px 700px at 50% 118%,rgba(29,131,184,.20),rgba(29,131,184,0) 70%),var(--bg)}
.tt{left:0;width:1920px;text-align:center}
.tt .l1,.tt .l3{font-size:92px;font-weight:600;letter-spacing:-.02em}
.tt .l2{display:flex;align-items:center;justify-content:center;gap:34px;font-size:118px;font-weight:700;letter-spacing:-.035em;line-height:1.02;margin:10px 0}
.ico{width:128px;height:128px;border-radius:50%;background:var(--blue);display:flex;align-items:center;justify-content:center;flex:none}
.ico svg{width:70px;height:70px;fill:none;stroke:#fff;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.chip{display:inline-flex;align-items:center;gap:16px;background:#fff;border-radius:999px;padding:12px 32px 12px 12px;box-shadow:0 10px 34px rgba(20,60,90,.12);font-size:32px;font-weight:600}
.av{width:60px;height:60px;border-radius:50%;background:var(--blue);color:#fff;font-weight:700;font-size:32px;display:flex;align-items:center;justify-content:center}
.chip small{font-size:26px;color:var(--muted);font-weight:600}
.bub{color:var(--sub);background:var(--bub);border-radius:34px;padding:30px 40px;font-size:40px;line-height:1.28;font-weight:600;width:820px}
.me{background:#fff;box-shadow:0 8px 26px rgba(20,60,90,.12);border-radius:999px;padding:16px 34px;font-size:32px;font-weight:700;color:var(--deep)}
.card{background:#fff;border-radius:32px;box-shadow:0 26px 70px rgba(20,60,90,.14);padding:44px 52px}
.k{font-size:24px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.row{display:flex;justify-content:space-between;align-items:baseline;gap:28px;padding:20px 0;border-top:2px solid #e9eef3;font-size:var(--fs,36px)}
.row .a{font-weight:600}.row .b{font-weight:700}
.btn{display:inline-flex;align-items:center;justify-content:center;height:96px;border-radius:999px;font-size:38px;font-weight:700}
.allow{background:var(--blue);color:#fff;width:300px}.deny{background:#eef2f5;color:var(--muted);width:240px}
.hide{opacity:0}.mas{z-index:5}
.note{position:absolute;left:120px;bottom:30px;font-size:22px;color:var(--muted);font-weight:600;z-index:40}
.note i{display:inline-block;width:11px;height:11px;border-radius:50%;background:var(--amber);margin-right:10px}

`;

const html = [];
const tw = []; // timeline lines
const aud = [];
const { mascot, mMood, mIn, mBob, mBlink, mWave, mHop } = makeMascot(tw);
let sfxN = 0;
const sfx = (file, t, vol, dur) => aud.push(`<audio id="sfx${++sfxN}" class="clip" src="assets/sfx/${file}" data-start="${t}" data-duration="${dur}" data-track-index="${5 + (sfxN % 3)}" data-volume="${vol}"></audio>`);
const pop = (t) => sfx("pop.mp3", +t.toFixed(3), 0.22, 0.72);
const click = (t) => sfx("click.mp3", +t.toFixed(3), 0.35, 0.36);
const chime = (t) => sfx("chime.mp3", +t.toFixed(3), 0.22, 1.5);
const IN = (sel, t, extra = "") => tw.push(`tl.from("${sel}",{opacity:0,y:26,duration:.45,ease:"power2.out"${extra}},${t});`);
const scene = (id, a, b, cls, body) => html.push(`<div class="clip ${cls}" id="${id}" data-start="${a}" data-duration="${+(b - a).toFixed(3)}" data-track-index="0">${body}</div>`);

// ---------- Intro (0 - T(16)) ----------
{
  const icons = [];
  const cols = 9, rows = 5;
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
    const n = r * cols + c, x = 120 + c * 200 + (r % 2) * 100, y = 90 + r * 190;
    icons.push(`<div class="abs wi" style="left:${x}px;top:${y}px;width:96px;height:96px;border-radius:26px;background:#fff;box-shadow:0 10px 30px rgba(20,60,90,.10);display:flex;align-items:center;justify-content:center"><div class="ico" style="width:60px;height:60px;background:${n % 3 === 0 ? "var(--blue)" : "#d3e6f1"}">${ICON[WALL[n % WALL.length]].replace("<svg", '<svg style="width:34px;height:34px;' + (n % 3 === 0 ? "" : "stroke:#1d83b8") + '"')}</div></div>`);
  }
  scene("intro", 0, T(16), "ch", `
    ${mascot("mI",830,120,260)}<div id="wall" class="abs" style="left:0;top:0;width:1920px;height:1080px">${icons.join("")}</div>
    <div id="veil" class="abs" style="left:0;top:0;width:1920px;height:1080px;background:var(--bg);opacity:0"></div>
    <div id="i1" class="abs tt" style="top:470px;font-size:170px;font-weight:700;letter-spacing:-.04em">Satva</div>
    <div id="i2" class="abs tt" style="top:450px;font-size:104px;font-weight:700;letter-spacing:-.03em;line-height:1.08">Satva is your own trusted,<br/>smart bookkeeping agent</div>
    <div id="i3" class="abs tt" style="top:430px;font-size:150px;font-weight:700;letter-spacing:-.04em;line-height:1.05;color:var(--deep)">One agent<br/>for everything.</div>`);
  tw.push(`tl.from(".wi",{opacity:0,scale:.6,duration:.5,stagger:{each:.03,from:"center"},ease:"back.out(1.6)"},0.1);`);
  tw.push(`tl.to("#wall",{y:-40,duration:${T(16)},ease:"none"},0);`);
  tw.push(`tl.to("#veil",{opacity:.92,duration:.4},${T(3)});`);
  tw.push(`tl.from("#i1",{opacity:0,scale:.9,duration:.5,ease:"power2.out"},${T(4)});`);
  tw.push(`tl.to("#i1",{opacity:0,duration:.25},${T(8) - 0.05});`);
  tw.push(`tl.from("#i2",{opacity:0,y:30,duration:.5,ease:"power2.out"},${T(8)});`);
  tw.push(`tl.to("#i2",{opacity:0,duration:.25},${T(12) - 0.05});`);
  tw.push(`tl.from("#i3",{opacity:0,y:30,duration:.55,ease:"power2.out"},${T(12)});`);
  pop(T(4)); pop(T(8)); pop(T(12));
  mIn("mI", T(4)); mBob("mI", T(4), T(16)); mMood("mI", T(12), "happy"); mWave("mI", T(8)); mBlink("mI", [T(6), T(10.5)]);
}

// ---------- Chapter helper: title phase then scene ----------
function chapter(c, sceneHtml, cues) {
  const a = T(c.k), b = T(c.k + 20), tEnd = T(c.k + 4);
  scene(`ch${c.id}`, a, b, "ch", `
    <div id="t${c.id}" class="abs tt" style="top:250px"><div class="l1">One agent</div><div class="l2"><span class="ico">${ICON[c.icon]}</span><span>${c.verb}</span></div><div class="l3">for you</div></div>
    ${sceneHtml}
    <img class="abs" src="assets/logo/satva-logo.svg" alt="Satva Solutions" style="right:110px;top:48px;width:190px" />
    <div class="note"><i></i>SANDBOX DATA · QuickBooks&reg; Online · demo figures</div>`);
  tw.push(`tl.from("#t${c.id}",{opacity:0,y:30,duration:.5,ease:"power2.out"},${a + 0.05});`);
  tw.push(`tl.to("#t${c.id}",{opacity:0,y:-20,duration:.3,ease:"power2.in"},${+(tEnd - 0.4).toFixed(3)});`);
  cues(T);
  pop(a + 0.05);
}

// A: posts your entries (real txn 89 recode, human approval, read-back)
chapter(chapters[0], `
  ${mascot("mA",170,150,170)}<div id="aChip" class="abs chip" style="left:390px;top:232px">Satva <small>is reviewing your purchases</small></div>
  <div id="aBub" class="abs bub" style="left:170px;top:410px">Tania's Nursery, <b class="mono">$46.98</b>, is coded to Job Expenses. Its twin is coded Plants and Soil. I'm <b>55% sure</b> they should match.</div>
  <div id="aCard" class="abs card" style="left:1010px;top:250px;width:760px">
    <div class="k">Satva wants to change 1 entry</div>
    <div style="font-size:38px;font-weight:700;margin:14px 0 6px">Tania's Nursery · <span class="mono" style="color:var(--amber)">$46.98</span></div>
    <div style="font-size:30px;color:var(--muted);line-height:1.3;margin-bottom:34px"><s>Job Expenses</s><br/><b style="color:var(--ink)">Job Materials:Plants and Soil</b></div>
    <div style="display:flex;gap:24px"><span class="btn deny">Deny</span><span id="aAllow" class="btn allow">Allow</span></div>
  </div>
  <div id="aOk" class="abs card" style="left:1010px;top:250px;width:760px;border:4px solid var(--ok)">
    <div style="font-size:44px;font-weight:700;color:var(--ok)">Posted and verified</div>
    <div class="mono" style="font-size:30px;color:var(--muted);margin-top:18px;line-height:1.5">Read back from QuickBooks&reg;<br/>SyncToken 1 → 2 · account 58 → 66</div>
  </div>
  <div id="aFiles" class="abs" style="left:170px;top:820px;font-size:34px;font-weight:600;color:var(--muted)">Also imports <b style="color:var(--deep)">CSV · OFX · QIF</b> statement files</div>`,
  () => {
    const c = chapters[0]; const k = c.k;
    IN("#aChip", T(k + 4)); pop(T(k + 4)); mIn("mA", T(k + 4)); mBob("mA", T(k + 4), T(k + 20)); mMood("mA", T(k + 4), "work"); mMood("mA", T(k + 13.6), "happy"); mHop("mA", T(k + 13.6)); mBlink("mA", [T(k + 8), T(k + 16.5)]);
    IN("#aBub", T(k + 5)); pop(T(k + 5));
    IN("#aCard", T(k + 9)); pop(T(k + 9));
    tw.push(`tl.to("#aAllow",{scale:.94,duration:.08},${T(k + 13)});tl.to("#aAllow",{scale:1,duration:.15},${T(k + 13) + 0.08});`); click(T(k + 13));
    tw.push(`tl.to("#aCard",{opacity:0,duration:.2},${T(k + 13.5)});`);
    IN("#aOk", T(k + 13.6)); chime(T(k + 13.6));
    IN("#aFiles", T(k + 16));
  });

// B: catches what doesn't add up (real $900, left flagged)
chapter(chapters[1], `
  ${mascot("mB",170,150,170)}<div id="bChip" class="abs chip" style="left:390px;top:232px">Satva <small>is reconciling</small></div>
  <div id="bCard" class="abs card" style="left:1010px;top:250px;width:760px">
    <div class="k">Monthly Payment</div>
    <div class="mono" style="font-size:120px;font-weight:500;color:var(--amber);letter-spacing:-.04em;margin:10px 0 8px">$900.00</div>
    <div class="row"><span class="a">Payee</span><span class="b">none recorded</span></div>
    <div class="row"><span class="a">Posted to</span><span class="b">Checking (cash)</span></div>
    <div id="bFlag" style="margin-top:24px;display:inline-block;border:5px solid var(--warn);color:var(--warn);font-size:38px;font-weight:700;padding:10px 26px;border-radius:14px;transform:rotate(-3deg)">DOESN'T MATCH ANYTHING</div>
  </div>
  <div id="bBub" class="abs bub" style="left:170px;top:410px">I can't tell what this <b>$900</b> is. A loan payment? A transfer? <b>I won't guess.</b></div>
  <div id="bR" class="abs" style="left:170px;top:700px;display:flex;gap:20px"><span class="me">Loan payment</span><span class="me">Transfer</span><span class="me">I'll check</span></div>
  <div id="bDone" class="abs" style="left:170px;top:830px;font-size:36px;font-weight:700;color:var(--ok)">Left flagged. Nothing was changed.</div>`,
  () => {
    const k = chapters[1].k;
    IN("#bChip", T(k + 4)); pop(T(k + 4)); mIn("mB", T(k + 4)); mBob("mB", T(k + 4), T(k + 20)); mMood("mB", T(k + 4), "work"); mMood("mB", T(k + 8), "puzzled"); mBlink("mB", [T(k + 6), T(k + 14)]);
    IN("#bCard", T(k + 5)); pop(T(k + 5));
    tw.push(`tl.from("#bFlag",{opacity:0,scale:1.6,duration:.18,ease:"power3.in"},${T(k + 8)});`); click(T(k + 8));
    IN("#bBub", T(k + 9)); pop(T(k + 9));
    IN("#bR", T(k + 13)); pop(T(k + 13));
    IN("#bDone", T(k + 16));
  });

// C: tracks who owes you (real AR aging)
chapter(chapters[2], `
  ${mascot("mC",170,150,170)}<div id="cChip" class="abs chip" style="left:390px;top:232px">Satva <small>is checking who owes you</small></div>
  <div id="cBub" class="abs bub" style="left:170px;top:410px"><b class="mono">$5,277.52</b> is more than 60 days late. <b>Paulsen Medical Supplies</b> is the biggest.</div>
  <div id="cNote" class="abs" style="left:170px;top:700px;font-size:32px;color:var(--muted);font-weight:600;width:800px;line-height:1.35">Read-only. Satva shows who's late. You decide who to chase.</div>
  <div id="cCard" class="abs card" style="left:1010px;top:200px;width:760px">
    <div class="k">Owed to you</div>
    <div class="mono" style="font-size:96px;font-weight:500;letter-spacing:-.04em;margin:6px 0 10px">$5,075.52</div>
    <div class="row"><span class="a">61 – 90 days</span><span class="b mono" style="color:var(--amber)">$3,756.02</span></div>
    <div class="row"><span class="a">91+ days</span><span class="b mono" style="color:var(--warn)">$1,521.50</span></div>
    <div class="row"><span class="a">Paulsen Medical Supplies</span><span class="b mono">$954.75</span></div>
    <div class="row"><span class="a">Geeta Kalapatapu</span><span class="b mono">$629.10</span></div>
    <div class="row"><span class="a">Freeman Sporting Goods</span><span class="b mono">$558.50</span></div>
  </div>`,
  () => {
    const k = chapters[2].k;
    IN("#cChip", T(k + 4)); pop(T(k + 4)); mIn("mC", T(k + 4)); mBob("mC", T(k + 4), T(k + 20)); mMood("mC", T(k + 4), "work"); mMood("mC", T(k + 9), "surprise"); mMood("mC", T(k + 12), "idle"); mBlink("mC", [T(k + 7), T(k + 15)]);
    IN("#cCard", T(k + 5)); pop(T(k + 5));
    IN("#cBub", T(k + 9)); pop(T(k + 9));
    IN("#cNote", T(k + 14));
  });

// D: finds the credits you forgot (real AP aging)
chapter(chapters[3], `
  ${mascot("mD",170,150,170)}<div id="dChip" class="abs chip" style="left:390px;top:232px">Satva <small>is checking what you owe</small></div>
  <div id="dBub" class="abs bub" style="left:170px;top:410px">Two vendor credits, <b class="mono">$6,300.00</b>, have sat unused for over 90 days.</div>
  <div id="dCard" class="abs card" style="left:960px;top:230px;width:830px;--fs:32px">
    <div class="k">Vendor credits · 91+ days</div>
    <div class="row" style="margin-top:14px"><span class="a">Ironclad Consulting Group</span><span class="b mono" style="color:var(--ok)">−$3,900.00</span></div>
    <div class="row"><span class="a">Bright Cleaning Services</span><span class="b mono" style="color:var(--ok)">−$2,400.00</span></div>
    <div id="dSum" class="row" style="border-top:4px double #111111"><span class="a">Unused credit</span><span class="b mono">$6,300.00</span></div>
    <div class="k" style="margin-top:34px">Also open</div>
    <div class="row"><span class="a">Diego's Road Warrior Bodyshop</span><span class="b mono">$755.00</span></div>
    <div class="row"><span class="a">PG&amp;E</span><span class="b mono">$86.44</span></div>
  </div>`,
  () => {
    const k = chapters[3].k;
    IN("#dChip", T(k + 4)); pop(T(k + 4)); mIn("mD", T(k + 4)); mBob("mD", T(k + 4), T(k + 20)); mMood("mD", T(k + 4), "work"); mMood("mD", T(k + 9), "surprise"); mMood("mD", T(k + 11), "happy"); mHop("mD", T(k + 11)); mBlink("mD", [T(k + 7), T(k + 15)]);
    IN("#dCard", T(k + 5)); pop(T(k + 5));
    IN("#dBub", T(k + 9)); pop(T(k + 9));
    tw.push(`tl.from("#dSum",{scale:1.06,duration:.3,ease:"power2.out"},${T(k + 11)});`); click(T(k + 11));
  });

// E: reports on your business (real P&L YTD)
chapter(chapters[4], `
  ${mascot("mE",170,150,170)}<div id="eChip" class="abs chip" style="left:390px;top:232px">Satva <small>is reading your P&amp;L</small></div>
  <div id="eBub" class="abs bub" style="left:170px;top:410px"><b class="mono">$2,916.00</b> is sitting in Miscellaneous. Want me to sort it?</div>
  <div id="eR" class="abs" style="left:170px;top:680px;display:flex;gap:20px"><span class="me">Yes, go ahead</span><span class="me">Not now</span></div>
  <div id="eCard" class="abs card" style="left:1010px;top:230px;width:760px">
    <div class="k">This year so far</div>
    <div class="row" style="margin-top:14px"><span class="a">Income</span><span class="b mono">$10,152.77</span></div>
    <div class="row"><span class="a">Expenses</span><span class="b mono">$5,269.31</span></div>
    <div class="row"><span class="a">Miscellaneous</span><span id="eMisc" class="b mono" style="color:var(--warn)">$2,916.00</span></div>
    <div class="row" style="border-top:4px double #111111"><span class="a">Net income</span><span class="b mono">$1,562.46</span></div>
  </div>`,
  () => {
    const k = chapters[4].k;
    IN("#eChip", T(k + 4)); pop(T(k + 4)); mIn("mE", T(k + 4)); mBob("mE", T(k + 4), T(k + 20)); mMood("mE", T(k + 4), "work"); mMood("mE", T(k + 9), "puzzled"); mMood("mE", T(k + 14), "idle"); mBlink("mE", [T(k + 7), T(k + 16)]);
    IN("#eCard", T(k + 5)); pop(T(k + 5));
    tw.push(`tl.fromTo("#eMisc",{scale:1},{scale:1.12,duration:.25,yoyo:true,repeat:1,transformOrigin:"100% 50%"},${T(k + 9)});`);
    IN("#eBub", T(k + 9)); pop(T(k + 9));
    IN("#eR", T(k + 13)); pop(T(k + 13));
  });

// F: asks before it acts (approval + audit trail from the real run)
chapter(chapters[5], `
  ${mascot("mF",170,50,150)}<div id="fCard" class="abs card" style="left:170px;top:230px;width:760px">
    <div class="k">Satva wants to</div>
    <div style="font-size:44px;font-weight:700;margin:12px 0 30px;line-height:1.15">change 1 entry in QuickBooks&reg; Online</div>
    <div style="display:flex;gap:24px"><span class="btn deny">Deny</span><span id="fAllow" class="btn allow">Allow</span></div>
  </div>
  <div id="fTrail" class="abs card" style="left:1010px;top:230px;width:760px">
    <div class="k">Audit trail</div>
    <div id="f1" class="row" style="margin-top:12px"><span class="a">Read the record first</span><span class="b" style="color:var(--ok)">✓</span></div>
    <div id="f2" class="row"><span class="a">Changed 1 field</span><span class="b" style="color:var(--ok)">✓</span></div>
    <div id="f3" class="row"><span class="a">Read it back to verify</span><span class="b" style="color:var(--ok)">✓</span></div>
    <div id="f4" class="row"><span class="a">Saved the audit trail</span><span class="b" style="color:var(--ok)">✓</span></div>
  </div>
  <div id="fLine" class="abs" style="left:170px;top:700px;font-size:44px;font-weight:700;width:800px;line-height:1.2;color:var(--deep)">Nothing is written without your Allow.</div>`,
  () => {
    const k = chapters[5].k;
    IN("#fCard", T(k + 4)); pop(T(k + 4)); mIn("mF", T(k + 4)); mBob("mF", T(k + 4), T(k + 20)); mMood("mF", T(k + 8.3), "happy"); mHop("mF", T(k + 8.3)); mBlink("mF", [T(k + 6), T(k + 14)]);
    tw.push(`tl.to("#fAllow",{scale:.94,duration:.08},${T(k + 8)});tl.to("#fAllow",{scale:1,duration:.15},${T(k + 8) + 0.08});`); click(T(k + 8));
    IN("#fTrail", T(k + 8.5));
    ["f1", "f2", "f3", "f4"].forEach((id, i) => { IN("#" + id, T(k + 9.5 + i * 1.5)); pop(T(k + 9.5 + i * 1.5)); });
    IN("#fLine", T(k + 15.5));
  });

// ---------- G: all your accounting systems, in one place ----------
scene("chG", T(G), T(END), "ch", `
  ${mascot("mG", 1500, 770, 200)}
  <div id="gT" class="abs tt" style="top:120px;font-size:104px;font-weight:700;letter-spacing:-.035em;line-height:1.05">All your accounting systems<br/>in one place</div>
  <div id="gRow" class="abs" style="left:0;width:1920px;top:440px;display:flex;justify-content:center;gap:24px;flex-wrap:wrap;padding:0 150px">
    ${SYS.map((n) => `<span class="chip g" style="font-size:34px"><span class="av" style="background:var(--ok);width:52px;height:52px;font-size:28px">✓</span>${n}</span>`).join("")}
  </div>
  <div id="gFiles" class="abs tt" style="top:700px;font-size:38px;font-weight:600;color:var(--sub)">and your statement files: <b style="color:var(--blue)">CSV · OFX · QIF</b></div>
  <div id="gBy" class="abs tt" style="top:790px;font-size:28px;font-weight:600;color:var(--muted)">Built by Satva Solutions · Accounting &amp; ERP integration</div>
  <div class="note"><i></i>SANDBOX DATA · demo figures</div>`);
tw.push(`tl.from("#gT",{opacity:0,y:30,duration:.5,ease:"power2.out"},${T(G) + 0.05});`);
tw.push(`tl.from(".g",{opacity:0,y:24,scale:.9,duration:.4,stagger:0.522,ease:"back.out(1.5)"},${T(G + 2)});`);
for (let i = 0; i < SYS.length; i++) pop(T(G + 2 + i));
IN("#gFiles", T(G + 10.5)); IN("#gBy", T(G + 12));
mIn("mG", T(G + 1)); mBob("mG", T(G + 1), T(END)); mMood("mG", T(G + 1), "happy"); mWave("mG", T(G + 3)); mBlink("mG", [T(G + 7)]);

// ---------- End card ----------
scene("end", T(END), DUR, "ch", `
  <img id="lg" class="abs" src="assets/logo/satva-logo.svg" alt="Satva Solutions" style="left:660px;top:170px;width:600px" />
  <div id="e1" class="abs tt" style="top:500px;font-size:108px;font-weight:700;letter-spacing:-.03em;color:var(--ink)">Satva Ledger</div>
  <div id="e2" class="abs tt" style="top:650px;font-size:64px;font-weight:600;color:var(--blue)">One agent for everything.</div>
  ${mascot("mX",1440,560,280)}
  <div id="e3" class="abs tt" style="top:760px;font-size:38px;font-weight:600;color:var(--muted)">Your own trusted, smart agent.</div>
  <div class="abs tt" style="top:960px;font-size:22px;font-weight:600;color:var(--muted)">Sandbox data. Demo figures. Voice and sound effects: ElevenLabs (elevenlabs.io).</div>`);
tw.push(`tl.from("#lg",{opacity:0,y:20,duration:.5,ease:"power2.out"},${T(END) + 0.1});`);
tw.push(`tl.from("#e1",{opacity:0,y:24,duration:.5,ease:"power2.out"},${T(END) + 0.5});`);
tw.push(`tl.from("#e2",{opacity:0,y:20,duration:.5,ease:"power2.out"},${T(END + 2)});`);
tw.push(`tl.from("#e3",{opacity:0,duration:.6},${T(END + 4)});`);
tw.push(`tl.to("#end",{opacity:0,duration:.8},${DUR - 0.8});`);
pop(T(END + 2));
mIn("mX", T(END) + 0.4); mBob("mX", T(END) + 0.4, T(END + 8)); mMood("mX", T(END) + 0.4, "happy"); mWave("mX", T(END) + 1.2); mBlink("mX", [T(END + 4)]);

// ---------- extra sound design (ElevenLabs sound-effects, generated 2026-09-21) ----------
const el = (f, t, v, d) => sfx(f, +t.toFixed(3), v, d);
chapters.forEach((c) => el("el-swoosh.mp3", T(c.k) - 0.05, 0.3, 0.8));
el("el-swoosh.mp3", T(G) - 0.05, 0.3, 0.8);
el("el-swoosh.mp3", T(END) - 0.05, 0.3, 0.8);
el("el-sparkle.mp3", T(4), 0.3, 1.0);          // mascot appears
el("el-boing.mp3", T(8), 0.3, 0.8);            // mascot waves
el("el-sparkle.mp3", T(12), 0.25, 1.0);        // "One agent for everything."
el("el-type.mp3", T(chapters[0].k + 5), 0.3, 1.2);   // A: bubble
el("el-boing.mp3", T(chapters[0].k + 13.6), 0.35, 0.8);
el("el-ding.mp3", T(chapters[0].k + 13.7), 0.35, 1.2); // A: posted and verified
el("el-stamp.mp3", T(chapters[1].k + 8), 0.5, 0.8);    // B: flagged
el("el-type.mp3", T(chapters[2].k + 9), 0.3, 1.2);     // C: bubble
el("el-coin.mp3", T(chapters[3].k + 9), 0.4, 0.8);     // D: credits found
el("el-sparkle.mp3", T(chapters[3].k + 11), 0.3, 1.0);
el("el-boing.mp3", T(chapters[3].k + 11), 0.3, 0.8);
el("el-type.mp3", T(chapters[4].k + 9), 0.3, 1.2);     // E: bubble
el("el-boing.mp3", T(chapters[5].k + 8.3), 0.35, 0.8); // F: allowed
el("el-ding.mp3", T(chapters[5].k + 8.4), 0.3, 1.2);
el("el-sparkle.mp3", T(G + 1), 0.3, 1.0);
el("el-boing.mp3", T(G + 3), 0.3, 0.8);
el("el-sparkle.mp3", T(END) + 0.4, 0.3, 1.0);
el("el-boing.mp3", T(END) + 1.2, 0.3, 0.8);

const page = `<!doctype html>
<html lang="en" data-resolution="landscape"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1920, height=1080"/>
<script src="assets/gsap.min.js"></script><style>${css}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="${DUR}" data-width="1920" data-height="1080">
${html.join("\n")}
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
fs.writeFileSync(out, page);
console.log("wrote", out, `${(page.length / 1024).toFixed(0)} KB`, "sfx:", sfxN);
