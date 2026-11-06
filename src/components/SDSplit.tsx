"use client";

import { useEffect, useRef, useState } from "react";
import { Divider } from "./Workspace";

const DEFAULT = 58; // % of the row for the problem (video) side

/** The problem on the left and your notes on the right, with a draggable bar between them (remembered in localStorage). */
export default function SDSplit({ left, right }: { left: React.ReactNode; right: React.ReactNode }) {
  const row = useRef<HTMLDivElement>(null);
  const [pct, setPct] = useState(DEFAULT);
  useEffect(() => {
    try { const v = Number(localStorage.getItem("sd-split")); if (v) setPct(v); } catch {}
  }, []);
  const resize = (v: number) => {
    const p = Math.min(80, Math.max(25, v));
    setPct(p);
    try { localStorage.setItem("sd-split", String(p)); } catch {}
  };
  return (
    <div ref={row} className="flex flex-col gap-6 lg:flex-row lg:items-start lg:gap-0" style={{ "--left": `${pct}%` } as React.CSSProperties}>
      <div className="min-w-0 space-y-6 lg:w-[var(--left)] lg:shrink-0">{left}</div>
      <div className="max-lg:hidden lg:sticky lg:top-20 lg:flex lg:h-[calc(100vh-10rem)] lg:px-1.5">
        <Divider
          dir="x"
          label="Drag to resize the problem and your notes"
          onMove={(e) => { const r = row.current?.getBoundingClientRect(); if (r) resize(((e.clientX - r.left) / r.width) * 100); }}
          onStep={(d) => resize(pct + d * 2)}
          onReset={() => resize(DEFAULT)}
        />
      </div>
      <div className="min-w-0 flex-1 lg:sticky lg:top-20 lg:h-[calc(100vh-10rem)]">{right}</div>
    </div>
  );
}
