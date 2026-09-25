// Where the satva-guide-gif skill lives. Override with SATVA_SKILL=/path/to/satva-guide-gif.
import os from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";

export const SKILL = process.env.SATVA_SKILL || path.join(os.homedir(), ".claude", "skills", "satva-guide-gif");
export const skillFile = (rel) => path.join(SKILL, rel);
export const skillUrl = (rel) => pathToFileURL(skillFile(rel)).href;
