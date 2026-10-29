import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import zlib from "node:zlib";

export type ImportedDeck = { name: string; cards: { front: string; back: string }[] };
export type Imported = { decks: ImportedDeck[]; media: Record<string, Uint8Array> };

const IMAGE = /\.(png|jpe?g|gif|webp|avif)$/i; // images only: sounds can't play here, and SVGs could carry scripts

/** The files in a .zip (an .apkg is one): stored or deflated entries, no zip64. */
export function unzip(buf: Buffer): Record<string, Buffer> {
  let eocd = buf.length - 22;
  while (eocd >= 0 && buf.readUInt32LE(eocd) !== 0x06054b50) eocd--;
  if (eocd < 0) throw new Error("Not a zip file (an .apkg should be one)");
  const out: Record<string, Buffer> = {};
  let p = buf.readUInt32LE(eocd + 16);
  for (let i = buf.readUInt16LE(eocd + 10); i > 0; i--) {
    if (buf.readUInt32LE(p) !== 0x02014b50) throw new Error("Damaged zip file");
    const method = buf.readUInt16LE(p + 10), size = buf.readUInt32LE(p + 20);
    const nameLen = buf.readUInt16LE(p + 28), extraLen = buf.readUInt16LE(p + 30), commentLen = buf.readUInt16LE(p + 32);
    const local = buf.readUInt32LE(p + 42);
    const name = buf.toString("utf8", p + 46, p + 46 + nameLen);
    const start = local + 30 + buf.readUInt16LE(local + 26) + buf.readUInt16LE(local + 28);
    const data = buf.subarray(start, start + size);
    out[name] = method === 0 ? data : method === 8 ? zlib.inflateRawSync(data) : Buffer.alloc(0);
    p += 46 + nameLen + extraLen + commentLen;
  }
  return out;
}

// Newer Anki exports compress the collection and media with zstd.
const ZSTD = Buffer.from([0x28, 0xb5, 0x2f, 0xfd]);
const unzstd = (b: Buffer): Buffer => {
  if (!b.subarray(0, 4).equals(ZSTD)) return b;
  const z = zlib as unknown as { zstdDecompressSync?: (b: Buffer) => Buffer }; // Node 22.15+, newer than our @types/node
  if (!z.zstdDecompressSync) throw new Error("This Anki file needs Node 22.15 or newer to read (or export it with \"Support older Anki versions\" ticked)");
  return z.zstdDecompressSync(b);
};

/** Media names by zip entry ("0", "1", …): JSON in older exports, a protobuf list (field 1 = entry, its field 1 = name) in newer ones. */
function mediaNames(raw: Buffer | undefined): Record<string, string> {
  if (!raw?.length) return {};
  const b = unzstd(raw);
  if (b[0] === 0x7b) return JSON.parse(b.toString("utf8"));
  const names: Record<string, string> = {};
  let i = 0, n = 0;
  const varint = (buf: Buffer, at: number): [number, number] => {
    let v = 0, shift = 0, x;
    do { x = buf[at++]; v += (x & 0x7f) * 2 ** shift; shift += 7; } while (x & 0x80);
    return [v, at];
  };
  while (i < b.length) {
    const [tag, a] = varint(b, i);
    const [len, s] = varint(b, a);
    if (tag !== 0x0a) break;
    const entry = b.subarray(s, s + len);
    let j = 0;
    while (j < entry.length) {
      const [t, k] = varint(entry, j);
      if ((t & 7) === 0) { j = varint(entry, k)[1]; continue; }
      const [l, m] = varint(entry, k);
      if (t === 0x0a) names[String(n)] = entry.toString("utf8", m, m + l);
      j = m + l;
    }
    n++;
    i = s + len;
  }
  return names;
}

const ENTITIES: Record<string, string> = { nbsp: " ", amp: "&", lt: "<", gt: ">", quot: '"', apos: "'" };

