"use client";
import Editor from "@monaco-editor/react";
import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import { NO_ASSIST } from "./editor-options";
import Markdown from "./Markdown";
import { isDark } from "./ThemeToggle";
import { Divider } from "./Workspace";
import { api } from "@/lib/client";

type Tab = "task" | "solution";
// Panel sizes in px (task panel, file list, AI assistant, test output); dragged by the dividers, remembered in this browser.
const LAYOUT = { left: 360, files: 190, ai: 320, bottom: 200 };
type Msg = { role: "assistant" | "you"; text: string };
const languageOf = (f: string) => (f.endsWith(".py") ? "python" : f.endsWith(".md") ? "markdown" : f.endsWith(".json") ? "json" : "plaintext");
const changedFrom = (base: Record<string, string>, files: Record<string, string>) => Object.fromEntries(Object.entries(files).filter(([f, c]) => base[f] !== c));
const validName = (f: string) => /^(?!\/)(?!.*(^|\/)\.)[\w./-]+$/.test(f) && !f.split("/").includes("..") && !f.endsWith("/"); // same rule as the server
const dirOf = (f: string) => f.split("/").slice(0, -1).join("/");

type Tree = { dirs: Record<string, Tree>; files: string[] };
function treeOf(paths: string[]): Tree {
  const root: Tree = { dirs: {}, files: [] };
  for (const p of paths) {
    const parts = p.split("/");
    let t = root;
    for (const d of parts.slice(0, -1)) t = t.dirs[d] ??= { dirs: {}, files: [] };
    t.files.push(p);
  }
  return root;
}

/** The repo as a folder tree: folders first (click to fold), changed files marked •, new files +. */
function FileTree({ tree, depth = 0, prefix = "", open, onOpen, folded, onFold, mark }: {
  tree: Tree; depth?: number; prefix?: string; open: string; onOpen: (f: string) => void;
  folded: Set<string>; onFold: (d: string) => void; mark: (f: string) => string;
}) {
  const pad = { paddingLeft: 12 + depth * 14 };
  return (
    <>
      {Object.keys(tree.dirs).sort().map((d) => {
        const dir = prefix + d;
        return (
          <div key={dir}>
            <button onClick={() => onFold(dir)} style={pad} className="flex w-full items-center gap-1 py-1 pr-3 text-left text-fg hover:bg-bg" aria-expanded={!folded.has(dir)}>
              <span className="w-3 text-muted">{folded.has(dir) ? "▸" : "▾"}</span>{d}/
            </button>
            {!folded.has(dir) && <FileTree tree={tree.dirs[d]} depth={depth + 1} prefix={dir + "/"} open={open} onOpen={onOpen} folded={folded} onFold={onFold} mark={mark} />}
          </div>
        );
      })}
      {[...tree.files].sort().map((f) => (
        <button key={f} onClick={() => onOpen(f)} title={f} style={{ paddingLeft: pad.paddingLeft + 16 }} className={`block w-full truncate py-1 pr-3 text-left ${f === open ? "bg-fg text-panel" : "text-muted hover:text-fg"}`}>
          {f.split("/").at(-1)}{mark(f) && <span className={f === open ? "" : "text-accent"}> {mark(f)}</span>}
        </button>
      ))}
    </>
  );
}

