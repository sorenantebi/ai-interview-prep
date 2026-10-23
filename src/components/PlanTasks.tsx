"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { problemHref } from "./ProblemList";
import { api } from "@/lib/client";
import type { Day } from "@/lib/plan";

/** Checklist for one plan day. Problem tasks are done when solved (checkbox shows it); any task can be ticked by hand. */
export default function PlanTasks({ day, solved }: { day: Day; solved: string[] }) {
  const router = useRouter();
  const [busy, setBusy] = useState(false);
  const done = new Set(solved);
  async function toggle(index: number) {
    setBusy(true);
    try { await api("/api/plan", { action: "toggle", date: day.date, index }); router.refresh(); } finally { setBusy(false); }
  }
  return (
    <ul className="space-y-1">
      {day.tasks.map((t, i) => {
        const solvedByProblem = (t.type === "leetcode" || t.type === "system-design") && done.has(t.path);
        const isDone = !!t.done || solvedByProblem;
        return (
          <li key={i} className="flex items-start gap-2 text-sm">
            <input
              type="checkbox"
              className="mt-1 accent-[var(--accent)]"
              checked={isDone}
              disabled={busy || (solvedByProblem && !t.done)}
              onChange={() => toggle(i)}
              aria-label={`Mark ${t.type === "note" ? t.text : t.title} done`}
              title={solvedByProblem && !t.done ? "Done: you solved this problem" : undefined}
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
