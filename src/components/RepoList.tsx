"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { api } from "@/lib/client";
import type { RepoInfo } from "@/lib/repos";

export default function RepoList({ repos }: { repos: RepoInfo[] }) {
  const router = useRouter();
  const [url, setUrl] = useState("");
  const [busy, setBusy] = useState<string | null>(null);
  const [msg, setMsg] = useState<{ ok: boolean; text: string } | null>(null);

  async function run(label: string, fn: () => Promise<string>) {
    setBusy(label);
    setMsg(null);
    try { setMsg({ ok: true, text: await fn() }); router.refresh(); } catch (e) { setMsg({ ok: false, text: (e as Error).message }); } finally { setBusy(null); }
  }
  const add = (e: React.FormEvent) => {
    e.preventDefault();
    run("add", async () => { const r = await api("/api/repos", { action: "add", url }); setUrl(""); return `Cloned into repos/${r.name}`; });
  };
  const pull = (name: string) => run(name, async () => (await api("/api/repos", { action: "pull", name })).output || "Already up to date");
  const remove = (name: string) =>
    confirm(`Delete the local copy of ${name}? (The remote repo is not touched.)`) &&
    run(name, async () => { const r = await fetch(`/api/repos?name=${encodeURIComponent(name)}`, { method: "DELETE" }); if (!r.ok) throw new Error((await r.json()).error); return `Removed ${name}`; });

  return (
    <div className="space-y-4">
      <form onSubmit={add} className="card flex flex-wrap items-center gap-2 p-3">
        <input className="input min-w-64 flex-1 font-mono" value={url} onChange={(e) => setUrl(e.target.value)} placeholder="https://github.com/owner/repo  ·  git@github.com:owner/repo.git  ·  owner/repo" aria-label="Git repository URL" required />
        <button className="btn-primary" disabled={!!busy}>{busy === "add" ? "Cloning…" : "+ Add repo"}</button>
      </form>
      {msg && <pre className={`whitespace-pre-wrap font-mono text-xs ${msg.ok ? "text-easy" : "text-hard"}`} role="status">{msg.text}</pre>}
      {repos.length === 0 ? (
        <p className="card p-4 text-sm text-muted">No repos yet. Paste a git URL above. Private repos use your own git login on this machine.</p>
      ) : (
        <ul className="card divide-y divide-border">
          {repos.map((r) => (
            <li key={r.name} className="flex flex-wrap items-center gap-x-4 gap-y-1 px-4 py-3">
              <Link href={`/repos/${encodeURIComponent(r.name)}`} className="font-display text-lg font-medium decoration-accent decoration-2 underline-offset-2 hover:underline">{r.name}</Link>
              <span className="font-mono text-xs text-muted">{r.branch}</span>
              <span className="min-w-0 flex-1 truncate font-mono text-xs text-muted" title={r.subject}>{r.commit} {r.subject} · {r.when}</span>
              <span className="w-full truncate font-mono text-[11px] text-muted sm:order-last">{r.url}</span>
              <button className="btn px-2 py-1 text-xs" onClick={() => pull(r.name)} disabled={!!busy}>{busy === r.name ? "…" : "Pull"}</button>
              <button className="btn px-2 py-1 text-xs hover:border-hard" onClick={() => remove(r.name)} disabled={!!busy}>Remove</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
