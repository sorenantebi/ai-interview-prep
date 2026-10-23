import Link from "next/link";
import CheatSheet, { type CheatEntry } from "@/components/CheatSheet";
import DashboardTabs from "@/components/DashboardTabs";
import Mantra from "@/components/Mantra";
import StreakCalendar from "@/components/StreakCalendar";
import TodayPlan from "@/components/TodayPlan";
import { readPlan } from "@/lib/plan";
import Patterns from "@/components/Patterns";
import SystemDesignSheet, { type SDEntry } from "@/components/SystemDesignSheet";
import { parseScene } from "@/components/ExcalidrawView";
import ReviewControls from "@/components/ReviewControls";
import { problemHref } from "@/components/ProblemList";
import { activityDays, areaStats, complexity, localDate, progress, read, safePath, streaks } from "@/lib/content";
import { strokesOf } from "@/lib/starter";
import fs from "node:fs/promises";

export const dynamic = "force-dynamic";

/** Your passing snapshot (solved.py), else your latest attempt (never the reference code), plus your notes. */
async function yourCode(path: string) {
  const [solved, attempt, solution, notes, drawing] = await Promise.all(["solved.py", "attempt.py", "solution.md", "notes.md", "drawing.json"].map((f) => read(`${path}/${f}`)));
  const code = solved ?? attempt;
  return {
    ...complexity(solution ?? ""),
    notes: notes ?? "",
    drawing: strokesOf(drawing),
    hasAttempt: attempt !== null,
    code: code?.trim() ?? "",
    codeSource: solved !== null ? "passed" : attempt !== null ? "latest" : null,
  } as const;
}

export default async function Dashboard({ searchParams }: { searchParams: Promise<{ view?: string }> }) {
  const [lc, sd, prog, interviews] = await Promise.all([
    areaStats("leetcode"),
    areaStats("system-design"),
    progress(),
    fs.readdir(safePath("interviews")).then((f) => f.filter((n) => n.endsWith(".md")), () => []),
  ]);
  const sum = (g: typeof lc, k: "total" | "solved") => g.reduce((a, x) => a + x[k], 0);
  const today = localDate(new Date());
  const patterns = await read("patterns.md");
  const [plan, activity] = await Promise.all([readPlan(), activityDays()]);
  const streak = streaks(activity, today);
  const solvedPaths = Object.keys(prog).filter((k) => prog[k].status === "solved");
  const sdSheet = await Promise.all(
    sd.map(async (g) => ({
      name: g.name,
      entries: await Promise.all(
        g.problems.map(async (p): Promise<SDEntry> => {
          const [diagram, notes] = await Promise.all([read(`${p.path}/diagram.excalidraw`), read(`${p.path}/notes.md`)]);
          return { path: p.path, title: p.title, difficulty: p.difficulty, done: prog[p.path]?.status === "solved" ? prog[p.path].at : undefined, diagram: parseScene(diagram), notes: notes ?? "" };
        }),
      ),
    })),
  );

  // Cheat sheet: solved LeetCode problems per topic, summarised from their solution.md.
  const cheat = (
    await Promise.all(
      lc.map(async (g) => ({
        name: g.name,
        entries: await Promise.all(
          g.problems
            .filter((p) => prog[p.path]?.status === "solved")
            .map(async (p): Promise<CheatEntry> => ({
              path: p.path, title: p.title, difficulty: p.difficulty, at: prog[p.path].at, review: prog[p.path].review,
              ...(await yourCode(p.path)),
            })),
        ),
      })),
    )
  ).filter((g) => g.entries.length);
  const due = Object.entries(prog)
    .filter(([, v]) => v.review && v.review.due <= today)
    .sort((a, b) => a[1].review!.due.localeCompare(b[1].review!.due));
  const recent = Object.entries(prog).sort((a, b) => b[1].at.localeCompare(a[1].at)).slice(0, 8);

  const tiles = [
    { label: "LeetCode solved", value: `${sum(lc, "solved")} / ${sum(lc, "total")}`, href: "/leetcode" },
    { label: "System design done", value: `${sum(sd, "solved")} / ${sum(sd, "total")}`, href: "/system-design" },
    { label: "Saved interviews", value: String(interviews.length), href: "/files?path=interviews" },
  ];

  return (
    <div className="space-y-8">
      <Mantra initial={((await read("mantra.txt")) ?? "lock the fuck in").trim()} />
      <h1 className="page-title">Dashboard</h1>
      <div className="grid gap-3 sm:grid-cols-3">
        {tiles.map((t) => (
          <Link key={t.label} href={t.href} className="card p-4 hover:border-fg">
            <div className="font-mono text-xs uppercase tracking-wide text-muted">{t.label}</div>
            <div className="mt-2 font-display text-4xl font-medium tracking-tight tabular-nums">{t.value}</div>
          </Link>
        ))}
      </div>
      <div className="grid gap-3 lg:grid-cols-2">
        <TodayPlan plan={plan} solved={solvedPaths} today={today} />
        <StreakCalendar days={activity} current={streak.current} longest={streak.longest} today={today} />
      </div>
      {due.length > 0 && (
        <section>
          <h2 className="tag mb-2">Due for review ({due.length})</h2>
          <ul className="card divide-y divide-border">
            {due.map(([p, v]) => (
              <li key={p} className="flex flex-wrap items-center gap-x-3 gap-y-2 px-4 py-2 text-sm">
                <Link href={problemHref(p)} className="flex-1 truncate hover:underline decoration-accent decoration-2 underline-offset-2">{p.split("/").slice(1).join(" › ")}</Link>
                <ReviewControls path={p} review={v.review} today={today} />
              </li>
            ))}
          </ul>
        </section>
      )}
      <DashboardTabs
        initial={{ "system-design": 1, patterns: 2 }[(await searchParams).view ?? ""] ?? 0}
        tabs={[
          { label: "LeetCode", content: <CheatSheet groups={cheat} today={today} /> },
          { label: "System design", content: <SystemDesignSheet groups={sdSheet} /> },
          { label: "Patterns", content: <Patterns markdown={patterns ?? ""} /> },
        ]}
      />
      <section>
        <h2 className="tag mb-2">Recent activity</h2>
        {recent.length === 0 ? (
          <p className="text-sm text-muted">Nothing yet. Open a problem on the LeetCode page to get started.</p>
        ) : (
          <ul className="card divide-y divide-border">
            {recent.map(([p, v]) => (
              <li key={p}>
                <Link href={problemHref(p)} className="flex justify-between gap-4 px-4 py-2 text-sm hover:bg-fg/5">
                  <span className="truncate">{p.split("/").slice(1).join(" › ")}</span>
                  <span className={v.status === "solved" ? "text-easy" : "text-medium"}>{v.status}</span>
                </Link>
              </li>
            ))}
          </ul>
        )}
      </section>
      <section className="flex flex-wrap gap-2">
        <Link href="/ai?tab=interview" className="btn-primary">Start a mock interview</Link>
        <Link href="/ai" className="btn">Add a problem with Claude</Link>
      </section>
    </div>
  );
}
