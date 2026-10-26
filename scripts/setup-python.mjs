// Creates .venv with the packages the ML Coding section needs (numpy, pandas, torch, and Jupyter for notebooks in Repos). The app uses .venv's Python when it exists.
import { execFileSync } from "node:child_process";
import { existsSync } from "node:fs";
import path from "node:path";

const win = process.platform === "win32";
const venvPython = path.join(".venv", win ? "Scripts/python.exe" : "bin/python");
const run = (cmd, args) => execFileSync(cmd, args, { stdio: "inherit" });
if (!existsSync(venvPython)) run(win ? "python" : "python3", ["-m", "venv", ".venv"]);
run(venvPython, ["-m", "pip", "install", "--upgrade", "numpy", "pandas", "torch", "notebook"]);
console.log("Python packages ready in .venv.");
