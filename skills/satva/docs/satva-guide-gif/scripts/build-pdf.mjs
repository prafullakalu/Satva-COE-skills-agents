/**
 * Render a body-only HTML fragment into a Satva house-format PDF.
 *
 *   node build-pdf.mjs doc.json      (paths in doc.json are relative to its dir)
 *
 * Uses installed Google Chrome when present (sharpest fonts), otherwise Playwright's
 * bundled Chromium (`npx playwright install chromium`).
 *
 * doc.json: { body, out, title, subtitle, project, for?, created, versionRows[] }
 * House format follows the Satva FRD/UAC templates: blue SATVA banner in the
 * page header, contact bar in the footer, Mulish, cover page with the project
 * block and a Version History table.
 */
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath, pathToFileURL } from "node:url";

// Resolve playwright from the WORKSPACE, not from the skill directory — the
// skill ships no node_modules of its own. Run this from a folder where
// `npm i playwright` has been done.
const { chromium } = createRequire(path.join(process.cwd(), "noop.cjs"))("playwright");

const SKILL = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const cfgPath = path.resolve(process.argv[2] || "doc.json");
// replace(): Windows editors and PowerShell write a UTF-8 BOM that JSON.parse rejects
const doc = JSON.parse(fs.readFileSync(cfgPath, "utf8").replace(/^﻿/, ""));
const HERE = path.dirname(cfgPath);

const asset = (f) => path.join(SKILL, "assets", f);
const b64 = (f) => fs.readFileSync(asset(f)).toString("base64");
const HEADER_IMG = `data:image/png;base64,${b64("satva-header.png")}`;
const FOOTER_IMG = `data:image/png;base64,${b64("satva-footer.png")}`;
const FONT = (f) => pathToFileURL(asset(f)).href;

const rows = (doc.versionRows || [[doc.created || "", "First release", "Satva Solutions"]])
  .map((r) => `<tr>${r.map((c) => `<td>${c}</td>`).join("")}</tr>`)
  .join("");

