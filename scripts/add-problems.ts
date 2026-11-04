// Adds LeetCode problems in bulk, like "Add from link" on the AI page: Claude writes question.md / solution.md, LeetCode's
// starters and NeetCode's solution go in, then the hidden tests are written and checked. Problems already in content/ are skipped.
// Usage: node scripts/add-problems.ts <list.json> [--model sonnet] [--jobs 4]
//   list.json: [{ "url": "https://leetcode.com/problems/<slug>/", "group": "<NN Topic folder>", "video": "<YouTube id>" | null,
//                "neetcode": "<neetcode.io problem url>" | null }]   (null: Claude's guessed neetcode link is dropped)
import fs from "node:fs";
import path from "node:path";
import { addFromLink } from "../src/lib/add-problem.ts";
import { generateTests } from "../src/lib/hidden-tests.ts";
import { slugOf } from "../src/lib/leetcode.ts";

const arg = (name: string, dflt: string) => { const i = process.argv.indexOf(name); return i > 0 ? process.argv[i + 1] : dflt; };
const model = arg("--model", "sonnet"), jobs = Number(arg("--jobs", "4"));
const list: { url: string; group: string; video?: string | null; neetcode?: string | null }[] = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const root = path.join(process.cwd(), "content/leetcode");

const have = new Set(fs.readdirSync(root).flatMap((t) => fs.statSync(path.join(root, t)).isDirectory() ? fs.readdirSync(path.join(root, t)).map((p) => path.join(root, t, p, "question.md")) : [])
  .filter((q) => fs.existsSync(q)).map((q) => slugOf(fs.readFileSync(q, "utf8").match(/^leetcode:\s*(\S+)/m)?.[1])));
const todo = list.filter((p) => !have.has(slugOf(p.url)));
console.log(`${todo.length} problems to add (${list.length - todo.length} already there) · model ${model} · ${jobs} at a time`);

const failed: string[] = [], noTests: string[] = [];
let done = 0;
async function one(p: (typeof list)[number]) {
  const name = slugOf(p.url);
  try {
    fs.mkdirSync(path.join(root, p.group), { recursive: true });
    const dir = await addFromLink(p.url, p.group, { model });
    for (const f of ["question.md", "solution.md"]) {
      const file = path.join(process.cwd(), "content", dir, f);
      let md = fs.readFileSync(file, "utf8").replace(/^neetcode:.*\n/m, "");
      if (p.neetcode) md = md.replace(/^(leetcode:.*\n)/m, `$1neetcode: ${p.neetcode}\n`);
      if (p.video && f === "question.md") md = md.replace("---\n", `---\nvideo: https://www.youtube.com/watch?v=${p.video}\n`);
      fs.writeFileSync(file, md);
    }
    await generateTests(dir, { model }).catch((e) => noTests.push(`${dir}: ${(e as Error).message.slice(0, 200)}`));
    console.log(`✓ ${++done}/${todo.length} ${dir}`);
  } catch (e) {
    failed.push(`${name}: ${(e as Error).message.slice(0, 300)}`);
    console.log(`✗ ${++done}/${todo.length} ${name}`);
  }
}

const queue = [...todo];
await Promise.all(Array.from({ length: jobs }, async () => { while (queue.length) await one(queue.shift()!); }));
console.log(`\ndone: ${todo.length - failed.length} added, ${failed.length} failed, ${noTests.length} without hidden tests (Submit writes them later)`);
if (failed.length) console.log("failed:\n" + failed.join("\n"));
if (noTests.length) console.log("no tests:\n" + noTests.join("\n"));
