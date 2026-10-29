import Link from "next/link";
import DeckTools from "@/components/DeckTools";
import { decks, dueToday, schedule } from "@/lib/cards";
import { localDate } from "@/lib/content";

export const dynamic = "force-dynamic";

export default async function CardsPage() {
  const [all, sched] = await Promise.all([decks(), schedule()]);
  const today = localDate(new Date());
  const rows = all.map((d) => ({ d, ...dueToday(d, sched, today) }));
  const todo = rows.reduce((n, r) => n + r.due.length + r.fresh.length, 0);
  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h1 className="page-title">Cards</h1>
        {todo > 0 && <Link href="/cards/review" className="btn-primary">Review all ({todo})</Link>}
      </div>
      {rows.length > 0 ? (
        <ul className="card divide-y divide-border">
          {rows.map(({ d, due, fresh, total }) => (
            <li key={d.file} className="flex flex-wrap items-center gap-x-4 gap-y-2 px-4 py-3">
              <Link href={`/cards/${encodeURIComponent(d.file)}`} className="flex-1 font-medium decoration-accent decoration-2 underline-offset-2 hover:underline">{d.name}</Link>
              <span className="font-mono text-xs tabular-nums text-muted">
                <span className={due.length ? "text-hard" : ""}>{due.length} due</span> · <span className={fresh.length ? "text-accent" : ""}>{fresh.length} new</span> · {total} cards
              </span>
              <Link href={`/cards/review?deck=${encodeURIComponent(d.file)}`} className={`btn px-2 py-1 text-xs ${due.length + fresh.length ? "" : "pointer-events-none opacity-40"}`}>Review</Link>
              <Link href={`/cards/${encodeURIComponent(d.file)}`} className="btn px-2 py-1 text-xs">Edit</Link>
            </li>
          ))}
        </ul>
      ) : (
        <p className="card p-4 text-sm text-muted">No decks yet. Import one from Anki, generate one with Claude, or start an empty one below.</p>
      )}
      <DeckTools decks={all.map((d) => ({ file: d.file, name: d.name }))} />
    </div>
  );
}
