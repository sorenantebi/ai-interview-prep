import { areaStats, localDate, progress, read, write } from "./content.ts";
import { claudeStream, prompt } from "./claude.ts";

// "review": redo a problem you already solved (done only when ticked); "leetcode"/"ml-coding"/"system-design": new problems (done when solved).
export type Area = "leetcode" | "ml-coding" | "system-design";
export const AREAS: Area[] = ["leetcode", "ml-coding", "system-design"];
export type Task =
  | { type: Area | "review"; path: string; title: string; done?: boolean }
  | { type: "note"; text: string; done?: boolean }
  | { type: "mock"; kind: "coding" | "system-design"; path?: string; title?: string; done?: boolean }; // a mock interview (optionally on one problem); done when ticked
export type Day = { date: string; focus?: string; tasks: Task[] };
export type Plan = { title: string; created: string; days: Day[] };
export type PlanSettings = { start: string; weeks: number; focus: string[]; notes: string; previous?: boolean }; // previous: build on the current plan

export async function readPlan(): Promise<Plan | null> {
  try { return JSON.parse((await read("plan.json")) ?? "null"); } catch { return null; }
}
export const savePlan = (p: Plan) => write("plan.json", JSON.stringify(p, null, 1));

export type ProblemOption = { path: string; title: string; difficulty?: string; solved: boolean };
export type ProblemGroup = { area: Area; name: string; problems: ProblemOption[] };

/** Every LeetCode, ML Coding and system design problem, by topic, for the "add to day" dropdown. */
export async function problemOptions(): Promise<ProblemGroup[]> {
  const prog = await progress();
  const out: ProblemGroup[] = [];
  for (const area of AREAS)
    for (const g of await areaStats(area).catch(() => []))
      out.push({ area, name: g.name, problems: g.problems.map((p) => ({ path: p.path, title: p.title, difficulty: p.difficulty, solved: prog[p.path]?.status === "solved" })) });
  return out;
}

/**
 * Adds a problem to a plan day (a solved one as a review, otherwise as new work), or a mock interview ("mock:coding" /
 * "mock:system-design"), optionally on one problem of that kind.
 */
export async function addTask(date: string, path: string, mockProblem?: string, text?: string): Promise<Plan> {
  const plan = await readPlan();
  const day = plan?.days.find((d) => d.date === date);
  if (plan && day && path === "note") {
    if (!text?.trim()) throw new Error("Write the task first");
    day.tasks.push({ type: "note", text: text.trim().slice(0, 300) });
    await savePlan(plan);
    return plan;
  }
  if (plan && day && (path === "mock:coding" || path === "mock:system-design")) {
    const kind = path === "mock:coding" ? "coding" : "system-design";
    const area = kind === "coding" ? "leetcode" : "system-design";
    const p = mockProblem ? (await problemOptions()).filter((g) => g.area === area).flatMap((g) => g.problems).find((x) => x.path === mockProblem) : undefined;
    if (mockProblem && !p) throw new Error("No such problem for that interview");
    day.tasks.push({ type: "mock", kind, ...(p ? { path: p.path, title: p.title } : {}) });
    await savePlan(plan);
    return plan;
  }
  const group = (await problemOptions()).find((g) => g.problems.some((p) => p.path === path));
  const problem = group?.problems.find((p) => p.path === path);
  if (!plan || !day || !group || !problem) throw new Error("No such day or problem");
  day.tasks.push({ type: problem.solved ? "review" : group.area, path, title: problem.title });
  await savePlan(plan);
  return plan;
}

