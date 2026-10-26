import Link from "next/link";
import ProblemList, { problemHref } from "@/components/ProblemList";
import { orderQuery, sequence } from "@/lib/order";
import { areaStats, progress } from "@/lib/content";

export const dynamic = "force-dynamic";

export default async function MlCodingPage({ searchParams }: { searchParams: Promise<{ topic?: string }> }) {
  const [stats, prog, { topic }] = await Promise.all([areaStats("ml-coding"), progress(), searchParams]);
  const selected = stats.find((s) => s.group === topic) ?? stats[0];
  const solved = stats.reduce((a, s) => a + s.solved, 0);
  const total = stats.reduce((a, s) => a + s.total, 0);
  // Same shuffle as LeetCode: the seed travels in the URL so prev / next keep following it.
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
        <div>
          <h1 className="page-title">ML Coding</h1>
          <p className="mt-1 text-sm text-muted">NumPy, pandas and PyTorch exercises for ML interviews. Write the function, Run your own inputs, Submit to the hidden tests.</p>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <span className="mr-2 text-sm tabular-nums text-muted">{solved} / {total} solved</span>
          {firstOf(false) && <Link href={firstOf(false)!} className="btn-primary">⤮ Shuffle all</Link>}
          {firstOf(true) && <Link href={firstOf(true)!} className="btn">⤮ Shuffle unsolved</Link>}
          <Link href="/ml-coding/new" className="btn">+ Add your own</Link>
        </div>
      </div>
      <div className="flex flex-wrap gap-2 text-sm">
        {stats.map((s) => (
          <Link key={s.group} href={`/ml-coding?topic=${encodeURIComponent(s.group)}`} scroll={false} className={`btn ${s.group === selected?.group ? "border-accent" : ""}`}>
            {s.name} <span className="text-muted">{s.solved}/{s.total}</span>
          </Link>
        ))}
      </div>
      {selected && (
        <section className="card">
          <div className="flex items-center justify-between border-b border-border px-4 py-3">
            <h2 className="font-medium">{selected.name}</h2>
            <span className="text-sm tabular-nums text-muted">{selected.solved} / {selected.total}</span>
          </div>
          <ProblemList problems={selected.problems} progress={prog} />
        </section>
      )}
    </div>
  );
}