/** Anki field HTML -> Markdown: line breaks, bold/italic/code, lists, images (as URLs from `img`); other tags dropped. */
export function htmlToMd(html: string, img: (name: string) => string | null = () => null): string {
  return html
    .replace(/\[sound:[^\]]*\]/g, "")
    .replace(/<img[^>]*src=["']?([^"'\s>]+)["']?[^>]*>/gi, (_, src) => { const url = img(decodeURIComponent(src)); return url ? `![](${url})` : ""; })
    .replace(/<pre[^>]*>([\s\S]*?)<\/pre>/gi, (_, code) => "\n```\n" + code.replace(/<br\s*\/?>/gi, "\n").replace(/<[^>]+>/g, "") + "\n```\n")
    .replace(/<br\s*\/?>|<\/(div|p|h\d|tr)>/gi, "\n")
    .replace(/<li[^>]*>/gi, "\n- ")
    .replace(/<\/?(b|strong)>/gi, "**")
    .replace(/<\/?(i|em)>/gi, "*")
    .replace(/<\/?code>/gi, "`")
    .replace(/<[^>]+>/g, "")
    .replace(/&(#x?[0-9a-f]+|\w+);/gi, (m, e: string) => e[0] === "#" ? String.fromCodePoint(e[1].toLowerCase() === "x" ? parseInt(e.slice(2), 16) : Number(e.slice(1))) : ENTITIES[e.toLowerCase()] ?? m)
    .replace(/\*{4}/g, "") // an empty <b></b>
    .replace(/[ \t]+\n/g, "\n")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

/** A note's fields -> front/back. Cloze notes ({{c1::answer::hint}}) hide the deletions on the front and bold them on the back. */
export function noteToCard(fields: string[], img?: (name: string) => string | null) {
  const [first = "", second = "", ...rest] = fields.map((f) => htmlToMd(f, img));
  if (/\{\{c\d+::/.test(first)) {
    const cloze = /\{\{c\d+::([\s\S]*?)(?:::([\s\S]*?))?\}\}/g;
    return { front: first.replace(cloze, (_, _a, hint) => `[${hint ?? "…"}]`), back: [first.replace(cloze, "**$1**"), second].filter(Boolean).join("\n\n") };
  }
  return { front: first, back: [second, ...rest].filter(Boolean).join("\n\n") };
}

/** An .apkg: its decks (cards in Anki's order, one per note) and the images they use. Anki's own review history isn't kept. */
export async function importApkg(buf: Buffer, mediaUrl: (name: string) => string): Promise<Imported> {
  const files = unzip(buf);
  const col = files["collection.anki21b"] ? unzstd(files["collection.anki21b"]) : files["collection.anki21"] ?? files["collection.anki2"];
  if (!col) throw new Error("No Anki collection in this file");
  const names = mediaNames(files["media"]);
  const media: Record<string, Uint8Array> = {};
  for (const [entry, name] of Object.entries(names)) if (IMAGE.test(name) && files[entry]) media[path.basename(name)] = unzstd(files[entry]);
  const img = (name: string) => (media[path.basename(name)] ? mediaUrl(path.basename(name)) : null);

  type Db = { prepare(sql: string): { all(): unknown[]; get(): unknown }; close(): void };
  // Loaded at runtime (Node 22.5+), so the bundler and our older @types/node don't need to know node:sqlite.
  const sqlite = (process as unknown as { getBuiltinModule?: (id: string) => { DatabaseSync: new (file: string, opts: { readOnly: boolean }) => Db } | undefined }).getBuiltinModule?.("node:sqlite");
  if (!sqlite) throw new Error("Importing .apkg files needs Node 22.15 or newer");
  const { DatabaseSync } = sqlite;
  const tmp = await fs.mkdtemp(path.join(os.tmpdir(), "prep-anki-"));
  try {
    await fs.writeFile(path.join(tmp, "c.db"), col);
    const db = new DatabaseSync(path.join(tmp, "c.db"), { readOnly: true });
    try {
      const deckNames = new Map<number, string>();
      try {
        for (const r of db.prepare("SELECT id, name FROM decks").all() as { id: number; name: string }[]) deckNames.set(Number(r.id), r.name.replaceAll("\x1f", "::"));
      } catch {
        const json = (db.prepare("SELECT decks FROM col").get() as { decks: string }).decks;
        for (const d of Object.values(JSON.parse(json || "{}")) as { id: number; name: string }[]) deckNames.set(Number(d.id), d.name);
      }
      const rows = db.prepare("SELECT n.flds AS flds, MIN(c.did) AS did FROM notes n JOIN cards c ON c.nid = n.id GROUP BY n.id ORDER BY MIN(c.due), n.id").all() as { flds: string; did: number }[];
      const byDeck = new Map<string, ImportedDeck>();
      for (const r of rows) {
        const name = deckNames.get(Number(r.did)) ?? "Imported";
        if (!byDeck.has(name)) byDeck.set(name, { name, cards: [] });
        const card = noteToCard(r.flds.split("\x1f"), img);
        if (card.front) byDeck.get(name)!.cards.push(card);
      }
      const decks = [...byDeck.values()].filter((d) => d.cards.length);
      if (!decks.length) throw new Error("No cards in this file. (An .apkg exported by a very new Anki may say \"please update\": export with \"Support older Anki versions\" ticked.)");
      return { decks, media };
    } finally {
      db.close();
    }
  } finally {
    await fs.rm(tmp, { recursive: true, force: true });
  }
}

/** Anki's "Notes in Plain Text" export: one note per line, fields separated by tabs, `#key:value` header lines. */
export function importTxt(text: string, name: string): Imported {
  const cards = text.split(/\r?\n/).filter((l) => l.trim() && !l.startsWith("#")).map((l) => noteToCard(l.split("\t").map((f) => f.replace(/^"([\s\S]*)"$/, "$1").replaceAll('""', '"'))));
  return { decks: [{ name, cards: cards.filter((c) => c.front) }], media: {} };
}
