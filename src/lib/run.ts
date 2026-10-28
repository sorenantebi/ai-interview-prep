import { execFile } from "node:child_process";
import { existsSync } from "node:fs";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";

const WIN = process.platform === "win32";
const VENV = path.join(process.cwd(), ".venv", WIN ? "Scripts/python.exe" : "bin/python");
/** PYTHON_BIN, else the project's .venv (npm run setup-python), else the system Python. */
export const python = () => process.env.PYTHON_BIN ?? (existsSync(VENV) ? VENV : WIN ? "python" : "python3");

// Runs the user's own code locally. shortcut: no sandbox, fine for a single-user local app; containerise before hosting.
export async function runPython(files: Record<string, string>, entry: string): Promise<{ ok: boolean; output: string }> {
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), "prep-run-"));
  // Importing torch alone can take several seconds on a cold start; C++ answers compile first.
  const limit = Object.values(files).some((f) => /^\s*(import|from) torch\b/m.test(f)) || "attempt.cpp" in files ? 30 : 10;
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

const CXX = process.env.CXX ?? (WIN ? "g++" : "c++");
// UBSan and the standard library's bounds checks catch overflow and out-of-range access (a double free still crashes).
// shortcut: no AddressSanitizer, its binaries hang on current macOS; add -fsanitize=address on Linux if use-after-free checks matter.
const SANITIZE = WIN ? [] : ["-fsanitize=undefined", "-fno-sanitize-recover=undefined", "-D_GLIBCXX_ASSERTIONS", "-D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_EXTENSIVE"];

type Exec = { code: number | null; killed: boolean; out: string };

/**
 * Your own compile commands, from the first lines of the file, run in order (C++ Basics):
 * `// compile: g++ -c main.cpp -o main.o` then `// compile: g++ main.o -o app`.
 * Returns each command's argv, or null without any; throws on a command it won't run.
 */
export function compileCommands(code: string): string[][] | null {
  const lines = code.match(/^(?:[ \t]*\/\/[ \t]*compile:.*\n?)+/)?.[0].trim().split("\n") ?? [];
  if (!lines.length) return null;
  return lines.map((line) => {
    const argv = (line.replace(/^\s*\/\/\s*compile:/, "").match(/(?:[^\s"']+|"[^"]*"|'[^']*')+/g) ?? []).map((t) => t.replace(/["']/g, ""));
    if (!["g++", "c++", "clang++", CXX].includes(argv[0])) throw new Error(`A compile line must start with g++, c++ or clang++ (got "${argv[0] ?? ""}").`);
    const o = argv.indexOf("-o");
    // outputs stay in the temp folder: a plain file name, so -o can't overwrite your files
    if (o >= 0 && !/^[\w.-]+$/.test(argv[o + 1] ?? "")) throw new Error("-o needs a plain file name, like -o app");
    return argv;
  });
}

/** Compiles `main` (with the other files next to it) in a temp dir, then hands the binary to `then`. `commands`: your own compile commands instead of ours. */
async function compiled<T>(files: Record<string, string>, main: string, then: (run: (args: string[], stdin?: string) => Promise<Exec & { stdout: string }>) => Promise<T>, commands?: string[][] | null): Promise<T | { ok: false; output: string; compileError: true }> {
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), "prep-cpp-"));
  const clean = (out: string) => out.replaceAll(dir + path.sep, "").replaceAll(dir, "").trim();
  const exec = (cmd: string, argv: string[], timeout: number, stdin = "") =>
    new Promise<Exec & { stdout: string }>((resolve) => {
      const child = execFile(cmd, argv, { cwd: dir, timeout, maxBuffer: 1 << 20 }, (err, stdout, stderr) =>
        resolve({
          code: !err ? 0 : typeof err.code === "number" ? err.code : err.code === "ENOENT" ? null : 1,
          killed: !!err?.killed,
          stdout,
          out: clean(stdout + stderr + (err?.signal && !err.killed ? `\nCrashed (${err.signal}): a double free, a null or dangling pointer, or an out-of-range access?` : "") + (err?.killed ? "\n⏱ Timed out after 20s (an infinite loop or a deadlock?)" : "")),
        }),
      );
      child.stdin?.on("error", () => {}); // the program may exit without reading its input
      child.stdin?.end(stdin);
    });
  try {
    for (const [name, content] of Object.entries(files)) await fs.writeFile(path.join(dir, name), content);
    let bin = path.join(dir, WIN ? "prog.exe" : "prog");
    for (const argv of commands ?? [[CXX, "-std=c++20", "-O1", "-g", "-pthread", ...SANITIZE, "-o", bin, main]]) {
      const c = await exec(argv[0], argv.slice(1), 60_000);
      if (c.code !== 0) {
        const missing = c.code === null || /not recognized/.test(c.out);
        return { ok: false, compileError: true, output: missing ? `No C++ compiler found (${argv[0]}). Install one (Xcode Command Line Tools on macOS, g++ on Linux/Windows).` : (commands ? `$ ${argv.join(" ")}\n` : "") + "Compile error:\n" + c.out.slice(0, 4000) };
      }
      const o = argv.indexOf("-o");
      if (commands) bin = path.join(dir, o >= 0 ? argv[o + 1] : WIN ? "a.exe" : "a.out"); // the last command's output is the program
    }
    return await then((args, stdin) => exec(bin, args, 20_000, stdin));
  } catch (e) {
    return { ok: false, compileError: true, output: (e as Error).message };
  } finally {
    await fs.rm(dir, { recursive: true, force: true });
  }
}

