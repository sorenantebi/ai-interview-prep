import RefreshOnShow from "./RefreshOnShow";
import Link from "next/link";
import PlanTasks from "./PlanTasks";
import { taskDone, type Plan } from "@/lib/plan";
import { fmtDate } from "@/lib/format";

export default function TodayPlan({ plan, solved, today }: { plan: Plan | null; solved: string[]; today: string }) {
  if (!plan)
    return (
      <section className="card flex flex-col items-start justify-center gap-3 p-4">
        <h2 className="font-medium">Study plan</h2>
        <p className="text-sm text-muted">Let Claude plan your weeks from the problems in this app, then tick them off here.</p>
        <Link href="/plan" className="btn-primary">Make a study plan</Link>
      </section>
    );
  const solvedSet = new Set(solved);
  const all = plan.days.flatMap((d) => d.tasks);
  const done = all.filter((t) => taskDone(t, solvedSet)).length;
  const todayDay = plan.days.find((d) => d.date === today);
  const behind = plan.days.filter((d) => d.date < today && d.tasks.some((t) => !taskDone(t, solvedSet)));
  const next = !todayDay ? plan.days.find((d) => d.date > today) : undefined;
  return (
    <section className="card space-y-3 p-4">
      <RefreshOnShow />
      <div className="flex flex-wrap items-baseline gap-x-3">
        <h2 className="font-medium">Today&apos;s plan</h2>
        <span className="font-mono text-xs text-muted">{plan.title} · {done}/{all.length} done</span>
        <Link href="/plan" className="ml-auto font-mono text-xs text-muted hover:text-fg">full plan →</Link>
      </div>
      <div className="h-1.5 bg-fg/10"><div className="h-full bg-accent" style={{ width: `${all.length ? (done / all.length) * 100 : 0}%` }} /></div>
      {todayDay ? (
        <div className="space-y-1">
          {todayDay.focus && <div className="font-mono text-xs text-muted">{todayDay.focus}</div>}
          <PlanTasks day={todayDay} solved={solved} />
        </div>
      ) : next ? (
        <p className="text-sm text-muted">Nothing planned today. Next up {fmtDate(next.date)}{next.focus ? `: ${next.focus}` : ""}.</p>
      ) : (
        <p className="text-sm text-muted">This plan has finished. <Link href="/plan" className="underline">Make a new one</Link>.</p>
      )}
      {behind.length > 0 && (
        <details className="border-t border-border pt-2">
          <summary className="cursor-pointer font-mono text-xs text-medium">{behind.length} earlier day{behind.length === 1 ? "" : "s"} with unfinished tasks</summary>
          <div className="mt-2 space-y-2">
            {behind.slice(-5).map((d) => (
              <div key={d.date}>
                <div className="font-mono text-[11px] text-muted">{fmtDate(d.date)}{d.focus ? ` · ${d.focus}` : ""}</div>
                <PlanTasks day={d} solved={solved} />
              </div>
            ))}
          </div>
        </details>
      )}
    </section>
  );
}
