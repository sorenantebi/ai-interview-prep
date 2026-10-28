import fs from "node:fs/promises";
import nodePath from "node:path";
import { NextRequest, NextResponse } from "next/server";
import { logActivity, read, safePath, setProgress, write } from "@/lib/content";
import { generateTests } from "@/lib/hidden-tests";
import { cppAttempt, runCases, runCpp, runProgram, runPython, type CaseResult, type IoCase } from "@/lib/run";
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
 * Quant Dev (C++) problems. tests.cpp: Run shows the EXAMPLE cases, Submit runs them all.
 * tests.json (C++ Basics, whole programs): Run feeds the example inputs to your program, Submit all of them.
 */
async function quant(path: string, code: string, mode: string): Promise<{ results?: CaseResult[]; error?: string; ok?: boolean; output?: string }> {
  const testsJson = await read(`${path}/tests.json`);
  if (testsJson !== null) {
    const all: IoCase[] = JSON.parse(testsJson).cases;
    const r = await runProgram(code, mode === "run" ? all.filter((c) => c.example) : all);
    if (!("results" in r)) return mode === "run" ? { error: r.output } : { ok: false, output: r.output };
    if (mode === "run") return { results: r.results.map((x) => ({ input: [x.stdin], output: x.output, expected: x.expected, ok: x.ok })) };
    const fail = r.results.find((x) => !x.ok);
    const summary = `${r.results.filter((x) => x.ok).length}/${r.results.length} passed`;
    return { ok: !fail, output: fail ? `${summary}\n\nFAIL ${fail.name}\nInput:\n${fail.stdin}\nExpected:\n${fail.expected}\nGot:\n${fail.output}` : `Accepted · ${summary}` };
  }
  const tests = await read(`${path}/tests.cpp`);
  if (tests === null) throw new Error("This problem has no tests.cpp or tests.json");
  const qtest = await fs.readFile(nodePath.join(process.cwd(), "src/lib/cpp/qtest.h"), "utf8");
  const r = await runCpp({ "qtest.h": qtest, "tests.cpp": tests, "attempt.cpp": code }, "tests.cpp", mode === "run" ? ["--examples"] : []);
  if (mode !== "run") return { ok: r.ok, output: r.compileError ? r.output : hidden(r) };
  if (r.compileError) return { error: r.output };
  // Example lines: "PASS <name>" / "FAIL <name><TAB>why"; anything else (a crash, a timeout) is shown as the error.
  const results: CaseResult[] = r.output.split("\n").flatMap((l) => {
    const m = l.match(/^(PASS|FAIL) ([^\t]*)(?:\t(.*))?$/);
    return m ? [{ input: [m[2]], ok: m[1] === "PASS", ...(m[3] ? { output: m[3] } : {}) }] : []; // a failed check is a wrong answer, not a crash
  });
  const extra = r.output.split("\n").filter((l) => !/^(PASS|FAIL) |^\d+\/\d+ passed$/.test(l)).join("\n").trim();
  return results.length && !extra ? { results } : { error: r.output || "No output" };
}

/**
 * mode "run": your test cases, compared with the NeetCode reference (like LeetCode's Run).
 * mode "submit": the hidden tests.py (like LeetCode's Submit), written by Claude when the problem is added, or here if it has none. Only Submit marks a problem solved.
 * lang "cpp": a C++ answer; LeetCode's run through lc_bridge.py under the same tests, Quant Dev's compile with their C++ tests.
 */
export async function POST(req: NextRequest) {
  const { path, code, mode, cases, names, regenerate, time, space, lang } = await req.json();
  try {
    safePath(path);
    const area = String(path).split("/")[0];
    const cpp = lang === "cpp" || area === "quant-dev";
    await write(`${path}/${cpp ? "attempt.cpp" : "attempt.py"}`, code);
    await logActivity();

    let r: { ok: boolean; output: string };
    let question = "";
    if (area === "quant-dev") {
      const q = await quant(path, code, mode);
      if (mode === "run") return NextResponse.json(q);
      r = { ok: !!q.ok, output: q.output ?? "" };
    } else {
      const [questionFile, solution, starterFile, starterCpp] = await Promise.all(["question.md", "solution.md", "starter.py", "starter.cpp"].map((f) => read(`${path}/${f}`)));
      question = questionFile ?? "";
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
      r = { ok: p.ok, output: hidden(p) };
    }

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
