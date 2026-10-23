"use client";
import { useEffect, useRef, useState } from "react";
import { putFile } from "@/lib/client";

export type Stroke = { d: [number, number][]; w: number; accent?: boolean };
const W = 800;
const H = 450;

const toPath = (d: [number, number][]) => (d.length === 1 ? `M${d[0][0]} ${d[0][1]}l0.1 0` : "M" + d.map(([x, y]) => `${x} ${y}`).join("L"));

/** Closed outline of the ellipse inside the box dragged from a to b (a circle when `round`), as stroke points. */
function ellipse(a: [number, number], b: [number, number], round: boolean): [number, number][] {
  let rx = Math.abs(b[0] - a[0]) / 2, ry = Math.abs(b[1] - a[1]) / 2;
  if (round) rx = ry = Math.max(rx, ry);
  const cx = a[0] + Math.sign(b[0] - a[0] || 1) * rx, cy = a[1] + Math.sign(b[1] - a[1] || 1) * ry;
  const n = Math.max(24, Math.round((rx + ry) / 3));
  return Array.from({ length: n + 1 }, (_, i) => {
    const t = (i / n) * 2 * Math.PI;
    return [Math.round((cx + rx * Math.cos(t)) * 10) / 10, Math.round((cy + ry * Math.sin(t)) * 10) / 10];
  });
}

/** Read-only rendering of a drawing (used on the dashboard). */
export function SketchView({ strokes, className = "" }: { strokes: Stroke[]; className?: string }) {
  return (
    <svg viewBox={`0 0 ${W} ${H}`} className={className} role="img" aria-label="Your drawing">
      {strokes.map((s, i) => (
        <path key={i} d={toPath(s.d)} fill="none" stroke={s.accent ? "var(--accent)" : "currentColor"} strokeWidth={s.w} strokeLinecap="round" strokeLinejoin="round" />
      ))}
    </svg>
  );
}

/** Small vector drawing pad; strokes are saved to <problem>/drawing.json. */
export default function SketchPad({ path, initial }: { path: string; initial: Stroke[] }) {
  const [strokes, setStrokes] = useState<Stroke[]>(initial);
  const [tool, setTool] = useState<"pen" | "accent" | "circle" | "eraser">("pen");
  const origin = useRef<[number, number] | null>(null);
  const [width, setWidth] = useState(3);
  const svg = useRef<SVGSVGElement>(null);
  const current = useRef<Stroke | null>(null);
  const first = useRef(true);

  useEffect(() => {
    if (first.current) { first.current = false; return; }
    const t = setTimeout(() => putFile(`${path}/drawing.json`, JSON.stringify({ strokes })), 800);
    return () => clearTimeout(t);
  }, [strokes, path]);

  const point = (e: React.PointerEvent): [number, number] => {
    const r = svg.current!.getBoundingClientRect();
    return [Math.round(((e.clientX - r.left) / r.width) * W * 10) / 10, Math.round(((e.clientY - r.top) / r.height) * H * 10) / 10];
  };
  const erase = ([x, y]: [number, number]) =>
    setStrokes((ss) => ss.filter((s) => !s.d.some(([a, b]) => (a - x) ** 2 + (b - y) ** 2 < 144)));

  function down(e: React.PointerEvent) {
    svg.current!.setPointerCapture(e.pointerId);
    const p = point(e);
    if (tool === "eraser") return erase(p);
    origin.current = p;
    current.current = { d: [p], w: width, ...(tool === "accent" ? { accent: true } : {}) };
    setStrokes((ss) => [...ss, current.current!]);
  }
  function move(e: React.PointerEvent) {
    if (!(e.buttons & 1)) return;
    const p = point(e);
    if (tool === "eraser") return erase(p);
    const s = current.current;
    if (!s) return;
    if (tool === "circle") {
      s.d = ellipse(origin.current!, p, e.shiftKey);
      setStrokes((ss) => [...ss.slice(0, -1), { ...s }]);
      return;
    }
    const [lx, ly] = s.d[s.d.length - 1];
    if ((p[0] - lx) ** 2 + (p[1] - ly) ** 2 < 4) return; // skip tiny moves to keep the file small
    s.d = [...s.d, p];
    setStrokes((ss) => [...ss.slice(0, -1), { ...s }]);
  }
  const up = () => { current.current = null; };

  const btn = (active: boolean) => `px-2 py-0.5 font-mono text-xs ${active ? "bg-fg text-panel" : "text-muted hover:text-fg"}`;
  return (
    <div className="space-y-1.5">
      <div className="flex flex-wrap items-center gap-1">
        <span className="mr-1 font-mono text-xs text-muted">sketch</span>
        <button className={btn(tool === "pen")} onClick={() => setTool("pen")}>pen</button>
        <button className={btn(tool === "accent")} onClick={() => setTool("accent")}><span className="text-accent">●</span> teal</button>
        <button className={btn(tool === "circle")} onClick={() => setTool("circle")} title="Drag to draw a circle (hold Shift for a perfect circle)">◯ circle</button>
        <button className={btn(tool === "eraser")} onClick={() => setTool("eraser")}>eraser</button>
        <label className="ml-1 flex items-center gap-1 font-mono text-xs text-muted">
          size <input type="range" min={1} max={10} value={width} onChange={(e) => setWidth(+e.target.value)} className="w-16 accent-[var(--accent)]" />
        </label>
        <span className="flex-1" />
        <button className={btn(false)} onClick={() => setStrokes((ss) => ss.slice(0, -1))} disabled={!strokes.length}>undo</button>
        <button className={btn(false)} onClick={() => confirm("Clear the drawing?") && setStrokes([])} disabled={!strokes.length}>clear</button>
      </div>
      <svg
        ref={svg}
        viewBox={`0 0 ${W} ${H}`}
        className={`aspect-[16/9] w-full touch-none border border-border bg-panel ${tool === "eraser" ? "cursor-cell" : "cursor-crosshair"}`}
        onPointerDown={down}
        onPointerMove={move}
        onPointerUp={up}
        onPointerLeave={up}
        role="img"
        aria-label="Drawing pad"
      >
        {strokes.map((s, i) => (
          <path key={i} d={toPath(s.d)} fill="none" stroke={s.accent ? "var(--accent)" : "currentColor"} strokeWidth={s.w} strokeLinecap="round" strokeLinejoin="round" />
        ))}
      </svg>
    </div>
  );
}