/** Compiles `main` (with the other files next to it) and runs it once. A compile error comes back with compileError set. */
export async function runCpp(files: Record<string, string>, main: string, args: string[] = []): Promise<{ ok: boolean; output: string; compileError?: boolean }> {
  return compiled(files, main, async (run) => {
    const r = await run(args);
    return { ok: r.code === 0, output: r.out.slice(0, 20_000) };
  });
}

export type IoCase = { name: string; stdin: string; stdout: string; example?: boolean };
export type IoResult = { name: string; stdin: string; expected: string; output: string; ok: boolean };
const sameOutput = (a: string, b: string) => a.replace(/[ \t]+$/gm, "").trim() === b.replace(/[ \t]+$/gm, "").trim();

/** C++ Basics: compiles your whole program (with its own main, and your own `// compile:` lines if it has them) and runs it on each case's stdin, comparing stdout. */
export async function runProgram(code: string, cases: IoCase[]): Promise<{ results: IoResult[] } | { ok: false; output: string; compileError: true }> {
  let commands;
  try {
    commands = compileCommands(code);
  } catch (e) {
    return { ok: false, compileError: true, output: (e as Error).message };
  }
  return compiled({ "main.cpp": code }, "main.cpp", async (run) => {
    const results: IoResult[] = [];
    for (const c of cases) {
      const r = await run([], c.stdin);
      const output = r.code === 0 || r.killed ? (r.killed ? r.out : r.stdout) : r.out;
      results.push({ name: c.name, stdin: c.stdin, expected: c.stdout, output: output.slice(0, 5000), ok: r.code === 0 && sameOutput(r.stdout, c.stdout) });
    }
    return { results };
  }, commands);
}

/** A C++ LeetCode answer as the files the Python tests / Run comparison need: attempt.py loads it through lc_bridge.py. */
export async function cppAttempt(code: string, starterCpp: string, starterPy: string): Promise<Record<string, string>> {
  const lib = path.join(process.cwd(), "src/lib/cpp");
  return {
    "attempt.py": "import lc_bridge\nlc_bridge.bind(globals())\nfrom lc_bridge import *\n",
    "attempt.cpp": code,
    "starter.cpp": starterCpp,
    "starter.py": starterPy,
    "lc_bridge.py": await fs.readFile(path.join(lib, "lc_bridge.py"), "utf8"),
    "lc_prelude.h": await fs.readFile(path.join(lib, "lc_prelude.h"), "utf8"),
  };
}

const MULTI = /any (of them|valid)|multiple (valid )?(answers|solutions)|more than one (valid )?answer/i;

export type CaseResult = { input: string[]; output?: string; expected?: string; ok?: boolean | null; error?: string; note?: string; stdout?: string };

/** Runs LeetCode-style cases against your code and the reference (NeetCode) code; see case_runner.py. */
export async function runCases(o: { attempt: string; reference: string; starter: string; cases: string[][]; question: string; files?: Record<string, string> }) {
  const runner = await fs.readFile(path.join(process.cwd(), "src/lib/case_runner.py"), "utf8");
  const spec = { cases: o.cases, anyOrder: /any order/i.test(o.question), multi: MULTI.test(o.question) };
  const r = await runPython(
    { "attempt.py": o.attempt, "reference.py": o.reference, "starter.py": o.starter, "spec.json": JSON.stringify(spec), "runner.py": runner, ...o.files }, // files: a C++ answer (cppAttempt)
    "runner.py",
  );
  const at = r.output.indexOf("__RESULTS__");
  if (at < 0) return { error: r.output || "The run produced no output" };
  return { results: JSON.parse(r.output.slice(at + "__RESULTS__".length)) as CaseResult[] };
}

/** Why a problem's hidden tests can't be trusted (they must pass the reference and fail the empty starter), or null. */
export async function testsProblem(o: { reference: string; starter: string; tests: string }): Promise<string | null> {
  const ref = await runPython({ "attempt.py": o.reference, "tests.py": o.tests }, "tests.py");
  if (!ref.ok) {
    const lines = ref.output.split("\n");
    const fail = lines.find((l) => l.trim() && !/^PASS\b/.test(l) && !/^\d+\/\d+ passed/.test(l)) ?? "";
    const summary = lines.find((l) => /^\d+\/\d+ passed/.test(l));
    // No summary line: tests.py itself crashed, so its traceback is the useful part.
    return summary ? `The solution fails the tests: ${summary}\n\n${fail.slice(0, 600)}` : "tests.py crashed with the solution:\n\n" + ref.output.slice(-1500);
  }
  if ((await runPython({ "attempt.py": o.starter, "tests.py": o.tests }, "tests.py")).ok) return "The tests also pass the empty starter, so they don't check anything.";
  return null;
}