const html = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>${doc.project} — ${doc.subtitle}</title>
<style>
  @font-face { font-family: Mulish; src: url("${FONT("Mulish-regular.ttf")}"); font-weight: 400; }
  @font-face { font-family: Mulish; src: url("${FONT("Mulish-bold.ttf")}"); font-weight: 700; }
  @font-face { font-family: Mulish; src: url("${FONT("Mulish-italic.ttf")}"); font-style: italic; }
  @font-face { font-family: "Roboto Mono"; src: url("${FONT("RobotoMono.ttf")}"); font-weight: 100 700; }
  @page { size: A4; }
  html, body { margin: 0; padding: 0; }
  body { font-family: Mulish, "Segoe UI", sans-serif; color: #1a1a1a;
         font-size: 10.5pt; line-height: 1.5; -webkit-print-color-adjust: exact; }

  h1 { font-size: 22pt; margin: 0 0 4pt; color: #0080C6; }
  h2 { font-size: 14pt; margin: 18pt 0 6pt; color: #0080C6; page-break-after: avoid; }
  h3 { font-size: 11.5pt; margin: 12pt 0 4pt; page-break-after: avoid; }
  p  { margin: 0 0 6pt; }
  ul, ol { margin: 4pt 0 8pt; padding-left: 16pt; }
  li { margin-bottom: 3pt; }
  code, pre { font-family: "Roboto Mono", Consolas, monospace; font-size: 9pt; }
  code { background: #f2f6fa; padding: 0 3px; border-radius: 3px; }
  pre { border: 1px solid #cfd9e3; background: #f7fafd; padding: 7pt 9pt;
        margin: 5pt 0 9pt; white-space: pre-wrap; word-break: break-all; }

  table { border-collapse: collapse; width: 100%; margin: 5pt 0 9pt;
          page-break-inside: avoid; }
  th, td { border: 1px solid #b9c7d4; padding: 4pt 7pt; font-size: 9.5pt;
           text-align: left; vertical-align: top; }
  th { background: #0080C6; color: #fff; font-weight: 700; }

  /* Screenshots: 150 mm by default (readable, and two fit a page with text). .wide = full
     column, .narrow = 98 mm for tall full-page captures that would strand the next paragraph. */
  figure { margin: 8pt auto 12pt; page-break-inside: avoid; max-width: 150mm; }
  figure.wide, figure.strip { max-width: 100%; }
  figure.narrow { max-width: 98mm; }
  figure img { width: 100%; border: 1px solid #b9c7d4; display: block; }
  figcaption { font-size: 9pt; color: #48606f; margin-top: 4pt; line-height: 1.35; }
  .keep { page-break-inside: avoid; }
  .break { page-break-before: always; }

  .cover { text-align: center; padding-top: 40pt; }
  .cover .kicker { font-size: 11pt; letter-spacing: .18em; text-transform: uppercase;
                   color: #0080C6; font-weight: 700; }
  .cover h1 { font-size: 30pt; margin: 10pt 0 2pt; color: #000000; }
  .cover .sub { font-size: 15pt; color: #5a6f80; margin-bottom: 26pt; }
  .cover table { width: 78%; margin: 0 auto 26pt; }
  .cover td:first-child { width: 38%; background: #eef5fb; font-weight: 700; }
  .tip { border-left: 3px solid #0080C6; background: #f2f8fd; padding: 6pt 9pt;
         margin: 6pt 0 9pt; page-break-inside: avoid; }
  .warn { border-left: 3px solid #d97706; background: #fff8ee; padding: 6pt 9pt;
          margin: 6pt 0 9pt; page-break-inside: avoid; }
</style></head><body>

<section class="cover">
  <div class="kicker">Satva Solutions</div>
  <h1>${doc.title}</h1>
  <div class="sub">${doc.subtitle}</div>
  <table>
    <tr><td>Name of the Project</td><td>${doc.project}</td></tr>
    <tr><td>For</td><td>${doc.for || "Satva Solutions &mdash; internal &amp; client teams"}</td></tr>
    <tr><td>Prepared By</td><td>Satva Solutions</td></tr>
    <tr><td>Created On</td><td>${doc.created || ""}</td></tr>
  </table>
  <h2 style="text-align:left">Version History</h2>
  <table>
    <tr><th style="width:22%">Revision Date</th><th>Description of Change</th><th style="width:22%">Author</th></tr>
    ${rows}
  </table>
</section>

<div class="break"></div>
${fs.readFileSync(path.join(HERE, doc.body), "utf8")}
</body></html>`;

const tmp = path.join(HERE, `.render-${path.basename(doc.body)}`);
fs.writeFileSync(tmp, html);

let browser;
try { browser = await chromium.launch({ channel: "chrome" }); }
catch { browser = await chromium.launch(); } // ponytail: no Chrome installed -> bundled Chromium
const page = await browser.newPage();
await page.goto(pathToFileURL(tmp).href, { waitUntil: "networkidle" });
await page.waitForTimeout(900); // let web fonts and images settle before paginating
await page.pdf({
  path: path.join(HERE, doc.out),
  format: "A4",
  printBackground: true,
  margin: { top: "30mm", bottom: "22mm", left: "18mm", right: "18mm" },
  displayHeaderFooter: true,
  headerTemplate: `<style>html,body{margin:0;padding:0}</style><div style="width:100%;margin:-5.3mm 0 0;padding:0">
      <img src="${HEADER_IMG}" style="width:100%;display:block" /></div>`,
  footerTemplate: `<style>html,body{margin:0;padding:0}</style><div style="width:100%;font-family:Mulish,'Segoe UI',sans-serif;font-size:7pt;color:#5a6f80">
      <img src="${FOOTER_IMG}" style="width:100%;display:block" />
      <div style="display:flex;justify-content:space-between;padding:2px 12mm 0">
        <span>${doc.project} &mdash; ${doc.subtitle}</span>
        <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
      </div></div>`,
});
await browser.close();
fs.unlinkSync(tmp);
console.log(`${doc.out}  (${(fs.statSync(path.join(HERE, doc.out)).size / 1024).toFixed(0)} KB)`);
