import Link from "next/link";
import DeckTools from "@/components/DeckTools";
import AnkiSwitch from "@/components/AnkiSwitch";
import { ankiSettings, decks, dueToday, reviewDecks, schedule } from "@/lib/cards";
import { localDate } from "@/lib/content";

export const dynamic = "force-dynamic";

export default async function CardsPage() {
  const [all, sched, settings] = await Promise.all([decks(), schedule(), ankiSettings()]);
  const today = localDate(new Date());
  const rows = all.map((d) => ({ d, ...dueToday(d, sched, today) }));
  const picked = new Set(reviewDecks(all, settings).map((d) => d.file));
  const todo = rows.filter((r) => picked.has(r.d.file)).reduce((n, r) => n + r.due.length + r.fresh.length, 0);
  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h1 className="page-title">Anki</h1>
        <div className="flex items-center gap-4">
          <AnkiSwitch checked={settings.daily} label="Daily review (on the dashboard)" />
          {todo > 0 && <Link href="/anki/review" className="btn-primary">Review picked decks ({todo})</Link>}
        </div>
      </div>
      {rows.length > 0 ? (
        <ul className="card divide-y divide-border">
          {rows.map(({ d, due, fresh, total }) => (
            <li key={d.file} className="flex flex-wrap items-center gap-x-4 gap-y-2 px-4 py-3">
              <Link href={`/anki/${encodeURIComponent(d.file)}`} className="flex-1 font-medium decoration-accent decoration-2 underline-offset-2 hover:underline">{d.name}</Link>
              <span className="font-mono text-xs tabular-nums text-muted">
                <span className={due.length ? "text-hard" : ""}>{due.length} due</span> · <span className={fresh.length ? "text-accent" : ""}>{fresh.length} new</span> · {total} cards
              </span>
              {settings.daily && <AnkiSwitch key={`${d.file}-${!settings.skip.includes(d.file)}`} deck={d.file} checked={!settings.skip.includes(d.file)} label="daily" />}
              <Link href={`/anki/review?deck=${encodeURIComponent(d.file)}`} className={`btn px-2 py-1 text-xs ${due.length + fresh.length ? "" : "pointer-events-none opacity-40"}`}>Review</Link>
              <Link href={`/anki/${encodeURIComponent(d.file)}`} className="btn px-2 py-1 text-xs">Edit</Link>
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
