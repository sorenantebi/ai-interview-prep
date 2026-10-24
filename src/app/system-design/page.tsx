import Link from "next/link";
import ProblemList from "@/components/ProblemList";
import Markdown from "@/components/Markdown";
import { areaStats, progress, read } from "@/lib/content";

export const dynamic = "force-dynamic";

export default async function SystemDesignPage() {
  const [stats, prog] = await Promise.all([areaStats("system-design"), progress()]);
  // ML categories (folder name starts with "ML") get their own section, with an optional guide.md in the folder.
  const isMl = (s: (typeof stats)[number]) => /^ml\b/i.test(s.name);
  const ml = stats.filter(isMl);
  const guides = await Promise.all(ml.map((s) => read(`system-design/${s.group}/guide.md`)));
  const grid = (list: typeof stats) => (
    <div className="grid gap-4 md:grid-cols-2">
      {list.map((s) => (
        <section key={s.group} className="card">
          <div className="flex items-center justify-between border-b border-border px-4 py-3">
            <h2 className="font-medium">{s.name}</h2>
            <span className="text-sm tabular-nums text-muted">{s.solved} / {s.total}</span>
          </div>
          <ProblemList problems={s.problems} progress={prog} />
        </section>
      ))}
    </div>
  );
  return (
    <div className="mx-auto max-w-6xl space-y-6">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h1 className="page-title">System Design</h1>
        <div className="flex gap-2">
          <a href="https://www.hellointerview.com/learn/system-design/in-a-hurry/introduction" target="_blank" rel="noreferrer" className="btn">Hello Interview guide ↗</a>
          <Link href="/ai?tab=interview&kind=system-design" className="btn-primary">Mock interview</Link>
        </div>
      </div>
      {grid(stats.filter((s) => !isMl(s)))}
      {ml.length > 0 && (
        <>
          <div className="flex flex-wrap items-baseline justify-between gap-2 pt-4">
            <h2 className="page-title">ML System Design</h2>
            <a href="https://www.hellointerview.com/learn/ml-system-design/in-a-hurry/introduction" target="_blank" rel="noreferrer" className="btn">Hello Interview ML guide ↗</a>
          </div>
          {guides.map((g, i) => g && (
            <details key={i} className="card">
              <summary className="cursor-pointer select-none px-6 py-4 font-medium">ML system design in a hurry: framework and core concepts</summary>
              <div className="border-t border-border px-6 py-5"><Markdown>{g}</Markdown></div>
            </details>
          ))}
          {grid(ml)}
        </>
      )}
    </div>
  );
}
