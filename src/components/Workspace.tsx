"use client";
import Editor from "@monaco-editor/react";
import { DOC, NO_ASSIST, docLanguage, registerDocLanguages } from "./editor-options";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import Markdown from "./Markdown";
import ReviewControls from "./ReviewControls";
import { isDark } from "./ThemeToggle";
import SketchPad, { type Stroke } from "./SketchPad";
import { api, putFile } from "@/lib/client";
import type { Review } from "@/lib/content";
import type { CaseResult } from "@/lib/run";

type Tab = "question" | "solution" | "notes" | "tests";
type Lang = "python" | "cpp";
const LANG_LABEL: Record<Lang, string> = { python: "Python", cpp: "C++" };
type Run = { results?: CaseResult[]; error?: string };

const mark = (ok?: boolean | null) => (ok === true ? "✓" : ok === false ? "✗" : "?");
const markColor = (ok?: boolean | null) => (ok === true ? "text-easy" : ok === false ? "text-hard" : "text-medium");

function verdict(run: Run): [string, string] {
  if (run.error) return ["Error", "text-hard"];
  const rs = run.results ?? [];
  if (rs.some((r) => r.error)) return ["Runtime Error", "text-hard"];
  if (rs.some((r) => r.ok === false)) return ["Wrong Answer", "text-hard"];
  if (rs.some((r) => r.ok == null)) return ["Check your answer", "text-medium"];
  return ["Accepted", "text-easy"];
}

/** A drag handle between panels (also works with arrow keys; double-click resets). */
function Divider({ dir, onMove, onStep, onReset }: { dir: "x" | "y"; onMove: (e: React.PointerEvent) => void; onStep: (delta: number) => void; onReset: () => void }) {
  const x = dir === "x";
  return (
    <div
      role="separator"
      aria-orientation={x ? "vertical" : "horizontal"}
      aria-label={x ? "Drag to resize the question and editor" : "Drag to resize the results panel"}
      tabIndex={0}
      title="Drag to resize · double-click to reset"
      onPointerDown={(e) => { e.currentTarget.setPointerCapture(e.pointerId); e.preventDefault(); }}
      onPointerMove={(e) => e.buttons & 1 && onMove(e)}
      onDoubleClick={onReset}
      onKeyDown={(e) => {
        const d = { ArrowLeft: -1, ArrowUp: -1, ArrowRight: 1, ArrowDown: 1 }[e.key];
        if (d) { e.preventDefault(); onStep(d); }
      }}
      className={`group flex shrink-0 touch-none select-none items-center justify-center outline-none ${x ? "w-3 cursor-col-resize max-lg:hidden" : "h-3 cursor-row-resize"}`}
    >
      <div className={`bg-border transition-colors group-hover:bg-accent group-focus-visible:bg-accent group-active:bg-accent ${x ? "h-10 w-1" : "h-1 w-10"}`} />
    </div>
  );
}

