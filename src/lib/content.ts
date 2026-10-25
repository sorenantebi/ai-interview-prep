import fs from "node:fs/promises";
import path from "node:path";
import matter from "gray-matter";

export const ROOT = path.resolve(process.env.CONTENT_DIR ?? path.join(process.cwd(), "content"));

/** Resolves a content-relative path; throws if it escapes ROOT. */
export function safePath(rel: string): string {
  const abs = path.resolve(ROOT, rel);
  if (abs !== ROOT && !abs.startsWith(ROOT + path.sep)) throw new Error(`Path outside content: ${rel}`);
  return abs;
}

export type TreeNode = { name: string; path: string; dir: boolean; children?: TreeNode[] };

export async function tree(rel = ""): Promise<TreeNode[]> {
  const entries = await fs.readdir(safePath(rel), { withFileTypes: true });
  const nodes = await Promise.all(
    entries
      .filter((e) => !e.name.startsWith("."))
      .sort((a, b) => Number(b.isDirectory()) - Number(a.isDirectory()) || a.name.localeCompare(b.name, undefined, { numeric: true }))
      .map(async (e) => {
        const p = path.posix.join(rel, e.name);
        if (!e.isDirectory()) return { name: e.name, path: p, dir: false };
        // Cloned repos can be huge: the Files tree lists them but you browse them on the Repos page.
        return { name: e.name, path: p, dir: true, children: rel === "repos" ? [] : await tree(p) };
      }),
  );
  return nodes;
}

export async function read(rel: string): Promise<string | null> {
  try {
    return await fs.readFile(safePath(rel), "utf8");
  } catch (e) {
    if ((e as NodeJS.ErrnoException).code === "ENOENT") return null;
    throw e;
  }
}

export async function write(rel: string, data: string | Uint8Array) {
  const abs = safePath(rel);
  await fs.mkdir(path.dirname(abs), { recursive: true });
  await fs.writeFile(abs, data);
}

export async function remove(rel: string) {
  if (!rel) throw new Error("Refusing to delete content root");
  await fs.rm(safePath(rel), { recursive: true });
}

export async function rename(from: string, to: string) {
  const dest = safePath(to);
  await fs.mkdir(path.dirname(dest), { recursive: true });
  await fs.rename(safePath(from), dest);
}

export async function mkdir(rel: string) {
  await fs.mkdir(safePath(rel), { recursive: true });
}

export const parse = (md: string) => {
  const { data, content } = matter(md);
  return { data: data as Record<string, string>, body: content };
};

export type Problem = { path: string; slug: string; title: string; difficulty?: string; leetcode?: string; neetcode?: string; video?: string };

