import { localDate } from "@/lib/content";

const WEEKS = 26;
// One hue, light -> dark (sequential): activity count buckets.
const LEVELS = [
  { min: 0, cls: "bg-fg/10", label: "none" },
  { min: 1, cls: "bg-accent/30", label: "1–2" },
  { min: 3, cls: "bg-accent/55", label: "3–5" },
  { min: 6, cls: "bg-accent/80", label: "6–9" },
  { min: 10, cls: "bg-accent", label: "10+" },
];
const level = (n: number) => [...LEVELS].reverse().find((l) => n >= l.min)!;

export default function StreakCalendar({ days, current, longest, today }: { days: Record<string, number>; current: number; longest: number; today: string }) {
  // Columns are weeks (Mon..Sun), ending with the week that contains today.
  const end = new Date(today + "T12:00");
  const start = new Date(end);
  start.setDate(end.getDate() - ((end.getDay() + 6) % 7) - (WEEKS - 1) * 7);
  const cols: { date: string; n: number; future: boolean }[][] = [];
  for (let w = 0; w < WEEKS; w++) {
    cols.push(Array.from({ length: 7 }, (_, i) => {
      const d = new Date(start);
      d.setDate(start.getDate() + w * 7 + i);
      const date = localDate(d);
      return { date, n: days[date] ?? 0, future: date > today };
    }));
  }
  const active = Object.values(days).filter((n) => n > 0).length;
  const month = (c: { date: string }[], i: number) => {
    const m = new Date(c[0].date + "T12:00").toLocaleDateString(undefined, { month: "short" });
    // Label a column only where a new month starts (not the first column, whose label would collide with the next).
    return i > 0 && new Date(cols[i - 1][0].date + "T12:00").getMonth() !== new Date(c[0].date + "T12:00").getMonth() ? m : "";
  };

  return (
    <section className="card p-4">
      <div className="mb-3 flex flex-wrap items-baseline gap-x-6 gap-y-1">
        <h2 className="font-medium">Streak</h2>
        <span className="font-display text-3xl font-medium tabular-nums">{current} <span className="text-base text-muted">day{current === 1 ? "" : "s"}</span></span>
        <span className="font-mono text-xs text-muted">longest {longest} · {active} active days</span>
      </div>
      <div className="overflow-x-auto">
        <div className="inline-grid gap-[3px]" style={{ gridTemplateColumns: `repeat(${WEEKS}, 12px)` }} role="img" aria-label={`Activity calendar for the last ${WEEKS} weeks: current streak ${current} days, longest ${longest}`}>
          {cols.map((c, i) => <div key={`m${i}`} className="h-4 overflow-visible whitespace-nowrap font-mono text-[10px] text-muted">{month(c, i)}</div>)}
          {Array.from({ length: 7 }, (_, row) =>
            cols.map((c) => {
              const cell = c[row];
              return (
                <div
                  key={cell.date}
                  className={`h-3 w-3 ${cell.future ? "bg-transparent" : level(cell.n).cls} ${cell.date === today ? "outline outline-1 outline-fg" : ""}`}
                  title={cell.future ? "" : `${cell.date}: ${cell.n} activit${cell.n === 1 ? "y" : "ies"}`}
                />
              );
            }),
          )}
        </div>
      </div>
      <div className="mt-2 flex items-center gap-1 font-mono text-[10px] text-muted">
        less {LEVELS.map((l) => <span key={l.label} className={`h-3 w-3 ${l.cls}`} title={l.label} />)} more
      </div>
    </section>
  );
}
