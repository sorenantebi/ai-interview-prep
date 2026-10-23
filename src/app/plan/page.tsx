import RefreshOnShow from "@/components/RefreshOnShow";
import PlanForm from "@/components/PlanForm";
import PlanTasks from "@/components/PlanTasks";
import DeletePlan from "@/components/DeletePlan";
import { localDate, progress } from "@/lib/content";
import { readPlan, taskDone } from "@/lib/plan";
import { fmtDate } from "@/lib/format";

export const dynamic = "force-dynamic";

export default async function PlanPage() {
  const [plan, prog] = await Promise.all([readPlan(), progress()]);
  const today = localDate(new Date());
  const solved = Object.keys(prog).filter((k) => prog[k].status === "solved");
  const solvedSet = new Set(solved);
  const all = plan?.days.flatMap((d) => d.tasks) ?? [];
  const done = all.filter((t) => taskDone(t, solvedSet)).length;
  // Group days into weeks counted from the first day.
  const weeks: { n: number; days: NonNullable<typeof plan>["days"] }[] = [];
  if (plan) {
    const first = new Date(plan.days[0].date + "T12:00").getTime();
    for (const d of plan.days) {
      const n = Math.floor((new Date(d.date + "T12:00").getTime() - first) / (7 * 86_400_000));
      (weeks[n] ??= { n, days: [] }).days.push(d);
    }
  }
  return (
    <div className="space-y-6">
      <RefreshOnShow />
      <h1 className="page-title">Study plan</h1>
      {plan && (
        <section className="space-y-4">
          <div className="flex flex-wrap items-end gap-3">
            <h2 className="font-display text-2xl font-medium">{plan.title}</h2>
            <span className="font-mono text-xs text-muted">{fmtDate(plan.days[0].date)} – {fmtDate(plan.days.at(-1)!.date)} · {done}/{all.length} tasks done</span>
            <span className="flex-1" />
            <DeletePlan />
          </div>
          <div className="h-2 bg-fg/10" role="meter" aria-valuemin={0} aria-valuemax={all.length} aria-valuenow={done} aria-label="Plan progress">
            <div className="h-full bg-accent" style={{ width: `${all.length ? (done / all.length) * 100 : 0}%` }} />
          </div>
          {weeks.filter(Boolean).map((w) => (
            <div key={w.n} className="space-y-2">
              <h3 className="tag">Week {w.n + 1}</h3>
              <div className="grid gap-2 md:grid-cols-2 xl:grid-cols-4">
                {w.days.map((d) => (
                  <div key={d.date} className={`card p-3 ${d.date === today ? "ring-2 ring-accent" : ""} ${d.date < today && d.tasks.every((t) => taskDone(t, solvedSet)) ? "opacity-60" : ""}`}>
                    <div className="mb-2 flex items-baseline justify-between gap-2">
                      <span className="font-mono text-xs font-medium">{d.date === today ? "Today" : fmtDate(d.date)}</span>
                      {d.focus && <span className="truncate font-mono text-[11px] text-muted">{d.focus}</span>}
                    </div>
                    <PlanTasks day={d} solved={solved} />
                  </div>
                ))}
              </div>
            </div>
          ))}
        </section>
      )}
      <PlanForm today={today} hasPlan={!!plan} />
    </div>
  );
}
