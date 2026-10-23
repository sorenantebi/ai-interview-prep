import Link from "next/link";
import Roadmap from "@/components/Roadmap";
import ProblemList, { problemHref } from "@/components/ProblemList";
import { orderQuery, sequence } from "@/lib/order";
import { areaStats, progress } from "@/lib/content";
import { LAYOUT } from "@/lib/roadmap";

export const dynamic = "force-dynamic";

export default async function LeetcodePage({ searchParams }: { searchParams: Promise<{ topic?: string; view?: string }> }) {
  const [stats, prog, { topic, view }] = await Promise.all([areaStats("leetcode"), progress(), searchParams]);
  const selected = stats.find((s) => s.group === topic) ?? stats[0];
  const extra = stats.filter((s) => !LAYOUT[s.name]);
  const solved = stats.reduce((a, s) => a + s.solved, 0);
  const total = stats.reduce((a, s) => a + s.total, 0);
  // A fresh random order per visit; the seed travels in the URL so prev / next keep following it.
  const seed = Math.floor(Math.random() * 1e9);
  const all = stats.flatMap((g) => g.problems.map((p) => p.path));
  const solvedSet = new Set(Object.keys(prog).filter((k) => prog[k].status === "solved"));
  const firstOf = (unsolved: boolean) => {
    const o = { random: true, seed, unsolved };
    const p = sequence(all, o, solvedSet)[0];
    return p ? problemHref(p) + orderQuery(o) : null;
  };

  return (
    <div className="mx-auto max-w-6xl space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <h1 className="page-title">LeetCode</h1>
        <div className="flex flex-wrap items-center gap-2">
          <span className="mr-2 text-sm tabular-nums text-muted">{solved} / {total} solved</span>
          {firstOf(false) && <Link href={firstOf(false)!} className="btn-primary">⤮ Shuffle all</Link>}
          {firstOf(true) && <Link href={firstOf(true)!} className="btn">⤮ Shuffle unsolved</Link>}
        </div>
      </div>
      <div className="flex gap-1" role="tablist" aria-label="LeetCode view">
        {([["roadmap", "Roadmap"], ["all", "All questions"]] as const).map(([v, label]) => (
          <Link key={v} href={v === "all" ? "/leetcode?view=all" : "/leetcode"} role="tab" aria-selected={(view === "all") === (v === "all")} className={`px-2.5 py-1 font-mono text-xs ${(view === "all") === (v === "all") ? "bg-fg text-panel" : "bg-panel text-muted hover:text-fg"}`}>
            {label}
          </Link>
        ))}
      </div>
      {view === "all" ? (
        <div className="card max-h-[78vh] overflow-y-auto">
          <nav className="flex flex-wrap gap-1 border-b border-border p-2" aria-label="Jump to topic">
            {stats.map((g, i) => (
              <a key={g.group} href={`#topic-${i}`} className="border border-border px-2 py-0.5 font-mono text-xs hover:bg-fg hover:text-panel">
                {g.name} <span className="opacity-60">{g.solved}/{g.total}</span>
              </a>
            ))}
          </nav>
          {stats.map((g, i) => (
            <section key={g.group} id={`topic-${i}`} className="scroll-mt-0">
              <h2 className="sticky top-0 z-10 flex justify-between border-b border-border bg-panel px-4 py-2 text-sm font-semibold">
                {g.name} <span className="font-normal tabular-nums text-muted">{g.solved} / {g.total}</span>
              </h2>
              <ProblemList problems={g.problems} progress={prog} />
            </section>
          ))}
        </div>
      ) : (
      <>
      <Roadmap stats={stats.map(({ group, name, total, solved }) => ({ group, name, total, solved }))} selected={selected?.group} />
      {extra.length > 0 && (
        <div className="flex flex-wrap gap-2 text-sm">
          <span className="text-muted">Other topics:</span>
          {extra.map((s) => (
            <Link key={s.group} href={`/leetcode?topic=${encodeURIComponent(s.group)}`} scroll={false} className={`btn ${s.group === selected?.group ? "border-accent" : ""}`}>
              {s.name} <span className="text-muted">{s.solved}/{s.total}</span>
            </Link>
          ))}
        </div>
      )}
      {selected && (
        <section className="card">
          <div className="flex items-center justify-between border-b border-border px-4 py-3">
            <h2 className="font-medium">{selected.name}</h2>
            <span className="text-sm tabular-nums text-muted">{selected.solved} / {selected.total}</span>
          </div>
          <ProblemList problems={selected.problems} progress={prog} />
        </section>
      )}
      </>
      )}
    </div>
  );
}
