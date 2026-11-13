// Writes the Learn tab (learn.md) of ML Coding problems with Claude; problems that already have one are skipped.
// Usage: node scripts/generate-learn.ts [problem or topic path under content/, e.g. "ml-coding/01 NumPy"] [--model sonnet] [--jobs 4] [--redo]
//   --redo: rewrite the existing pages in the current format of content/prompts/ml-learn.md too
import { areaStats, read } from "../src/lib/content.ts";
import { writeLearn } from "../src/lib/learn.ts";

const arg = (name: string, dflt: string) => { const i = process.argv.indexOf(name); return i > 0 ? process.argv[i + 1] : dflt; };
const model = arg("--model", "sonnet"), jobs = Number(arg("--jobs", "4"));
const only = process.argv[2]?.startsWith("--") ? "" : (process.argv[2] ?? "");
const redo = process.argv.includes("--redo");
const all = (await areaStats("ml-coding")).flatMap((g) => g.problems.map((p) => p.path)).filter((p) => p.startsWith(only));
const todo: string[] = [];
for (const p of all) if (redo || (await read(`${p}/learn.md`)) === null) todo.push(p);
const failed: string[] = [];
let done = 0;

const queue = [...todo];
await Promise.all(Array.from({ length: jobs }, async () => {
  while (queue.length) {
    const p = queue.shift()!;
    try {
      await writeLearn(p, model, redo);
      console.log(`✓ ${++done}/${todo.length} ${p}`);
    } catch (e) {
      failed.push(`${p}: ${(e as Error).message.slice(0, 400)}`);
      console.log(`✗ ${++done}/${todo.length} ${p}`);
    }
  }
}));
console.log(`\ndone: ${todo.length - failed.length} ok, ${failed.length} failed`);
if (failed.length) console.log(failed.join("\n"));
