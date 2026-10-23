"use client";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { api } from "@/lib/client";
import type { Review } from "@/lib/content";

const RATINGS = [
  ["again", "Again", "Forgot it: review tomorrow"],
  ["hard", "Hard", "Struggled: same interval again"],
  ["good", "Good", "Solved it: next interval"],
  ["easy", "Easy", "Trivial: skip an interval"],
] as const;

/** Spaced-repetition toggle, editable next-review date, and rating buttons when a review is due. */
export default function ReviewControls({ path, review, today }: { path: string; review?: Review; today: string }) {
  const router = useRouter();
  const [busy, setBusy] = useState(false);
  async function act(action: string, due?: string) {
    setBusy(true);
    try { await api("/api/progress", { path, review: action, due }); router.refresh(); } finally { setBusy(false); }
  }
  if (!review)
    return <button className="btn px-2 py-1 text-xs" disabled={busy} onClick={() => act("enable")} title="Schedule this problem for spaced-repetition reviews">↻ Add to reviews</button>;
  const due = review.due <= today;
  return (
    <div className="flex flex-wrap items-center gap-1.5 text-xs">
      <label className={`flex items-center gap-1.5 font-mono ${due ? "font-medium text-medium" : "text-muted"}`}>
        {due ? "review due" : "↻ next review"}
        <input
          type="date"
          className="border border-border bg-panel px-1 py-0.5 font-mono text-xs text-fg"
          value={review.due}
          min={today}
          disabled={busy}
          onChange={(e) => e.target.value && act("set", e.target.value)}
          aria-label="Next review date"
        />
      </label>
      {due && RATINGS.map(([a, label, title]) => (
        <button key={a} className="btn px-2 py-1 text-xs" disabled={busy} onClick={() => act(a)} title={title}>{label}</button>
      ))}
      <button className="px-1 text-muted hover:text-hard" disabled={busy} onClick={() => act("disable")} title="Stop reviewing this problem" aria-label="Stop reviewing">✕</button>
    </div>
  );
}
