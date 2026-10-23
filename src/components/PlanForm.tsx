"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { api } from "@/lib/client";

const AREAS = ["LeetCode (NeetCode roadmap)", "System design", "Mock interviews", "Spaced-repetition reviews"];

/** Estimated progress while Claude writes the plan: fills over the expected time, then creeps towards 99%. */
function Progress({ seconds, expected }: { seconds: number; expected: number }) {
  const pct = seconds < expected ? 90 * (seconds / expected) : 90 + 9 * (1 - Math.exp(-(seconds - expected) / expected));
  const stage = seconds < 3 ? "Reading your problems and progress…" : seconds < expected * 0.9 ? "Claude is planning your days…" : "Checking the plan against your problems…";
  return (
    <div className="space-y-1.5" role="status" aria-live="polite">
      <div className="h-2 overflow-hidden bg-fg/10" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={Math.round(pct)} aria-label="Making your plan">
        <div className="h-full bg-accent transition-[width] duration-300" style={{ width: `${pct}%` }} />
      </div>
      <div className="flex justify-between font-mono text-xs text-muted">
        <span>{stage}</span>
        <span className="tabular-nums">{seconds}s · usually ~{expected}s</span>
      </div>
    </div>
  );
}

export default function PlanForm({ today, hasPlan }: { today: string; hasPlan: boolean }) {
  const router = useRouter();
  const [start, setStart] = useState(today);
  const [weeks, setWeeks] = useState(8);
  const [hours, setHours] = useState(2);
  const [focus, setFocus] = useState<string[]>(AREAS);
  const [notes, setNotes] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [seconds, setSeconds] = useState(0);
  useEffect(() => {
    if (!busy) return;
    setSeconds(0);
    const t0 = Date.now(), id = setInterval(() => setSeconds(Math.floor((Date.now() - t0) / 1000)), 250);
    return () => clearInterval(id);
  }, [busy]);
  const expected = Math.round(15 + 7 * weeks); // a 1-week plan took ~20s in testing; longer plans write more

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (hasPlan && !confirm("Replace your current plan? Ticked tasks in it will be lost.")) return;
    setBusy(true);
    setError("");
    try { await api("/api/plan", { action: "generate", start, weeks, hours, focus, notes }); router.refresh(); } catch (err) { setError((err as Error).message); } finally { setBusy(false); }
  }

  return (
    <form onSubmit={submit} className="card space-y-4 p-5">
      <h2 className="font-display text-xl font-medium">{hasPlan ? "Make a new plan" : "Make a study plan"}</h2>
      <div className="grid gap-3 sm:grid-cols-3">
        <label className="space-y-1 text-sm"><span className="font-medium">Start</span><input type="date" className="input font-mono" value={start} onChange={(e) => setStart(e.target.value)} required /></label>
        <label className="space-y-1 text-sm"><span className="font-medium">Weeks</span><input type="number" min={1} max={26} className="input font-mono" value={weeks} onChange={(e) => setWeeks(+e.target.value)} required /></label>
        <label className="space-y-1 text-sm"><span className="font-medium">Hours per day</span><input type="number" min={0.5} max={12} step={0.5} className="input font-mono" value={hours} onChange={(e) => setHours(+e.target.value)} required /></label>
      </div>
      <fieldset className="space-y-1 text-sm">
        <legend className="mb-1 font-medium">Cover</legend>
        <div className="flex flex-wrap gap-x-4 gap-y-1">
          {AREAS.map((a) => (
            <label key={a} className="flex items-center gap-1.5">
              <input type="checkbox" className="accent-[var(--accent)]" checked={focus.includes(a)} onChange={(e) => setFocus((f) => (e.target.checked ? [...f, a] : f.filter((x) => x !== a)))} />
              {a}
            </label>
          ))}
        </div>
      </fieldset>
      <label className="block space-y-1 text-sm">
        <span className="font-medium">Notes for the plan (optional)</span>
        <textarea className="input" rows={3} value={notes} onChange={(e) => setNotes(e.target.value)} placeholder="e.g. Google onsite on Dec 10, weak at DP and graphs, weekends free for longer sessions" />
      </label>
      <div className="flex items-center gap-3">
        <button className="btn-primary" disabled={busy || !focus.length}>{busy ? "Claude is planning…" : hasPlan ? "Replace plan" : "Make plan"}</button>
        <Link href={`/files?path=${encodeURIComponent("prompts/study-plan.md")}`} className="text-xs text-muted hover:text-fg">Edit prompt</Link>
      </div>
      {busy && <Progress seconds={seconds} expected={expected} />}
      {error && <pre className="whitespace-pre-wrap text-sm text-hard">{error}</pre>}
    </form>
  );
}
