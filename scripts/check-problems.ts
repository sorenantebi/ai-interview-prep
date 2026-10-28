// Checks coding problems end to end: node scripts/check-problems.ts <problem dir or topic dir>...
// C++ problems (a tests.cpp): see checkCpp. Python problems:
// The question's examples run through Run tests (and print next to the question's Output lines),
// the hidden tests pass with the reference solution and fail with the empty starter.
import fs from "node:fs";
import path from "node:path";
import { codeBlock, parseExamples } from "../src/lib/starter.ts";
import { runCases, runCpp, runProgram, runPython, type IoCase } from "../src/lib/run.ts";

const qtest = fs.readFileSync("src/lib/cpp/qtest.h", "utf8");
/** C++ problems (Quant Dev): the reference passes every case, the starter compiles and fails, there are examples. */
async function checkCpp(dir: string, read: (f: string) => string): Promise<string[]> {
  const problems: string[] = [];
  const [question, solution, starter, tests] = ["question.md", "solution.md", "starter.cpp", "tests.cpp"].map(read);
  const reference = codeBlock(solution, "cpp");
  if (!reference) problems.push("solution.md has no ```cpp block");
  if (!/^difficulty: (Easy|Medium|Hard)$/m.test(question)) problems.push("question.md frontmatter needs difficulty: Easy|Medium|Hard");
  const examples = (tests.match(/^EXAMPLE\(/gm) ?? []).length, cases = (tests.match(/^CASE\(/gm) ?? []).length;
  if (examples < 1 || cases < 4) problems.push(`tests.cpp needs at least 1 EXAMPLE and 4 CASE (has ${examples} / ${cases})`);
  const run = (attempt: string, args: string[] = []) => runCpp({ "qtest.h": qtest, "tests.cpp": tests, "attempt.cpp": attempt }, "tests.cpp", args);
  const pass = await run(reference);
  if (!pass.ok) problems.push("the reference fails:\n" + pass.output.split("\n").filter((l) => !l.startsWith("PASS")).slice(0, 10).join("\n"));
  else console.log(`  ${path.basename(dir)}: ${pass.output.split("\n").at(-1)}`);
  const ex = await run(reference, ["--examples"]);
  if (!ex.ok) problems.push("the reference fails the examples:\n" + ex.output.slice(0, 800));
  const fail = await run(starter);
  if (fail.compileError) problems.push("the starter doesn't compile with tests.cpp:\n" + fail.output.slice(0, 1500));
  else if (fail.ok) problems.push("the hidden tests pass with the starter");
  return problems;
}

const dirs = process.argv.slice(2).flatMap((d) => (fs.existsSync(path.join(d, "question.md")) ? [d] : fs.readdirSync(d).map((x) => path.join(d, x)).filter((x) => fs.existsSync(path.join(x, "question.md")))));
let bad = 0;
/** Whole C++ programs (C++ Basics, a tests.json of stdin/stdout cases): the reference passes, the starter compiles and fails. */
async function checkProgram(dir: string, read: (f: string) => string): Promise<string[]> {
  const problems: string[] = [];
  const [question, solution, starter] = ["question.md", "solution.md", "starter.cpp"].map(read);
  const cases: IoCase[] = JSON.parse(read("tests.json")).cases;
  const reference = codeBlock(solution, "cpp");
  if (!reference) problems.push("solution.md has no ```cpp block");
  if (!/^difficulty: (Easy|Medium|Hard)$/m.test(question)) problems.push("question.md frontmatter needs difficulty: Easy|Medium|Hard");
  if (cases.filter((c) => c.example).length < 1 || cases.filter((c) => !c.example).length < 4) problems.push("tests.json needs at least 1 example case and 4 hidden cases");
  const pass = await runProgram(reference, cases);
  if (!("results" in pass)) problems.push("the reference doesn't compile:\n" + pass.output.slice(0, 1500));
  else {
    for (const r of pass.results.filter((r) => !r.ok)) problems.push(`the reference fails "${r.name}": got ${JSON.stringify(r.output)}, expected ${JSON.stringify(r.expected)}`);
    console.log(`  ${path.basename(dir)}: ${pass.results.filter((r) => r.ok).length}/${cases.length} passed`);
  }
  const fail = await runProgram(starter, cases);
  if (!("results" in fail)) problems.push("the starter doesn't compile:\n" + fail.output.slice(0, 1500));
  else if (fail.results.every((r) => r.ok)) problems.push("the starter passes every case");
  return problems;
}

/** Python problems (ML Coding): the examples run, the reference passes tests.py and the starter fails it. */
async function checkPython(dir: string, read: (f: string) => string): Promise<string[]> {
  const problems: string[] = [];
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
  return problems;
}

for (const dir of dirs) {
  const read = (f: string) => fs.readFileSync(path.join(dir, f), "utf8");
  let problems: string[];
  try {
    const has = (f: string) => fs.existsSync(path.join(dir, f));
    problems = await (has("tests.cpp") ? checkCpp : has("tests.json") ? checkProgram : checkPython)(dir, read);
  } catch (e) {
    problems = [(e as Error).message];
  }
  if (problems.length) bad++;
  console.log(`${problems.length ? "✗" : "✓"} ${dir}${problems.length ? "\n    " + problems.join("\n    ") : ""}`);
}
console.log(`${dirs.length - bad}/${dirs.length} problems OK`);
process.exit(bad ? 1 : 0);
