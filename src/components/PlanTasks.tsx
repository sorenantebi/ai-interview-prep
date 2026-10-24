"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { createContext, startTransition, useContext, useEffect, useState } from "react";
import { problemHref } from "./ProblemList";
import { api } from "@/lib/client";
import type { Day, ProblemGroup } from "@/lib/plan";

// The problem list is given once for the whole plan page, not copied into every day card.
const Options = createContext<ProblemGroup[]>([]);
export function PlanOptions({ groups, children }: { groups: ProblemGroup[]; children: React.ReactNode }) {
  return <Options.Provider value={groups}>{children}</Options.Provider>;
}

/** "+ add" under a day: pick any problem (solved ones become reviews). */
function AddTask({ date }: { date: string }) {
  const router = useRouter();
  const groups = useContext(Options);
  const [open, setOpen] = useState(false);
  const [busy, setBusy] = useState(false);
  async function add(path: string) {
    if (!path) return;
    setBusy(true);
    try { await api("/api/plan", { action: "add", date, path }); setOpen(false); startTransition(() => router.refresh()); }
    catch (e) { alert((e as Error).message); }
    finally { setBusy(false); }
  }
  if (!groups.length) return null; // e.g. the dashboard's today card, which has no problem list
  if (!open) return <button className="mt-1 font-mono text-[11px] text-muted hover:text-fg" onClick={() => setOpen(true)}>+ add</button>;
  return (
    <select className="input mt-1 py-1 text-xs" autoFocus disabled={busy} defaultValue="" onChange={(e) => add(e.target.value)} onBlur={() => !busy && setOpen(false)} aria-label={`Add a problem to ${date}`}>
      <option value="" disabled>Pick a problem…</option>
      {groups.map((g) => (
        <optgroup key={g.area + g.name} label={`${g.area === "leetcode" ? "LeetCode" : "System design"} · ${g.name}`}>
          {g.problems.map((p) => <option key={p.path} value={p.path}>{p.title}{p.difficulty ? ` (${p.difficulty})` : ""}{p.solved ? " ✓" : ""}</option>)}
        </optgroup>
      ))}
    </select>
  );
}

/** Checklist for one plan day. Problem tasks are done when solved (checkbox shows it); any task can be ticked by hand. */
export default function PlanTasks({ day, solved }: { day: Day; solved: string[] }) {
  const router = useRouter();
  const done = new Set(solved);
  // Optimistic ticks: the box flips at once; the page (counts, progress) refreshes in the background.
  const [ticked, setTicked] = useState<Record<number, boolean>>({});
  useEffect(() => setTicked({}), [day]); // fresh data from the server replaces the optimistic state
  function toggle(index: number, next: boolean) {
    setTicked((t) => ({ ...t, [index]: next }));
    api("/api/plan", { action: "toggle", date: day.date, index, done: next })
      .then(() => startTransition(() => router.refresh()))
      .catch(() => setTicked((t) => ({ ...t, [index]: !next }))); // save failed: undo the tick
  }
  function remove(index: number) {
    api("/api/plan", { action: "remove", date: day.date, index }).then(() => startTransition(() => router.refresh())).catch((e) => alert(e.message));
  }
  return (
    <>
    <ul className="space-y-1">
      {day.tasks.map((t, i) => {
        // Same rule as taskDone() in lib/plan.ts (not imported: that module is server-only).
        const auto = t.done === undefined && (t.type === "leetcode" || t.type === "system-design") && done.has(t.path);
        const isDone = ticked[i] ?? t.done ?? auto;
        return (
          <li key={i} className="flex items-start gap-2 text-sm">
            <input
              type="checkbox"
              className="mt-1 accent-[var(--accent)]"
              checked={isDone}
              onChange={() => toggle(i, !isDone)}
              aria-label={`Mark ${t.type === "note" ? t.text : t.title} done`}
              title={auto ? "Ticked because you solved this problem; click to untick" : undefined}
            />
            {t.type === "note" ? (
              <span className={isDone ? "text-muted line-through" : ""}>{t.text}</span>
            ) : (
              <Link href={problemHref(t.path)} className={`decoration-accent decoration-2 underline-offset-2 hover:underline ${isDone ? "text-muted line-through" : ""}`}>
                <span className="mr-1.5 font-mono text-[11px] text-muted no-underline" title={{ leetcode: "New LeetCode problem", "system-design": "System design", review: "Review: redo it from scratch" }[t.type]}>{{ leetcode: "LC", "system-design": "SD", review: "↻ review" }[t.type]}</span>
                {t.title}
              </Link>
            )}
            <button className="ml-auto px-1 font-mono text-xs text-muted hover:text-hard" onClick={() => remove(i)} aria-label="Remove from this day" title="Remove from this day">×</button>
          </li>
        );
      })}
    </ul>
    <AddTask date={day.date} />
    </>
  );
}