/** LeetCode-style testcase editor (inputs only) plus the results of the last Run. */
function TestsPanel(props: { names: string[]; cases: string[][]; examples: string[][]; onChange: (c: string[][]) => void; run: Run | null; busy: boolean; onRun: () => void }) {
  const { names, cases, onChange, run } = props;
  const [sel, setSel] = useState(0);
  const [view, setView] = useState<"cases" | "result">("cases");
  const [rsel, setRsel] = useState(0);
  useEffect(() => { if (run) { setView("result"); setRsel(Math.max(0, (run.results ?? []).findIndex((r) => r.ok !== true))); } }, [run]);
  const i = Math.min(sel, cases.length - 1);
  const set = (j: number, v: string) => onChange(cases.map((c, k) => (k === i ? c.map((x, n) => (n === j ? v : x)) : c)));
  const chip = (active: boolean) => `px-2.5 py-1 font-mono text-xs ${active ? "bg-fg text-panel" : "border border-border hover:border-fg"}`;

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center gap-1 border-b border-border p-2">
        <button className={chip(view === "cases")} onClick={() => setView("cases")}>Testcase</button>
        <button className={chip(view === "result")} onClick={() => setView("result")} disabled={!run}>Test result</button>
        <span className="flex-1" />
        <button className="btn px-2 py-1 text-xs" onClick={props.onRun} disabled={props.busy}>▶ Run</button>
      </div>
      {view === "cases" && !names.length ? (
        <p className="p-3 font-mono text-xs text-muted">Run compiles your code and runs the examples from the question. Submit runs the hidden tests too.</p>
      ) : view === "cases" ? (
        <div className="space-y-3 p-3">
          <div className="flex flex-wrap items-center gap-1">
            {cases.map((_, k) => (
              <span key={k} className="inline-flex">
                <button className={chip(k === i)} onClick={() => setSel(k)}>Case {k + 1}</button>
                {cases.length > 1 && k === i && (
                  <button className="border border-l-0 border-border px-1.5 text-xs text-muted hover:text-hard" aria-label={`Remove case ${k + 1}`} onClick={() => { onChange(cases.filter((_, n) => n !== k)); setSel(Math.max(0, k - 1)); }}>×</button>
                )}
              </span>
            ))}
            <button className="px-2 py-1 font-mono text-xs text-muted hover:text-fg" onClick={() => { onChange([...cases, [...cases[i]]]); setSel(cases.length); }} aria-label="Add a case">+ case</button>
            <span className="flex-1" />
            <button className="font-mono text-[11px] text-muted hover:text-fg" onClick={() => { onChange(props.examples); setSel(0); }}>reset to examples</button>
          </div>
          {names.map((name, j) => (
            <label key={name} className="block space-y-1">
              <span className="font-mono text-xs text-muted">{name} =</span>
              <textarea
                className="input resize-y font-mono text-[13px]"
                rows={Math.min(8, Math.max(1, (cases[i]?.[j] ?? "").split("\n").length))}
                value={cases[i]?.[j] ?? ""}
                onChange={(e) => set(j, e.target.value)}
                spellCheck={false}
              />
            </label>
          ))}
          <p className="font-mono text-[11px] text-muted">Inputs only, like LeetCode. Expected output comes from NeetCode&apos;s solution.</p>
        </div>
      ) : run ? (
        <div className="space-y-3 p-3">
          <div className={`font-display text-xl font-medium ${verdict(run)[1]}`}>{verdict(run)[0]}</div>
          {run.error ? (
            <pre className="overflow-x-auto whitespace-pre-wrap bg-hard/10 p-2 font-mono text-xs">{run.error}</pre>
          ) : (
            <>
              <div className="flex flex-wrap gap-1">
                {run.results!.map((r, k) => (
                  <button key={k} className={chip(k === rsel)} onClick={() => setRsel(k)}>
                    <span className={k === rsel ? "" : markColor(r.ok)}>{mark(r.error ? false : r.ok)}</span> Case {k + 1}
                  </button>
                ))}
              </div>
              {(() => {
                const r = run.results![rsel];
                if (!r) return null;
                const box = (label: string, value: string, cls = "") => (
                  <div className="space-y-1">
                    <div className="font-mono text-xs text-muted">{label}</div>
                    <pre className={`overflow-x-auto whitespace-pre-wrap bg-fg/5 p-2 font-mono text-[13px] ${cls}`}>{value}</pre>
                  </div>
                );
                return (
                  <div className="space-y-2">
                    {box(names.length ? "Input" : "Case", names.length ? r.input.map((v, n) => `${names[n] ?? `arg${n + 1}`} = ${v}`).join("\n") : r.input.join("\n"))}
                    {r.error ? box("Error", r.error, "text-hard") : r.output !== undefined && box("Output", r.output, r.ok === false ? "text-hard" : "")}
                    {r.expected !== undefined && box("Expected", r.expected)}
                    {r.stdout && box("Stdout", r.stdout)}
                    {r.note && <p className="font-mono text-[11px] text-medium">{r.note}</p>}
                  </div>
                );
              })()}
            </>
          )}
        </div>
      ) : null}
    </div>
  );
}

