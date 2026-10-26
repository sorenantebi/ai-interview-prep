"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import type { PlanProgress } from "@/lib/plan";

const AREAS = ["LeetCode (NeetCode roadmap)", "ML coding (NumPy, pandas, PyTorch)", "System design", "Mock interviews", "Spaced-repetition reviews"];

const fmtTokens = (n: number) => (n >= 1000 ? `${(n / 1000).toFixed(1)}k` : String(n));

/** Live progress from the streamed plan: what Claude is doing, days written out of all days, and tokens used. */
function Progress({ p, seconds }: { p: PlanProgress | null; seconds: number }) {
  const pct = !p ? 0 : p.phase === "checking" ? 100 : (100 * p.days) / p.total;
  const day = p?.date ? new Date(p.date + "T00:00").toLocaleDateString(undefined, { weekday: "short", month: "short", day: "numeric" }) : "";
  const stage = !p ? "Reading your problems and progress…"
    : p.phase === "thinking" ? "Claude is thinking about your plan…"
    : p.phase === "checking" ? "Checking the plan against your problems…"
    : !p.date ? "Claude is starting to write…"
    : `Writing ${day}${p.focus ? ` · ${p.focus}` : ""} (day ${Math.max(p.days, 1)} of ${p.total})`;
  return (
    <div className="space-y-1.5" role="status" aria-live="polite">
      <div className="h-2 overflow-hidden bg-fg/10" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={Math.round(pct)} aria-label="Making your plan">
        <div className={`h-full bg-accent transition-[width] duration-300 ${p?.phase === "thinking" || !p ? "animate-pulse" : ""}`} style={{ width: `${Math.max(pct, 2)}%` }} />
      </div>
      <div className="flex justify-between gap-3 font-mono text-xs text-muted">
        <span>{stage}</span>
        <span className="shrink-0 tabular-nums">
          {p?.tokens ? `${fmtTokens(p.tokens.input)} in · ~${fmtTokens(p.tokens.output)} out · ` : ""}{seconds}s
        </span>
      </div>
    </div>
  );
}

export default function PlanForm({ today, hasPlan }: { today: string; hasPlan: boolean }) {
  const router = useRouter();
  const [start, setStart] = useState(today);
  const [weeks, setWeeks] = useState(8);
  const [focus, setFocus] = useState<string[]>(AREAS.filter((a) => !a.startsWith("ML coding"))); // ML coding is opt-in
  const [notes, setNotes] = useState("");
  const [previous, setPrevious] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [seconds, setSeconds] = useState(0);
  useEffect(() => {
    if (!busy) return;
    setSeconds(0);
    const t0 = Date.now(), id = setInterval(() => setSeconds(Math.floor((Date.now() - t0) / 1000)), 250);
    return () => clearInterval(id);
  }, [busy]);
  const [progress, setProgress] = useState<PlanProgress | null>(null);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (hasPlan && !confirm(previous ? "Replace your current plan with one built on it? Ticks stay on tasks that keep their day." : "Replace your current plan? Ticked tasks in it will be lost.")) return;
    setBusy(true);
    setError("");
    setProgress(null);
    try {
      const res = await fetch("/api/plan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ action: "generate", start, weeks, focus, notes, previous: hasPlan && previous }) });
      if (!res.ok || !res.body) throw new Error((await res.text()) || `HTTP ${res.status}`);
      // One JSON line per update: {progress}, then {plan} or {error}.
      const reader = res.body.pipeThrough(new TextDecoderStream()).getReader();
      let buf = "", done = false;
      while (!done) {
        const chunk = await reader.read();
        if (chunk.done) throw new Error("The connection closed before the plan was finished");
        buf += chunk.value;
        const lines = buf.split("\n");
        buf = lines.pop()!;
        for (const line of lines.filter(Boolean)) {
          const msg = JSON.parse(line);
          if (msg.error) throw new Error(msg.error);
          if (msg.progress) setProgress(msg.progress);
          if (msg.plan) done = true;
        }
      }
      router.refresh();
    } catch (err) { setError((err as Error).message); } finally { setBusy(false); }
  }

  return (
    <form onSubmit={submit} className="card space-y-4 p-5">
      <h2 className="font-display text-xl font-medium">{hasPlan ? "Make a new plan" : "Make a study plan"}</h2>
      <div className="grid gap-3 sm:grid-cols-2">
        <label className="space-y-1 text-sm"><span className="font-medium">Start</span><input type="date" className="input font-mono" value={start} onChange={(e) => setStart(e.target.value)} required /></label>
        <label className="space-y-1 text-sm"><span className="font-medium">Weeks</span><input type="number" min={1} max={26} className="input font-mono" value={weeks} onChange={(e) => setWeeks(+e.target.value)} required /></label>
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
      {hasPlan && (
        <label className="flex items-start gap-2 text-sm">
          <input type="checkbox" className="mt-1 accent-[var(--accent)]" checked={previous} onChange={(e) => setPrevious(e.target.checked)} />
          <span><span className="font-medium">Build on my current plan</span> <span className="text-muted">— Claude sees your current plan and what you&apos;ve done in it. Say how to use it in the notes, e.g. &quot;extend it by 4 weeks&quot;, &quot;same structure, more DP&quot;.</span></span>
        </label>
      )}
      <div className="flex items-center gap-3">
        <button className="btn-primary" disabled={busy || !focus.length}>{busy ? "Claude is planning…" : hasPlan ? "Replace plan" : "Make plan"}</button>
        <Link href={`/files?path=${encodeURIComponent("prompts/study-plan.md")}`} className="text-xs text-muted hover:text-fg">Edit prompt</Link>
      </div>
      {busy && <Progress p={progress} seconds={seconds} />}
      {error && <pre className="whitespace-pre-wrap text-sm text-hard">{error}</pre>}
    </form>
  );
}
