"use client";
import { useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import Markdown from "./Markdown";
import { api } from "@/lib/client";
import type { ChatMessage } from "@/lib/page";

/**
 * Your own page with a chat sidebar. The page renders in a sandboxed iframe (scripts allowed, but no access to the
 * app, its API or your files), so anything on it, written by you or by Claude, can't reach outside the page.
 */
export default function MyPage({ initialHtml, initialChat, files }: { initialHtml: string; initialChat: ChatMessage[]; files: { name: string; url: string }[] }) {
  const router = useRouter();
  const [html, setHtml] = useState(initialHtml);
  const [draft, setDraft] = useState(initialHtml);
  const [editing, setEditing] = useState(false);
  const [chat, setChat] = useState(initialChat);
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState<string | null>(null);
  const [error, setError] = useState("");
  const upload = useRef<HTMLInputElement>(null);
  const log = useRef<HTMLDivElement>(null);
  // Scroll only the chat panel to the newest message (scrollIntoView would also scroll the window and hide the toolbar).
  useEffect(() => { log.current?.scrollTo({ top: log.current.scrollHeight, behavior: "smooth" }); }, [chat, busy]);

  async function call(label: string, body: object) {
    setBusy(label);
    setError("");
    try {
      const r = await api("/api/page", body);
      if (r.html !== undefined) { setHtml(r.html); setDraft(r.html); }
      if (r.messages) setChat(r.messages);
      return true;
    } catch (e) {
      setError((e as Error).message);
      return false;
    } finally {
      setBusy(null);
    }
  }

  async function send() {
    const text = message.trim();
    if (!text || busy) return;
    setMessage("");
    setChat((c) => [...c, { role: "you", text, at: new Date().toISOString() }]); // show it right away
    if (!(await call("Claude is working on your page…", { action: "chat", message: text }))) {
      setChat((c) => c.slice(0, -1));
      setMessage(text);
    }
  }

  async function addPicture(file: File) {
    setBusy("Uploading…");
    setError("");
    try {
      const form = new FormData();
      form.append("file", file);
      const res = await fetch("/api/page", { method: "POST", body: form });
      const r = await res.json();
      if (!res.ok) throw new Error(r.error);
      setMessage((m) => m || `Put the picture ${r.name} `);
      router.refresh();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(null);
      if (upload.current) upload.current.value = "";
    }
  }

  return (
    <div className="grid h-[calc(100vh-7.5rem)] gap-3 lg:grid-cols-[1fr_24rem]">
      {/* The page */}
      <section className="flex min-h-[60vh] min-w-0 flex-col gap-2">
        <div className="flex flex-wrap items-center gap-2">
          <button className="btn" disabled={!!busy} onClick={() => upload.current?.click()}>Add picture</button>
          <input ref={upload} type="file" accept="image/png,image/jpeg,image/gif,image/webp,image/svg+xml" className="hidden" onChange={(e) => e.target.files?.[0] && addPicture(e.target.files[0])} />
          <button className="btn" disabled={!!busy} onClick={() => call("Undoing…", { action: "undo" })}>Undo</button>
          <button className={`btn ${editing ? "border-fg" : ""}`} onClick={() => { setDraft(html); setEditing((v) => !v); }}>{editing ? "Close editor" : "Edit HTML"}</button>
          {editing && <button className="btn-primary" disabled={!!busy || draft === html} onClick={() => call("Saving…", { action: "save", html: draft })}>Save HTML</button>}
          {files.length > 0 && (
            <span className="flex flex-wrap items-center gap-1 font-mono text-[11px] text-muted">
              pictures: {files.map((f) => <a key={f.name} href={f.url} target="_blank" rel="noreferrer" className="border border-border px-1.5 py-0.5 hover:text-fg">{f.name}</a>)}
            </span>
          )}
        </div>
        <div className={`grid min-h-0 flex-1 gap-2 ${editing ? "xl:grid-cols-2" : ""}`}>
          {editing && <textarea className="input min-h-64 resize-none font-mono text-[13px]" value={draft} onChange={(e) => setDraft(e.target.value)} spellCheck={false} aria-label="Page HTML" />}
          <iframe title="Your page" className="card h-full min-h-96 w-full bg-white" sandbox="allow-scripts allow-forms allow-popups allow-modals" srcDoc={editing ? draft : html} />
        </div>
      </section>

      {/* The chat */}
      <aside className="card flex min-h-[50vh] flex-col">
        <div className="flex items-center justify-between border-b border-border px-3 py-2">
          <h2 className="font-medium">Chat with Claude</h2>
          {chat.length > 0 && <button className="font-mono text-[11px] text-muted hover:text-fg" disabled={!!busy} onClick={() => confirm("Clear the chat? Your page stays as it is.") && call("Clearing…", { action: "clear-chat" })}>clear chat</button>}
        </div>
        <div ref={log} className="min-h-0 flex-1 space-y-3 overflow-y-auto p-3">
          {chat.length === 0 && (
            <p className="text-sm text-muted">Tell Claude what you want on your page: “add my goals for this week”, “make it dark”, “add a countdown to my interview on Dec 10”. Ask follow-ups to refine it.</p>
          )}
          {chat.map((m, i) => (
            <div key={i} className={m.role === "you" ? "ml-6 bg-fg/5 p-2.5 text-sm" : "mr-6 text-sm"}>
              <div className="mb-0.5 font-mono text-[11px] text-muted">{m.role === "you" ? "You" : "Claude"}{m.changed ? " · changed the page" : ""}</div>
              {m.role === "you" ? <p className="whitespace-pre-wrap">{m.text}</p> : <div className="[&_.md]:text-sm"><Markdown>{m.text}</Markdown></div>}
            </div>
          ))}
          {busy && <p className="font-mono text-xs text-muted" role="status">{busy}</p>}
          {error && <p className="text-sm text-hard" role="alert">{error}</p>}
        </div>
        <form className="border-t border-border p-2" onSubmit={(e) => { e.preventDefault(); send(); }}>
          <textarea
            className="input resize-none"
            rows={3}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }}
            placeholder="Message Claude… (Enter sends, Shift+Enter for a new line)"
            aria-label="Message Claude about your page"
          />
          <button className="btn-primary mt-2 w-full justify-center" disabled={!!busy || !message.trim()}>Send</button>
        </form>
      </aside>
    </div>
  );
}
