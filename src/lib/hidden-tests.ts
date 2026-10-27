import { claude, files, prompt } from "./claude.ts";
import { read, write } from "./content.ts";
import { testsProblem } from "./run.ts";
import { codeBlock, starterFrom } from "./starter.ts";

/**
 * Has Claude write a LeetCode problem's hidden tests (<dir>/tests.py) and saves them only if NeetCode's solution passes
 * and the empty starter fails; one retry that shows Claude what was wrong. Returns the tests, or throws why it couldn't.
 */
export async function generateTests(dir: string, opts: { model?: string } = {}) {
  const [question, solution, starter] = await Promise.all(["question.md", "solution.md", "starter.py"].map((f) => read(`${dir}/${f}`)));
  const reference = codeBlock(solution ?? "");
  const input = await prompt("generate-tests", { question: question ?? "", solution: solution ?? "" });
  let problem = "";
  for (let attempt = 1; attempt <= 2; attempt++) {
    const retry = problem ? `\n\n# Your previous tests.py was wrong, fix it:\n${problem.slice(-1500)}` : "";
    const tests = files((await claude(input + retry, opts)).text)["tests.py"]?.replace(/^```\w*\n|\n?```\s*$/g, "");
    problem = tests ? (await testsProblem({ reference, starter: starter ?? starterFrom(reference), tests })) ?? "" : "Your reply had no tests.py section.";
    if (!problem) {
      await write(`${dir}/tests.py`, tests!);
      return tests!;
    }
  }
  throw new Error(`Claude couldn't write hidden tests that NeetCode's solution passes: ${problem.slice(0, 600)}`);
}
