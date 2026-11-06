import fs from "node:fs/promises";
import path from "node:path";
import { read, remove, safePath, write } from "./content.ts";
import { runPython } from "./run.ts";
import { files } from "./claude.ts";
import { slug } from "./add-problem.ts";

/**
 * A repo problem: content/repo-debugging/<topic>/<slug>/ holds question.md, repo/ (the project, with its visible tests in
 * repo/tests/), hidden_tests.py, solution/ (the fixed files and solution.md) and work.json (your changes, git-ignored).
 */
export const AREA = "repo-debugging";

/** Every text file under a folder of a problem, by path relative to that folder ("inventory/models.py"). */
export async function folderFiles(rel: string): Promise<Record<string, string>> {
  const out: Record<string, string> = {};
  const walk = async (sub: string) => {
    const entries = await fs.readdir(safePath(path.posix.join(rel, sub)), { withFileTypes: true }).catch(() => []);
    for (const e of entries) {
      const p = sub ? `${sub}/${e.name}` : e.name;
      if (e.isDirectory()) { if (e.name !== "__pycache__") await walk(p); }
      else if (!/\.pyc$/.test(e.name)) out[p] = (await read(path.posix.join(rel, p))) ?? "";
    }
  };
  await walk("");
  return out;
}

/** Your changes to a repo: changed and added files, and the original files you deleted. */
type Work = { files: Record<string, string>; deleted: string[] };

/** The project as you see it: the original repo with your changes, additions and deletions applied. */
export async function workingRepo(problem: string) {
  const repo = await folderFiles(`${problem}/repo`);
  let work: Work = { files: {}, deleted: [] };
  try { work = { ...work, ...JSON.parse((await read(`${problem}/work.json`)) ?? "{}") }; } catch {}
  const files = Object.fromEntries(Object.entries(repo).filter(([f]) => !work.deleted.includes(f)));
  return { repo, files: { ...files, ...work.files } };
}

/** A file name inside the repo: relative, no "..", no hidden files. */
export const repoFileName = (f: string) => /^(?!\/)(?!.*(^|\/)\.)[\w./-]+$/.test(f) && !f.split("/").includes("..") && !f.endsWith("/");

/** Saves the whole project as you have it now (every file), as its difference from the original repo in work.json. */
export async function saveWork(problem: string, files: Record<string, string>) {
  const names = Object.keys(files);
  if (names.length > 300 || names.some((f) => !repoFileName(f) || typeof files[f] !== "string" || files[f].length > 500_000)) throw new Error("Bad file name or file too large");
  const { repo } = await workingRepo(problem);
  const work: Work = { files: Object.fromEntries(Object.entries(files).filter(([f, c]) => repo[f] !== c)), deleted: Object.keys(repo).filter((f) => !(f in files)) };
  if (Object.keys(work.files).length || work.deleted.length) await write(`${problem}/work.json`, JSON.stringify(work, null, 1));
  else await remove(`${problem}/work.json`).catch(() => {});
}

/** Runs the visible tests (Run) or the visible plus hidden tests (Submit) against a set of repo files. */
export async function runRepo(problem: string, files: Record<string, string>, hidden: boolean) {
  const runner = await fs.readFile(path.join(process.cwd(), "src/lib/repo_runner.py"), "utf8");
  const extra: Record<string, string> = { "repo_runner.py": runner };
  if (hidden) extra["hidden_tests.py"] = (await read(`${problem}/hidden_tests.py`)) ?? "";
  return runPython({ ...files, ...extra }, "repo_runner.py", 30);
}

/** Why a repo problem can't be trusted (the original must fail Submit, the solution must pass it), or null. */
export async function repoProblem(problem: string): Promise<string | null> {
  const repo = await folderFiles(`${problem}/repo`);
  const fixed = Object.fromEntries(Object.entries(await folderFiles(`${problem}/solution`)).filter(([f]) => f !== "solution.md"));
  const extra = Object.keys(fixed).filter((f) => !(f in repo));
  if (extra.length) return `solution/ has files that aren't in repo/: ${extra.join(", ")}`;
  if ((await runRepo(problem, repo, true)).ok) return "The original repo already passes the tests.";
  const sol = await runRepo(problem, { ...repo, ...fixed }, true);
  return sol.ok ? null : "The solution fails the tests:\n" + sol.output.slice(-1500);
}

/** Saves a generated repo problem (Claude's `=== FILE:` reply) under a topic, keeping it only if its tests check out. */
export async function saveRepoProblem(reply: string, group: string): Promise<string> {
  const f = files(reply);
  const title = f["question.md"]?.match(/^# (.+)$/m)?.[1];
  if (!title || !f["hidden_tests.py"] || !f["solution/solution.md"] || !Object.keys(f).some((k) => k.startsWith("repo/tests/")))
    throw new Error("The reply is missing question.md, repo/tests/, hidden_tests.py or solution/solution.md");
  const dir = `${AREA}/${group}/${slug(title)}`;
  if ((await read(`${dir}/question.md`)) !== null) throw new Error(`${dir} already exists`);
  const odd = Object.keys(f).find((name) => !repoFileName(name) || !/^(question\.md|hidden_tests\.py|repo\/|solution\/)/.test(name));
  if (odd) throw new Error(`Unexpected file ${odd}`);
  for (const [name, content] of Object.entries(f)) await write(`${dir}/${name}`, content);
  const bad = await repoProblem(dir);
  if (bad) {
    await remove(dir);
    throw new Error(bad);
  }
  return dir;
}
