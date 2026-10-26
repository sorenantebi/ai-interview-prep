import { execFile } from "node:child_process";
import { existsSync } from "node:fs";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";

const WIN = process.platform === "win32";
const VENV = path.join(process.cwd(), ".venv", WIN ? "Scripts/python.exe" : "bin/python");
/** PYTHON_BIN, else the project's .venv (npm run setup-python), else the system Python. */
const python = () => process.env.PYTHON_BIN ?? (existsSync(VENV) ? VENV : WIN ? "python" : "python3");

// Runs the user's own code locally. shortcut: no sandbox, fine for a single-user local app; containerise before hosting.
export async function runPython(files: Record<string, string>, entry: string): Promise<{ ok: boolean; output: string }> {
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), "prep-run-"));
  // Importing torch alone can take several seconds on a cold start.
  const limit = Object.values(files).some((f) => /^\s*(import|from) torch\b/m.test(f)) ? 30 : 10;
  try {
    for (const [name, content] of Object.entries(files)) await fs.writeFile(path.join(dir, name), content);
    return await new Promise((resolve) => {
      execFile(python(), [entry], { cwd: dir, timeout: limit * 1000, maxBuffer: 1 << 20 }, (err, stdout, stderr) => {
        const killed = err && "killed" in err && err.killed;
        const missing = /No module named '(numpy|pandas|torch)'/.test(stderr) ? "\nThis needs numpy, pandas and torch: run `npm run setup-python` once." : "";
        resolve({ ok: !err, output: (stdout + stderr + (killed ? `\n⏱ Timed out after ${limit}s` : "") + missing).trim() });
      });
    });
  } finally {
    await fs.rm(dir, { recursive: true, force: true });
  }
}

const MULTI = /any (of them|valid)|multiple (valid )?(answers|solutions)|more than one (valid )?answer/i;

export type CaseResult = { input: string[]; output?: string; expected?: string; ok?: boolean | null; error?: string; note?: string; stdout?: string };

/** Runs LeetCode-style cases against your code and the reference (NeetCode) code; see case_runner.py. */
export async function runCases(o: { attempt: string; reference: string; starter: string; cases: string[][]; question: string }) {
  const runner = await fs.readFile(path.join(process.cwd(), "src/lib/case_runner.py"), "utf8");
  const spec = { cases: o.cases, anyOrder: /any order/i.test(o.question), multi: MULTI.test(o.question) };
  const r = await runPython(
    { "attempt.py": o.attempt, "reference.py": o.reference, "starter.py": o.starter, "spec.json": JSON.stringify(spec), "runner.py": runner },
    "runner.py",
  );
  const at = r.output.indexOf("__RESULTS__");
  if (at < 0) return { error: r.output || "The run produced no output" };
  return { results: JSON.parse(r.output.slice(at + "__RESULTS__".length)) as CaseResult[] };
}
