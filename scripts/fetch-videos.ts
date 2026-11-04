// Adds NeetCode's YouTube video to each LeetCode problem: a `video:` line in question.md's frontmatter, matched by the
// LeetCode slug in NeetCode's problem list (github.com/neetcode-gh/leetcode, MIT). Usage: node scripts/fetch-videos.ts
import fs from "node:fs";
import path from "node:path";
import { slugOf } from "../src/lib/leetcode.ts";

const root = path.join(process.cwd(), "content/leetcode");
const res = await fetch("https://raw.githubusercontent.com/neetcode-gh/leetcode/main/.problemSiteData.json");
if (!res.ok) throw new Error(`NeetCode problem list: HTTP ${res.status}`);
const videos = new Map((await res.json() as { link: string; video?: string }[]).filter((p) => p.video).map((p) => [p.link.replace(/\/$/, ""), p.video!]));
const report = { added: 0, none: [] as string[] };

for (const topic of fs.readdirSync(root).filter((d) => fs.statSync(path.join(root, d)).isDirectory())) {
  for (const p of fs.readdirSync(path.join(root, topic))) {
    const q = path.join(root, topic, p, "question.md");
    if (!fs.existsSync(q)) continue;
    const md = fs.readFileSync(q, "utf8");
    const id = videos.get(slugOf(md.match(/^leetcode:\s*(\S+)/m)?.[1]) ?? "");
    if (!id || !md.startsWith("---\n")) { report.none.push(p); continue; }
    const line = `video: https://www.youtube.com/watch?v=${id}`;
    fs.writeFileSync(q, /^video:.*$/m.test(md.split("\n---")[0]) ? md.replace(/^video:.*$/m, line) : md.replace("---\n", `---\n${line}\n`));
    report.added++;
  }
}
console.log(JSON.stringify(report, null, 1));
