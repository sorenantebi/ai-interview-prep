// Pre-generates the hidden Submit tests (tests.py) for every LeetCode problem that doesn't have them yet.
// Each file is checked like when you add a problem: NeetCode's solution must pass and the empty starter fail (one retry).
// Usage: node scripts/generate-tests.ts [--model sonnet] [--jobs 4] [--force]
import fs from "node:fs";
import path from "node:path";
import { generateTests } from "../src/lib/hidden-tests.ts";

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
  try {
    await generateTests(`leetcode/${name}`, { model });
    console.log(`✓ ${++done}/${todo.length} ${name}`);
  } catch (e) {
    failed.push(`${name}: ${(e as Error).message.split("\n").filter(Boolean).slice(-2).join(" / ").slice(0, 200)}`);
    console.log(`✗ ${++done}/${todo.length} ${name}`);
  }
}

const queue = [...todo];
await Promise.all(Array.from({ length: jobs }, async () => { while (queue.length) await one(queue.shift()!); }));
console.log(`\ndone: ${todo.length - failed.length} saved, ${failed.length} failed`);
if (failed.length) console.log(failed.join("\n"));
