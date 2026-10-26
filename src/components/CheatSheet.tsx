"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import Markdown from "./Markdown";
import Difficulty from "./Difficulty";
import ReviewControls from "./ReviewControls";
import { SketchView, type Stroke } from "./SketchPad";
import { problemHref } from "./ProblemList";
import { putFile } from "@/lib/client";
import { fmtDate } from "@/lib/format";
import type { Review } from "@/lib/content";

export type CheatEntry = {
  path: string; title: string; difficulty?: string; at: string; review?: Review; hasAttempt: boolean;
  code: string; codeSource: "passed" | "latest" | null; time?: string; space?: string; notes: string;
  mine: { time: string; space: string; timeOk: boolean | null; spaceOk: boolean | null; claimed?: { time: string; space: string } } | null; drawing: Stroke[];
};

// Problem | Your solution | Complexity | Your notes | Drawing (ML Coding has no complexity column)
const COLS = "grid-cols-1 lg:grid-cols-[minmax(200px,1fr)_minmax(0,2fr)_130px_minmax(200px,1.3fr)_minmax(180px,1fr)]";
const COLS_NO_COMPLEXITY = "grid-cols-1 lg:grid-cols-[minmax(200px,1fr)_minmax(0,2fr)_minmax(200px,1.3fr)_minmax(180px,1fr)]";
const cell = "border-border p-3 lg:border-l lg:first:border-l-0";

/** Excel-style cell: edits notes.md in place and saves when you click away. */
export function NotesCell({ path, initial }: { path: string; initial: string }) {
  const [value, setValue] = useState(initial);
  const [saved, setSaved] = useState(initial);
  const [error, setError] = useState("");
  async function save() {
    if (value === saved) return;
    try { await putFile(`${path}/notes.md`, value); setSaved(value); setError(""); } catch (e) { setError((e as Error).message); }
  }
  return (
    <div className="flex h-full flex-col gap-1">
      <textarea
        className="min-h-24 w-full flex-1 resize-y bg-transparent text-sm leading-relaxed outline-none placeholder:text-muted/70 focus:bg-fg/5"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onBlur={save}
        placeholder="Your notes: the key idea, the trick, what you got wrong…"
        aria-label="Your notes"
      />
      <span className="font-mono text-[11px] text-muted">{error ? <span className="text-hard">{error}</span> : value !== saved ? "unsaved: click outside to save" : value ? "notes.md" : ""}</span>
    </div>
  );
}

export default function CheatSheet({ groups, today, complexity = true }: { groups: { name: string; entries: CheatEntry[] }[]; today: string; complexity?: boolean }) {
  const router = useRouter();
  const cols = complexity ? COLS : COLS_NO_COMPLEXITY;
  async function reset(path: string) {
    if (!confirm("Clear your working code for this problem? You start from the blank template next time. Your passing solution stays in the cheat sheet.")) return;
    await fetch(`/api/files?path=${encodeURIComponent(`${path}/attempt.py`)}`, { method: "DELETE" });
    router.refresh();
  }
  if (!groups.length) return <p className="card p-4 text-sm text-muted">Solved problems show up here as a cheat sheet, grouped by topic.</p>;

  return (
    <div className="card max-h-[80vh] overflow-y-auto">
      <nav className="flex flex-wrap gap-1 border-b border-border p-2" aria-label="Cheat sheet topics">
        {groups.map((g, i) => (
          <a key={g.name} href={`#cheat-${i}`} className="border border-border px-2 py-0.5 font-mono text-xs hover:bg-fg hover:text-panel">
            {g.name} <span className="opacity-60">{g.entries.length}</span>
          </a>
        ))}
      </nav>
      <div className={`sticky top-0 z-20 hidden border-b border-fg bg-panel font-mono text-[11px] uppercase tracking-wide text-muted lg:grid ${cols}`}>
        {["Problem", "Your solution", ...(complexity ? ["Complexity"] : []), "Your notes", "Drawing"].map((h) => <div key={h} className={`${cell} py-2`}>{h}</div>)}
      </div>
      {groups.map((g, i) => (
        <section key={g.name} id={`cheat-${i}`} className="scroll-mt-9">
          <h3 className="sticky top-0 z-10 flex justify-between border-b border-border bg-fg/5 px-3 py-1.5 text-sm font-semibold backdrop-blur lg:top-[33px]">
            {g.name} <span className="font-normal text-muted">{g.entries.length}</span>
          </h3>
          {g.entries.map((e) => (
            <div key={e.path} className={`grid border-b border-border ${cols}`}>
              <div className={`${cell} space-y-2`}>
                <Link href={problemHref(e.path)} className="block font-medium decoration-accent decoration-2 underline-offset-2 hover:underline">{e.title}</Link>
                <div className="flex flex-wrap items-center gap-x-3 gap-y-1">
                  <Difficulty level={e.difficulty} />
                  <span className="font-mono text-xs text-muted">solved {fmtDate(e.at)}</span>
                </div>
                <ReviewControls path={e.path} review={e.review} today={today} />
                {e.hasAttempt && <button className="btn px-2 py-1 text-xs" onClick={() => reset(e.path)}>Reset code</button>}
              </div>
              <div className={`${cell} min-w-0`}>
                {e.code ? (
                  <>
                    <div className="mb-1 font-mono text-[11px] text-muted">{e.codeSource === "passed" ? "passing solution" : "latest code (tests not passed yet)"}</div>
                    <div className="max-h-64 overflow-y-auto text-xs [&_.md]:text-xs [&_pre]:mb-0">
                      <Markdown>{"```python\n" + e.code + "\n```"}</Markdown>
                    </div>
                  </>
                ) : (
                  <p className="font-mono text-xs text-muted">No saved code. Pass the tests on the problem page to store your solution here.</p>
                )}
              </div>
              {complexity && <div className={`${cell} space-y-2`}>
                {(["time", "space"] as const).map((k) => {
                  const ok = e.mine?.[k === "time" ? "timeOk" : "spaceOk"];
                  return (
                    <div key={k}>
                      <div className="font-mono text-[11px] uppercase tracking-wide text-muted">{k}</div>
                      {e.mine?.claimed ? (
                        <div title="What you submitted, checked against your code">
                          <code className={`font-mono text-base ${ok ? "text-easy" : "text-hard"}`}>{ok ? "✓ " : "✗ "}{e.mine.claimed[k]}</code>
                          {!ok && <div className="font-mono text-xs">is <code>{e.mine[k]}</code></div>}
                        </div>
                      ) : (
                        <code className="font-mono text-base" title="From the reference solution">{e[k] ?? "–"}</code>
                      )}
                      {e.mine?.claimed && <div className="font-mono text-[10px] text-muted" title="From the reference solution">ref {e[k] ?? "–"}</div>}
                    </div>
                  );
                })}
              </div>}
              <div className={cell}>
                <NotesCell path={e.path} initial={e.notes} />
              </div>
              <div className={cell}>
                {e.drawing.length > 0 ? (
                  <Link href={`${problemHref(e.path)}?tab=notes`} className="block border border-border bg-panel hover:border-fg" title="Open the drawing">
                    <SketchView strokes={e.drawing} className="w-full" />
                  </Link>
                ) : (
                  <Link href={`${problemHref(e.path)}?tab=notes`} className="font-mono text-xs text-muted hover:text-fg">+ draw</Link>
                )}
              </div>
            </div>
          ))}
        </section>
      ))}
    </div>
  );
}
