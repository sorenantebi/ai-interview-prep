import Link from "next/link";
import ProblemList from "@/components/ProblemList";
import { areaStats, progress } from "@/lib/content";

export const dynamic = "force-dynamic";

export default async function SystemDesignPage() {
  const [stats, prog] = await Promise.all([areaStats("system-design"), progress()]);
  return (
    <div className="mx-auto max-w-6xl space-y-6">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h1 className="page-title">System Design</h1>
        <div className="flex gap-2">
          <a href="https://www.hellointerview.com/learn/system-design/in-a-hurry/introduction" target="_blank" rel="noreferrer" className="btn">Hello Interview guide ↗</a>
          <Link href="/ai?tab=interview&kind=system-design" className="btn-primary">Mock interview</Link>
        </div>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        {stats.map((s) => (
          <section key={s.group} className="card">
            <div className="flex items-center justify-between border-b border-border px-4 py-3">
              <h2 className="font-medium">{s.name}</h2>
              <span className="text-sm tabular-nums text-muted">{s.solved} / {s.total}</span>
            </div>
            <ProblemList problems={s.problems} progress={prog} />
          </section>
        ))}
      </div>
    </div>
  );
}