/** Lists problems (folders with question.md) under area/group, e.g. leetcode/"01 Arrays & Hashing". */
export async function problems(groupRel: string): Promise<Problem[]> {
  const dirs = (await fs.readdir(safePath(groupRel), { withFileTypes: true })).filter((d) => d.isDirectory());
  const out = await Promise.all(
    dirs.map(async (d): Promise<Problem | null> => {
      const p = path.posix.join(groupRel, d.name);
      const md = await read(`${p}/question.md`);
      if (md === null) return null;
      const { data, body } = parse(md);
      const title = data.problem ?? body.match(/^# (.+)$/m)?.[1] ?? d.name;
      return { path: p, slug: d.name, title, difficulty: data.difficulty, leetcode: data.leetcode, neetcode: data.neetcode, video: data.video };
    }),
  );
  const rank: Record<string, number> = { Easy: 0, Medium: 1, Hard: 2 };
  return out.filter((x): x is Problem => !!x).sort((a, b) => (rank[a.difficulty ?? ""] ?? 3) - (rank[b.difficulty ?? ""] ?? 3) || a.title.localeCompare(b.title));
}

/** Top-level groups (topic/category folders) of an area. */
export async function groups(area: string) {
  const dirs = (await fs.readdir(safePath(area), { withFileTypes: true })).filter((d) => d.isDirectory());
  return dirs.map((d) => d.name).sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
}

export type Review = { step: number; due: string }; // due = local YYYY-MM-DD
export type Progress = Record<string, { status: "solved" | "attempted"; at: string; review?: Review }>;

export async function progress(): Promise<Progress> {
  return JSON.parse((await read("progress.json")) ?? "{}");
}

export async function setProgress(problemPath: string, status: "solved" | "attempted" | null) {
  const p = await progress();
  const prev = p[problemPath];
  if (status === "attempted" && prev?.status === "solved") return; // a failed re-run keeps the solve
  if (status) p[problemPath] = { ...prev, status, at: new Date().toISOString() };
  else delete p[problemPath];
  await write("progress.json", JSON.stringify(p, null, 2));
}

/** Days until the next review for each step of the spaced-repetition ladder. */
export const INTERVALS = [1, 3, 7, 14, 30, 60, 120];
export type ReviewAction = "enable" | "disable" | "again" | "hard" | "good" | "easy" | "set";
export const localDate = (d: Date) => d.toLocaleDateString("en-CA"); // YYYY-MM-DD in local time

/** `due` (YYYY-MM-DD) is only used by "set", which picks the next review date by hand and keeps the step. */
export async function review(problemPath: string, action: ReviewAction, now = new Date(), due?: string) {
  const p = await progress();
  const entry = p[problemPath];
  if (!entry) throw new Error("Solve the problem before adding it to reviews");
  if (action === "disable") delete entry.review;
  else if (action === "set") {
    if (!due || !/^\d{4}-\d{2}-\d{2}$/.test(due) || isNaN(Date.parse(due))) throw new Error(`Invalid review date ${due}`);
    entry.review = { step: entry.review?.step ?? 0, due };
  } else {
    const cur = entry.review?.step ?? 0;
    const step = action === "enable" || action === "again" ? 0 : action === "hard" ? cur : Math.min(cur + (action === "easy" ? 2 : 1), INTERVALS.length - 1);
    const due = new Date(now);
    due.setDate(due.getDate() + INTERVALS[step]);
    entry.review = { step, due: localDate(due) };
  }
  await write("progress.json", JSON.stringify(p, null, 2));
  return p;
}

/** Reference time/space complexity from a solution.md Complexity section. */
export function complexity(solution: string) {
  return {
    time: solution.match(/\*\*Time:\*\*\s*`([^`]+)`/)?.[1],
    space: solution.match(/\*\*Space:\*\*\s*`([^`]+)`/)?.[1],
  };
}

export type GroupStats = { group: string; name: string; total: number; solved: number; problems: Problem[] };

/** Every group of an area with its problems and solved counts. */
export async function areaStats(area: string): Promise<GroupStats[]> {
  const prog = await progress();
  return Promise.all(
    (await groups(area)).map(async (group) => {
      const ps = await problems(`${area}/${group}`);
      return { group, name: group.replace(/^\d+\s*/, ""), total: ps.length, solved: ps.filter((p) => prog[p.path]?.status === "solved").length, problems: ps };
    }),
  );
}

/** Counts one activity (a run, a solve, an interview turn, a ticked plan task) for today; feeds the streak calendar. */
export async function logActivity() {
  let a: Record<string, number> = {};
  try { a = JSON.parse((await read("activity.json")) ?? "{}"); } catch {}
  const d = localDate(new Date());
  a[d] = (a[d] ?? 0) + 1;
  await write("activity.json", JSON.stringify(a, null, 1));
}

/** Activity per local day: logged activity plus older history (solves in progress.json, saved interviews). */
export async function activityDays(): Promise<Record<string, number>> {
  let a: Record<string, number> = {};
  try { a = JSON.parse((await read("activity.json")) ?? "{}"); } catch {}
  const days = { ...a };
  for (const v of Object.values(await progress())) {
    const d = localDate(new Date(v.at));
    if (!a[d]) days[d] = (days[d] ?? 0) + 1;
  }
  const interviews = await fs.readdir(safePath("interviews")).catch(() => [] as string[]);
  for (const f of interviews) {
    const d = f.match(/^(\d{4}-\d{2}-\d{2})/)?.[1];
    if (d && !a[d]) days[d] = (days[d] ?? 0) + 1;
  }
  return days;
}

/** Current streak (counting from today, or from yesterday if today has nothing yet) and longest streak, in days. */
export function streaks(days: Record<string, number>, today: string) {
  const active = (d: string) => (days[d] ?? 0) > 0;
  const shift = (d: string, n: number) => { const x = new Date(d + "T12:00"); x.setDate(x.getDate() + n); return localDate(x); };
  let cur = 0;
  let d = active(today) ? today : shift(today, -1);
  while (active(d)) { cur++; d = shift(d, -1); }
  let longest = 0, run = 0, prev = "";
  for (const day of Object.keys(days).filter(active).sort()) {
    run = prev && shift(prev, 1) === day ? run + 1 : 1;
    longest = Math.max(longest, run);
    prev = day;
  }
  return { current: cur, longest };
}

/**
 * Moves a problem to another topic folder (e.g. leetcode/<new topic>/<slug>) and updates everything that points at it:
 * progress/reviews, study plan tasks and the topic shown in its question and solution. Returns the new path.
 */
export async function moveProblem(problemPath: string, group: string): Promise<string> {
  const [area, , slug] = problemPath.split("/");
  if (!slug || problemPath.split("/").length !== 3) throw new Error("Not a problem path");
  if (!group.trim() || group.includes("/") || group.startsWith(".")) throw new Error("Pick a topic");
  const to = `${area}/${group}/${slug}`;
  if (to === problemPath) return to;
  if (await fs.stat(safePath(to)).catch(() => null)) throw new Error(`${to} already exists`);
  await rename(problemPath, to);

  const topic = group.replace(/^\d+\s*/, "");
  for (const f of ["question.md", "solution.md"]) {
    const md = await read(`${to}/${f}`);
    if (md !== null) await write(`${to}/${f}`, md.replace(/^topic: .*$/m, `topic: "${topic}"`).replace(/(\*\*Topic:\*\* )[^·\n]+/, `$1${topic} `));
  }
  const prog = await progress();
  if (prog[problemPath]) {
    prog[to] = prog[problemPath];
    delete prog[problemPath];
    await write("progress.json", JSON.stringify(prog, null, 2));
  }
  const plan = await read("plan.json");
  if (plan?.includes(JSON.stringify(problemPath))) await write("plan.json", plan.split(JSON.stringify(problemPath)).join(JSON.stringify(to)));
  return to;
}
