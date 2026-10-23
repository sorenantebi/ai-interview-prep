import { areaStats, localDate, progress, read, write } from "./content.ts";
import { claude, prompt } from "./claude.ts";

// "review": redo a problem you already solved (done only when ticked); "leetcode"/"system-design": new problems (done when solved).
export type Task = { type: "leetcode" | "system-design" | "review"; path: string; title: string; done?: boolean } | { type: "note"; text: string; done?: boolean };
export type Day = { date: string; focus?: string; tasks: Task[] };
export type Plan = { title: string; created: string; days: Day[] };
export type PlanSettings = { start: string; weeks: number; hours: number; focus: string[]; notes: string };

export async function readPlan(): Promise<Plan | null> {
  try { return JSON.parse((await read("plan.json")) ?? "null"); } catch { return null; }
}
export const savePlan = (p: Plan) => write("plan.json", JSON.stringify(p, null, 1));

const addDays = (d: string, n: number) => { const x = new Date(d + "T12:00"); x.setDate(x.getDate() + n); return localDate(x); };

/** Keeps only well-formed days in range and tasks that point at problems that exist (titles come from our data). */
export function validatePlan(raw: unknown, titles: Map<string, string>, start: string, end: string): Plan {
  const r = raw as { title?: unknown; days?: unknown };
  if (!r || !Array.isArray(r.days)) throw new Error("Claude's plan had no days");
  const days: Day[] = [];
  for (const d of r.days as { date?: unknown; focus?: unknown; tasks?: unknown }[]) {
    const date = typeof d?.date === "string" && /^\d{4}-\d{2}-\d{2}$/.test(d.date) ? d.date : null;
    if (!date || date < start || date > end || !Array.isArray(d.tasks)) continue;
    const tasks: Task[] = [];
    for (const t of d.tasks as { type?: unknown; path?: unknown; text?: unknown }[]) {
      if ((t?.type === "leetcode" || t?.type === "system-design" || t?.type === "review") && typeof t.path === "string" && titles.has(t.path)) tasks.push({ type: t.type, path: t.path, title: titles.get(t.path)! });
      else if (t?.type === "note" && typeof t.text === "string" && t.text.trim()) tasks.push({ type: "note", text: t.text.trim().slice(0, 300) });
    }
    if (tasks.length) days.push({ date, focus: typeof d.focus === "string" ? d.focus.slice(0, 80) : undefined, tasks });
  }
  if (!days.length) throw new Error("Claude's plan had no usable days");
  days.sort((a, b) => a.date.localeCompare(b.date));
  return { title: typeof r.title === "string" ? r.title.slice(0, 120) : "Study plan", created: new Date().toISOString(), days };
}

export async function generatePlan(s: PlanSettings): Promise<Plan> {
  const weeks = Math.min(26, Math.max(1, Math.round(s.weeks)));
  const end = addDays(s.start, weeks * 7 - 1);
  const prog = await progress();
  const titles = new Map<string, string>();
  const lines: string[] = [];
  for (const area of ["leetcode", "system-design"]) {
    for (const g of await areaStats(area)) {
      for (const p of g.problems) {
        titles.set(p.path, p.title);
        const e = prog[p.path];
        const status = e?.status !== "solved" ? "not solved" : e.review ? `solved, review due ${e.review.due}` : `solved ${e.at.slice(0, 10)}`;
        lines.push(`${p.path} | ${p.title} | ${p.difficulty ?? "?"} | ${status}`);
      }
    }
  }
  const input = await prompt("study-plan", {
    start: s.start, end, weeks: String(weeks), days: String(weeks * 7), hours: String(s.hours),
    focus: s.focus.join(", ") || "LeetCode and system design", notes: s.notes || "none", problems: lines.join("\n"),
  });
  const { text } = await claude(input);
  const json = text.match(/```json\s*([\s\S]*?)```/)?.[1] ?? text.slice(text.indexOf("{"), text.lastIndexOf("}") + 1);
  let raw: unknown;
  try { raw = JSON.parse(json); } catch { throw new Error("Claude's answer was not valid JSON:\n\n" + text.slice(0, 800)); }
  return validatePlan(raw, titles, s.start, end);
}

/** Your tick or untick (`done`) wins; untouched new-problem tasks count as done once the problem is solved. */
export const taskDone = (t: Task, solved: Set<string>) => t.done ?? ((t.type === "leetcode" || t.type === "system-design") && solved.has(t.path));

/**
 * Solving a problem completes its plan tasks: new-problem tasks on any day, and reviews due today or earlier
 * (a review planned for later isn't done by solving it now). Overrides an earlier untick.
 */
export async function completeTasks(problemPath: string) {
  const plan = await readPlan();
  if (!plan) return;
  const today = localDate(new Date());
  let changed = false;
  for (const d of plan.days)
    for (const t of d.tasks)
      if (t.type !== "note" && t.path === problemPath && !t.done && (t.type !== "review" || d.date <= today)) {
        t.done = true;
        changed = true;
      }
  if (changed) await savePlan(plan);
}
