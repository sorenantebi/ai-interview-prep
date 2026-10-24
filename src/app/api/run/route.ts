import { NextRequest, NextResponse } from "next/server";
import { logActivity, read, safePath, setProgress, write } from "@/lib/content";
import { claude, files, prompt } from "@/lib/claude";
import { runCases, runPython } from "@/lib/run";
import { completeTasks } from "@/lib/plan";
import { checkComplexity } from "@/lib/complexity";
import { codeBlock, starterFrom } from "@/lib/starter";

/**
 * mode "run": your test cases, compared with the NeetCode reference (like LeetCode's Run).
 * mode "submit": Claude's hidden tests.py, generated on first use (like LeetCode's Submit). Only Submit marks a problem solved.
 */
export async function POST(req: NextRequest) {
  const { path, code, mode, cases, names, regenerate, time, space } = await req.json();
  try {
    safePath(path);
    await write(`${path}/attempt.py`, code);
    await logActivity();
    const [question, solution, starterFile] = await Promise.all(["question.md", "solution.md", "starter.py"].map((f) => read(`${path}/${f}`)));
    const reference = codeBlock(solution ?? "");

    if (mode === "run") {
      if (Array.isArray(cases)) await write(`${path}/testcases.json`, JSON.stringify({ names, cases }, null, 2));
      const r = await runCases({ attempt: code, reference, starter: starterFile ?? starterFrom(reference), cases, question: question ?? "" });
      return NextResponse.json(r);
    }

    // Stating your complexity is optional; without it Submit doesn't need Claude at all (once tests.py exists).
    const claimed = { time: String(time ?? "").trim(), space: String(space ?? "").trim() };
    let tests = regenerate ? null : await read(`${path}/tests.py`);
    if (tests === null) {
      const input = await prompt("generate-tests", { question: question ?? "", solution: solution ?? "" });
      tests = files((await claude(input)).text)["tests.py"]?.replace(/^```\w*\n|\n?```\s*$/g, "") ?? null;
      if (!tests) throw new Error("Claude did not return a tests.py section");
      await write(`${path}/tests.py`, tests);
    }
    const r = await runPython({ "attempt.py": code, "tests.py": tests }, "tests.py");
    let complexity = null;
    if (r.ok) {
      await write(`${path}/solved.py`, code); // snapshot of your passing code, shown in the cheat sheet
      await completeTasks(path);
    }
    if (r.ok && (claimed.time || claimed.space)) {
      // Check the complexity you stated against your code (a failed check, e.g. Claude offline, doesn't undo the solve).
      try {
        complexity = { ...(await checkComplexity(question ?? "", code, claimed)), at: new Date().toISOString() };
        await write(`${path}/complexity.json`, JSON.stringify(complexity, null, 2));
      } catch (e) {
        complexity = { error: (e as Error).message };
      }
    }
    await setProgress(path, r.ok ? "solved" : "attempted");
    // Hidden tests: show the summary and the first failure only, never the passing cases.
    const lines = r.output.split("\n");
    const firstFail = lines.findIndex((l) => !/^PASS\b/.test(l) && l.trim() && !/^\d+\/\d+ passed/.test(l));
    const summary = lines.find((l) => /^\d+\/\d+ passed/.test(l)) ?? "";
    const output = r.ok ? `Accepted · ${summary}` : [summary, firstFail >= 0 ? lines.slice(firstFail, firstFail + 6).join("\n") : ""].filter(Boolean).join("\n\n");
    return NextResponse.json({ ok: r.ok, output, complexity });
  } catch (e) {
    return NextResponse.json({ error: (e as Error).message }, { status: 500 });
  }
}