export async function removeTask(date: string, index: number): Promise<Plan> {
  const plan = await readPlan();
  const day = plan?.days.find((d) => d.date === date);
  if (!plan || !day?.tasks[index]) throw new Error("No such task");
  day.tasks.splice(index, 1);
  await savePlan(plan);
  return plan;
}

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
      if ((AREAS.includes(t?.type as Area) || t?.type === "review") && typeof t.path === "string" && titles.has(t.path)) tasks.push({ type: t.type as Area | "review", path: t.path, title: titles.get(t.path)! });
      else if (t?.type === "note" && typeof t.text === "string" && t.text.trim()) tasks.push({ type: "note", text: t.text.trim().slice(0, 300) });
      else if (t?.type === "mock") {
        const kind = (t as { kind?: unknown }).kind === "system-design" ? "system-design" : "coding";
        const ok = typeof t.path === "string" && titles.has(t.path) && t.path.startsWith(kind === "coding" ? "leetcode/" : "system-design/");
        tasks.push({ type: "mock", kind, ...(ok ? { path: t.path as string, title: titles.get(t.path as string)! } : {}) });
      }
    }
    if (tasks.length) days.push({ date, focus: typeof d.focus === "string" ? d.focus.slice(0, 80) : undefined, tasks });
  }
  if (!days.length) throw new Error("Claude's plan had no usable days");
  days.sort((a, b) => a.date.localeCompare(b.date));
  return { title: typeof r.title === "string" ? r.title.slice(0, 120) : "Study plan", created: new Date().toISOString(), days };
}

export type PlanProgress = { phase: "thinking" | "writing" | "checking"; days: number; total: number; date?: string; focus?: string; tokens?: { input: number; output: number } };

/** Watches the plan JSON as Claude writes it: how many days are done, and which one it's on. */
export function planProgress(partial: string, total: number): Omit<PlanProgress, "phase"> {
  const dates = [...partial.matchAll(/"date"\s*:\s*"(\d{4}-\d{2}-\d{2})"/g)].map((m) => m[1]);
  const focus = [...partial.matchAll(/"focus"\s*:\s*"([^"]*)"/g)].map((m) => m[1]).at(-1);
  return { days: dates.length, total, date: dates.at(-1), focus };
}

/**
 * Makes sure every required problem is in the plan: anything Claude left out is spread evenly over the plan's days,
 * keeping the given (roadmap) order. A problem counts as covered when it appears with the same task type.
 */
export function coverAll(plan: Plan, required: { type: Area | "review"; path: string; title: string }[]): Plan {
  const have = new Set(plan.days.flatMap((d) => d.tasks.map((t) => ("path" in t && t.type !== "mock" ? `${t.type}|${t.path}` : ""))));
  const missing = required.filter((r) => !have.has(`${r.type}|${r.path}`));
  missing.forEach((r, i) => plan.days[Math.floor((i * plan.days.length) / missing.length)].tasks.push({ ...r }));
  return plan;
}

/** The plan in a compact form for Claude: one line per day, ✓ for done tasks, exact problem paths. */
export function planSummary(plan: Plan, solved: Set<string>): string {
  const task = (t: Task) =>
    (taskDone(t, solved) ? "✓ " : "○ ") +
    (t.type === "note" ? `note: ${t.text}` : t.type === "mock" ? `mock ${t.kind}${t.path ? `: ${t.path}` : ""}` : `${t.type}: ${t.path}`);
  return [`"${plan.title}"`, ...plan.days.map((d) => `${d.date} | ${d.focus ?? ""} | ${d.tasks.map(task).join("; ")}`)].join("\n");
}

/** Keeps your ticks (and unticks) from the old plan on tasks that are still on the same day in the new one. */
export function carryTicks(plan: Plan, old: Plan): Plan {
  const key = (t: Task) => `${t.type}|${"path" in t ? t.path : ""}|${t.type === "note" ? t.text : t.type === "mock" ? t.kind : ""}`;
  const was = new Map(old.days.flatMap((d) => d.tasks.filter((t) => t.done !== undefined).map((t) => [`${d.date}|${key(t)}`, t.done] as const)));
  for (const d of plan.days) for (const t of d.tasks) { const done = was.get(`${d.date}|${key(t)}`); if (done !== undefined) t.done = done; }
  return plan;
}

