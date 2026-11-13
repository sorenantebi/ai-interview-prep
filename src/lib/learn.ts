import { read, write } from "./content.ts";
import { claude, prompt } from "./claude.ts";
import { runPython } from "./run.ts";
import { codeBlock } from "./starter.ts";
import { topicName } from "./add-problem.ts";

/**
 * learn.md: the beginner lesson of an ML Coding problem (the idea, a worked example, the tools with demos, common
 * mistakes, hints), shown in the problem's Learn tab.
 */
const SECTIONS = ["# Learn:", "## The idea", "## Work it by hand", "## Tools you'll need", "## Common mistakes", "## Hints", "### Hint 1", "### Hint 2", "### Hint 3"];

// Runs every python block in its own namespace and names the first one that fails.
const RUNNER = `import json, traceback
for i, src in enumerate(json.load(open("blocks.json")), 1):
    try:
        exec(compile(src, f"block {i}", "exec"), {"__name__": "__main__"})
    except Exception:
        print(f"Python block {i} fails:\\n{src}\\n{traceback.format_exc(limit=1)}")
        raise SystemExit(1)
`;

/** Why a learn page can't be kept (missing sections, a demo that doesn't run, the solution's code in it), or null. */
export async function learnProblem(md: string, solution: string): Promise<string | null> {
  const missing = SECTIONS.filter((s) => !md.split("\n").some((l) => l.startsWith(s)));
  if (missing.length) return `Missing sections: ${missing.join(", ")}`;
  const leaked = codeBlock(solution).split("\n").map((l) => l.trim())
    .filter((l) => l.length >= 20 && !/^(import|from|def|return \w+$)/.test(l))
    .find((l) => md.includes(l));
  if (leaked) return `It contains a line of the solution: ${leaked}`;
  const blocks = [...md.matchAll(/```python\n([\s\S]*?)```/g)].map((m) => m[1]);
  if (!blocks.length) return "No runnable ```python demos in Tools you'll need.";
  const run = await runPython({ "run.py": RUNNER, "blocks.json": JSON.stringify(blocks) }, "run.py", 60);
  return run.ok ? null : run.output.slice(-1500);
}

/**
 * Writes learn.md for an ML Coding problem with Claude, keeping it only if it passes learnProblem (one retry).
 * `redo`: rewrite the existing learn.md in the current format instead of starting from scratch.
 */
export async function writeLearn(problem: string, model?: string, redo = false): Promise<void> {
  const [question, solution] = await Promise.all([read(`${problem}/question.md`), read(`${problem}/solution.md`)]);
  if (!question || !solution) throw new Error(`${problem} needs question.md and solution.md`);
  const old = redo ? await read(`${problem}/learn.md`) : null;
  const rewrite = old ? `\n\nAn older version of this page, in a different format, is below. Rewrite it into the format above, keeping its content, numbers and demos where they are right:\n<old-page>\n${old}\n</old-page>` : "";
  const input = await prompt("ml-learn", { topic: topicName(problem.split("/")[1]), question, solution, rewrite });
  let why = "";
  for (let attempt = 1; attempt <= 2; attempt++) {
    const retry = why ? `\n\nYour previous page was rejected: ${why}\nWrite the whole page again, fixed.` : "";
    const md = (await claude(input + retry, { model })).text.trim().replace(/^```(?:markdown|md)?\n([\s\S]*)\n```$/, "$1");
    why = (await learnProblem(md, solution)) ?? "";
    if (!why) return write(`${problem}/learn.md`, md + "\n");
  }
  throw new Error(why);
}
