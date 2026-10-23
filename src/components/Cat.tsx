"use client";
import { useEffect, useRef, useState } from "react";
import { CAT_COLORS, CAT_FRAMES, type CatFrame } from "./cat-frames";

const S = 1; // screen pixels per sprite pixel
const W = 48 * S;
const H = 36 * S;
const SPEED = 45; // px per second
const WALK = ["walk1", "walk2", "walk3", "walk4"] as const; // ball feet: back foot hops forward, together, front foot hops forward, together
const STEP = 0.14; // seconds per walk frame


function Sprite({ frame }: { frame: CatFrame }) {
  return (
    <svg width={W} height={H} viewBox="0 0 48 36" shapeRendering="crispEdges" aria-hidden>
      {CAT_FRAMES[frame].flatMap((row, y) => [...row].map((c, x) => (c === "." ? null : <rect key={`${x}-${y}`} x={x} y={y} width={1} height={1} fill={CAT_COLORS[c]} />)))}
    </svg>
  );
}

type Pose = [x: number, y: number, rot: number]; // feet centre + rotation in degrees

/**
 * The cat walks a loop round the screen with its feet on whatever it walks on: upright on a ledge under the top bar,
 * feet against the right edge going down, upright on the bottom edge, feet against the left edge going up.
 * At a corner it simply hops onto the next edge. `s` is the distance along the loop (clockwise).
 */
function geometry(navBottom: number) {
  const vw = window.innerWidth, vh = window.innerHeight, y0 = navBottom + H, m = W / 2;
  const edges: [Pose, Pose][] = [
    [[m, y0, 0], [vw - m, y0, 0]], // top ledge
    [[vw, y0 + m, -90], [vw, vh - m, -90]], // right edge, feet on the wall
    [[vw - m, vh, 0], [m, vh, 0]], // bottom edge
    [[0, vh - m, 90], [0, y0 + m, 90]], // left edge, feet on the wall
  ];
  const lens = edges.map(([a, b]) => Math.hypot(b[0] - a[0], b[1] - a[1]));
  const starts = lens.map((_, i) => lens.slice(0, i).reduce((n, l) => n + l, 0));
  const P = starts[3] + lens[3];
  const place = (s: number): Pose => {
    s = ((s % P) + P) % P;
    let i = 3;
    while (i > 0 && starts[i] > s) i--;
    const [a, b] = edges[i], t = lens[i] ? (s - starts[i]) / lens[i] : 0;
    return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2]];
  };
  // Mostly the top ledge, sometimes partway down a side, rarely anywhere.
  const target = () => {
    const r = Math.random();
    if (r < 0.7) return lens[0] * (0.05 + 0.9 * Math.random());
    if (r < 0.92) return Math.random() < 0.5 ? starts[1] + lens[1] * 0.45 * Math.random() : P - lens[3] * 0.45 * Math.random();
    return P * Math.random();
  };
  return { P, place, target };
}

export default function Cat() {
  const el = useRef<HTMLButtonElement>(null);
  const [frame, setFrame] = useState<CatFrame>("stand");
  const [hearts, setHearts] = useState<number[]>([]);
  const [pets, setPets] = useState(0);
  const petting = useRef(false);

  useEffect(() => {
    try { setPets(Number(localStorage.getItem("cat-pets")) || 0); } catch {}
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const navBottom = () => document.querySelector("header")?.getBoundingClientRect().bottom ?? 56;
    let g = geometry(navBottom());
    let s = window.innerWidth * 0.8, goal = s, pauseUntil = 0, last = performance.now(), step = 0, raf = 0;
    const onResize = () => { g = geometry(navBottom()); };
    window.addEventListener("resize", onResize);

    const tick = (now: number) => {
      const dt = Math.min(0.05, (now - last) / 1000);
      last = now;
      let moving = false, dir = 1;
      if (!petting.current && !reduced && now > pauseUntil) {
        // Walk the shorter way round the loop.
        let d = ((goal - s) % g.P + g.P) % g.P;
        if (d > g.P / 2) d -= g.P;
        if (Math.abs(d) < 1) {
          pauseUntil = now + 1200 + Math.random() * 3500;
          goal = g.target();
        } else {
          dir = Math.sign(d);
          s += dir * Math.min(Math.abs(d), SPEED * dt);
          moving = true;
        }
      }
      const [x, y, rot] = g.place(s);
      // Face the way it walks: compare the movement with the sprite's local "forward" (+x) after rotation.
      const [nx, ny] = g.place(s + dir);
      const r = (rot * Math.PI) / 180, along = (nx - x) * Math.cos(r) + (ny - y) * Math.sin(r);
      const faceRight = moving && Math.abs(along) > 0.01 ? along > 0 : el.current?.dataset.face !== "l";
      if (el.current) {
        el.current.dataset.face = faceRight ? "r" : "l";
        el.current.style.transform = `translate(${x}px, ${y}px) rotate(${rot}deg) scaleX(${faceRight ? 1 : -1}) translate(${-W / 2}px, ${-H}px)`;
      }
      if (!petting.current) {
        step = moving ? step + dt : 0;
        setFrame(moving ? WALK[Math.floor(step / STEP) % WALK.length] : "stand");
      }
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => { cancelAnimationFrame(raf); window.removeEventListener("resize", onResize); };
  }, []);

  function pet() {
    petting.current = true;
    setFrame("pet");
    const id = Date.now();
    setHearts((h) => [...h, id, id + 1, id + 2]);
    setPets((n) => {
      try { localStorage.setItem("cat-pets", String(n + 1)); } catch {}
      return n + 1;
    });
    setTimeout(() => setHearts((h) => h.filter((x) => x < id || x > id + 2)), 1600);
    setTimeout(() => { petting.current = false; }, 2600);
  }

  return (
    <button
      ref={el}
      onClick={pet}
      tabIndex={-1}
      aria-label={`Pet the cat (petted ${pets} times)`}
      title={`purr… petted ${pets}×`}
      className="fixed left-0 top-0 z-40 cursor-pointer select-none"
      style={{ width: W, height: H, transformOrigin: "0 0", willChange: "transform" }}
    >
      <Sprite frame={frame} />
      {hearts.map((h, i) => (
        <span key={h} className="cat-heart pointer-events-none absolute font-mono text-lg text-[#f386a1]" style={{ left: W * 0.55 + (i % 3) * 12 - 12, top: -4, animationDelay: `${(i % 3) * 120}ms` }}>♥</span>
      ))}
      {frame === "pet" && <span className="cat-heart pointer-events-none absolute -top-5 left-1/2 font-mono text-xs text-fg">purr</span>}
    </button>
  );
}
