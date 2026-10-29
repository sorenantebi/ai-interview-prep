import crypto from "node:crypto";
import fs from "node:fs/promises";
import { localDate, read, safePath, write } from "./content.ts";

export type Card = { id: string; front: string; back: string };
export type Deck = { file: string; name: string; cards: Card[] };
export type Grade = 1 | 2 | 3 | 4; // Again, Hard, Good, Easy (like Anki)
export type CardState = { due: string; ivl: number; ease: number; reps: number; lapses: number; first: string };
export type Schedule = Record<string, CardState>; // "<deck file>/<card id>" -> its schedule

export const NEW_PER_DAY = 20; // new cards per deck per day, Anki's default
const DIR = "decks";

/** A deck's file name (no ".md") from any name: no slashes or odd characters, so it's a safe path. */
export const deckFile = (name: string) => name.replace(/::|\x1f/g, " - ").replace(/[^\w .()&+,'-]+/g, "_").replace(/^[\s.]+|\s+$/g, "").slice(0, 100) || "Deck";
export const cardKey = (deck: string, id: string) => `${deck}/${id}`;
export const deckPath = (file: string) => {
  if (file !== deckFile(file)) throw new Error("Bad deck name");
  return `${DIR}/${file}.md`;
};

/**
 * A deck file: `# Deck name`, then per card `## <front>` (more front lines may follow), `### Answer`, then the back.
 * shortcut: a card's id is a hash of its front, so editing the front starts its schedule over; store ids in the file if that matters.
 */
export function parseDeck(file: string, md: string): Deck {
  const [head, ...parts] = md.split(/^## /m);
  const name = head.match(/^# (.+)$/m)?.[1].trim() || file;
  const seen = new Map<string, number>();
  const cards = parts.map((p) => {
    const [front, back = ""] = p.split(/^### Answer[ \t]*$/m);
    let id = crypto.createHash("sha1").update(front.trim()).digest("hex").slice(0, 12);
    const n = (seen.get(id) ?? 0) + 1;
    seen.set(id, n);
    if (n > 1) id += `-${n}`; // the same front twice
    return { id, front: front.trim(), back: back.trim() };
  });
  return { file, name, cards };
}

export function deckToMd(name: string, cards: { front: string; back: string }[]) {
  // A front or back line starting with "## " / "### Answer" would split the card when read back: indent it by a space.
  const safe = (s: string) => s.trim().replace(/^(##|### Answer)/gm, " $1");
  return `# ${name.trim()}\n\n` + cards.filter((c) => c.front.trim()).map((c) => `## ${safe(c.front)}\n### Answer\n${safe(c.back)}\n`).join("\n");
}

export async function decks(): Promise<Deck[]> {
  const files = (await fs.readdir(safePath(DIR)).catch(() => [] as string[])).filter((f) => f.endsWith(".md")).sort();
  return Promise.all(files.map(async (f) => parseDeck(f.slice(0, -3), (await read(`${DIR}/${f}`)) ?? "")));
}

export async function deck(file: string): Promise<Deck | null> {
  const md = await read(deckPath(file));
  return md === null ? null : parseDeck(file, md);
}

/** Saves a deck under a new file name, adding " (2)" etc. instead of overwriting another deck. */
export async function newDeck(name: string, cards: { front: string; back: string }[]): Promise<string> {
  const base = deckFile(name);
  for (let n = 1; ; n++) {
    const file = n === 1 ? base : `${base} (${n})`;
    if ((await read(deckPath(file))) === null) {
      await write(deckPath(file), deckToMd(name, cards));
      return file;
    }
  }
}

export async function schedule(): Promise<Schedule> {
  try { return JSON.parse((await read("cards.json")) ?? "{}"); } catch { return {}; }
}

const addDays = (day: string, n: number) => {
  const d = new Date(day + "T12:00:00");
  d.setDate(d.getDate() + n);
  return localDate(d);
};

/**
 * Anki's SM-2: Again relearns the card today (it comes back in this session), Hard/Good/Easy grow its interval in days.
 * A new card: Again today, Hard and Good tomorrow, Easy in 4 days.
 */
export function next(s: CardState | undefined, g: Grade, today: string): CardState {
  const cur = s ?? { due: today, ivl: 0, ease: 2.5, reps: 0, lapses: 0, first: today };
  let { ivl, ease, lapses } = cur;
  if (g === 1) {
    if (cur.reps > 0 && cur.ivl > 0) lapses++;
    ease = s ? Math.max(1.3, ease - 0.2) : ease;
    ivl = 0;
  } else if (!s || cur.ivl === 0) {
    ivl = g === 4 ? 4 : 1; // new or relearning
  } else if (g === 2) {
    ivl = Math.max(cur.ivl + 1, Math.round(cur.ivl * 1.2));
    ease = Math.max(1.3, ease - 0.15);
  } else if (g === 3) {
    ivl = Math.max(cur.ivl + 1, Math.round(cur.ivl * ease));
  } else {
    ivl = Math.max(cur.ivl + 1, Math.round(cur.ivl * ease * 1.3));
    ease += 0.15;
  }
  return { due: addDays(today, ivl), ivl, ease: Math.round(ease * 100) / 100, reps: cur.reps + 1, lapses, first: cur.first };
}

/** What each button would schedule, for the button labels ("now" means again in this session). */
export const preview = (s: CardState | undefined, today: string) =>
  ([1, 2, 3, 4] as Grade[]).map((g) => {
    const d = next(s, g, today).ivl;
    return d === 0 ? "now" : d < 30 ? `${d}d` : d < 365 ? `${Math.round(d / 30)}mo` : `${(d / 365).toFixed(1)}y`;
  });

/** Today's cards in a deck: reviews due (oldest first), then new cards up to NEW_PER_DAY minus those already started today. */
export function dueToday(d: Deck, sched: Schedule, today: string) {
  const due: Card[] = [], fresh: Card[] = [];
  let startedToday = 0;
  for (const c of d.cards) {
    const s = sched[cardKey(d.file, c.id)];
    if (!s) fresh.push(c);
    else {
      if (s.first === today) startedToday++;
      if (s.due <= today) due.push(c);
    }
  }
  due.sort((a, b) => sched[cardKey(d.file, a.id)].due.localeCompare(sched[cardKey(d.file, b.id)].due));
  const newToday = fresh.slice(0, Math.max(0, NEW_PER_DAY - startedToday));
  return { due, fresh: newToday, total: d.cards.length };
}

let saving: Promise<unknown> = Promise.resolve();

/** Grades one card and saves its next review. Grades are saved one at a time, so two quick ones can't overwrite each other. */
export function gradeCard(deckName: string, id: string, g: Grade, today = localDate(new Date())): Promise<CardState> {
  const run = saving.then(async () => {
    const sched = await schedule();
    const key = cardKey(deckName, id);
    sched[key] = next(sched[key], g, today);
    await write("cards.json", JSON.stringify(sched, null, 1));
    return sched[key];
  });
  saving = run.catch(() => {});
  return run;
}
