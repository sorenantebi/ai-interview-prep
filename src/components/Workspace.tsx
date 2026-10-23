"use client";
import Editor, { type EditorProps } from "@monaco-editor/react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import Markdown from "./Markdown";
import ReviewControls from "./ReviewControls";
import SketchPad, { type Stroke } from "./SketchPad";
import { api, putFile } from "@/lib/client";
import type { Review } from "@/lib/content";
import type { CaseResult } from "@/lib/run";

// No autocomplete, hints or auto-closing in either mode: you type every character, like in a real interview.
const NO_ASSIST: EditorProps["options"] = {
  minimap: { enabled: false }, fontSize: 14, fontFamily: "var(--font-jetbrains), monospace", scrollBeyondLastLine: false,
  quickSuggestions: false, suggestOnTriggerCharacters: false, wordBasedSuggestions: "off", parameterHints: { enabled: false },
  acceptSuggestionOnEnter: "off", tabCompletion: "off", snippetSuggestions: "none", inlineSuggest: { enabled: false },
  hover: { enabled: "off" }, autoClosingBrackets: "never", autoClosingQuotes: "never", autoSurround: "never", formatOnType: false,
  occurrencesHighlight: "off", selectionHighlight: false, codeLens: false,
};
// "Doc" = Google-interview style blank white sheet: no highlighting, line numbers, guides or auto-indent.
const DOC: EditorProps["options"] = {
  ...NO_ASSIST, lineNumbers: "off", glyphMargin: false, folding: false, lineDecorationsWidth: 16, renderLineHighlight: "none",
  guides: { indentation: false, bracketPairs: false }, matchBrackets: "never", autoIndent: "none", renderWhitespace: "none",
  padding: { top: 16 }, wordWrap: "on",
};

