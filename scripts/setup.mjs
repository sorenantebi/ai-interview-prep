// One-time setup after cloning: installs packages, builds, and creates the app for this OS, so the first click opens fast.
// `npm run setup -- --python` also installs the ML Coding / Jupyter packages (a few GB with torch).
import { execSync } from "node:child_process";

const run = (cmd) => execSync(cmd, { stdio: "inherit" });
const app = { darwin: "mac-app", linux: "linux-app", win32: "windows-app" }[process.platform];
run("npm install");
run("npm run build");
if (process.argv.includes("--python")) run("npm run setup-python");
if (app) run(`npm run ${app}`);
console.log(`\nSetup done.${process.argv.includes("--python") ? "" : " For ML Coding and notebooks, also run: npm run setup-python"}`);
