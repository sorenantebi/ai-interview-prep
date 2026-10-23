// Minimal read-only renderer for Excalidraw scenes (rectangle, ellipse, diamond, arrow, line, text) as plain SVG.
// shortcut: clean lines instead of Excalidraw's hand-drawn style and no embedded images; use @excalidraw/excalidraw if those are needed.

type El = {
  id: string; type: string; x: number; y: number; width: number; height: number; angle?: number;
  strokeColor?: string; backgroundColor?: string; strokeWidth?: number; strokeStyle?: string; opacity?: number;
  roundness?: { type: number } | null; points?: [number, number][]; startArrowhead?: string | null; endArrowhead?: string | null;
  text?: string; fontSize?: number; fontFamily?: number; textAlign?: string; verticalAlign?: string; lineHeight?: number; containerId?: string | null;
};
export type Scene = { elements: El[] };

const dash = (s?: string) => (s === "dashed" ? "8 6" : s === "dotted" ? "2 5" : undefined);
const fill = (c?: string) => (!c || c === "transparent" ? "none" : c);

function bounds(els: El[]) {
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
  for (const e of els) {
    const pts = e.points?.length ? e.points.map(([px, py]) => [e.x + px, e.y + py]) : [[e.x, e.y], [e.x + e.width, e.y + e.height]];
    for (const [x, y] of pts) { minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y); }
  }
  return { minX, minY, w: maxX - minX, h: maxY - minY };
}

function head(x: number, y: number, fromX: number, fromY: number, color: string, w: number) {
  const a = Math.atan2(y - fromY, x - fromX), L = 10 + w * 2;
  const r = (n: number) => Math.round(n * 100) / 100; // trig differs in the last digits between Node and browsers (hydration)
  const p = (da: number) => `${r(x - L * Math.cos(a + da))},${r(y - L * Math.sin(a + da))}`;
  return <polyline points={`${p(0.45)} ${x},${y} ${p(-0.45)}`} fill="none" stroke={color} strokeWidth={w} strokeLinecap="round" strokeLinejoin="round" />;
}

function Shape({ e }: { e: El }) {
  const stroke = e.strokeColor ?? "#1e1e1e", sw = e.strokeWidth ?? 1;
  const common = { stroke, strokeWidth: sw, strokeDasharray: dash(e.strokeStyle), opacity: (e.opacity ?? 100) / 100 };
  const rot = e.angle ? `rotate(${(e.angle * 180) / Math.PI} ${e.x + e.width / 2} ${e.y + e.height / 2})` : undefined;
  if (e.type === "rectangle")
    return <rect x={e.x} y={e.y} width={e.width} height={e.height} rx={e.roundness ? Math.min(16, Math.min(e.width, e.height) * 0.15) : 0} fill={fill(e.backgroundColor)} transform={rot} {...common} />;
  if (e.type === "ellipse")
    return <ellipse cx={e.x + e.width / 2} cy={e.y + e.height / 2} rx={e.width / 2} ry={e.height / 2} fill={fill(e.backgroundColor)} transform={rot} {...common} />;
  if (e.type === "diamond") {
    const { x, y, width: w, height: h } = e;
    return <polygon points={`${x + w / 2},${y} ${x + w},${y + h / 2} ${x + w / 2},${y + h} ${x},${y + h / 2}`} fill={fill(e.backgroundColor)} transform={rot} {...common} />;
  }
  if ((e.type === "arrow" || e.type === "line" || e.type === "freedraw") && e.points?.length) {
    const pts = e.points.map(([px, py]) => [e.x + px, e.y + py]);
    const [a, b] = [pts[pts.length - 2] ?? pts[0], pts[pts.length - 1]];
    return (
      <g opacity={common.opacity}>
        <polyline points={pts.map((p) => p.join(",")).join(" ")} fill="none" stroke={stroke} strokeWidth={sw} strokeDasharray={common.strokeDasharray} strokeLinecap="round" strokeLinejoin="round" />
        {e.endArrowhead && head(b[0], b[1], a[0], a[1], stroke, sw)}
        {e.startArrowhead && pts.length > 1 && head(pts[0][0], pts[0][1], pts[1][0], pts[1][1], stroke, sw)}
      </g>
    );
  }
  return null;
}

function Text({ e, byId }: { e: El; byId: Map<string, El> }) {
  const lines = (e.text ?? "").split("\n");
  const size = e.fontSize ?? 16, lh = size * (e.lineHeight ?? 1.25);
  const box = e.containerId ? byId.get(e.containerId) : undefined;
  let x: number, top: number, anchor: "start" | "middle" | "end";
  if (box?.points?.length) {
    // Label on an arrow: centre on the middle of the line.
    const pts = box.points, m = pts[Math.floor((pts.length - 1) / 2)], n = pts[Math.ceil((pts.length - 1) / 2)];
    x = box.x + (m[0] + n[0]) / 2; top = box.y + (m[1] + n[1]) / 2 - (lines.length * lh) / 2; anchor = "middle";
  } else if (box) {
    // Bound text: centre in its container (more robust than the stored position).
    anchor = e.textAlign === "left" ? "start" : e.textAlign === "right" ? "end" : "middle";
    x = anchor === "start" ? box.x + 8 : anchor === "end" ? box.x + box.width - 8 : box.x + box.width / 2;
    top = e.verticalAlign === "top" ? box.y + 6 : box.y + (box.height - lines.length * lh) / 2;
  } else {
    anchor = e.textAlign === "center" ? "middle" : e.textAlign === "right" ? "end" : "start";
    x = anchor === "middle" ? e.x + e.width / 2 : anchor === "end" ? e.x + e.width : e.x;
    top = e.y;
  }
  return (
    <text x={x} fontSize={size} textAnchor={anchor} fill={e.strokeColor ?? "#1e1e1e"} opacity={(e.opacity ?? 100) / 100} fontFamily={e.fontFamily === 3 ? "var(--font-jetbrains, 'JetBrains Mono'), ui-monospace, monospace" : "var(--font-inter, Inter), Helvetica, Arial, sans-serif"}>
      {lines.map((l, i) => <tspan key={i} x={x} y={top + i * lh + size * 0.9}>{l || " "}</tspan>)}
    </text>
  );
}

export default function ExcalidrawView({ scene, className = "", title }: { scene: Scene; className?: string; title: string }) {
  const els = scene.elements ?? [];
  if (!els.length) return null;
  const byId = new Map(els.map((e) => [e.id, e]));
  const b = bounds(els), pad = 20;
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox={`${b.minX - pad} ${b.minY - pad} ${b.w + 2 * pad} ${b.h + 2 * pad}`} className={`bg-white ${className}`} style={{ background: "#fff" }} role="img" aria-label={title}>
      {els.map((e) => (e.type === "text" ? <Text key={e.id} e={e} byId={byId} /> : <Shape key={e.id} e={e} />))}
    </svg>
  );
}

/** Parses a .excalidraw file; null when missing or unreadable. */
export function parseScene(json: string | null): Scene | null {
  try { return json ? (JSON.parse(json) as Scene) : null; } catch { return null; }
}
