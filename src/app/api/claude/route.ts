import { NextRequest, NextResponse } from "next/server";
import { difficultyOf, interviewMinutes } from "@/lib/interview";
import { areaStats, logActivity, read, safePath, write } from "@/lib/content";
import { shuffle } from "@/lib/order";
import { claude, files, prompt } from "@/lib/claude";
import { testsProblem } from "@/lib/run";
import { generateTests } from "@/lib/hidden-tests";
import { codeBlock } from "@/lib/starter";
import { leetcodeInfo, neetcodeSolution, slugOf } from "@/lib/leetcode";
import { checkComplexity } from "@/lib/complexity";

const slug = (s: string) => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

const unfence = (code: string) => code.replace(/^```\w*\n|\n?```\s*$/g, "");

/** Writes question.md/solution.md (and any `extra` files) from a model reply into <area>/<group>/<slug of title>. */
async function saveProblem(text: string, area: string, group: string, extra: string[] = []) {
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

/** Writes the hidden tests now, so Submit never waits on Claude; if that fails the problem is still kept, and Submit tries again. */
const testsWarning = (dir: string) =>
  generateTests(dir).then(() => undefined, (e) => `${(e as Error).message}\n\nThe problem is saved; Submit will try writing the tests again.`);

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
        return NextResponse.json({ path: dir, warning: await testsWarning(dir) });
      }
      case "generate-leetcode": {
        safePath(`leetcode/${b.group}`);
        const format = await prompt("_leetcode-format", { topic: topicName(b.group) });
        const input = await prompt("generate-leetcode", { topic: topicName(b.group), difficulty: b.difficulty, idea: b.idea || "none", format });
        const dir = await saveProblem((await claude(input)).text, "leetcode", b.group);
        return NextResponse.json({ path: dir, warning: await testsWarning(dir) });
      }
      case "generate-ml-coding": {
        safePath(`ml-coding/${b.group}`);
        const names = ["question.md", "starter.py", "solution.md", "tests.py"];
        const template = (await Promise.all(names.map(async (n) => `=== FILE: ${n} ===\n${(await read(`ml-coding/_template/${n}`)) ?? ""}`))).join("\n") + "\n=== END ===";
        const input = await prompt("generate-ml-coding", { topic: topicName(b.group), difficulty: b.difficulty, idea: b.idea || "none", template });
        const { text } = await claude(input);
        const f = files(text);
        if (!f["starter.py"] || !f["tests.py"]) throw new Error("Claude's reply did not contain starter.py and tests.py:\n\n" + text.slice(0, 1500));
        // Only keep a problem whose tests accept the reference solution and reject the empty starter.
        const bad = await testsProblem({ reference: codeBlock(f["solution.md"] ?? ""), starter: unfence(f["starter.py"]), tests: unfence(f["tests.py"]) });
        if (bad) throw new Error(`Nothing was saved, try again. ${bad}`);
        return NextResponse.json({ path: await saveProblem(text, "ml-coding", b.group, ["starter.py", "tests.py"]) });
      }
      case "system-design": {
        safePath(`system-design/${b.group}`);
        const input = await prompt("system-design", { request: b.request, category: topicName(b.group) });
        return NextResponse.json({ path: await saveProblem((await claude(input, { tools: ["WebFetch"] })).text, "system-design", b.group) });
      }
      case "hint": {
        const input = await prompt("hint", { question: (await read(`${b.path}/question.md`)) ?? "", code: b.code, output: b.output || "(not run yet)" });
        return NextResponse.json({ text: (await claude(input)).text });
      }
      case "complexity": {
        return NextResponse.json(await checkComplexity((await read(`${b.path}/question.md`)) ?? "", String(b.code ?? "")));
      }
      case "interview": {
        await logActivity();
        // First turn builds the interviewer prompt; later turns resume the same CLI session.
        if (b.sessionId) return NextResponse.json(await claude(b.message, { sessionId: b.sessionId }));
        // Claude picks the same "obvious" problem for the same prompt, so the randomness comes from here: no theme → a
        // random problem from your list; a theme → Claude picks from the list in a fresh random order.
        const all = (await areaStats(b.kind === "system-design" ? "system-design" : "leetcode")).flatMap((g) => g.problems);
        const path: string | undefined = b.problemPath || (b.theme ? undefined : all[Math.floor(Math.random() * all.length)]?.path);
        const problem = path
          ? ((await read(`${path}/question.md`)) ?? "")
          : `choose (theme: ${b.theme}). Pick from this list, which is in random order: take the first one that fits the theme.\n` +
            shuffle(all.map((p) => `- ${p.title} (${p.difficulty ?? "?"})`), Date.now()).join("\n");
        const minutes = interviewMinutes(b.kind, path ? difficultyOf(problem) : undefined);
        const input = (await prompt(b.kind === "system-design" ? "interview-system-design" : "interview-coding", { problem, minutes: String(minutes) })) + "\n\nBegin the interview now.";
        return NextResponse.json({ ...(await claude(input)), minutes }); // the page starts its clock when this first reply arrives
      }
      default:
        return NextResponse.json({ error: `Unknown action ${b.action}` }, { status: 400 });
    }
  } catch (e) {
    return NextResponse.json({ error: (e as Error).message }, { status: 500 });
  }
}
