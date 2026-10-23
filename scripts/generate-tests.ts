// Pre-generates the hidden Submit tests (tests.py) for every LeetCode problem that doesn't have them yet.
// Each file is checked against NeetCode's solution: tests that fail on the reference are wrong, so they're retried once.
// Usage: node scripts/generate-tests.ts [--model sonnet] [--jobs 4] [--force]
import fs from "node:fs";
import path from "node:path";
import { claude, files, prompt } from "../src/lib/claude.ts";
import { runPython } from "../src/lib/run.ts";
import { codeBlock } from "../src/lib/starter.ts";

const arg = (name: string, dflt: string) => { const i = process.argv.indexOf(name); return i > 0 ? process.argv[i + 1] : dflt; };
const model = arg("--model", "sonnet"), jobs = Number(arg("--jobs", "4")), force = process.argv.includes("--force");
const root = path.join(process.cwd(), "content/leetcode");
const todo = fs.readdirSync(root).flatMap((t) => fs.readdirSync(path.join(root, t)).map((p) => path.join(root, t, p)))
  .filter((d) => fs.existsSync(path.join(d, "question.md")) && (force || !fs.existsSync(path.join(d, "tests.py"))));

console.log(`${todo.length} problems to do · model ${model} · ${jobs} at a time`);
const failed: string[] = [];
let done = 0;

async function one(dir: string) {
  const name = path.relative(root, dir);
  const question = fs.readFileSync(path.join(dir, "question.md"), "utf8");
  const solution = fs.readFileSync(path.join(dir, "solution.md"), "utf8");
  const reference = codeBlock(solution);
  let last = "";
  for (let attempt = 1; attempt <= 2; attempt++) {
    try {
      const extra = attempt > 1 ? `\n\n# Your previous tests failed on the correct reference solution. Fix them:\n${last.slice(-1500)}` : "";
      const tests = files((await claude((await prompt("generate-tests", { question, solution })) + extra, { model })).text)["tests.py"]?.replace(/^```\w*\n|\n?```\s*$/g, "");
      if (!tests) { last = "no tests.py in the answer"; continue; }
      const r = await runPython({ "attempt.py": reference, "tests.py": tests }, "tests.py");
      if (r.ok) { fs.writeFileSync(path.join(dir, "tests.py"), tests); console.log(`✓ ${++done}/${todo.length} ${name}`); return; }
      last = r.output;
    } catch (e) { last = (e as Error).message; }
  }
  failed.push(`${name}: ${last.split("\n").filter(Boolean).slice(-2).join(" / ").slice(0, 200)}`);
  console.log(`✗ ${++done}/${todo.length} ${name}`);
}

const queue = [...todo];
await Promise.all(Array.from({ length: jobs }, async () => { while (queue.length) await one(queue.shift()!); }));
console.log(`\ndone: ${todo.length - failed.length} saved, ${failed.length} failed`);
if (failed.length) console.log(failed.join("\n"));
