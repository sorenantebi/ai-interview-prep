"use client";
import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import Markdown from "./Markdown";
import { problemHref } from "./ProblemList";
import { api, putFile } from "@/lib/client";
import { timerCommand } from "./Timer";
import type { TreeNode } from "@/lib/content";

type Tab = "link" | "generate" | "system-design" | "interview";
const TABS: [Tab, string][] = [["link", "Add LeetCode from link"], ["generate", "Generate LeetCode problem"], ["system-design", "Add system design"], ["interview", "Mock interview"]];

const groupsOf = (tree: TreeNode[], area: string) => tree.find((n) => n.path === area)?.children?.filter((n) => n.dir).map((n) => n.name) ?? [];
const problemsOf = (tree: TreeNode[], area: string) =>
  (tree.find((n) => n.path === area)?.children ?? []).flatMap((g) => (g.children ?? []).filter((p) => p.children?.some((f) => f.name === "question.md")).map((p) => p.path));

/** Topic picker: existing folders, or type a new name to create one. */
function GroupInput({ id, groups, value, onChange }: { id: string; groups: string[]; value: string; onChange: (v: string) => void }) {
  return (
    <>
      <input id={id} className="input" list={`${id}-list`} value={value} onChange={(e) => onChange(e.target.value)} placeholder="Pick a topic or type a new one" required />
      <datalist id={`${id}-list`}>{groups.map((g) => <option key={g} value={g} />)}</datalist>
    </>
  );
}

function Creator({ tab, tree, onCreated }: { tab: Exclude<Tab, "interview">; tree: TreeNode[]; onCreated: () => void }) {
  const area = tab === "system-design" ? "system-design" : "leetcode";
  const [group, setGroup] = useState("");
  const [text, setText] = useState("");
  const [difficulty, setDifficulty] = useState("Medium");
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<{ path?: string; error?: string }>({});

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);
    setResult({});
    const body =
      tab === "link" ? { action: "add-leetcode", group, url: text }
      : tab === "generate" ? { action: "generate-leetcode", group, difficulty, idea: text }
      : { action: "system-design", group, request: text };
    try {
      setResult({ path: (await api("/api/claude", body)).path });
      setText("");
      onCreated();
    } catch (err) {
      setResult({ error: (err as Error).message });
    } finally {
      setBusy(false);
    }
  }

  const promptFile = { link: "add-leetcode-from-link", generate: "generate-leetcode", "system-design": "system-design" }[tab];
  return (
    <form onSubmit={submit} className="card max-w-2xl space-y-4 p-5">
      <label className="block space-y-1 text-sm">
        <span className="font-medium">{tab === "system-design" ? "Category" : "Topic"}</span>
        <GroupInput id={`${tab}-group`} groups={groupsOf(tree, area)} value={group} onChange={setGroup} />
      </label>
      {tab === "link" && (
        <label className="block space-y-1 text-sm">
          <span className="font-medium">LeetCode or NeetCode URL</span>
          <input className="input" type="url" required value={text} onChange={(e) => setText(e.target.value)} placeholder="https://leetcode.com/problems/two-sum/" />
        </label>
      )}
      {tab === "generate" && (
        <>
          <label className="block space-y-1 text-sm">
            <span className="font-medium">Difficulty</span>
            <select className="input" value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
              {["Easy", "Medium", "Hard"].map((d) => <option key={d}>{d}</option>)}
            </select>
          </label>
          <label className="block space-y-1 text-sm">
            <span className="font-medium">Extra instructions (optional)</span>
            <textarea className="input" rows={3} value={text} onChange={(e) => setText(e.target.value)} placeholder="e.g. a sliding window twist on a real-world logging scenario" />
          </label>
        </>
      )}
      {tab === "system-design" && (
        <label className="block space-y-1 text-sm">
          <span className="font-medium">Problem or idea</span>
          <textarea className="input" rows={3} required value={text} onChange={(e) => setText(e.target.value)} placeholder="e.g. Design Spotify, or: a system that dedupes uploaded photos at scale" />
        </label>
      )}
      <div className="flex items-center gap-3">
        <button className="btn-primary" disabled={busy}>{busy ? "Claude is writing…" : "Create"}</button>
        <Link href={`/files?path=${encodeURIComponent(`prompts/${promptFile}.md`)}`} className="text-xs text-muted hover:text-fg">Edit prompt</Link>
      </div>
      {busy && <p className="text-sm text-muted" role="status">This usually takes 30–90 seconds.</p>}
      {result.path && <p className="text-sm text-easy">Created: <Link className="underline" href={problemHref(result.path)}>{result.path}</Link></p>}
      {result.error && <pre className="whitespace-pre-wrap text-sm text-hard">{result.error}</pre>}
    </form>
  );
}

