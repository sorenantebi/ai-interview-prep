import { NextRequest, NextResponse } from "next/server";
import { difficultyOf, interviewMinutes } from "@/lib/interview";
import { areaStats, logActivity, progress, read, safePath, submissions } from "@/lib/content";
import { shuffle } from "@/lib/order";
import { claude, files, prompt } from "@/lib/claude";
import { testsProblem } from "@/lib/run";
import { generateTests } from "@/lib/hidden-tests";
import { codeBlock } from "@/lib/starter";
import { addFromLink, saveProblem, topicName, unfence } from "@/lib/add-problem";
import { checkComplexity } from "@/lib/complexity";

/** Writes the hidden tests now, so Submit never waits on Claude; if that fails the problem is still kept, and Submit tries again. */
const testsWarning = (dir: string) =>
  generateTests(dir).then(() => undefined, (e) => `${(e as Error).message}\n\nThe problem is saved; Submit will try writing the tests again.`);

export async function POST(req: NextRequest) {
  const b = await req.json();
  try {
    switch (b.action) {
      case "add-leetcode": {
        safePath(`leetcode/${b.group}`);
        const dir = await addFromLink(String(b.url), b.group);
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
        const input = await prompt("hint", { question: (await read(`${b.path}/question.md`)) ?? "", code: b.code, lang: b.lang === "cpp" ? "cpp" : "python", output: b.output || "(not run yet)" });
        return NextResponse.json({ text: (await claude(input)).text });
      }
      case "complexity": {
        return NextResponse.json(await checkComplexity((await read(`${b.path}/question.md`)) ?? "", String(b.code ?? ""), undefined, b.lang === "cpp" ? "cpp" : "python"));
      }
      case "interview": {
        await logActivity();
        // First turn builds the interviewer prompt; later turns resume the same CLI session.
        if (b.sessionId) return NextResponse.json(await claude(b.message, { sessionId: b.sessionId }));
        // Claude picks the same "obvious" problem for the same prompt, so the randomness comes from here: no theme → a
        // random problem from your list; a theme → Claude picks from the list in a fresh random order.
        const prog = await progress();
        const isSolved = (p: string) => prog[p]?.status === "solved";
        // Your solved problems only when you ask for them (the option, or a theme like "one I've solved").
        const all = (await areaStats(b.kind === "system-design" ? "system-design" : "leetcode")).flatMap((g) => g.problems).filter((p) => !b.solvedOnly || isSolved(p.path));
        if (!all.length) throw new Error("You haven't solved any problems here yet.");
        const path: string | undefined = b.problemPath || (b.theme ? undefined : all[Math.floor(Math.random() * all.length)]?.path);
        const problem = path
          ? ((await read(`${path}/question.md`)) ?? "")
          : `choose (theme: ${b.theme}). Pick from this list, which is in random order: take the first one that fits the theme. ` +
            `"(solved)" marks problems the candidate has solved before; only use that if the theme asks for it.\n` +
            shuffle(all.map((p) => `- ${p.title} (${p.difficulty ?? "?"})${isSolved(p.path) ? " (solved)" : ""}`), Date.now()).join("\n");
        // The candidate's past passing answers to this problem, for the feedback (the interviewer keeps them to itself).
        const past = path && b.kind !== "system-design" ? await submissions(path) : [];
        const history = past.length
          ? past.map((x) => `${x.at ? x.at.slice(0, 10) : "earlier"} (${x.lang}${x.time || x.space ? `, said time ${x.time || "?"} / space ${x.space || "?"}` : ""}):\n\`\`\`${x.lang}\n${x.code}\n\`\`\``).join("\n\n")
          : "none";
        const minutes = interviewMinutes(b.kind, path ? difficultyOf(problem) : undefined);
        const input = (await prompt(b.kind === "system-design" ? "interview-system-design" : "interview-coding", { problem, minutes: String(minutes), history })) + "\n\nBegin the interview now.";
        return NextResponse.json({ ...(await claude(input)), minutes }); // the page starts its clock when this first reply arrives
      }
      default:
        return NextResponse.json({ error: `Unknown action ${b.action}` }, { status: 400 });
    }
  } catch (e) {
    return NextResponse.json({ error: (e as Error).message }, { status: 500 });
  }
}
