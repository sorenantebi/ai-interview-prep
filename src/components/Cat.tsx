"use client";
import { useEffect, useRef, useState } from "react";

// The cat from Purr (github.com/sorenantebi/purr): its 32px-cell sprite sheet, recoloured white, same animation rows and
// idle → yawn/wash → wander behaviour. Here it walks left and right along a ledge just under the top bar
// (foot = the sprite's lowest pixel row in that animation, so its feet stay on one line).
const SHEET = "/cat/cat.png";
const CELL = 32;
const SCALE = 2;
const SIZE = CELL * SCALE;
const SPEED = 56; // px/s on screen (Purr: 18 px/s at 1×)
const ANIMS = {
  idle: { row: 16, cols: [0, 1], frameMs: 600, foot: 22 },
  walk_right: { row: 6, cols: [0, 1, 2, 3, 4, 5, 6, 7], frameMs: 60, foot: 24 },
  walk_left: { row: 7, cols: [0, 1, 2, 3, 4, 5, 6, 7], frameMs: 60, foot: 24 },
  yawn: { row: 35, cols: [0, 1, 2, 3, 4, 5, 6, 7], frameMs: 400, foot: 23 },
  wash: { row: 38, cols: [0, 1, 2, 3, 4, 5, 6], frameMs: 400, foot: 23 },
} as const;
type Anim = keyof typeof ANIMS;
type State = "idle" | "wander" | "yawn" | "wash" | "sit";

// White coat: the sheet's greys (body, shade, highlight) become white and light greys; the dark outline,
// eyes and nose keep their colours so the cat stays crisp on any background.
const WHITE: Record<string, [number, number, number]> = {
  "98,103,115": [246, 246, 248], // body
  "65,71,82": [204, 207, 214], // shade
  "134,141,155": [255, 255, 255], // highlight
};

function whiten(img: HTMLImageElement) {
  const c = document.createElement("canvas");
  c.width = img.width;
  c.height = img.height;
  const ctx = c.getContext("2d")!;
  ctx.drawImage(img, 0, 0);
  const data = ctx.getImageData(0, 0, c.width, c.height), d = data.data;
  for (let i = 0; i < d.length; i += 4) {
    const to = d[i + 3] ? WHITE[`${d[i]},${d[i + 1]},${d[i + 2]}`] : undefined;
    if (to) [d[i], d[i + 1], d[i + 2]] = to;
  }
  ctx.putImageData(data, 0, 0);
  return c;
}

export default function Cat() {
  const canvas = useRef<HTMLCanvasElement>(null);
  const box = useRef<HTMLButtonElement>(null);
  const cat = useRef({ x: 0, target: 0, facing: "right" as "left" | "right", state: "idle" as State, next: "wander" as State, timer: 2000, frame: 0, elapsed: 0 });
  const [hearts, setHearts] = useState<number[]>([]);
  const [pets, setPets] = useState(0);
  const [purring, setPurring] = useState(false);

  useEffect(() => {
    try { setPets(Number(localStorage.getItem("cat-pets")) || 0); } catch {}
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const ledge = () => document.querySelector("header")?.getBoundingClientRect().bottom ?? 56;
    const range = () => [16, window.innerWidth - SIZE - 16];
    const c = cat.current;
    c.x = c.target = window.innerWidth * 0.8;
    let sheet: HTMLCanvasElement | null = null, raf = 0, last = performance.now();
    const img = new Image();
    img.onload = () => { sheet = whiten(img); };
    img.src = SHEET;

    const anim = (): Anim => (c.state === "wander" ? (c.facing === "left" ? "walk_left" : "walk_right") : c.state === "yawn" || c.state === "wash" ? c.state : "idle");
    const tick = (now: number) => {
      const dt = Math.min(50, now - last);
      last = now;
      const a = ANIMS[anim()];
      c.elapsed += dt;
      if (c.elapsed >= a.frameMs) { c.elapsed = 0; c.frame = (c.frame + 1) % a.cols.length; }

      // Purr's state machine, minus sleeping in the sun.
      if (c.state === "idle" && !reduced) {
        c.timer -= dt;
        if (c.timer <= 0) {
          c.state = Math.random() < 0.4 ? "wash" : "yawn";
          c.timer = c.state === "wash" ? 3600 : 2400;
          c.next = Math.random() < 0.75 ? "wander" : "idle";
          c.frame = 0;
        }
      } else if (c.state === "yawn" || c.state === "wash") {
        c.timer -= dt;
        if (c.timer <= 0) {
          c.state = c.next;
          c.frame = 0;
          c.timer = 4000 + Math.random() * 8000;
          if (c.state === "wander") { const [lo, hi] = range(); c.target = lo + Math.random() * (hi - lo); }
        }
      } else if (c.state === "wander") {
        const d = c.target - c.x;
        if (Math.abs(d) < 1) { c.state = "idle"; c.frame = 0; c.timer = 4000 + Math.random() * 8000; }
        else { c.x += Math.sign(d) * Math.min(Math.abs(d), (SPEED * dt) / 1000); c.facing = d > 0 ? "right" : "left"; }
      }

      const [lo, hi] = range();
      c.x = Math.min(hi, Math.max(lo, c.x));
      const feet = ledge() + 42; // the ledge: just enough room for the cat (ears up when walking) under the top bar
      if (box.current) box.current.style.transform = `translate(${Math.round(c.x)}px, ${Math.round(feet - (ANIMS[anim()].foot + 1) * SCALE)}px)`;
      const ctx = canvas.current?.getContext("2d");
      if (ctx && sheet) {
        ctx.clearRect(0, 0, CELL, CELL);
        const cur = ANIMS[anim()];
        ctx.drawImage(sheet, cur.cols[c.frame % cur.cols.length] * CELL, cur.row * CELL, CELL, CELL, 0, 0, CELL, CELL);
      }
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, []);

  function pet() {
    const c = cat.current;
    c.state = "sit";
    c.frame = 0;
    setPurring(true);
    const id = Date.now();
    setHearts((h) => [...h, id, id + 1, id + 2]);
    setPets((n) => {
      try { localStorage.setItem("cat-pets", String(n + 1)); } catch {}
      return n + 1;
    });
    setTimeout(() => setHearts((h) => h.filter((x) => x < id || x > id + 2)), 1600);
    setTimeout(() => { setPurring(false); if (c.state === "sit") { c.state = "idle"; c.timer = 800 + Math.random() * 1200; } }, 2600);
  }

  return (
    <button
      ref={box}
      onClick={pet}
      tabIndex={-1}
      aria-label={`Pet the cat (petted ${pets} times)`}
      title={`purr… petted ${pets}×`}
      className="fixed left-0 top-0 z-40 cursor-pointer select-none"
      style={{ width: SIZE, height: SIZE, willChange: "transform" }}
    >
      <canvas ref={canvas} width={CELL} height={CELL} className="h-full w-full [image-rendering:pixelated]" />
      {hearts.map((h, i) => (
        <span key={h} className="cat-heart pointer-events-none absolute font-mono text-lg text-[#f386a1]" style={{ left: SIZE * 0.5 + (i % 3) * 12 - 12, top: 4, animationDelay: `${(i % 3) * 120}ms` }}>♥</span>
      ))}
      {purring && <span className="cat-heart pointer-events-none absolute left-1/2 top-0 font-mono text-xs text-fg">purr</span>}
    </button>
  );
}
