// Checks coding problems end to end: node scripts/check-problems.ts <problem dir or topic dir>...
// The question's examples run through Run tests (and print next to the question's Output lines),
// the hidden tests pass with the reference solution and fail with the empty starter.
import fs from "node:fs";
import path from "node:path";
import { codeBlock, parseExamples } from "../src/lib/starter.ts";
import { runCases, runPython } from "../src/lib/run.ts";

const dirs = process.argv.slice(2).flatMap((d) => (fs.existsSync(path.join(d, "question.md")) ? [d] : fs.readdirSync(d).map((x) => path.join(d, x)).filter((x) => fs.existsSync(path.join(x, "question.md")))));
let bad = 0;
for (const dir of dirs) {
  const read = (f: string) => fs.readFileSync(path.join(dir, f), "utf8");
  const problems: string[] = [];
  try {
    const [question, solution, starter, tests] = ["question.md", "solution.md", "starter.py", "tests.py"].map(read);
    const reference = codeBlock(solution);
    if (!reference) problems.push("solution.md has no ```python block");
    if (!/^difficulty: (Easy|Medium|Hard)$/m.test(question)) problems.push("question.md frontmatter needs difficulty: Easy|Medium|Hard");
    const ex = parseExamples(question, starter);
    if (ex.cases.length < 2 || ex.cases.some((c) => c.length !== ex.names.length || c.some((v) => !v))) problems.push(`examples not parsed: names=${JSON.stringify(ex.names)} cases=${JSON.stringify(ex.cases)}`);
    const run = await runCases({ attempt: reference, reference, starter, cases: ex.cases, question });
    if ("error" in run) problems.push("Run tests failed: " + run.error);
    else {
      const outputs = [...question.matchAll(/^Output:\s*(.+)$/gm)].map((m) => m[1].trim());
      run.results!.forEach((r, i) => {
        if (r.ok !== true) problems.push(`example ${i + 1}: ${JSON.stringify(r)}`);
        console.log(`  ${path.basename(dir)} example ${i + 1}: question says ${outputs[i]} | reference gives ${r.output}`);
      });
    }
    const pass = await runPython({ "attempt.py": reference, "tests.py": tests }, "tests.py");
    if (!pass.ok) problems.push("hidden tests fail with the reference:\n" + pass.output.split("\n").filter((l) => !l.startsWith("PASS")).slice(0, 8).join("\n"));
    if (!/^\d+\/\d+ passed$/m.test(pass.output)) problems.push("tests.py must print an 'N/M passed' line");
    const fail = await runPython({ "attempt.py": starter, "tests.py": tests }, "tests.py");
    if (fail.ok) problems.push("hidden tests pass with the empty starter");
  } catch (e) {
    problems.push((e as Error).message);
  }
  if (problems.length) bad++;
  console.log(`${problems.length ? "✗" : "✓"} ${dir}${problems.length ? "\n    " + problems.join("\n    ") : ""}`);
}
console.log(`${dirs.length - bad}/${dirs.length} problems OK`);
process.exit(bad ? 1 : 0);