/** A repo problem: the files, an editor, Run (visible tests) / Submit (plus hidden tests), and an AI assistant that only reads. */
export default function RepoWorkspace(props: {
  path: string; question: string; repo: Record<string, string>; files: Record<string, string>; // files: the repo with your changes
  explanation: string; fixed: Record<string, string>; status?: string;
}) {
  const { path, repo } = props;
  const [files, setFiles] = useState<Record<string, string>>(props.files);
  const names = Object.keys(files).sort();
  const [open, setOpen] = useState(names.find((f) => !f.startsWith("tests/") && !f.endsWith("__init__.py")) ?? names[0] ?? "");
  const [folded, setFolded] = useState<Set<string>>(new Set());
  const fold = (d: string) => setFolded((s) => { const n = new Set(s); if (n.has(d)) n.delete(d); else n.add(d); return n; });
  const mark = (f: string) => (!(f in repo) ? "+" : files[f] !== repo[f] ? "•" : "");
  const dirty = JSON.stringify(files) !== JSON.stringify(repo);
  function newFile() {
    const name = prompt("New file path (folders are created as needed)", open ? `${dirOf(open)}/`.replace(/^\//, "") : "")?.trim();
    if (!name) return;
    if (!validName(name)) return alert("Use a relative path like inventory/helpers.py (letters, digits, _ - . and /).");
    if (!(name in files)) setFiles((fs) => ({ ...fs, [name]: "" }));
    setOpen(name);
  }
  function deleteFile() {
    if (!open || !confirm(`Delete ${open}?${open in repo ? " (Reset all files brings it back.)" : ""}`)) return;
    const rest = names.filter((f) => f !== open);
    setFiles((fs) => Object.fromEntries(Object.entries(fs).filter(([f]) => f !== open)));
    setOpen(rest.find((f) => dirOf(f) === dirOf(open)) ?? rest[0] ?? "");
  }
  const [tab, setTab] = useState<Tab>("task");
  const [output, setOutput] = useState<{ ok?: boolean; text: string; submit?: boolean } | null>(null);
  const [busy, setBusy] = useState<string | null>(null);
  const [status, setStatus] = useState(props.status);
  const [showSolution, setShowSolution] = useState(false);
  const [layout, setLayout] = useState(LAYOUT);
  const row = useRef<HTMLDivElement>(null);
  const main = useRef<HTMLElement>(null);
  useEffect(() => {
    try { setLayout((l) => ({ ...l, ...JSON.parse(localStorage.getItem("repo-layout") ?? "{}") })); } catch {}
  }, []);
  const resize = (next: Partial<typeof LAYOUT>) => setLayout((l) => {
    const v = { ...l, ...next };
    v.left = Math.min(900, Math.max(240, v.left));
    v.files = Math.min(400, Math.max(120, v.files));
    v.ai = Math.min(900, Math.max(260, v.ai));
    v.bottom = Math.min((main.current?.clientHeight ?? 800) - 160, Math.max(80, v.bottom));
    try { localStorage.setItem("repo-layout", JSON.stringify(v)); } catch {}
    return v;
  });
  const [dark, setDark] = useState(false);
  useEffect(() => {
    const update = () => setDark(isDark());
    update();
    window.addEventListener("prep-theme", update);
    return () => window.removeEventListener("prep-theme", update);
  }, []);

  // Your changes (edited, added and deleted files) are saved to work.json a second after you stop.
  const saved = useRef(JSON.stringify(props.files));
  useEffect(() => {
    const now = JSON.stringify(files);
    if (now === saved.current) return;
    const t = setTimeout(() => api("/api/repo", { action: "save", path, files }).then(() => { saved.current = now; }, () => {}), 1000);
    return () => clearTimeout(t);
  }, [files, path]);

  async function test(action: "run" | "submit") {
    setBusy(action === "run" ? "Running the tests…" : "Running the tests and the hidden tests…");
    try {
      const r = await api("/api/repo", { action, path, files });
      saved.current = JSON.stringify(files);
      setOutput({ ok: r.ok, text: r.output, submit: action === "submit" });
      if (action === "submit") setStatus((s) => (r.ok ? "solved" : s === "solved" ? s : "attempted"));
    } catch (e) {
      setOutput({ ok: false, text: (e as Error).message });
    } finally {
      setBusy(null);
    }
  }

  async function resetAll() {
    if (!confirm("Undo all your changes and go back to the original repo?")) return;
    await api("/api/repo", { action: "reset", path });
    saved.current = JSON.stringify(repo);
    setFiles({ ...repo });
    setOutput(null);
  }

  // The assistant gets every file on the first message, then only the files changed since it last saw them.
  const [msgs, setMsgs] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState<string | null>(null);
  const seen = useRef<Record<string, string>>({});
  const chat = useRef<HTMLDivElement>(null);
  // Scroll the chat itself (scrollIntoView would scroll the whole page too).
  useEffect(() => { chat.current?.scrollTo({ top: chat.current.scrollHeight, behavior: "smooth" }); }, [msgs, busy]);
  async function ask() {
    const message = input.trim();
    if (!message || busy) return;
    setInput("");
    setMsgs((m) => [...m, { role: "you", text: message }]);
    setBusy("The assistant is thinking…");
    try {
      // Deleted files go along as empty, so the assistant knows they're gone.
      const gone = Object.fromEntries(Object.keys(seen.current).filter((f) => !(f in files)).map((f) => [f, "(deleted)"]));
      const changed = sessionId ? { ...changedFrom(seen.current, files), ...gone } : {};
      const r = await api("/api/repo", { action: "assistant", path, message, sessionId, changed, files });
      seen.current = { ...files };
      setSessionId(r.sessionId);
      setMsgs((m) => [...m, { role: "assistant", text: r.text }]);
    } catch (e) {
      setMsgs((m) => [...m, { role: "assistant", text: `_${(e as Error).message}_` }]);
    } finally {
      setBusy(null);
    }
  }

  const title = props.question.match(/^# (.+)$/m)?.[1] ?? path.split("/").at(-1);
  return (
    <div className="mx-auto flex h-[calc(100vh-7rem)] max-w-[1400px] flex-col gap-3">
      <div className="flex flex-wrap items-center gap-2">
        <Link href={`/repo-debugging?topic=${encodeURIComponent(path.split("/")[1])}`} className="text-sm text-muted hover:text-fg">← {path.split("/")[1].replace(/^\d+\s*/, "")}</Link>
        <h1 className="ml-2 mr-auto font-medium">{title}</h1>
        {status === "solved" && <span className="btn border-easy text-easy">✓ Solved</span>}
        <button className="btn" onClick={resetAll} disabled={!!busy || !dirty}>Reset all files</button>
      </div>
      <div ref={row} className="flex min-h-0 flex-1 max-lg:flex-col max-lg:gap-3">
        <section className="card flex min-h-0 flex-col lg:w-[var(--w)] lg:shrink-0" style={{ "--w": `${layout.left}px` } as React.CSSProperties}>
          <div className="flex gap-1 border-b border-border p-2" role="tablist">
            {(["task", "solution"] as Tab[]).map((t) => (
              <button key={t} role="tab" aria-selected={tab === t} onClick={() => setTab(t)} className={`px-3 py-1 font-mono text-xs capitalize ${tab === t ? "bg-fg text-panel" : "text-muted hover:text-fg"}`}>
                {t}
              </button>
            ))}
          </div>
          <div className="min-h-0 flex-1 overflow-y-auto p-4">
            {tab === "task" && <Markdown>{props.question.replace(/^---[\s\S]*?---\n/, "")}</Markdown>}
            {tab === "solution" && (showSolution ? (
              <div className="space-y-4">
                <Markdown>{props.explanation || "_No solution file._"}</Markdown>
                {Object.entries(props.fixed).map(([f, c]) => (
                  <div key={f}>
                    <p className="mb-1 font-mono text-xs text-muted">{f} (fixed)</p>
                    <Markdown>{"```python\n" + c.replace(/\n$/, "") + "\n```"}</Markdown>
                  </div>
                ))}
              </div>
            ) : (
              <button className="btn" onClick={() => setShowSolution(true)}>Show the solution</button>
            ))}
          </div>
        </section>
        <Divider dir="x" label="Drag to resize the task panel" onMove={(e) => resize({ left: e.clientX - (row.current?.getBoundingClientRect().left ?? 0) })} onStep={(d) => resize({ left: layout.left + d * 20 })} onReset={() => resize({ left: LAYOUT.left })} />
        <section ref={main} className="card flex min-h-0 min-w-0 flex-1 flex-col max-lg:h-[80vh]">
          <div className="flex min-h-0 flex-1">
            <nav className="flex shrink-0 flex-col border-r border-border font-mono text-xs" style={{ width: layout.files }} aria-label="Files">
              <div className="flex items-center gap-1 border-b border-border px-3 py-1.5 text-muted">
                <span className="mr-auto uppercase tracking-wide">Files</span>
                <button className="hover:text-fg" onClick={newFile} title="New file">+ new</button>
              </div>
              <div className="min-h-0 flex-1 overflow-y-auto py-1">
                <FileTree tree={treeOf(names)} open={open} onOpen={setOpen} folded={folded} onFold={fold} mark={mark} />
              </div>
            </nav>
            <Divider dir="x" label="Drag to resize the file list" onMove={(e) => resize({ files: e.clientX - (main.current?.getBoundingClientRect().left ?? 0) })} onStep={(d) => resize({ files: layout.files + d * 20 })} onReset={() => resize({ files: LAYOUT.files })} />
            <div className="flex min-w-0 flex-1 flex-col">
              <div className="flex items-center gap-2 border-b border-border px-3 py-1.5 font-mono text-xs text-muted">
                <span className="mr-auto truncate">{open}</span>
                {open in repo && files[open] !== repo[open] && <button className="hover:text-fg" onClick={() => setFiles((fs) => ({ ...fs, [open]: repo[open] }))}>undo changes</button>}
                {open && <button className="hover:text-hard" onClick={deleteFile}>delete file</button>}
              </div>
              <div className="min-h-0 flex-1">
                {open in files ? <Editor key={open} path={open} language={languageOf(open)} value={files[open]} onChange={(v) => setFiles((fs) => ({ ...fs, [open]: v ?? "" }))} theme={dark ? "vs-dark" : "light"} options={NO_ASSIST} /> : <p className="p-4 text-sm text-muted">No file open. Pick one on the left, or make a new one.</p>}
              </div>
            </div>
          </div>
          <Divider dir="y" label="Drag to resize the test output" onMove={(e) => resize({ bottom: (main.current?.getBoundingClientRect().bottom ?? 0) - 49 - e.clientY })} onStep={(d) => resize({ bottom: layout.bottom - d * 20 })} onReset={() => resize({ bottom: LAYOUT.bottom })} />
          <div className="shrink-0 overflow-y-auto border-t border-border p-3" style={{ height: layout.bottom }}>
            {busy && !busy.startsWith("The assistant") ? <p className="text-sm text-muted">{busy}</p> : output ? (
              <>
                <p className={`mb-2 font-medium ${output.ok ? "text-easy" : "text-hard"}`}>{output.ok ? (output.submit ? "Accepted: every test passes" : "All visible tests pass") : "Some tests fail"}</p>
                <pre className="whitespace-pre-wrap font-mono text-xs">{output.text}</pre>
              </>
            ) : <p className="text-sm text-muted">Run runs the tests in tests/. Submit also runs the hidden tests and marks the problem solved when everything passes.</p>}
          </div>
          <div className="flex gap-2 border-t border-border p-2">
            <button className="btn" onClick={() => test("run")} disabled={!!busy}>▶ Run tests</button>
            <button className="btn-primary" onClick={() => test("submit")} disabled={!!busy}>Submit</button>
          </div>
        </section>
        <Divider dir="x" label="Drag to resize the AI assistant" onMove={(e) => resize({ ai: (row.current?.getBoundingClientRect().right ?? 0) - e.clientX })} onStep={(d) => resize({ ai: layout.ai - d * 20 })} onReset={() => resize({ ai: LAYOUT.ai })} />
        <section className="card flex min-h-0 flex-col p-3 lg:w-[var(--w)] lg:shrink-0 max-lg:h-[60vh]" style={{ "--w": `${layout.ai}px` } as React.CSSProperties} aria-label="AI assistant">
          <h2 className="font-mono text-xs uppercase tracking-wide">AI assistant</h2>
          <p className="mb-2 text-xs text-muted">Reads every file (with your edits) but can&apos;t edit them, like the chat in an AI-enabled interview. How you use it is part of the interview.</p>
          <div ref={chat} className="min-h-0 flex-1 space-y-3 overflow-y-auto">
            {msgs.map((m, i) => (
              <div key={i} className={m.role === "you" ? "ml-8 bg-bg p-2 text-sm" : "text-sm"}>
                {m.role === "you" ? <p className="whitespace-pre-wrap">{m.text}</p> : <Markdown>{m.text}</Markdown>}
              </div>
            ))}
            {busy?.startsWith("The assistant") && <p className="text-sm text-muted">{busy}</p>}
          </div>
          <textarea
            className="input mt-2 min-h-20 text-sm"
            value={input}
            placeholder="Ask the assistant. Enter sends, Shift+Enter adds a line."
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); ask(); } }}
          />
        </section>
      </div>
    </div>
  );
}