export async function generatePlan(s: PlanSettings, onProgress: (p: PlanProgress) => void = () => {}): Promise<Plan> {
  const weeks = Math.min(26, Math.max(1, Math.round(s.weeks)));
  const end = addDays(s.start, weeks * 7 - 1);
  const prog = await progress();
  const titles = new Map<string, string>();
  const lines: string[] = [];
  const required: Parameters<typeof coverAll>[1] = []; // every problem: unsolved as new work, solved as a review
  // Focus labels from the form ("LeetCode (NeetCode roadmap)", "ML coding", "System design", …) name the areas covered.
  const covers = (label: string) => !s.focus.length || s.focus.some((f) => f.toLowerCase().startsWith(label));
  const LABEL: Record<Area, string> = { leetcode: "leetcode", "ml-coding": "ml coding", "system-design": "system design" };
  for (const area of AREAS) {
    if (area === "ml-coding" && !covers(LABEL[area])) continue; // only listed (and paid for in tokens) when picked
    for (const g of await areaStats(area).catch(() => [])) {
      for (const p of g.problems) {
        titles.set(p.path, p.title);
        const e = prog[p.path];
        const status = e?.status !== "solved" ? "not solved" : e.review ? `solved, review due ${e.review.due}` : `solved ${e.at.slice(0, 10)}`;
        lines.push(`${p.path} | ${p.title} | ${p.difficulty ?? "?"} | ${status}`);
        required.push({ type: e?.status === "solved" ? "review" : area, path: p.path, title: p.title });
      }
    }
  }
  const input = await prompt("study-plan", {
    start: s.start, end, weeks: String(weeks), days: String(weeks * 7),
    focus: s.focus.join(", ") || "LeetCode and system design", notes: s.notes || "none", problems: lines.join("\n"),
    // Only when you ask to build on it (the checkbox); otherwise Claude plans from scratch.
    previous: s.previous ? await readPlan().then((p) => (p ? planSummary(p, new Set(Object.keys(prog).filter((k) => prog[k].status === "solved"))) : "none")) : "none",
  });
  const total = weeks * 7;
  onProgress({ phase: "thinking", days: 0, total });
  let written = "", tokens: PlanProgress["tokens"];
  const { text } = await claudeStream(input, (e) => {
    if (e.kind === "tokens") tokens = { input: e.input, output: e.output };
    else if (e.kind === "text") written += e.text;
    onProgress({ phase: written ? "writing" : "thinking", ...planProgress(written, total), tokens });
  });
  onProgress({ phase: "checking", ...planProgress(text, total), tokens });
  const json = text.match(/```json\s*([\s\S]*?)```/)?.[1] ?? text.slice(text.indexOf("{"), text.lastIndexOf("}") + 1);
  let raw: unknown;
  try { raw = JSON.parse(json); } catch { throw new Error("Claude's answer was not valid JSON:\n\n" + text.slice(0, 800)); }
  const plan = validatePlan(raw, titles, s.start, end);
  const old = s.previous ? await readPlan() : null;
  if (old) carryTicks(plan, old);
  // Every problem of each covered area ends up in the plan. Each area's gaps are spread over the whole plan on their
  // own, so leftovers don't pile up as all-coding first and all-system-design last.
  for (const area of AREAS)
    if (covers(LABEL[area])) coverAll(plan, required.filter((r) => r.path.startsWith(area + "/") && (r.type !== "review" || covers("spaced"))));
  return plan;
}

/** Your tick or untick (`done`) wins; untouched new-problem tasks count as done once the problem is solved. */
export const taskDone = (t: Task, solved: Set<string>) => t.done ?? (AREAS.includes(t.type as Area) && "path" in t && solved.has(t.path!));

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
      if (t.type !== "mock" && "path" in t && t.path === problemPath && !t.done && (t.type !== "review" || d.date <= today)) {
        t.done = true;
        changed = true;
      }
  if (changed) await savePlan(plan);
}
