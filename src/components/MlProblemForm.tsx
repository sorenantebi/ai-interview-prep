"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Editor from "@monaco-editor/react";
import { api } from "@/lib/client";
import { problemHref } from "./ProblemList";
import { NO_ASSIST } from "./editor-options";
import { isDark } from "./ThemeToggle";

const HELP: Record<string, string> = {
  "question.md": "The problem page. Run reads the `Input:` lines of the examples (name = value, in parameter order).",
  "starter.py": "Imports plus one function, every parameter type-hinted, body `pass`.",
  "solution.md": "Your reference solution in the ```python block. Run compares your output with it.",
  "tests.py": "Hidden tests for Submit: edit FUNC, NUMPY_ONLY, reference and CASES.",
};

export default function MlProblemForm({ groups, template }: { groups: string[]; template: Record<string, string> }) {
  const router = useRouter();
  const [group, setGroup] = useState(groups[0] ?? "");
  const [files, setFiles] = useState(template);
  const [tab, setTab] = useState("question.md");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [dark, setDark] = useState(false);
  useEffect(() => {
    const update = () => setDark(isDark());
    update();
    window.addEventListener("prep-theme", update);
    return () => window.removeEventListener("prep-theme", update);
  }, []);

  async function save(force = false) {
    setBusy(true);
    setError("");
    try {
      router.push(problemHref((await api("/api/problem", { action: "create-ml", group, files, force })).path));
    } catch (e) {
      setError((e as Error).message);
      setBusy(false);
    }
  }

  return (
    <div className="space-y-3">
      <label className="flex max-w-md items-center gap-2 text-sm">
        <span className="font-medium">Topic</span>
        <input className="input" list="ml-groups" value={group} onChange={(e) => setGroup(e.target.value)} placeholder="Pick a topic or type a new one" />
        <datalist id="ml-groups">{groups.map((g) => <option key={g} value={g} />)}</datalist>
      </label>
      <div className="card overflow-hidden">
        <div className="flex flex-wrap border-b border-border" role="tablist">
          {Object.keys(template).map((n) => (
            <button key={n} role="tab" aria-selected={tab === n} onClick={() => setTab(n)} className={`px-3 py-2 font-mono text-xs ${tab === n ? "bg-fg text-panel" : "text-muted hover:text-fg"}`}>
              {n}{files[n] !== template[n] ? " •" : ""}
            </button>
          ))}
          <span className="flex-1" />
          <button className="px-3 py-2 font-mono text-xs text-muted hover:text-fg" onClick={() => confirm(`Reset ${tab} to the skeleton?`) && setFiles({ ...files, [tab]: template[tab] })}>reset to skeleton</button>
        </div>
        <p className="border-b border-border px-3 py-1.5 text-xs text-muted">{HELP[tab]}</p>
        <div className="h-[60vh]">
          <Editor
            path={tab}
            language={tab.endsWith(".py") ? "python" : "markdown"}
            theme={dark ? "vs-dark" : "light"}
            value={files[tab]}
            onChange={(v) => setFiles((f) => ({ ...f, [tab]: v ?? "" }))}
            options={NO_ASSIST}
          />
        </div>
      </div>
      <div className="flex flex-wrap items-center gap-3">
        <button className="btn-primary" onClick={() => save()} disabled={busy || !group.trim()}>{busy ? "Checking the tests…" : "Save problem"}</button>
        {error && !busy && <button className="btn" onClick={() => save(true)}>Save anyway</button>}
      </div>
      {error && <pre className="whitespace-pre-wrap text-sm text-hard">{error}</pre>}
    </div>
  );
}
