"use client";
import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import { putFile } from "@/lib/client";
import type { TreeNode } from "@/lib/content";

const DEFAULT = "notes/notepad.md";

/** A tab on the left edge that pops out a notepad. Each note is a .md file in content/notes/; it autosaves. */
export default function Notepad() {
  const [open, setOpen] = useState(false);
  const [file, setFile] = useState(DEFAULT);
  const [notes, setNotes] = useState<string[]>([]);
  const [text, setText] = useState<string | null>(null); // null until loaded
  const [status, setStatus] = useState("");
  const saved = useRef("");

  // The notes list: every .md in content/notes/; remember the last one you had open.
  useEffect(() => {
    if (!open) return;
    try { const last = localStorage.getItem("notepad-file"); if (last) setFile(last); } catch {}
    fetch("/api/files").then((r) => r.json()).then((t: TreeNode[]) => {
      const md = (t.find((n) => n.path === "notes")?.children ?? []).filter((n) => !n.dir && n.name.endsWith(".md")).map((n) => n.path);
      setNotes(md);
    }).catch(() => {});
  }, [open]);

  function switchTo(p: string) {
    if (p === file) return;
    setNotes((n) => (n.includes(file) ? n : [...n, file].sort())); // keep the note you leave in the list
    if (text !== null && text !== saved.current) putFile(file, text).catch(() => {}); // don't lose the last keystrokes
    setFile(p);
    setText(null);
    setStatus("");
    try { localStorage.setItem("notepad-file", p); } catch {}
  }
  function newNote() {
    const name = prompt("Name of the new note", "untitled")?.trim().replace(/\.md$/i, "").replace(/[^\w\- ]+/g, "_");
    if (!name) return;
    const p = `notes/${name}.md`;
    if (!notes.includes(p)) { setNotes((n) => [...n, p].sort()); putFile(p, "").catch(() => {}); }
    switchTo(p);
  }

  useEffect(() => {
    if (!open || text !== null) return;
    let stale = false; // you switched notes before this one loaded
    fetch(`/api/files?path=${encodeURIComponent(file)}`)
      .then((r) => r.json())
      .then((d) => { if (!stale) { saved.current = d.content ?? ""; setText(saved.current); } }) // missing file: start empty
      .catch(() => !stale && setText(""));
    return () => { stale = true; };
  }, [open, text, file]);

  useEffect(() => {
    if (text === null || text === saved.current) return;
    setStatus("…");
    const t = setTimeout(() => {
      putFile(file, text).then(() => { saved.current = text; setStatus("saved"); }, (e) => setStatus(`not saved: ${e.message}`));
    }, 700);
    return () => clearTimeout(t);
  }, [text, file]);

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && setOpen(false);
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open]);

  return (
    <div className={`fixed left-0 top-1/2 z-40 flex -translate-y-1/2 items-center transition-transform duration-500 ease-[cubic-bezier(0.34,1.4,0.64,1)] motion-reduce:transition-none ${open ? "translate-x-0" : "-translate-x-[min(24rem,85vw)]"}`}>
      <section className="card flex h-[70vh] rounded-r-[12px] shadow-lg w-[min(24rem,85vw)] flex-col" aria-label="Notepad" aria-hidden={!open}>
        <div className="flex items-center gap-2 border-b border-border px-3 py-2">
          <select className="min-w-0 flex-1 bg-transparent font-medium outline-none" value={file} onChange={(e) => switchTo(e.target.value)} aria-label="Pick a note" tabIndex={open ? 0 : -1}>
            {[...new Set([...notes, file])].map((p) => <option key={p} value={p}>{p.slice(6, -3)}</option>)}
          </select>
          <button className="font-mono text-[11px] text-muted hover:text-fg" onClick={newNote} tabIndex={open ? 0 : -1}>+ new</button>
        </div>
        <div className="flex justify-between border-b border-border px-3 py-1 font-mono text-[11px] text-muted">
          <Link href={`/files?path=${encodeURIComponent(file)}`} className="truncate hover:text-fg" tabIndex={open ? 0 : -1}>{file}</Link>
          <span>{status}</span>
        </div>
        <textarea
          className="min-h-0 flex-1 resize-none bg-transparent p-3 font-mono text-[13px] leading-relaxed outline-none"
          value={text ?? ""}
          disabled={text === null}
          onChange={(e) => setText(e.target.value)}
          placeholder={text === null ? "Loading…" : "Jot anything down. It saves as you type."}
          aria-label="Notepad text"
          tabIndex={open ? 0 : -1}
        />
      </section>
      <button
        onClick={() => setOpen((o) => !o)}
        className="cursor-pointer rounded-r-[10px] border border-l-0 border-border bg-panel pb-4 pl-1.5 pr-1.5 pt-4 font-mono text-xs leading-none text-muted shadow-md transition-[padding,background-color,color] duration-200 [writing-mode:vertical-rl] hover:bg-fg hover:pl-2.5 hover:text-panel motion-reduce:transition-none"
        aria-expanded={open}
        title={open ? "Close the notepad (Esc)" : "Open the notepad"}
      >
        {open ? "‹ close" : "notes"}
      </button>
    </div>
  );
}
