/**
 * Cursor-animated demo frames: a fake cursor, a caption bar and a click ripple
 * are injected into the real page, tweened between targets, and screenshotted
 * one PNG per frame. Feed the frames to build-gif.py.
 *
 * import { Demo } from "./cursor-demo.mjs";
 *   const d = new Demo(outDir, { captionBg: "#0b3b2b" });
 *   await d.install(page, "Sign in with Google");
 *   await d.hold(9); await d.moveTo("#btn"); await d.click("#btn");
 *
 * Clicks are ripple-only by default: pass a `real` callback when the demo
 * should actually perform the interaction. Never film a third party's UI —
 * illustrate hand-off screens (OAuth consent, editors) with your own artwork.
 */
import fs from "node:fs";
import path from "node:path";

const OVERLAY = (captionBg) => {
  if (window.__demo) return;
  const root = document.createElement("div");
  root.id = "__demo_overlay";
  root.innerHTML = `
    <style>
      #__demo_cursor,#__demo_ripple,#__demo_caption{position:fixed;pointer-events:none;z-index:2147483647}
      #__demo_cursor{left:0;top:0;width:26px;height:26px;transform:translate(-2px,-2px);
        filter:drop-shadow(0 2px 3px rgba(0,0,0,.45))}
      #__demo_ripple{border-radius:50%;border:3px solid rgba(255,255,255,.95);
        box-shadow:0 0 0 3px rgba(20,20,20,.55) inset,0 0 0 2px rgba(20,20,20,.45);opacity:0}
      #__demo_caption{left:0;right:0;bottom:0;height:56px;background:${captionBg};color:#fff;
        display:flex;align-items:center;justify-content:center;font:600 22px/1.2 -apple-system,
        Segoe UI,Roboto,sans-serif;letter-spacing:.2px;box-shadow:0 -2px 14px rgba(0,0,0,.35)}
    </style>
    <div id="__demo_caption"></div>
    <div id="__demo_ripple"></div>
    <svg id="__demo_cursor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path d="M5 2.5 L5 20.2 L9.4 16.1 L12.2 22.2 L15.5 20.7 L12.7 14.8 L18.6 14.6 Z"
            fill="#fff" stroke="#111" stroke-width="1.6" stroke-linejoin="round"/>
    </svg>`;
  document.documentElement.appendChild(root);
  const cur = root.querySelector("#__demo_cursor");
  const rip = root.querySelector("#__demo_ripple");
  const cap = root.querySelector("#__demo_caption");
  window.__demo = {
    x: 0, y: 0,
    move(x, y) { this.x = x; this.y = y; cur.style.left = x + "px"; cur.style.top = y + "px"; },
    caption(t) { cap.textContent = t; },
    ripple(r, o) {
      rip.style.width = rip.style.height = r * 2 + "px";
      rip.style.left = this.x - r + "px";
      rip.style.top = this.y - r + "px";
      rip.style.opacity = o;
    },
    scale(sel, s) {
      const e = document.querySelector(sel);
      if (!e) return;
      e.style.transition = "transform .08s";
      e.style.transform = s === 1 ? "" : `scale(${s})`;
    },
  };
};

// easeInOutCubic — the cursor accelerates away and settles onto its target
const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);

export class Demo {
  constructor(outDir, { captionBg = "#12131a", clean = true } = {}) {
    this.out = outDir;
    this.captionBg = captionBg;
    this.n = 0;
    this.page = null;
    fs.mkdirSync(outDir, { recursive: true });
    if (clean) for (const f of fs.readdirSync(outDir)) fs.unlinkSync(path.join(outDir, f));
  }

  shot() {
    return this.page.screenshot({
      path: path.join(this.out, `f${String(this.n++).padStart(4, "0")}.png`),
    });
  }

  async hold(count) { for (let i = 0; i < count; i++) await this.shot(); }

  /** Attach the overlay to `page` and make it the page being filmed. */
  async install(page, caption, at = { x: 500, y: 480 }) {
    this.page = page;
    await page.evaluate(OVERLAY, this.captionBg);
    await page.evaluate(([c, x, y]) => { window.__demo.caption(c); window.__demo.move(x, y); },
      [caption, at.x, at.y]);
  }

  caption(t) { return this.page.evaluate((c) => window.__demo.caption(c), t); }

  centre(sel) {
    return this.page.evaluate((s) => {
      const e = document.querySelector(s);
      if (!e) return null;
      const r = e.getBoundingClientRect();
      return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
    }, sel);
  }

  /** Glide the cursor to `sel`. Returns false (and logs) when it is missing. */
  async moveTo(sel, steps = 15) {
    const to = await this.centre(sel);
    if (!to) { console.log("  MISSING target:", sel); return false; }
    const from = await this.page.evaluate(() => ({ x: window.__demo.x, y: window.__demo.y }));
    for (let i = 1; i <= steps; i++) {
      const t = ease(i / steps);
      await this.page.evaluate(([x, y]) => window.__demo.move(x, y),
        [from.x + (to.x - from.x) * t, from.y + (to.y - from.y) * t]);
      await this.shot();
    }
    return true;
  }

  /** Ripple + target pop. `real` optionally performs the actual interaction. */
  async click(sel, real = null) {
    const RADII = [8, 18, 30, 42];
    const OPAC = [0.95, 0.8, 0.5, 0.15];
    for (let i = 0; i < RADII.length; i++) {
      await this.page.evaluate(([r, o, s, sc]) => {
        window.__demo.ripple(r, o); window.__demo.scale(s, sc);
      }, [RADII[i], OPAC[i], sel, i < 2 ? 0.97 : 1]);
      await this.shot();
    }
    await this.page.evaluate(([s]) => { window.__demo.ripple(0, 0); window.__demo.scale(s, 1); }, [sel]);
    if (real) await real();
  }

  /** Type into `sel`, one frame per two characters. */
  async type(sel, text) {
    for (let i = 1; i <= text.length; i++) {
      await this.page.evaluate(([s, v]) => { document.querySelector(s).value = v; },
        [sel, text.slice(0, i)]);
      if (i % 2 === 0 || i === text.length) await this.shot();
    }
  }

  /** Scroll so `sel` sits `topGap` px below the viewport top, tweened. */
  async scrollTo(sel, topGap = 210, steps = 7) {
    const target = await this.page.evaluate(([s, gap]) => {
      const e = document.querySelector(s);
      if (!e) return null;
      const y = e.getBoundingClientRect().top + window.scrollY - gap;
      const max = document.documentElement.scrollHeight - window.innerHeight;
      return Math.max(0, Math.min(y, max));
    }, [sel, topGap]);
    if (target === null) return;
    const from = await this.page.evaluate(() => window.scrollY);
    for (let i = 1; i <= steps; i++) {
      const t = ease(i / steps);
      await this.page.evaluate((y) => window.scrollTo(0, y), from + (target - from) * t);
      await this.shot();
    }
  }
}