type Msg = { role: "interviewer" | "you"; text: string };
const INTERVIEW_MINUTES = 45;

function Interview({ tree, initialKind, initialProblem }: { tree: TreeNode[]; initialKind: string; initialProblem: string }) {
  const [kind, setKind] = useState(initialKind === "system-design" ? "system-design" : "coding");
  const [problem, setProblem] = useState(initialProblem);
  const [theme, setTheme] = useState("");
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [msgs, setMsgs] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [saved, setSaved] = useState("");
  const bottom = useRef<HTMLDivElement>(null);
  useEffect(() => bottom.current?.scrollIntoView({ behavior: "smooth" }), [msgs, busy]);

  const options = problemsOf(tree, kind === "coding" ? "leetcode" : "system-design");

  async function call(body: object, mine?: string) {
    setBusy(true);
    setError("");
    if (mine) setMsgs((m) => [...m, { role: "you", text: mine }]);
    try {
      const r = await api("/api/claude", { action: "interview", ...body });
      setSessionId(r.sessionId);
      setMsgs((m) => [...m, { role: "interviewer", text: r.text }]);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }

  const start = () => {
    setMsgs([]);
    setSaved("");
    timerCommand({ action: "countdown", minutes: INTERVIEW_MINUTES }); // the interview clock starts with the interview
    call({ kind, problemPath: problem || undefined, theme });
  };
  const send = (text: string) => { if (text.trim() && sessionId) { setInput(""); call({ sessionId, message: text }, text); } };

  async function save() {
    const title = problem ? problem.split("/").at(-1)! : theme || "open";
    const date = new Date().toISOString().slice(0, 10);
    const path = saved || `interviews/${date}-${kind}-${title.toLowerCase().replace(/[^a-z0-9]+/g, "-")}.md`;
    const md = `---\nkind: ${kind}\nproblem: "${problem || theme || "chosen by interviewer"}"\ndate: ${date}\n---\n# Mock interview: ${title}\n\n` +
      msgs.map((m) => `**${m.role === "you" ? "You" : "Interviewer"}:**\n\n${m.text}`).join("\n\n---\n\n") + "\n";
    try { await putFile(path, md); setSaved(path); } catch (e) { setError((e as Error).message); }
  }

  if (!sessionId && !msgs.length)
    return (
      <div className="card max-w-2xl space-y-4 p-5">
        <div className="flex gap-2" role="radiogroup" aria-label="Interview type">
          {["coding", "system-design"].map((k) => (
            <button key={k} role="radio" aria-checked={kind === k} onClick={() => { setKind(k); setProblem(""); }} className={`btn ${kind === k ? "border-fg bg-fg text-panel" : ""}`}>
              {k === "coding" ? "Coding" : "System design"}
            </button>
          ))}
        </div>
        <label className="block space-y-1 text-sm">
          <span className="font-medium">Problem</span>
          <select className="input" value={problem} onChange={(e) => setProblem(e.target.value)}>
            <option value="">Let the interviewer choose</option>
            {options.map((p) => <option key={p} value={p}>{p.split("/").slice(1).join(" › ")}</option>)}
          </select>
        </label>
        {!problem && (
          <label className="block space-y-1 text-sm">
            <span className="font-medium">Theme (optional)</span>
            <input className="input" value={theme} onChange={(e) => setTheme(e.target.value)} placeholder={kind === "coding" ? "e.g. graphs, medium-hard" : "e.g. real-time systems at Meta"} />
          </label>
        )}
        <div className="flex items-center gap-3">
          <button className="btn-primary" onClick={start} disabled={busy}>{busy ? "Starting…" : "Start interview"}</button>
          <Link href={`/files?path=${encodeURIComponent(`prompts/interview-${kind}.md`)}`} className="text-xs text-muted hover:text-fg">Edit interviewer prompt</Link>
        </div>
        {error && <pre className="whitespace-pre-wrap text-sm text-hard">{error}</pre>}
      </div>
    );

  return (
    <div className="flex max-w-3xl flex-col gap-3">
      <div className="card max-h-[60vh] space-y-4 overflow-y-auto p-4">
        {msgs.map((m, i) => (
          <div key={i} className={m.role === "you" ? "ml-8 border-l-2 border-accent bg-fg/5 p-3" : "mr-8"}>
            <div className="mb-1 text-xs font-medium text-muted">{m.role === "you" ? "You" : "Interviewer"}</div>
            <Markdown>{m.text}</Markdown>
          </div>
        ))}
        {busy && <p className="text-sm text-muted" role="status">Interviewer is typing…</p>}
        {error && <pre className="whitespace-pre-wrap text-sm text-hard">{error}</pre>}
        <div ref={bottom} />
      </div>
      <textarea
        className="input font-mono"
        rows={4}
        value={input}
        disabled={busy}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(input); } }}
        placeholder="Your answer. Enter sends, Shift+Enter adds a new line. Use ``` for code."
      />
      <div className="flex flex-wrap gap-2">
        <button className="btn-primary" onClick={() => send(input)} disabled={busy || !input.trim()}>Send</button>
        <button className="btn" onClick={() => { timerCommand({ action: "pause" }); send("END INTERVIEW"); }} disabled={busy}>End & get feedback</button>
        <button className="btn" onClick={save} disabled={busy || !msgs.length}>{saved ? "Save again" : "Save transcript"}</button>
        <button className="btn" onClick={() => { setSessionId(null); setMsgs([]); }} disabled={busy}>New interview</button>
        {saved && <Link href={`/files?path=${encodeURIComponent(saved)}`} className="self-center text-sm text-easy underline">Saved to {saved}</Link>}
      </div>
    </div>
  );
}

