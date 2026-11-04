import { NextRequest, NextResponse } from "next/server";
import { logActivity, read, safePath, setProgress, write } from "@/lib/content";
import { generateTests } from "@/lib/hidden-tests";
import { cppAttempt, runCases, runPython } from "@/lib/run";
import { completeTasks } from "@/lib/plan";
import { checkComplexity } from "@/lib/complexity";
import { codeBlock, starterFrom } from "@/lib/starter";

/** Hidden tests: the summary and the first failure only, never the passing cases. */
function hidden(r: { ok: boolean; output: string }) {
  const bridge = r.output.match(/lc_bridge\.(?:CompileError|Unsupported): ([\s\S]*)/);
  if (bridge) return (/CompileError/.test(r.output) ? "Compile error:\n" : "") + bridge[1].trim();
  const lines = r.output.split("\n");
  const firstFail = lines.findIndex((l) => !/^PASS\b/.test(l) && l.trim() && !/^\d+\/\d+ passed/.test(l));
  const summary = lines.find((l) => /^\d+\/\d+ passed/.test(l)) ?? "";
  return r.ok ? `Accepted · ${summary}` : [summary, firstFail >= 0 ? lines.slice(firstFail, firstFail + 6).join("\n") : ""].filter(Boolean).join("\n\n");
}

/**
 * mode "run": your test cases, compared with the NeetCode reference (like LeetCode's Run).
 * mode "submit": the hidden tests.py (like LeetCode's Submit), written by Claude when the problem is added, or here if it has none. Only Submit marks a problem solved.
 * lang "cpp": a C++ answer, run through lc_bridge.py under the same tests.
 */
export async function POST(req: NextRequest) {
  const { path, code, mode, cases, names, regenerate, time, space, lang } = await req.json();
  try {
    safePath(path);
    const cpp = lang === "cpp";
    await write(`${path}/${cpp ? "attempt.cpp" : "attempt.py"}`, code);
    await logActivity();

    const [questionFile, solution, starterFile, starterCpp] = await Promise.all(["question.md", "solution.md", "starter.py", "starter.cpp"].map((f) => read(`${path}/${f}`)));
    const question = questionFile ?? "";
    const reference = codeBlock(solution ?? "");
    const starter = starterFile ?? starterFrom(reference);
    if (cpp && starterCpp === null) throw new Error("C++ isn't available for this problem yet (no C++ starter). Use Python here.");
    const files = cpp ? await cppAttempt(code, starterCpp!, starter) : { "attempt.py": code };

    if (mode === "run") {
      if (Array.isArray(cases)) await write(`${path}/testcases.json`, JSON.stringify({ names, cases }, null, 2));
      const run = await runCases({ attempt: code, reference, starter, cases, question, files });
      // A compile error shows up as the same load error on every case: show it once.
      const first = "results" in run ? run.results?.[0]?.error : undefined;
      if (cpp && first && /CompileError|Unsupported/.test(first)) return NextResponse.json({ error: first.replace(/^\w+Error: |^Unsupported: /, "") });
      return NextResponse.json(run);
    }
    let tests = regenerate ? null : await read(`${path}/tests.py`);
    tests ??= await generateTests(path);
    const p = await runPython({ ...files, "tests.py": tests }, "tests.py");
    const r = { ok: p.ok, output: hidden(p) };

    // Stating your complexity is optional; without it Submit doesn't need Claude at all (once the tests exist).
    const claimed = { time: String(time ?? "").trim(), space: String(space ?? "").trim() };
    let complexity = null;
    if (r.ok) {
      await write(`${path}/${cpp ? "solved.cpp" : "solved.py"}`, code); // snapshot of your passing code, shown in the cheat sheet
      await completeTasks(path);
    }
    if (r.ok && (claimed.time || claimed.space)) {
      // Check the complexity you stated against your code (a failed check, e.g. Claude offline, doesn't undo the solve).
      try {
        complexity = { ...(await checkComplexity(question, code, claimed, cpp ? "cpp" : "python")), at: new Date().toISOString() };
        await write(`${path}/${cpp ? "complexity.cpp.json" : "complexity.json"}`, JSON.stringify(complexity, null, 2)); // per language, like solved.py / solved.cpp
      } catch (e) {
        complexity = { error: (e as Error).message };
      }
    }
    await setProgress(path, r.ok ? "solved" : "attempted");
    return NextResponse.json({ ok: r.ok, output: r.output, complexity });
  } catch (e) {
    return NextResponse.json({ error: (e as Error).message }, { status: 500 });
  }
}
