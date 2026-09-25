/**
 * Step 2 — annotated screenshots (1440x900 @2x = 2880x1800, numbered rings).
 * Runs against the skill's own neutral illustration pages so it works out of the box.
 * To document YOUR app: point `page.goto` at it, seed fake data, and change the selectors.
 */
import { chromium } from "playwright";
import { skillUrl } from "./paths.mjs";

const { inject, mark, clear, shot, report } = await import(skillUrl("scripts/callouts.mjs"));
const OUT = "shots";

const browser = await chromium.launch({ channel: "chrome" }).catch(() => chromium.launch());
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
const page = await ctx.newPage();

await page.goto(skillUrl("examples/approve.html"), { waitUntil: "networkidle" });
await page.evaluate(() => window.showPerms(window.PERM_COUNT));
await inject(page);
await mark(page, "#perms", "1");
await mark(page, "#approve", "2");
await shot(page, OUT, "s01-approve");
await clear(page);

await page.goto(skillUrl("examples/editor.html"), { waitUntil: "networkidle" });
await page.evaluate(() => window.showDone());
await inject(page);
await mark(page, "#code", "1");
await mark(page, "#status", "2");
await shot(page, OUT, "s02-config");

report(); // must print "no selector problems"
await browser.close();
