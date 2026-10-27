// npm start: installs packages if needed, builds if the code changed, starts the server and opens your browser.
// Ctrl+C stops it. If prep is already running, it just opens the browser.
import { execSync, spawn } from "node:child_process";
import fs from "node:fs";

const PORT = process.env.PORT ?? "3000";
const URL = `http://localhost:${PORT}`;
const run = (cmd) => execSync(cmd, { stdio: "inherit" });
const up = () => fetch(`${URL}/api/progress`).then((r) => r.ok, () => false);
const mtime = (p) => fs.statSync(p, { throwIfNoEntry: false })?.mtimeMs ?? 0;
const newer = (p, t) => fs.statSync(p).isDirectory() ? fs.readdirSync(p).some((f) => newer(`${p}/${f}`, t)) : mtime(p) > t;
function openBrowser() {
  const [cmd, args] = process.platform === "darwin" ? ["open", [URL]] : process.platform === "win32" ? ["cmd", ["/c", "start", "", URL]] : ["xdg-open", [URL]];
  spawn(cmd, args, { stdio: "ignore", detached: true }).unref();
}

if (await up()) {
  console.log(`prep is already running at ${URL}`);
  openBrowser();
  process.exit(0);
}
// After a fresh clone or a pull that changed dependencies.
if (mtime("package-lock.json") > mtime("node_modules/.package-lock.json")) run("npm install");
const built = mtime(".next/BUILD_ID");
if (!built || ["src", "public", "package.json", "next.config.ts"].some((p) => newer(p, built))) run("npx next build");

const server = spawn(process.execPath, ["node_modules/next/dist/bin/next", "start", "-H", "127.0.0.1", "-p", PORT], { stdio: "inherit" });
server.on("exit", (code) => process.exit(code ?? 0));
for (const sig of ["SIGINT", "SIGTERM", "SIGHUP"]) process.on(sig, () => server.kill(sig)); // closing the terminal stops the server too
for (let i = 0; i < 60 && !(await up()); i++) await new Promise((r) => setTimeout(r, 500));
openBrowser();
