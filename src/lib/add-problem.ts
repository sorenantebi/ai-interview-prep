import { claude, files, prompt } from "./claude.ts";
import { read, write } from "./content.ts";
import { leetcodeInfo, neetcodeSolution, slugOf } from "./leetcode.ts";
import { withCpp } from "./starter.ts";

export const slug = (s: string) => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
export const unfence = (code: string) => code.replace(/^```\w*\n|\n?```\s*$/g, "");
export const topicName = (group: string) => group.replace(/^\d+\s*/, "");

/** Writes question.md/solution.md (and any `extra` files) from a model reply into <area>/<group>/<slug of title>. */
export async function saveProblem(text: string, area: string, group: string, extra: string[] = []) {
  const f = files(text);
  if (!f["question.md"] || !f["solution.md"]) throw new Error("Claude's reply did not contain question.md and solution.md:\n\n" + text.slice(0, 1500));
  const title = f["question.md"].match(/^# (?:Design )?(.+)$/m)?.[1] ?? "untitled";
  const dir = `${area}/${group}/${slug(title)}`;
  if ((await read(`${dir}/question.md`)) !== null) throw new Error(`${dir} already exists`);
  await write(`${dir}/question.md`, f["question.md"]);
  await write(`${dir}/solution.md`, f["solution.md"]);
  for (const name of extra) await write(`${dir}/${name}`, unfence(f[name]));
  return dir;
}

/** LeetCode's starters -> starter.py / starter.cpp, NeetCode's code -> the solution's code block and its C++ section. */
export async function applyLeetcodeAndNeetcode(dir: string, url: string) {
  const s = slugOf(url);
  if (!s) return;
  const info = await leetcodeInfo(s);
  if (info.starter) await write(`${dir}/starter.py`, info.starter);
  if (info.cppStarter) await write(`${dir}/starter.cpp`, info.cppStarter);
  const [nc, ncCpp] = await Promise.all([neetcodeSolution(info.id), neetcodeSolution(info.id, "cpp")]);
  let solution = await read(`${dir}/solution.md`);
  if (nc && solution?.includes("```python")) solution = solution.replace(/```python\n[\s\S]*?```/, () => "```python\n" + nc + "```");
  if (ncCpp && solution) solution = withCpp(solution, ncCpp);
  if (solution) await write(`${dir}/solution.md`, solution);
}

/** LeetCode's statement as plain text, for Claude to read (LeetCode's pages need JavaScript, so fetching them often fails). */
const pageText = (html: string) =>
  html.replace(/<sup>(.*?)<\/sup>/g, "^$1").replace(/<br\s*\/?>|<\/(p|li|pre|div)>/gi, "\n").replace(/<[^>]+>/g, "")
    .replace(/&nbsp;/g, " ").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&amp;/g, "&")
    .replace(/\n{3,}/g, "\n\n").trim();

/** Claude writes question.md / solution.md for a LeetCode link, then LeetCode's starters and NeetCode's code go in. */
export async function addFromLink(url: string, group: string, opts: { model?: string } = {}) {
  const format = await prompt("_leetcode-format", { topic: topicName(group) });
  const content = await leetcodeInfo(slugOf(url) ?? "").then((i) => i.content, () => null);
  const input = await prompt("add-leetcode-from-link", { url, format }) +
    (content ? `\n\n# The problem page's text (use this, no need to fetch the page)\n\n${pageText(content)}` : "");
  const { text } = await claude(input, { ...opts, tools: content ? [] : ["WebFetch"] });
  const dir = await saveProblem(text, "leetcode", group);
  await applyLeetcodeAndNeetcode(dir, url).catch(() => {}); // best effort: Claude's files still work without it
  return dir;
}
