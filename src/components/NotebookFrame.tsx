"use client";
import { useState } from "react";
import { api } from "@/lib/client";

/** A repo notebook, opened in the app's local Jupyter and embedded in the page. */
export default function NotebookFrame({ path }: { path: string }) {
  const [url, setUrl] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  async function open() {
    setBusy(true);
    setError("");
    try { setUrl((await api("/api/jupyter", { path })).url); } catch (e) { setError((e as Error).message); } finally { setBusy(false); }
  }
  if (url) return <iframe src={url} title={`Jupyter: ${path}`} className="h-[85vh] w-full border border-border bg-white" />;
  return (
    <div className="card space-y-3 p-5">
      <button className="btn-primary" onClick={open} disabled={busy}>{busy ? "Starting Jupyter…" : "▶ Open in Jupyter"}</button>
      <p className="text-sm text-muted">Runs the notebook&apos;s code on your computer, with your permissions. Only run notebooks from repos you trust.</p>
      {error && <pre className="whitespace-pre-wrap text-sm text-hard">{error}</pre>}
    </div>
  );
}
