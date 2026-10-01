/**
 * Annotated full-screen screenshots: numbered rings drawn into the DOM in
 * document coordinates before capture, so a ring lands on its element in both
 * viewport and fullPage shots.
 *
 * import { inject, mark, show, shot, problems } from "./callouts.mjs";
 */
import fs from "node:fs";
import path from "node:path";

const CALLOUT_CSS = `
.__cal { position:absolute; z-index:2147483647; pointer-events:none;
  border:3px solid #111; border-radius:10px;
  box-shadow:0 0 0 3px rgba(255,255,255,.95), 0 6px 18px rgba(0,0,0,.28); }
.__badge { position:absolute; z-index:2147483647; pointer-events:none;
  width:34px; height:34px; border-radius:50%; background:#111; color:#fff;
  font:700 19px/34px "Segoe UI",system-ui,sans-serif; text-align:center;
  box-shadow:0 0 0 3px #fff, 0 3px 10px rgba(0,0,0,.35); }
`;

export const problems = [];

export const inject = async (page) => {
  await page.addStyleTag({ content: CALLOUT_CSS });
  await page.evaluate(() => {
    // nth = -1 rings the union of every match (e.g. a whole list)
    window.__mark = (sel, num, nth = 0) => {
      const els = document.querySelectorAll(sel);
      if (!els.length || (nth >= 0 && !els[nth])) return "MISSING " + sel;
      const rs = [...(nth < 0 ? els : [els[nth]])].map((e) => e.getBoundingClientRect());
      const r = {
        left: Math.min(...rs.map((x) => x.left)),
        top: Math.min(...rs.map((x) => x.top)),
        right: Math.max(...rs.map((x) => x.right)),
        bottom: Math.max(...rs.map((x) => x.bottom)),
      };
      r.width = r.right - r.left;
      r.height = r.bottom - r.top;
      const sx = window.scrollX, sy = window.scrollY, pad = 6;
      const ring = document.createElement("div");
      ring.className = "__cal";
      ring.style.left = r.left + sx - pad + "px";
      ring.style.top = r.top + sy - pad + "px";
      ring.style.width = r.width + pad * 2 + "px";
      ring.style.height = r.height + pad * 2 + "px";
      document.body.appendChild(ring);
      if (num === null) return "ok";

      // The badge sits OUTSIDE the ring so it never covers the text it points
      // at: try candidate positions in order, take the first that collides with
      // nothing already drawn and no visible run of text.
      const b = document.createElement("div");
      b.className = "__badge";
      b.textContent = num;
      const S = 34, g = 10;
      const L = r.left + sx - pad, T = r.top + sy - pad;
      const R = r.right + sx + pad, B = r.bottom + sy + pad;
      const cands = [
        [L - S - g, T + (B - T) / 2 - S / 2],
        [R + g, T + (B - T) / 2 - S / 2],
        [L - S - g, T - S - g],
        [L, T - S - g],
        [L, B + g],
        [8, T + (B - T) / 2 - S / 2],
      ];
      const taken = [...document.querySelectorAll(".__cal,.__badge")].map((n) =>
        n.getBoundingClientRect(),
      );
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      for (let n; (n = w.nextNode()); ) {
        if (!n.textContent.trim() || n.parentElement.closest(".__badge")) continue;
        const rg = document.createRange();
        rg.selectNodeContents(n);
        taken.push(...rg.getClientRects());
      }
      const hits = (x, y) =>
        x < 2 || y < 2 ||
        x + S > document.documentElement.scrollWidth - 2 ||
        taken.some(
          (t) =>
            x < t.left + sx + t.width && x + S > t.left + sx &&
            y < t.top + sy + t.height && y + S > t.top + sy,
        );
      const pick = cands.find(([x, y]) => !hits(x, y)) || cands[0];
      b.style.left = pick[0] + "px";
      b.style.top = pick[1] + "px";
      document.body.appendChild(b);
      return "ok";
    };
    window.__clear = () =>
      document.querySelectorAll(".__cal,.__badge").forEach((n) => n.remove());
  });
};

export const mark = async (page, sel, num, nth = 0) => {
  const r = await page.evaluate(([s, n, i]) => window.__mark(s, n, i), [sel, num, nth]);
  if (r !== "ok") problems.push(`${sel} -> ${r}`);
};

export const clear = (page) => page.evaluate(() => window.__clear());

/** Scroll `sel` to the middle of the viewport before annotating. */
export const show = async (page, sel) => {
  const ok = await page.evaluate((s) => {
    const el = document.querySelector(s);
    if (!el) return false;
    el.scrollIntoView({ block: "center", behavior: "instant" });
    return true;
  }, sel);
  if (!ok) problems.push(`scrollIntoView missing ${sel}`);
  await page.waitForTimeout(250);
};

export const shot = async (page, dir, name, fullPage = false) => {
  fs.mkdirSync(dir, { recursive: true });
  await page.waitForTimeout(200);
  await page.screenshot({ path: path.join(dir, `${name}.png`), fullPage });
  console.log("  ->", name);
};

export const report = () =>
  console.log(problems.length ? "PROBLEMS:\n" + problems.join("\n") : "no selector problems");
