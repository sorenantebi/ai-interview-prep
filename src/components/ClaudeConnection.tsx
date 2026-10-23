"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/client";

type Status = { installed: boolean; loggedIn: boolean; method?: string; plan?: string };

/** Shows whether Claude Code is logged in, with a button that opens a terminal to log in (macOS, Windows, Linux). */
export default function ClaudeConnection() {
  const [status, setStatus] = useState<Status | null>(null);
  const [msg, setMsg] = useState("");
  const check = () => fetch("/api/claude-auth").then((r) => r.json()).then(setStatus).catch(() => setStatus(null));
  useEffect(() => { check(); }, []);

  async function login() {
    const r = await api("/api/claude-auth", {});
    setMsg(r.opened ? "A terminal window opened: finish logging in there (it opens your browser), then press Check again." : `Couldn't open a terminal here. Run this yourself: ${r.command}`);
  }

  const dot = (ok: boolean) => <span className={`inline-block h-2.5 w-2.5 ${ok ? "bg-easy" : "bg-hard"}`} aria-hidden />;
  return (
    <section className="card flex flex-wrap items-center gap-3 p-4 text-sm">
      {!status ? (
        <span className="text-muted">Checking Claude Code…</span>
      ) : !status.installed ? (
        <>{dot(false)}<span>Claude Code isn&apos;t installed. See <b>Set up Claude</b> in the README.</span></>
      ) : status.loggedIn ? (
        <>{dot(true)}<span>Claude Code connected <span className="font-mono text-xs text-muted">{[status.method, status.plan && `${status.plan} plan`].filter(Boolean).join(" · ")}</span></span></>
      ) : (
        <>{dot(false)}<span>Claude Code isn&apos;t logged in, so AI features won&apos;t work.</span><button className="btn-primary" onClick={login}>Log in to Claude</button></>
      )}
      <button className="btn ml-auto px-2 py-1 text-xs" onClick={() => { setMsg(""); setStatus(null); check(); }}>Check again</button>
      {msg && <p className="w-full font-mono text-xs text-muted" role="status">{msg}</p>}
    </section>
  );
}
