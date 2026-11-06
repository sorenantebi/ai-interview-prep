import Link from "next/link";
import ProblemList from "@/components/ProblemList";
import { areaStats, progress } from "@/lib/content";
import { AREA } from "@/lib/repo";

export const dynamic = "force-dynamic";

export default async function RepoDebuggingPage({ searchParams }: { searchParams: Promise<{ topic?: string }> }) {
  const [stats, prog, { topic }] = await Promise.all([areaStats(AREA), progress(), searchParams]);
  const selected = stats.find((s) => s.group === topic) ?? stats[0];
  const solved = stats.reduce((a, s) => a + s.solved, 0);
  const total = stats.reduce((a, s) => a + s.total, 0);
  return (
    <div className="mx-auto max-w-6xl space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="page-title">AI Assisted</h1>
          <p className="mt-1 max-w-3xl text-sm text-muted">
            The newer interview formats: a small, unfamiliar codebase instead of a blank function. Fix bugs behind failing tests
            (Stripe-style bug squash), extend a codebase with a feature, or do Meta&apos;s AI-enabled round (fix a bug → build the
            feature → make it fast), with an AI assistant that can read the files but not edit them.
          </p>
        </div>
        <span className="text-sm tabular-nums text-muted">{solved} / {total} solved</span>
      </div>
      <div className="flex flex-wrap gap-2 text-sm">
        {stats.map((s) => (
          <Link key={s.group} href={`/repo-debugging?topic=${encodeURIComponent(s.group)}`} scroll={false} className={`btn ${s.group === selected?.group ? "border-accent" : ""}`}>
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
