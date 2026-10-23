"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { startTransition, useEffect, useState } from "react";
import { problemHref } from "./ProblemList";
import { api } from "@/lib/client";
import type { Day } from "@/lib/plan";

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
  return (
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
          </li>
        );
      })}
    </ul>
  );
}