type Tab = "question" | "solution" | "notes" | "tests";
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
      {view === "cases" ? (
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
                    {box("Input", r.input.map((v, n) => `${names[n] ?? `arg${n + 1}`} = ${v}`).join("\n"))}
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
  path: string; question: string; solution: string; attempt: string | null; starter: string;
  names: string[]; cases: string[][]; examples: string[][]; notes: string; drawing: Stroke[]; status?: string; review?: Review; today: string;
  nav: { prev: string | null; next: string | null; pos: number; total: number; random: boolean; unsolved: boolean };
}) {
  const { path } = props;
  const [tab, setTab] = useState<Tab>((useSearchParams().get("tab") as Tab) ?? "question");
  const [code, setCode] = useState(props.attempt ?? props.starter);
  const [notes, setNotes] = useState(props.notes);
  const [cases, setCases] = useState(props.cases);
  const [run, setRun] = useState<Run | null>(null);
  const [submit, setSubmit] = useState<{ ok: boolean; output: string } | null>(null);
  const [coach, setCoach] = useState("");
  const [busy, setBusy] = useState<string | null>(null);
  const [status, setStatus] = useState(props.status);
  const dark = useRef(false);
  if (typeof window !== "undefined") dark.current = window.matchMedia("(prefers-color-scheme: dark)").matches;
  const [mode, setMode] = useState<"doc" | "ide">("doc");
  useEffect(() => {
    try { if (localStorage.getItem("editorMode") === "ide") setMode("ide"); } catch {}
  }, []);
  const switchMode = (m: "doc" | "ide") => {
    setMode(m);
    try { localStorage.setItem("editorMode", m); } catch {}
  };

  // Autosave attempt.py and your test cases one second after you stop typing.
  useEffect(() => {
    if (code === (props.attempt ?? props.starter)) return;
    const t = setTimeout(() => putFile(`${path}/attempt.py`, code), 1000);
    return () => clearTimeout(t);
  }, [code, path, props.attempt, props.starter]);
  useEffect(() => {
    if (cases === props.cases) return;
    const t = setTimeout(() => putFile(`${path}/testcases.json`, JSON.stringify({ names: props.names, cases }, null, 2)), 1000);
    return () => clearTimeout(t);
  }, [cases, path, props.cases, props.names]);

  async function runCases() {
    setTab("tests");
    setBusy("Running your test cases…");
    try {
      setRun(await api("/api/run", { path, code, mode: "run", cases, names: props.names }));
    } catch (e) {
      setRun({ error: (e as Error).message });
    } finally {
      setBusy(null);
    }
  }

  async function submitCode(regenerate = false) {
    setBusy(regenerate ? "Claude is writing new hidden tests…" : "Submitting (the first submit asks Claude to write hidden tests)…");
    setSubmit(null);
    try {
      const r = await api("/api/run", { path, code, mode: "submit", regenerate });
      setSubmit(r);
      setStatus((s) => (r.ok ? "solved" : s === "solved" ? s : "attempted"));
    } catch (e) {
      setSubmit({ ok: false, output: (e as Error).message });
    } finally {
      setBusy(null);
    }
  }

  async function ask(kind: "hint" | "review") {
    setBusy(kind === "hint" ? "Asking for a hint…" : "Reviewing…");
    try {
      setCoach((await api("/api/claude", { action: "hint", mode: kind, path, code, output: submit?.output ?? "" })).text);
    } catch (e) {
      setCoach("**Error:** " + (e as Error).message);
    } finally {
      setBusy(null);
    }
  }

  async function toggleSolved() {
    const next = status === "solved" ? null : "solved";
    await api("/api/progress", { path, status: next });
    setStatus(next ?? undefined);
  }

  const group = path.split("/")[1];
  return (
    <div className="flex h-[calc(100vh-7.5rem)] flex-col gap-3 max-lg:h-auto">
      <div className="flex flex-wrap items-center gap-2 text-sm">
        {props.nav.random ? (
          <Link href="/leetcode" className="text-muted hover:text-fg">← exit shuffle</Link>
        ) : (
          <Link href={`/leetcode?topic=${encodeURIComponent(group)}`} className="text-muted hover:text-fg">← {group.replace(/^\d+\s*/, "")}</Link>
        )}
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
      <div className="grid min-h-0 flex-1 gap-3 lg:grid-cols-2">
        <section className="card flex min-h-0 flex-col">
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
            {tab === "notes" && (
              <div className="space-y-4">
                <textarea
                  className="input min-h-48 font-mono"
                  value={notes}
                  placeholder="Your notes (saved to notes.md and shown in the dashboard cheat sheet)"
                  onChange={(e) => setNotes(e.target.value)}
                  onBlur={() => putFile(`${path}/notes.md`, notes)}
                />
                <SketchPad path={path} initial={props.drawing} />
              </div>
            )}
          </div>
        </section>
        <section className="flex min-h-0 flex-col gap-3">
          <div className="card flex min-h-80 flex-1 flex-col overflow-hidden">
            <div className="flex items-center gap-1 border-b border-border p-2" role="radiogroup" aria-label="Editor mode">
              {([["doc", "Doc"], ["ide", "IDE"]] as const).map(([m, label]) => (
                <button key={m} role="radio" aria-checked={mode === m} onClick={() => switchMode(m)} className={`px-3 py-1 font-mono text-xs ${mode === m ? "bg-fg text-panel" : "text-muted hover:text-fg"}`}>
                  {label}
                </button>
              ))}
              <span className="ml-2 truncate font-mono text-[11px] text-muted">
                {mode === "doc" ? "blank sheet: no highlighting, no autocomplete, like a Google interview" : "syntax highlighting, still no autocomplete"}
              </span>
            </div>
            <div className="min-h-0 flex-1">
              <Editor
                key={mode}
                language={mode === "doc" ? "plaintext" : "python"}
                value={code}
                onChange={(v) => setCode(v ?? "")}
                theme={mode === "doc" ? "light" : dark.current ? "vs-dark" : "light"}
                options={mode === "doc" ? DOC : NO_ASSIST}
              />
            </div>
          </div>
          <div className="flex flex-wrap gap-2">
            <button className="btn" disabled={!!busy} onClick={runCases} title="Run your test cases">▶ Run</button>
            <button className="btn-primary" disabled={!!busy} onClick={() => submitCode()} title="Run the hidden tests; passing marks the problem solved">Submit</button>
            <button className="btn" disabled={!!busy} onClick={() => ask("hint")}>Hint</button>
            <button className="btn" disabled={!!busy} onClick={() => ask("review")}>Review my code</button>
            <button className="btn" disabled={!!busy} onClick={() => confirm("Reset code to the starter template?") && setCode(props.starter)}>Reset</button>
          </div>
          {(busy || submit || coach) && (
            <div className="card max-h-72 space-y-3 overflow-y-auto p-3">
              {busy && <p className="text-sm text-muted" role="status">{busy}</p>}
              {submit && (
                <div className="space-y-1">
                  <div className={`font-display text-lg font-medium ${submit.ok ? "text-easy" : "text-hard"}`}>{submit.ok ? "Accepted" : "Not accepted"}</div>
                  <pre className="whitespace-pre-wrap font-mono text-xs">{submit.output}</pre>
                  {!submit.ok && (
                    <button className="font-mono text-[11px] text-muted hover:text-fg" onClick={() => submitCode(true)} disabled={!!busy}>hidden tests look wrong? regenerate them</button>
                  )}
                </div>
              )}
              {coach && <Markdown>{coach}</Markdown>}
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
