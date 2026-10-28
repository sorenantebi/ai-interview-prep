// Adds C++ to the LeetCode problems: LeetCode's C++ starter -> starter.cpp, NeetCode's C++ solution -> a "## C++"
// section at the end of solution.md. Touches nothing else. Usage: node scripts/fetch-cpp.ts [only-this-slug]
import fs from "node:fs";
import path from "node:path";
import { leetcodeInfo, neetcodeSolution, slugOf } from "../src/lib/leetcode.ts";
import { withCpp } from "../src/lib/starter.ts";

const root = path.join(process.cwd(), "content/leetcode");
const only = process.argv[2];
const report = { starter: 0, solution: 0, noStarter: [] as string[], noSolution: [] as string[], failed: [] as string[] };

for (const topic of fs.readdirSync(root).filter((d) => fs.statSync(path.join(root, d)).isDirectory())) {
  for (const p of fs.readdirSync(path.join(root, topic))) {
    const dir = path.join(root, topic, p);
    const q = path.join(dir, "question.md");
    if (!fs.existsSync(q) || (only && p !== only)) continue;
    const slug = slugOf(fs.readFileSync(q, "utf8").match(/^leetcode:\s*(\S+)/m)?.[1]);
    if (!slug) { report.failed.push(`${p}: no leetcode url`); continue; }
    try {
      const info = await leetcodeInfo(slug);
      if (info.cppStarter) { fs.writeFileSync(path.join(dir, "starter.cpp"), info.cppStarter); report.starter++; } else report.noStarter.push(p);
      const cpp = await neetcodeSolution(info.id, "cpp");
      const s = path.join(dir, "solution.md");
      if (cpp && fs.existsSync(s)) { fs.writeFileSync(s, withCpp(fs.readFileSync(s, "utf8"), cpp)); report.solution++; } else report.noSolution.push(p);
    } catch (e) {
      report.failed.push(`${p}: ${(e as Error).message}`);
    }
    await new Promise((r) => setTimeout(r, 250)); // be polite to LeetCode
  }
}
console.log(JSON.stringify(report, null, 2));
