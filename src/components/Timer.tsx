"use client";
import { useEffect, useState } from "react";

type State = { kind: "stopwatch" | "countdown"; startedAt: number | null; elapsed: number; duration: number; interview?: boolean };
const IDLE: State = { kind: "stopwatch", startedAt: null, elapsed: 0, duration: 0 };
const KEY = "prep-timer";
const PRESETS = [15, 20, 30, 45, 60];
const EVENT = "prep-timer";

/** Lets other parts of the app drive the top-bar timer, e.g. a mock interview starting a 45-minute countdown. */
export function timerCommand(detail: { action: "countdown"; minutes: number; interview?: boolean } | { action: "pause" } | { action: "reset" }) {
  window.dispatchEvent(new CustomEvent(EVENT, { detail }));
}

const load = (): State => {
  try {
    const s = { ...IDLE, ...JSON.parse(localStorage.getItem(KEY) ?? "{}") };
    return s.interview ? IDLE : s; // a mock interview ends when its page goes away, so its clock does too
  } catch { return IDLE; }
};
const fmt = (ms: number) => {
  const s = Math.max(0, Math.round(ms / 1000));
  const h = Math.floor(s / 3600);
  const mm = String(Math.floor((s % 3600) / 60)).padStart(2, "0");
  const ss = String(s % 60).padStart(2, "0");
  return h ? `${h}:${mm}:${ss}` : `${mm}:${ss}`;
};

/** Global stopwatch / countdown in the top bar; survives page changes and reloads (stored in this browser). */
export default function Timer() {
  const [state, setState] = useState<State>(IDLE);
  const [open, setOpen] = useState(false);
  const [custom, setCustom] = useState("25");
  const [, tick] = useState(0);

  useEffect(() => setState(load()), []);
  useEffect(() => {
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch {}
  }, [state]);
  useEffect(() => {
    if (state.startedAt === null) return;
    const id = setInterval(() => tick((n) => n + 1), 500);
    return () => clearInterval(id);
  }, [state.startedAt]);

  const elapsed = state.elapsed + (state.startedAt ? Date.now() - state.startedAt : 0);
  const shown = state.kind === "countdown" ? state.duration - elapsed : elapsed;
  const done = state.kind === "countdown" && state.duration > 0 && shown <= 0;
  const running = state.startedAt !== null;
  const active = running || elapsed > 0;

  useEffect(() => {
    const base = document.title.replace(/^⏰ Time's up · /, "");
    document.title = done ? `⏰ Time's up · ${base}` : base;
  }, [done]);

  const start = (kind: State["kind"], minutes = 0, interview = false) => { setState({ kind, startedAt: Date.now(), elapsed: 0, duration: minutes * 60_000, interview }); setOpen(false); };
  const pause = () => setState((s) => ({ ...s, startedAt: null, elapsed: s.elapsed + (s.startedAt ? Date.now() - s.startedAt : 0) }));
  useEffect(() => {
    const on = (e: Event) => {
      const d = (e as CustomEvent).detail;
      if (d.action === "countdown") start("countdown", d.minutes, !!d.interview);
      else if (d.action === "pause") pause();
      else if (d.action === "reset") setState((s) => (s.interview ? IDLE : s)); // only clears an interview's clock
    };
    window.addEventListener(EVENT, on);
    return () => window.removeEventListener(EVENT, on);
  }, []);
  const resume = () => setState((s) => ({ ...s, startedAt: Date.now() }));
  const reset = () => setState(IDLE);

  const left = state.kind === "countdown" && state.duration > 0 ? Math.max(0, Math.min(1, shown / state.duration)) : null; // countdown progress
  return (
    <div className="relative">
      <button
        onClick={() => setOpen((o) => !o)}
        className={`relative flex h-8 cursor-pointer items-center gap-2 overflow-hidden whitespace-nowrap px-3 font-mono text-sm tabular-nums transition-colors ${
          done ? "animate-pulse bg-hard text-white" : active ? "bg-fg text-panel" : open ? "bg-fg text-panel" : "bg-panel hover:bg-fg hover:text-panel"
        }`}
        aria-expanded={open}
        aria-label={active ? `Timer ${fmt(shown)}${running ? "" : ", paused"}` : "Timer"}
        title={active ? (running ? "Timer running · click for controls" : "Timer paused · click to resume or reset") : "Start a countdown or stopwatch"}
      >
        <svg viewBox="0 0 16 16" className="h-4 w-4 shrink-0" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" aria-hidden>
          <circle cx="8" cy="9" r="5.5" />
          <path d="M8 9V6.5M6.5 1.5h3M12.2 4.3l1-1" />
        </svg>
        <span className="min-w-[3.25rem] text-left">{done ? "time's up" : active ? fmt(shown) : "timer"}</span>
        {active && !done && <span className={`h-1.5 w-1.5 rounded-full ${running ? "animate-pulse bg-accent" : "bg-muted"}`} aria-hidden />}
        {left !== null && !done && <span className="absolute bottom-0 left-0 h-0.5 bg-accent transition-[width] duration-500" style={{ width: `${left * 100}%` }} aria-hidden />}
      </button>
      {open && (
        <div className="absolute right-0 top-full z-50 mt-1 w-80 space-y-4 border border-fg bg-panel p-4 text-sm shadow-lg">
          {active && (
            <div className="flex items-center gap-2">
              <span className="mr-auto font-mono text-4xl tabular-nums">{fmt(shown)}</span>
              {running ? <button className="btn" onClick={pause}>pause</button> : <button className="btn" onClick={resume} disabled={done}>resume</button>}
              <button className="btn" onClick={reset}>reset</button>
            </div>
          )}
          <div>
            <div className="mb-1.5 font-mono text-xs uppercase tracking-wide text-muted">Countdown</div>
            <div className="flex flex-wrap gap-1">
              {PRESETS.map((m) => <button key={m} className="btn font-mono" onClick={() => start("countdown", m)}>{m}m</button>)}
            </div>
            <form className="mt-1.5 flex gap-1" onSubmit={(e) => { e.preventDefault(); if (+custom > 0) start("countdown", +custom); }}>
              <input className="input w-24 font-mono" type="number" min={1} max={600} value={custom} onChange={(e) => setCustom(e.target.value)} aria-label="Custom minutes" />
              <button className="btn">start</button>
            </form>
          </div>
          <div>
            <div className="mb-1.5 font-mono text-xs uppercase tracking-wide text-muted">Stopwatch</div>
            <button className="btn" onClick={() => start("stopwatch")}>start stopwatch</button>
          </div>
        </div>
      )}
    </div>
  );
}
