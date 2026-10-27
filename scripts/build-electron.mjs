// Builds the desktop app: a self-contained Next.js server plus the starter content, packaged with Electron.
// `npm run dist` makes the installer for this OS in dist/ (a .dmg on macOS); `--no-pack` only stages .electron/ for `npm run electron`.
import { execFileSync, execSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const run = (cmd, env = {}) => execSync(cmd, { stdio: "inherit", env: { ...process.env, ...env } });
const OUT = ".electron";
fs.rmSync(OUT, { recursive: true, force: true });

run("npx next build", { STANDALONE: "1", NEXT_DIST_DIR: ".next-electron" });
fs.cpSync(".next-electron/standalone", `${OUT}/server`, { recursive: true, verbatimSymlinks: true });
fs.cpSync(".next-electron/static", `${OUT}/server/.next-electron/static`, { recursive: true });
fs.cpSync("public", `${OUT}/server/public`, { recursive: true });

// Starter content: only what git tracks or would track (new, not ignored), never your progress, notes or code.
const ls = (...args) => execFileSync("git", ["ls-files", "-z", ...args, "content"], { encoding: "utf8" }).split("\0").filter(Boolean);
const tracked = [...new Set([...ls("--recurse-submodules"), ...ls("--others", "--exclude-standard")])];
for (const f of tracked) {
  fs.mkdirSync(path.dirname(`${OUT}/${f}`), { recursive: true });
  fs.copyFileSync(f, `${OUT}/${f}`);
}
console.log(`Staged ${tracked.length} content files.`);

if (!process.argv.includes("--no-pack")) run("npx electron-builder --publish never");
