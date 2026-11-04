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

/** "+ add" under a day: pick any problem (solved ones become reviews), a mock interview, or write your own task. */
function AddTask({ date }: { date: string }) {
  const router = useRouter();
  const groups = useContext(Options);
  const [open, setOpen] = useState(false);
  const [busy, setBusy] = useState(false);
  const [mock, setMock] = useState<"coding" | "system-design" | null>(null); // picked a mock: now choose its problem
  const [custom, setCustom] = useState<string | null>(null); // picked "custom task": now type it
  async function add(path: string, problem?: string, text?: string) {
    if (!path) return;
    setBusy(true);
    try { await api("/api/plan", { action: "add", date, path, problem, text }); setOpen(false); setMock(null); setCustom(null); startTransition(() => router.refresh()); }
    catch (e) { alert((e as Error).message); }
    finally { setBusy(false); }
  }
  if (!groups.length) return null; // e.g. the dashboard's today card, which has no problem list
  if (custom !== null) {
    return (
      <form className="mt-1" onSubmit={(e) => { e.preventDefault(); if (custom.trim()) add("note", undefined, custom); }}>
        <input className="input py-1 text-xs" autoFocus disabled={busy} value={custom} maxLength={300} onChange={(e) => setCustom(e.target.value)}
          onBlur={() => !busy && !custom.trim() && (setCustom(null), setOpen(false))} onKeyDown={(e) => e.key === "Escape" && (setCustom(null), setOpen(false))}
          placeholder="Your task, then Enter" aria-label={`Custom task for ${date}`} />
      </form>
    );
  }
  if (mock) {
    const area = mock === "coding" ? "leetcode" : "system-design";
    return (
      <select className="input mt-1 py-1 text-xs" autoFocus disabled={busy} defaultValue="" onChange={(e) => add(`mock:${mock}`, e.target.value === "any" ? undefined : e.target.value)} onBlur={() => !busy && (setMock(null), setOpen(false))} aria-label={`Problem for the mock ${mock} interview`}>
        <option value="" disabled>Mock {mock === "coding" ? "coding" : "system design"} interview on…</option>
        <option value="any">Interviewer picks</option>
        {groups.filter((g) => g.area === area).map((g) => (
          <optgroup key={g.name} label={g.name}>
            {g.problems.map((p) => <option key={p.path} value={p.path}>{p.title}{p.difficulty ? ` (${p.difficulty})` : ""}{p.solved ? " ✓" : ""}</option>)}
          </optgroup>
        ))}
      </select>
    );
  }
  if (!open) return <button className="mt-1 font-mono text-[11px] text-muted hover:text-fg" onClick={() => setOpen(true)}>+ add</button>;
  return (
    <select className="input mt-1 py-1 text-xs" autoFocus disabled={busy} defaultValue="" onChange={(e) => (e.target.value === "custom" ? setCustom("") : e.target.value.startsWith("mock:") ? setMock(e.target.value.slice(5) as "coding" | "system-design") : add(e.target.value))} onBlur={() => !busy && setOpen(false)} aria-label={`Add a problem to ${date}`}>
      <option value="" disabled>Pick a problem…</option>
      <option value="custom">✎ Custom task…</option>
      <optgroup label="Mock interview">
        <option value="mock:coding">Mock coding interview</option>
        <option value="mock:system-design">Mock system design interview</option>
      </optgroup>
      {groups.map((g) => (
        <optgroup key={g.area + g.name} label={`${{ leetcode: "LeetCode", "ml-coding": "ML coding", "system-design": "System design" }[g.area]} · ${g.name}`}>
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
        const auto = t.done === undefined && (t.type === "leetcode" || t.type === "ml-coding" || t.type === "system-design") && done.has(t.path);
        const isDone = ticked[i] ?? t.done ?? auto;
        return (
          <li key={i} className="flex items-start gap-2 text-sm">
            <input
              type="checkbox"
              className="mt-1 accent-[var(--accent)]"
              checked={isDone}
              onChange={() => toggle(i, !isDone)}
              aria-label={`Mark ${t.type === "note" ? t.text : t.type === "mock" ? `mock ${t.kind} interview` : t.title} done`}
              title={auto ? "Ticked because you solved this problem; click to untick" : undefined}
            />
            {t.type === "note" ? (
              <span className={isDone ? "text-muted line-through" : ""}>{t.text}</span>
            ) : t.type === "mock" ? (
              <Link href={`/ai?tab=interview&kind=${t.kind}${t.path ? `&problem=${encodeURIComponent(t.path)}` : ""}`} className={`decoration-accent decoration-2 underline-offset-2 hover:underline ${isDone ? "text-muted line-through" : ""}`}>
                <span className="mr-1.5 font-mono text-[11px] text-muted">mock</span>
                {t.kind === "coding" ? "Coding interview" : "System design interview"}{t.title ? `: ${t.title}` : ""}
              </Link>
            ) : (
              <Link href={problemHref(t.path) + (t.type === "review" ? "?review=1" : "")} className={`decoration-accent decoration-2 underline-offset-2 hover:underline ${isDone ? "text-muted line-through" : ""}`}>
                <span className="mr-1.5 font-mono text-[11px] text-muted no-underline" title={{ leetcode: "New LeetCode problem", "ml-coding": "New ML coding problem", "system-design": "System design", review: "Review: redo it from scratch" }[t.type]}>{{ leetcode: "LC", "ml-coding": "ML", "system-design": "SD", review: "↻ review" }[t.type]}</span>
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
