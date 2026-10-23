// One-off: for every LeetCode problem in content/, write LeetCode's Python starter to starter.py and swap the
// code in solution.md for NeetCode's solution. Usage: node scripts/fetch-neetcode.ts [only-this-slug]
import fs from "node:fs";
import path from "node:path";
import { leetcodeInfo, neetcodeSolution, slugOf } from "../src/lib/leetcode.ts";
import { codeBlock, starterFrom } from "../src/lib/starter.ts";

const root = path.join(process.cwd(), "content/leetcode");
const only = process.argv[2];
const report = { starter: 0, derived: [] as string[], neetcode: 0, noNeetcode: [] as string[], failed: [] as string[] };

for (const topic of fs.readdirSync(root).filter((d) => fs.statSync(path.join(root, d)).isDirectory())) {
  for (const p of fs.readdirSync(path.join(root, topic))) {
    const dir = path.join(root, topic, p);
    const q = path.join(dir, "question.md");
    const s = path.join(dir, "solution.md");
    if (!fs.existsSync(q) || (only && p !== only)) continue;
    const slug = slugOf(fs.readFileSync(q, "utf8").match(/^leetcode:\s*(\S+)/m)?.[1]);
    if (!slug) { report.failed.push(`${p}: no leetcode url`); continue; }
    try {
      const info = await leetcodeInfo(slug);
      const solution = fs.existsSync(s) ? fs.readFileSync(s, "utf8") : "";
      // Premium problems have no LeetCode starter: take the signature from the existing (typed) solution.
      const starter = info.starter ?? starterFrom(codeBlock(solution));
      if (!info.starter) report.derived.push(p);
      else report.starter++;
      fs.writeFileSync(path.join(dir, "starter.py"), starter);

      const nc = await neetcodeSolution(info.id);
      if (nc && solution.includes("```python")) {
        fs.writeFileSync(s, solution.replace(/```python\n[\s\S]*?```/, () => "```python\n" + nc + "```"));
        report.neetcode++;
      } else report.noNeetcode.push(p);
    } catch (e) {
      report.failed.push(`${p}: ${(e as Error).message}`);
    }
    await new Promise((r) => setTimeout(r, 250)); // be polite to LeetCode
  }
}
console.log(JSON.stringify(report, null, 2));
