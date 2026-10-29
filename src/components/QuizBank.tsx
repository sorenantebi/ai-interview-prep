"use client";
import { useState } from "react";
import Markdown from "./Markdown";
import { api } from "@/lib/client";
import type { QuizMarks, QuizQuestion } from "@/lib/quiz";

type Filter = "all" | "new" | "again" | "known";

/** getcracked-style questions: think (or type) your answer, reveal, then mark it "got it" or "again" (which hides the answer for a fresh try). */
export default function QuizBank({ questions, initial }: { questions: QuizQuestion[]; initial: QuizMarks }) {
  const [marks, setMarks] = useState(initial);
  const [open, setOpen] = useState<Record<string, boolean>>({});
  const [filter, setFilter] = useState<Filter>("all");
  const markOf = (id: string) => marks[id]?.mark;
  const shown = questions.filter((q) => filter === "all" || (filter === "new" ? !markOf(q.id) : markOf(q.id) === filter));
  const count = (f: Filter) => questions.filter((q) => (f === "all" ? true : f === "new" ? !markOf(q.id) : markOf(q.id) === f)).length;

  async function mark(id: string, m: "known" | "again") {
    const next = markOf(id) === m ? null : m; // clicking the active mark clears it
    setMarks((all) => {
      const copy = { ...all };
      if (next) copy[id] = { mark: next, at: new Date().toISOString() };
      else delete copy[id];
      return copy;
    });
    await api("/api/quiz", { id, mark: next });
  }

  const chip = (active: boolean) => `px-2.5 py-1 font-mono text-xs ${active ? "bg-fg text-panel" : "border border-border hover:border-fg"}`;
  return (
    <div className="space-y-3">
      <div className="flex flex-wrap items-center gap-1" role="radiogroup" aria-label="Show">
        {(["all", "new", "again", "known"] as Filter[]).map((f) => (
          <button key={f} role="radio" aria-checked={filter === f} className={chip(filter === f)} onClick={() => setFilter(f)}>
            {{ all: "All", new: "Not tried", again: "Again", known: "Got it" }[f]} <span className="opacity-70">{count(f)}</span>
          </button>
        ))}
      </div>
      {!shown.length && <p className="card p-4 text-sm text-muted">Nothing here.</p>}
      {shown.map((q, i) => (
        <article key={q.id} className="card space-y-3 p-4">
          <header className="flex flex-wrap items-baseline gap-2">
            <span className="font-mono text-xs text-muted">{i + 1}.</span>
            <h3 className="font-medium">{q.title}</h3>
            <span className={`tag ${q.difficulty === "Easy" ? "text-easy" : q.difficulty === "Hard" ? "text-hard" : "text-medium"}`}>{q.difficulty}</span>
            <span className="flex-1" />
            {markOf(q.id) && <span className={`font-mono text-xs ${markOf(q.id) === "known" ? "text-easy" : "text-hard"}`}>{markOf(q.id) === "known" ? "✓ got it" : "↻ again"}</span>}
          </header>
          <Markdown>{q.body}</Markdown>
          {open[q.id] ? (
            <div className="space-y-3 border-t border-border pt-3">
              <Markdown>{q.answer}</Markdown>
              <div className="flex gap-2">
                <button className={`btn ${markOf(q.id) === "known" ? "border-easy text-easy" : ""}`} onClick={() => mark(q.id, "known")}>✓ Got it</button>
                <button className={`btn ${markOf(q.id) === "again" ? "border-hard text-hard" : ""}`} onClick={() => { mark(q.id, "again"); setOpen((o) => ({ ...o, [q.id]: false })); }}>↻ Again</button>
                <button className="btn" onClick={() => setOpen((o) => ({ ...o, [q.id]: false }))}>Hide answer</button>
              </div>
            </div>
          ) : (
            <div className="space-y-2">
              <textarea className="input min-h-16 font-mono text-sm" placeholder="Your answer (optional, not saved)" aria-label={`Your answer to ${q.title}`} />
              <button className="btn-primary" onClick={() => setOpen((o) => ({ ...o, [q.id]: true }))}>Show answer</button>
            </div>
          )}
        </article>
      ))}
    </div>
  );
}