export default function AiStudio() {
  const params = useSearchParams();
  const [tab, setTab] = useState<Tab>((params.get("tab") as Tab) ?? "link");
  const [tree, setTree] = useState<TreeNode[]>([]);
  const refresh = () => fetch("/api/files").then((r) => r.json()).then(setTree);
  useEffect(() => { refresh(); }, []);

  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <div>
        <h1 className="page-title">AI & Interviews</h1>
        <p className="mt-1 text-sm text-muted">Runs on your local Claude Code login. Everything Claude creates is saved under Files.</p>
      </div>
      <div className="flex flex-wrap gap-1 border-b border-border" role="tablist">
        {TABS.map(([t, label]) => (
          <button key={t} role="tab" aria-selected={tab === t} onClick={() => setTab(t)} className={`-mb-px border-b-2 px-3 py-2 text-sm ${tab === t ? "border-fg font-medium" : "border-transparent text-muted hover:text-fg"}`}>
            {label}
          </button>
        ))}
      </div>
      {tab === "interview" ? (
        <Interview tree={tree} initialKind={params.get("kind") ?? "coding"} initialProblem={params.get("problem") ?? ""} />
      ) : (
        <Creator key={tab} tab={tab} tree={tree} onCreated={refresh} />
      )}
    </div>
  );
}
