import { NextRequest, NextResponse } from "next/server";
import { logActivity, read, safePath, write } from "@/lib/content";
import { claude, files, prompt } from "@/lib/claude";
import { leetcodeInfo, neetcodeSolution, slugOf } from "@/lib/leetcode";

const slug = (s: string) => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

/** Writes question.md/solution.md from a model reply into <area>/<group>/<slug of title>. */
async function saveProblem(text: string, area: string, group: string) {
  const f = files(text);
  if (!f["question.md"] || !f["solution.md"]) throw new Error("Claude's reply did not contain question.md and solution.md:\n\n" + text.slice(0, 1500));
  const title = f["question.md"].match(/^# (?:Design )?(.+)$/m)?.[1] ?? "untitled";
  const dir = `${area}/${group}/${slug(title)}`;
  if ((await read(`${dir}/question.md`)) !== null) throw new Error(`${dir} already exists`);
  await write(`${dir}/question.md`, f["question.md"]);
  await write(`${dir}/solution.md`, f["solution.md"]);
  return dir;
}

const topicName = (group: string) => group.replace(/^\d+\s*/, "");

/** LeetCode's starter -> starter.py, NeetCode's code -> the solution's code block (as for the seeded problems). */
async function applyLeetcodeAndNeetcode(dir: string, url: string) {
  const slug = slugOf(url);
  if (!slug) return;
  const info = await leetcodeInfo(slug);
  if (info.starter) await write(`${dir}/starter.py`, info.starter);
  const nc = await neetcodeSolution(info.id);
  const solution = await read(`${dir}/solution.md`);
  if (nc && solution?.includes("```python")) await write(`${dir}/solution.md`, solution.replace(/```python\n[\s\S]*?```/, () => "```python\n" + nc + "```"));
}

export async function POST(req: NextRequest) {
  const b = await req.json();
  try {
    switch (b.action) {
      case "add-leetcode": {
        safePath(`leetcode/${b.group}`);
        const format = await prompt("_leetcode-format", { topic: topicName(b.group) });
        const input = await prompt("add-leetcode-from-link", { url: b.url, format });
        const { text } = await claude(input, { tools: ["WebFetch"] });
        const dir = await saveProblem(text, "leetcode", b.group);
        await applyLeetcodeAndNeetcode(dir, b.url).catch(() => {}); // best effort: Claude's files still work without it
        return NextResponse.json({ path: dir });
      }
      case "generate-leetcode": {
        safePath(`leetcode/${b.group}`);
        const format = await prompt("_leetcode-format", { topic: topicName(b.group) });
        const input = await prompt("generate-leetcode", { topic: topicName(b.group), difficulty: b.difficulty, idea: b.idea || "none", format });
        return NextResponse.json({ path: await saveProblem((await claude(input)).text, "leetcode", b.group) });
      }
      case "system-design": {
        safePath(`system-design/${b.group}`);
        const input = await prompt("system-design", { request: b.request, category: topicName(b.group) });
        return NextResponse.json({ path: await saveProblem((await claude(input, { tools: ["WebFetch"] })).text, "system-design", b.group) });
      }
      case "hint": {
        const input = await prompt("hint", { mode: b.mode, question: (await read(`${b.path}/question.md`)) ?? "", code: b.code, output: b.output || "(not run yet)" });
        return NextResponse.json({ text: (await claude(input)).text });
      }
      case "interview": {
        await logActivity();
        // First turn builds the interviewer prompt; later turns resume the same CLI session.
        if (b.sessionId) return NextResponse.json(await claude(b.message, { sessionId: b.sessionId }));
        const problem = b.problemPath ? ((await read(`${b.problemPath}/question.md`)) ?? "") : `choose (theme: ${b.theme || "any"})`;
        const input = (await prompt(b.kind === "system-design" ? "interview-system-design" : "interview-coding", { problem })) + "\n\nBegin the interview now.";
        return NextResponse.json(await claude(input));
      }
      default:
        return NextResponse.json({ error: `Unknown action ${b.action}` }, { status: 400 });
    }
  } catch (e) {
    return NextResponse.json({ error: (e as Error).message }, { status: 500 });
  }
}
