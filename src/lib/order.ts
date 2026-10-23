/** Deterministic shuffle (mulberry32 + Fisher-Yates), so a seed in the URL keeps the same random order across pages. */
export function shuffle<T>(items: T[], seed: number): T[] {
  const out = [...items];
  let s = seed >>> 0;
  const rand = () => {
    s = (s + 0x6d2b79f5) >>> 0;
    let t = s;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(rand() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

export type Order = { random: boolean; seed: number; unsolved: boolean };

export const orderQuery = (o: Order) => (o.random ? `?order=random&seed=${o.seed}${o.unsolved ? "&only=unsolved" : ""}` : "");

/** The sequence prev/next walks: roadmap order, or a seeded shuffle (optionally only unsolved, always keeping `current`). */
export function sequence(paths: string[], o: Order, solved: Set<string>, current?: string): string[] {
  const pool = o.unsolved ? paths.filter((p) => !solved.has(p) || p === current) : paths;
  return o.random ? shuffle(pool, o.seed) : pool;
}
