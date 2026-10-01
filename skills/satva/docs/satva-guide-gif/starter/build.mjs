/** Runs the whole pipeline: screenshots -> GIF frames -> GIF + storyboard -> PDF. `npm run build` */
import { spawnSync } from "node:child_process";
import { skillFile } from "./paths.mjs";

const run = (cmd, args) => {
  const r = spawnSync(cmd, args, { stdio: "inherit" });
  if (r.status !== 0) { console.error(`FAILED: ${cmd} ${args.join(" ")}`); process.exit(r.status ?? 1); }
};
const python = spawnSync("python3", ["--version"]).status === 0 ? "python3" : "python";

run("node", ["capture.mjs"]);
run("node", ["frames.mjs"]);
run(python, [skillFile("scripts/build-gif.py"), "gif/frames", "Satva-Guide-Sample-Demo.gif", "storyboard.png"]);
run("node", [skillFile("scripts/build-pdf.mjs"), "doc.json"]);
