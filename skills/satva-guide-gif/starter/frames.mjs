/**
 * Step 3a — record the narrated, cursor-animated walkthrough as PNG frames (gif/frames/).
 * Clicks are ripple-only: they never trigger the real control, which is what keeps a
 * third-party consent screen out of the film.
 */
import { chromium } from "playwright";
import { skillUrl } from "./paths.mjs";

const { Demo } = await import(skillUrl("scripts/cursor-demo.mjs"));

const browser = await chromium.launch({ channel: "chrome" }).catch(() => chromium.launch());
const ctx = await browser.newContext({ viewport: { width: 1000, height: 700 }, deviceScaleFactor: 1 });
const d = new Demo("gif/frames", { captionBg: "#0080C6" });

// Scene 1 — read the permissions, then approve
let page = await ctx.newPage();
await page.goto(skillUrl("examples/approve.html"), { waitUntil: "networkidle" });
await d.install(page, "Step 1: review what you are approving");
await d.hold(8);
for (let k = 1; k <= 4; k++) { await page.evaluate((n) => window.showPerms(n), k); await d.hold(5); }
await d.caption("Step 2: click Install app to approve");
await d.moveTo("#approve");
await d.click("#approve");
await d.hold(6);
await page.close();

// Scene 2 — paste the configuration
page = await ctx.newPage();
await page.goto(skillUrl("examples/editor.html"), { waitUntil: "networkidle" });
await d.install(page, "Step 3: paste the configuration into your tool");
await d.hold(6);
for (let k = 1; k <= 10; k++) { await page.evaluate((n) => window.showLines(n), k); await d.hold(3); }
await page.evaluate(() => window.showDone());
await d.caption("Step 4: save, then restart your AI tool — done");
await d.hold(14);
await browser.close();
