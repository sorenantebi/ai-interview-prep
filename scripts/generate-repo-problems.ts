// Generates the Repo Debugging problems in bulk with Claude: each one is kept only if the original repo fails the tests and
// the solution passes them (a failed one is retried once, with the reason). Problems already there are skipped.
// Usage: node scripts/generate-repo-problems.ts <list.json> [--model sonnet] [--jobs 4]
//   list.json: [{ "group": "01 Bug Fixing", "kind": "bug-fix" | "extend" | "multi-stage", "difficulty": "Easy" | "Medium" | "Hard", "idea": "<scenario>" }]
import fs from "node:fs";
import { claude, prompt } from "../src/lib/claude.ts";
import { saveRepoProblem } from "../src/lib/repo.ts";

const arg = (name: string, dflt: string) => { const i = process.argv.indexOf(name); return i > 0 ? process.argv[i + 1] : dflt; };
const model = arg("--model", "sonnet"), jobs = Number(arg("--jobs", "4"));
const list: { group: string; kind: string; difficulty: string; idea: string }[] = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const failed: string[] = [];
let done = 0;

async function one(p: (typeof list)[number]) {
  const input = await prompt("generate-repo-debugging", { kind: p.kind, difficulty: p.difficulty, idea: p.idea });
  let why = "";
  for (let attempt = 1; attempt <= 2; attempt++) {
    try {
      const retry = why ? `\n\nYour previous attempt was rejected: ${why.slice(0, 1500)}\nWrite the whole problem again, fixed.` : "";
      const dir = await saveRepoProblem((await claude(input + retry, { model })).text, p.group);
      console.log(`✓ ${++done}/${list.length} ${dir}`);
      return;
    } catch (e) {
      why = (e as Error).message;
      if (/already exists/.test(why)) { console.log(`- ${++done}/${list.length} ${why}`); return; }
    }
  }
  failed.push(`${p.idea.slice(0, 60)}: ${why.slice(0, 300)}`);
  console.log(`✗ ${++done}/${list.length} ${p.idea.slice(0, 60)}`);
}

const queue = [...list];
await Promise.all(Array.from({ length: jobs }, async () => { while (queue.length) await one(queue.shift()!); }));
console.log(`\ndone: ${list.length - failed.length} ok, ${failed.length} failed`);
if (failed.length) console.log(failed.join("\n"));
