"use client";
import { useCallback, useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Markdown from "./Markdown";
import { api, putFile } from "@/lib/client";
import type { TreeNode } from "@/lib/content";

const parentOf = (p: string) => p.split("/").slice(0, -1).join("/");

function Tree({ nodes, selected, open, onSelect, onToggle }: { nodes: TreeNode[]; selected: string; open: Set<string>; onSelect: (n: TreeNode) => void; onToggle: (p: string) => void }) {
  return (
    <ul className="pl-3">
      {nodes.map((n) => (
        <li key={n.path}>
          <button
            onClick={() => (n.dir ? onToggle(n.path) : onSelect(n))}
            className={`flex w-full items-center gap-1 truncate px-1.5 py-0.5 text-left font-mono text-[13px] ${selected === n.path ? "bg-fg text-panel" : "hover:bg-fg/5"}`}
          >
            <span className="w-3 text-xs text-muted">{n.dir ? (open.has(n.path) ? "▾" : "▸") : ""}</span>
            <span className="truncate">{n.name}</span>
          </button>
          {n.dir && open.has(n.path) && n.children && <Tree nodes={n.children} selected={selected} open={open} onSelect={onSelect} onToggle={onToggle} />}
        </li>
      ))}
    </ul>
  );
}

export default function FileBrowser() {
  const router = useRouter();
  const params = useSearchParams();
  const [tree, setTree] = useState<TreeNode[]>([]);
  const [open, setOpen] = useState<Set<string>>(new Set());
  const [selected, setSelected] = useState(params.get("path") ?? "");
  const [content, setContent] = useState<string | null>(null);
  const [draft, setDraft] = useState("");
  const [editing, setEditing] = useState(false);
  const [error, setError] = useState("");

  const refresh = useCallback(() => fetch("/api/files").then((r) => r.json()).then(setTree), []);
  useEffect(() => { refresh(); }, [refresh]);

  // Open every ancestor of the selected path, and load it if it is a file.
  useEffect(() => {
    if (!selected) return;
    setOpen((o) => { const n = new Set(o); selected.split("/").forEach((_, i, a) => n.add(a.slice(0, i + 1).join("/"))); return n; });
    setEditing(false);
    fetch(`/api/files?path=${encodeURIComponent(selected)}`).then(async (r) => {
      const d = await r.json();
      setContent(r.ok ? d.content : null); // directories and missing files return 400/404
      setDraft(d.content ?? "");
    });
  }, [selected]);

  const select = (p: string) => { setSelected(p); router.replace(`/files?path=${encodeURIComponent(p)}`, { scroll: false }); };
  const isFile = content !== null;
  const dir = isFile ? parentOf(selected) : selected;

  async function act(fn: () => Promise<unknown>) {
    setError("");
    try { await fn(); await refresh(); } catch (e) { setError((e as Error).message); }
  }
  const newFile = () => { const n = prompt(`New file in /${dir}`, "untitled.md"); if (n) act(async () => { const p = dir ? `${dir}/${n}` : n; await putFile(p, ""); select(p); setEditing(true); }); };
  const newFolder = () => { const n = prompt(`New folder in /${dir}`); if (n) act(async () => { const p = dir ? `${dir}/${n}` : n; await api("/api/files", { action: "mkdir", path: p }); select(p); }); };
  const renameIt = () => { const to = prompt("Rename / move to", selected); if (to && to !== selected) act(async () => { await api("/api/files", { action: "rename", path: selected, to }); select(to); }); };
  const del = () => { if (confirm(`Delete ${selected}${isFile ? "" : " and everything inside it"}?`)) act(async () => { const r = await fetch(`/api/files?path=${encodeURIComponent(selected)}`, { method: "DELETE" }); if (!r.ok) throw new Error((await r.json()).error); select(parentOf(selected)); }); };
  const save = () => act(async () => { await putFile(selected, draft); setContent(draft); setEditing(false); });

  return (
    <div className="mx-auto flex max-w-7xl flex-col gap-4">
      <div className="flex flex-wrap items-center gap-2">
        <h1 className="page-title mr-auto">Files</h1>
        <button className="btn" onClick={newFile}>+ File</button>
        <button className="btn" onClick={newFolder}>+ Folder</button>
        <button className="btn" onClick={renameIt} disabled={!selected}>Rename</button>
        <button className="btn hover:border-hard" onClick={del} disabled={!selected}>Delete</button>
      </div>
      {error && <p className="text-sm text-hard" role="alert">{error}</p>}
      <div className="grid gap-4 md:grid-cols-[18rem_1fr]">
        <aside className="card max-h-[75vh] overflow-y-auto py-2 pr-2">
          <button onClick={() => select("")} className={`ml-3 px-1.5 font-mono text-[13px] ${selected === "" ? "font-medium text-fg" : "text-muted"}`}>content/</button>
          <Tree nodes={tree} selected={selected} open={open} onSelect={(n) => select(n.path)} onToggle={(p) => { select(p); setOpen((o) => { const n = new Set(o); if (o.has(p) && selected === p) n.delete(p); else n.add(p); return n; }); }} />
        </aside>
        <section className="card min-h-[50vh] min-w-0 p-4">
          {!isFile ? (
            <p className="text-sm text-muted">{selected ? `/${selected}` : "content/"}: pick a file, or use + File / + Folder to add one here.</p>
          ) : (
            <>
              <div className="mb-3 flex items-center gap-2 border-b border-border pb-3">
                <span className="mr-auto truncate font-mono text-xs text-muted">{selected}</span>
                {editing ? (
                  <>
                    <button className="btn" onClick={() => { setDraft(content); setEditing(false); }}>Cancel</button>
                    <button className="btn-primary" onClick={save}>Save</button>
                  </>
                ) : (
                  <button className="btn" onClick={() => setEditing(true)}>Edit</button>
                )}
              </div>
              {editing ? (
                <textarea className="input h-[65vh] font-mono text-[13px]" value={draft} onChange={(e) => setDraft(e.target.value)} spellCheck={false} />
              ) : selected.endsWith(".md") ? (
                <Markdown>{content}</Markdown>
              ) : (
                <pre className="overflow-x-auto whitespace-pre font-mono text-[13px]">{content}</pre>
              )}
            </>
          )}
        </section>
      </div>
    </div>
  );
}
