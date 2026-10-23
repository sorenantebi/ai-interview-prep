"use client";
import dynamic from "next/dynamic";
import { useRef, useState } from "react";
import "@excalidraw/excalidraw/index.css";
import { putFile } from "@/lib/client";
import type { Scene } from "./ExcalidrawView";

// Fonts are served from /public/excalidraw so the editor works offline (set before the editor module loads).
if (typeof window !== "undefined") (window as unknown as { EXCALIDRAW_ASSET_PATH: string }).EXCALIDRAW_ASSET_PATH = "/excalidraw/";

const Excalidraw = dynamic(() => import("@excalidraw/excalidraw").then((m) => m.Excalidraw), {
  ssr: false,
  loading: () => <p className="p-4 font-mono text-xs text-muted">Loading Excalidraw…</p>,
});

/** Your own notes for a system design problem: text (notes.md) and an Excalidraw canvas (notes.excalidraw). */
export default function SDNotes({ path, notes, scene }: { path: string; notes: string; scene: Scene | null }) {
  const [text, setText] = useState(notes);
  const [saved, setSaved] = useState("");
  const timer = useRef<ReturnType<typeof setTimeout>>(undefined);
  const lastVersion = useRef(-1);

  // Excalidraw calls onChange on every pointer move; only save when the drawing itself changed.
  const onChange = (elements: readonly { version: number; isDeleted?: boolean }[], appState: { viewBackgroundColor: string }, files: unknown) => {
    const version = elements.reduce((n, e) => n + e.version, 0);
    if (lastVersion.current === -1) { lastVersion.current = version; return; } // first call is the initial load
    if (version === lastVersion.current) return;
    lastVersion.current = version;
    clearTimeout(timer.current);
    timer.current = setTimeout(async () => {
      const data = { type: "excalidraw", version: 2, source: "interview-prep", elements: elements.filter((e) => !e.isDeleted), appState: { viewBackgroundColor: appState.viewBackgroundColor }, files };
      await putFile(`${path}/notes.excalidraw`, JSON.stringify(data));
      setSaved(`drawing saved ${new Date().toLocaleTimeString()}`);
    }, 800);
  };

  return (
    <section className="card">
      <div className="flex items-baseline justify-between border-b border-border px-4 py-3">
        <h2 className="font-medium">My notes</h2>
        <span className="font-mono text-[11px] text-muted">{saved || "saved to notes.md and notes.excalidraw · shown in the dashboard"}</span>
      </div>
      <div className="p-4">
        <textarea
          className="input min-h-28 font-mono"
          value={text}
          onChange={(e) => setText(e.target.value)}
          onBlur={() => putFile(`${path}/notes.md`, text).then(() => setSaved(`notes saved ${new Date().toLocaleTimeString()}`))}
          placeholder="Key decisions, trade-offs, what you'd say first in the interview…"
          aria-label="Your notes"
        />
      </div>
      <div className="h-[560px] border-t border-border">
        <Excalidraw
          initialData={{ elements: (scene?.elements ?? []) as never, appState: { viewBackgroundColor: "#ffffff" }, files: ((scene as { files?: unknown } | null)?.files ?? {}) as never }}
          onChange={onChange as never}
          theme="light"
        />
      </div>
    </section>
  );
}
