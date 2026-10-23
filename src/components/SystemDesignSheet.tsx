"use client";
import Link from "next/link";
import { useState } from "react";
import Difficulty from "./Difficulty";
import ExcalidrawView, { type Scene } from "./ExcalidrawView";
import { NotesCell } from "./CheatSheet";
import { problemHref } from "./ProblemList";
import { fmtDate } from "@/lib/format";

export type SDEntry = { path: string; title: string; difficulty?: string; done?: string; diagram: Scene | null; notes: string; drawing: Scene | null };

// Problem | Solution diagram | Your notes
const COLS = "grid-cols-1 lg:grid-cols-[minmax(200px,0.8fr)_minmax(0,2.4fr)_minmax(240px,1.2fr)]";
const cell = "border-border p-3 lg:border-l lg:first:border-l-0";

export default function SystemDesignSheet({ groups }: { groups: { name: string; entries: SDEntry[] }[] }) {
  const [onlyDone, setOnlyDone] = useState(false);
  const shown = groups.map((g) => ({ ...g, entries: onlyDone ? g.entries.filter((e) => e.done) : g.entries })).filter((g) => g.entries.length);
  const doneCount = groups.reduce((n, g) => n + g.entries.filter((e) => e.done).length, 0);
  const chip = (active: boolean) => `px-2 py-0.5 font-mono text-xs ${active ? "bg-fg text-panel" : "border border-border hover:border-fg"}`;

  return (
    <div className="card max-h-[80vh] overflow-y-auto">
      <nav className="flex flex-wrap items-center gap-1 border-b border-border p-2" aria-label="System design categories">
        <button className={chip(!onlyDone)} onClick={() => setOnlyDone(false)}>All {groups.reduce((n, g) => n + g.entries.length, 0)}</button>
        <button className={chip(onlyDone)} onClick={() => setOnlyDone(true)}>Done {doneCount}</button>
        <span className="mx-1 text-border">|</span>
        {shown.map((g, i) => (
          <a key={g.name} href={`#sd-${i}`} className="border border-border px-2 py-0.5 font-mono text-xs hover:bg-fg hover:text-panel">{g.name}</a>
        ))}
      </nav>
      <div className={`sticky top-0 z-20 hidden border-b border-fg bg-panel font-mono text-[11px] uppercase tracking-wide text-muted lg:grid ${COLS}`}>
        {["Problem", "Solution diagram", "Your notes"].map((h) => <div key={h} className={`${cell} py-2`}>{h}</div>)}
      </div>
      {shown.length === 0 && <p className="p-4 text-sm text-muted">Nothing marked done yet. Use “Mark done” on a system design problem.</p>}
      {shown.map((g, i) => (
        <section key={g.name} id={`sd-${i}`} className="scroll-mt-9">
          <h3 className="sticky top-0 z-10 flex justify-between border-b border-border bg-fg/5 px-3 py-1.5 text-sm font-semibold backdrop-blur lg:top-[33px]">
            {g.name} <span className="font-normal text-muted">{g.entries.length}</span>
          </h3>
          {g.entries.map((e) => (
            <div key={e.path} className={`grid border-b border-border ${COLS}`}>
              <div className={`${cell} space-y-2`}>
                <Link href={problemHref(e.path)} className="block font-medium decoration-accent decoration-2 underline-offset-2 hover:underline">{e.title}</Link>
                <Difficulty level={e.difficulty} />
                <div className="font-mono text-xs text-muted">{e.done ? `done ${fmtDate(e.done)}` : "not done yet"}</div>
              </div>
              <div className={`${cell} min-w-0`}>
                {e.diagram ? (
                  <Link href={problemHref(e.path)} className="block border border-border hover:border-fg" title="Open the problem">
                    <ExcalidrawView scene={e.diagram} title={`${e.title} solution diagram`} className="max-h-80 w-full" />
                  </Link>
                ) : (
                  <p className="font-mono text-xs text-muted">No diagram.</p>
                )}
              </div>
              <div className={cell}>
                <div className={e.drawing?.elements?.length ? "h-36" : "h-full"}>
                  <NotesCell path={e.path} initial={e.notes} />
                </div>
                {e.drawing?.elements?.length ? (
                  <Link href={problemHref(e.path)} className="mt-2 block border border-border hover:border-fg" title="Open your drawing">
                    <ExcalidrawView scene={e.drawing} title={`${e.title}: your notes drawing`} className="max-h-60 w-full" />
                  </Link>
                ) : null}
              </div>
            </div>
          ))}
        </section>
      ))}
    </div>
  );
}