export default function Workspace(props: {
  path: string; question: string; solution: string; fresh?: boolean; // fresh: a review, start from the starter
  langs: Lang[]; attempts: Record<Lang, string | null>; starters: Record<Lang, string>; // the languages this problem offers
  names: string[]; cases: string[][]; examples: string[][]; notes: string; drawing: Stroke[]; status?: string; review?: Review; today: string;
  nav: { prev: string | null; next: string | null; pos: number; total: number; random: boolean; unsolved: boolean };
  topics: string[];
}) {
  const { path } = props;
  const [tab, setTab] = useState<Tab>((useSearchParams().get("tab") as Tab) ?? "question");
  const [lang, setLang] = useState<Lang>(props.langs[0]);
  useEffect(() => {
    try { const l = localStorage.getItem("codeLang") as Lang | null; if (l && props.langs.includes(l)) setLang(l); } catch {}
  }, [props.langs]);
  const switchLang = (l: Lang) => {
    setLang(l);
    try { localStorage.setItem("codeLang", l); } catch {}
  };
  const saved = (l: Lang) => props.attempts[l] ?? props.starters[l];
  const [codes, setCodes] = useState<Record<Lang, string>>({ python: props.fresh ? props.starters.python : saved("python"), cpp: props.fresh ? props.starters.cpp : saved("cpp") });
  const code = codes[lang];
  const setCode = (v: string) => setCodes((c) => ({ ...c, [lang]: v }));
  const [notes, setNotes] = useState(props.notes);
  const [cases, setCases] = useState(props.cases);
  const [run, setRun] = useState<Run | null>(null);
  type Verdict = { time: string; space: string; timeOk: boolean | null; spaceOk: boolean | null; why: string; claimed?: { time: string; space: string }; error?: string };
  const [submit, setSubmit] = useState<{ ok: boolean; output: string; complexity?: Verdict | null } | null>(null);
  // Panel sizes: question width (% of the row) and results height (px); remembered in this browser.
  const LAYOUT = { left: 50, bottom: 240 };
  const [layout, setLayout] = useState(LAYOUT);
  const row = useRef<HTMLDivElement>(null);
  const right = useRef<HTMLElement>(null);
  useEffect(() => {
    try { setLayout((l) => ({ ...l, ...JSON.parse(localStorage.getItem("workspace-layout") ?? "{}") })); } catch {}
  }, []);
  const resize = (next: Partial<typeof LAYOUT>) => setLayout((l) => {
    const v = { ...l, ...next };
    v.left = Math.min(80, Math.max(20, v.left));
    v.bottom = Math.min((right.current?.clientHeight ?? 800) - 220, Math.max(80, v.bottom));
    try { localStorage.setItem("workspace-layout", JSON.stringify(v)); } catch {}
    return v;
  });
  const [myTime, setMyTime] = useState("");
  const [mySpace, setMySpace] = useState("");
  const router = useRouter();
  const [coach, setCoach] = useState("");
  const [busy, setBusy] = useState<string | null>(null);
  const [status, setStatus] = useState(props.status);
  const [dark, setDark] = useState(false);
  useEffect(() => {
    const update = () => setDark(isDark());
    update();
    window.addEventListener("prep-theme", update);
    return () => window.removeEventListener("prep-theme", update);
  }, []);
  const [mode, setMode] = useState<"doc" | "ide">("doc");
  useEffect(() => {
    try { if (localStorage.getItem("editorMode") === "ide") setMode("ide"); } catch {}
  }, []);
  const switchMode = (m: "doc" | "ide") => {
    setMode(m);
    try { localStorage.setItem("editorMode", m); } catch {}
  };

  // Review: drop ?review=1 from the URL so reloading keeps what you've written since (autosave stores the blank start).
  useEffect(() => {
    if (!props.fresh) return;
    const url = new URL(window.location.href);
    url.searchParams.delete("review");
    router.replace(url.pathname + url.search, { scroll: false });
  }, [props.fresh, router]);
  // Autosave attempt.py / attempt.cpp and your test cases one second after you stop typing.
  const unchanged = code === saved(lang);
  useEffect(() => {
    if (unchanged) return;
    const t = setTimeout(() => putFile(`${path}/attempt.${lang === "cpp" ? "cpp" : "py"}`, code), 1000);
    return () => clearTimeout(t);
  }, [code, lang, path, unchanged]);
  useEffect(() => {
    if (cases === props.cases) return;
    const t = setTimeout(() => putFile(`${path}/testcases.json`, JSON.stringify({ names: props.names, cases }, null, 2)), 1000);
    return () => clearTimeout(t);
  }, [cases, path, props.cases, props.names]);

  async function runCases() {
    setTab("tests");
    setBusy("Running your test cases…");
    try {
      setRun(await api("/api/run", { path, code, lang, mode: "run", cases, names: props.names }));
    } catch (e) {
      setRun({ error: (e as Error).message });
    } finally {
      setBusy(null);
    }
  }

  // After a passing submit, the Time/Space boxes turn green (right) or red (wrong) until you edit them.
  function mark(k: "time" | "space") {
    const c = submit?.complexity;
    const ok = c && !c.error ? c[k === "time" ? "timeOk" : "spaceOk"] : null;
    if (ok === null || c?.claimed?.[k] !== (k === "time" ? myTime : mySpace).trim()) return "";
    return ok ? "bg-easy/15 text-easy" : "bg-hard/15 text-hard";
  }

  async function submitCode(regenerate = false) {
    setBusy(regenerate ? "Claude is writing new hidden tests…" : myTime.trim() || mySpace.trim() ? "Submitting, then Claude checks your complexity…" : "Submitting…");
    setSubmit(null);
    try {
      const r = await api("/api/run", { path, code, lang, mode: "submit", regenerate, time: myTime, space: mySpace });
      setSubmit(r);
      setStatus((s) => (r.ok ? "solved" : s === "solved" ? s : "attempted"));
    } catch (e) {
      setSubmit({ ok: false, output: (e as Error).message });
    } finally {
      setBusy(null);
    }
  }

  async function hint() {
    setBusy("Asking for a hint…");
    try {
      setCoach((await api("/api/claude", { action: "hint", path, code, lang, output: submit?.output ?? "" })).text);
    } catch (e) {
      setCoach("**Error:** " + (e as Error).message);
    } finally {
      setBusy(null);
    }
  }

  async function complexity() {
    setBusy("Working out your code's complexity…");
    try {
      const r: Verdict = await api("/api/claude", { action: "complexity", path, code, lang });
      setCoach(`**Your code's complexity**\n\n- Time: \`${r.time}\`\n- Space: \`${r.space}\`\n\n${r.why}`);
    } catch (e) {
      setCoach("**Error:** " + (e as Error).message);
    } finally {
      setBusy(null);
    }
  }

  async function moveTo(group: string) {
    if (!group || !confirm(`Move this problem to “${group.replace(/^\d+\s*/, "")}”? Your code, notes and progress move with it.`)) return;
    try {
      const r = await api("/api/problem", { action: "move", path, group });
      router.push("/" + r.path.split("/").map(encodeURIComponent).join("/"));
    } catch (e) {
      alert((e as Error).message);
    }
  }

  async function toggleSolved() {
    const next = status === "solved" ? null : "solved";
    await api("/api/progress", { path, status: next });
    setStatus(next ?? undefined);
  }

  const [area, group] = path.split("/");
  return (
    <div className="flex h-[calc(100vh-7.5rem)] flex-col gap-3 max-lg:h-auto">
      <div className="flex flex-wrap items-center gap-2 text-sm">
        {props.nav.random ? (
          <Link href={`/${area}`} className="text-muted hover:text-fg">← exit shuffle</Link>
        ) : (
          <Link href={`/${area}?topic=${encodeURIComponent(group)}`} className="text-muted hover:text-fg">← {group.replace(/^\d+\s*/, "")}</Link>
        )}
        <select
          className="border border-border bg-panel px-1.5 py-1 font-mono text-xs text-muted hover:text-fg"
          value=""
          onChange={(e) => moveTo(e.target.value === "+" ? (prompt("New topic name (e.g. 19 Strings)") ?? "").trim() : e.target.value)}
          aria-label="Move this problem to another topic"
          title="Change this problem's topic"
        >
          <option value="">topic: {group.replace(/^\d+\s*/, "")} ▾</option>
          {props.topics.filter((t) => t !== group).map((t) => <option key={t} value={t}>move to {t.replace(/^\d+\s*/, "")}</option>)}
          <option value="+">move to a new topic…</option>
        </select>
        <span className="flex items-center gap-1">
          {props.nav.prev ? <Link href={props.nav.prev} className="btn px-2 py-1" aria-label="Previous problem">← prev</Link> : <span className="btn px-2 py-1 opacity-40">← prev</span>}
          <span className="px-1 font-mono text-xs tabular-nums text-muted">
            {props.nav.random && <span className="tag mr-1.5">{props.nav.unsolved ? "shuffle · unsolved" : "shuffle"}</span>}
            {props.nav.pos} / {props.nav.total}
          </span>
          {props.nav.next ? <Link href={props.nav.next} className="btn px-2 py-1" aria-label="Next problem">next →</Link> : <span className="btn px-2 py-1 opacity-40">next →</span>}
        </span>
        <span className="flex-1" />
        {status === "solved" && <ReviewControls path={path} review={props.review} today={props.today} />}
        <Link href={`/ai?tab=interview&kind=coding&problem=${encodeURIComponent(path)}`} className="btn">Mock interview</Link>
        <button onClick={toggleSolved} className={`btn ${status === "solved" ? "border-easy text-easy" : ""}`}>
          {status === "solved" ? "✓ Solved" : "Mark solved"}
        </button>
      </div>
      <div ref={row} className="flex min-h-0 flex-1 max-lg:flex-col max-lg:gap-3">
        <section className="card flex min-h-0 flex-col lg:w-[var(--left)] lg:shrink-0" style={{ "--left": `${layout.left}%` } as React.CSSProperties}>
          <div className="flex gap-1 border-b border-border p-2" role="tablist">
            {(["question", "solution", "notes", "tests"] as Tab[]).map((t) => (
              <button key={t} role="tab" aria-selected={tab === t} onClick={() => setTab(t)} className={`px-3 py-1 font-mono text-xs capitalize ${tab === t ? "bg-fg text-panel" : "text-muted hover:text-fg"}`}>
                {t}
              </button>
            ))}
          </div>
          <div className={`min-h-0 flex-1 overflow-y-auto ${tab === "tests" ? "" : "p-4"}`}>
            {tab === "tests" && (
              <TestsPanel names={props.names} cases={cases} examples={props.examples} onChange={setCases} run={run} busy={!!busy} onRun={runCases} />
            )}
            {tab === "question" && <Markdown>{props.question}</Markdown>}
            {tab === "solution" && <Markdown>{props.solution || "_No solution file._"}</Markdown>}
            {/* Kept mounted so the drawing and its pending save survive switching tabs. */}
            <div className={`space-y-4 ${tab === "notes" ? "" : "hidden"}`}>
                <textarea
                  className="input min-h-48 font-mono"
                  value={notes}
                  placeholder="Your notes (saved to notes.md and shown in the dashboard cheat sheet)"
                  onChange={(e) => setNotes(e.target.value)}
                  onBlur={() => putFile(`${path}/notes.md`, notes)}
                />
                <SketchPad path={path} initial={props.drawing} />
            </div>
          </div>
        </section>
        <Divider
          dir="x"
          onMove={(e) => { const r = row.current!.getBoundingClientRect(); resize({ left: ((e.clientX - r.left) / r.width) * 100 }); }}
          onStep={(d) => resize({ left: layout.left + d * 2 })}
          onReset={() => resize({ left: LAYOUT.left })}
        />
        <section ref={right} className="flex min-h-0 min-w-0 flex-1 flex-col gap-3">
          <div className="card flex min-h-48 flex-1 flex-col overflow-hidden">
            <div className="flex items-center gap-1 border-b border-border p-2" role="radiogroup" aria-label="Editor mode">
              {([["doc", "Doc"], ["ide", "IDE"]] as const).map(([m, label]) => (
                <button key={m} role="radio" aria-checked={mode === m} onClick={() => switchMode(m)} className={`px-3 py-1 font-mono text-xs ${mode === m ? "bg-fg text-panel" : "text-muted hover:text-fg"}`}>
                  {label}
                </button>
              ))}
              {props.langs.length > 1 && (
                <span className="ml-2 flex shrink-0 items-center gap-1 border-l border-border pl-2" role="radiogroup" aria-label="Language">
                  {props.langs.map((l) => (
                    <button key={l} role="radio" aria-checked={lang === l} onClick={() => switchLang(l)} className={`whitespace-nowrap px-3 py-1 font-mono text-xs ${lang === l ? "bg-fg text-panel" : "text-muted hover:text-fg"}`}>{LANG_LABEL[l]}</button>
                  ))}
                </span>
              )}
              <span className="ml-2 truncate font-mono text-[11px] text-muted">
                {mode === "doc" ? "blank sheet: no highlighting, no autocomplete, like a Google interview" : "syntax highlighting, still no autocomplete"}
              </span>
            </div>
            <div className="min-h-0 flex-1">
              <Editor
                key={`${mode}-${lang}`}
                language={mode === "doc" ? docLanguage(lang) : lang}
                beforeMount={registerDocLanguages}
                value={code}
                onChange={(v) => setCode(v ?? "")}
                theme={mode === "doc" ? "light" : dark ? "vs-dark" : "light"}
                options={mode === "doc" ? DOC : NO_ASSIST}
              />
            </div>
          </div>
          <div className="flex flex-wrap gap-2">
            <button className="btn" disabled={!!busy} onClick={runCases} title="Run your test cases">▶ Run</button>
            {area === "leetcode" && <span className="inline-flex items-center border border-border bg-panel">
              <label className={`flex items-center gap-1 px-2 font-mono text-xs text-muted ${mark("time")}`}>Time<input className="w-14 bg-transparent py-1.5 text-fg outline-none" value={myTime} onChange={(e) => setMyTime(e.target.value)} placeholder="O(n)" aria-label="Your solution's time complexity" /></label>
              <label className={`flex items-center gap-1 border-l border-border px-2 font-mono text-xs text-muted ${mark("space")}`}>Space<input className="w-14 bg-transparent py-1.5 text-fg outline-none" value={mySpace} onChange={(e) => setMySpace(e.target.value)} placeholder="O(1)" aria-label="Your solution's space complexity" /></label>
            </span>}
            <button className="btn-primary" disabled={!!busy} onClick={() => submitCode()} title="Run the hidden tests; passing marks the problem solved. Fill in Time/Space (optional) to have Claude check them">Submit</button>
            <button className="btn" disabled={!!busy} onClick={hint}>Hint</button>
            {area === "leetcode" && <button className="btn" disabled={!!busy} onClick={complexity} title="Claude works out the time and space complexity of your current code">Complexity</button>}
            <button className="btn" disabled={!!busy} onClick={() => confirm("Reset code to the starter template?") && setCode(props.starters[lang])}>Reset</button>
          </div>
          {(busy || submit || coach) && (
            <>
            <Divider
              dir="y"
              onMove={(e) => resize({ bottom: right.current!.getBoundingClientRect().bottom - e.clientY })}
              onStep={(d) => resize({ bottom: layout.bottom - d * 20 })}
              onReset={() => resize({ bottom: LAYOUT.bottom })}
            />
            <div className="card -mt-3 shrink-0 space-y-3 overflow-y-auto p-3" style={{ height: layout.bottom }}>
              {busy && <p className="text-sm text-muted" role="status">{busy}</p>}
              {submit && (
                <div className="space-y-1">
                  <div className={`font-display text-lg font-medium ${submit.ok ? "text-easy" : "text-hard"}`}>{submit.ok ? "Accepted" : "Not accepted"}</div>
                  <pre className="whitespace-pre-wrap font-mono text-xs">{submit.output}</pre>
                  {submit.complexity && (submit.complexity.error ? (
                    <p className="font-mono text-xs text-medium">Couldn&apos;t check your complexity: {submit.complexity.error}</p>
                  ) : (
                    <div className="space-y-0.5 border-t border-border pt-2 text-sm">
                      {(["time", "space"] as const).map((k) => {
                        const ok = submit.complexity![k === "time" ? "timeOk" : "spaceOk"];
                        if (ok === null) return null; // you didn't give this one
                        return (
                          <div key={k} className={ok ? "text-easy" : "text-hard"}>
                            {ok ? "✓" : "✗"} {k === "time" ? "Time" : "Space"}: you said <code className="font-mono">{submit.complexity!.claimed?.[k]}</code>{ok ? "" : <> · it&apos;s <code className="font-mono">{submit.complexity![k]}</code></>}
                          </div>
                        );
                      })}
                      <p className="text-xs text-muted">{submit.complexity.why}</p>
                    </div>
                  ))}
                  {!submit.ok && area === "leetcode" && ( // ML Coding ships hand-checked tests; the generator is LeetCode-specific
                    <button className="font-mono text-[11px] text-muted hover:text-fg" onClick={() => submitCode(true)} disabled={!!busy}>hidden tests look wrong? regenerate them</button>
                  )}
                </div>
              )}
              {coach && <Markdown>{coach}</Markdown>}
            </div>
            </>
          )}
        </section>
      </div>
    </div>
  );
}
