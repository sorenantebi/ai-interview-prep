import { NextRequest, NextResponse } from "next/server";
import { localDate, logActivity, remove, safePath, write } from "@/lib/content";
import { deck, deckPath, deckToMd, gradeCard, newDeck, parseDeck, preview, type Grade } from "@/lib/cards";
import { importApkg, importTxt } from "@/lib/anki";
import { claude, files, prompt } from "@/lib/claude";

const MAX_UPLOAD = 300 * 1024 * 1024; // decks with images get big
const fail = (e: unknown) => NextResponse.json({ error: (e as Error).message }, { status: 400 });
const text = (v: unknown, max = 20_000) => typeof v === "string" && v.length <= max;

/** Upload an .apkg or Anki's plain-text export: each Anki deck becomes a decks/<name>.md, its images go to decks/media/. */
async function upload(req: NextRequest) {
  const file = (await req.formData()).get("file");
  if (!(file instanceof File)) throw new Error("No file");
  if (file.size > MAX_UPLOAD) throw new Error("Files up to 300 MB");
  const buf = Buffer.from(await file.arrayBuffer());
  const stem = file.name.replace(/\.[^.]+$/, "");
  const media = (name: string) => `/api/files/raw?path=${encodeURIComponent(`decks/media/${name}`)}`;
  const got = /\.(apkg|colpkg)$/i.test(file.name) ? await importApkg(buf, media) : importTxt(buf.toString("utf8"), stem);
  for (const [name, data] of Object.entries(got.media)) {
    safePath(`decks/media/${name}`);
    await write(`decks/media/${name}`, data);
  }
  const made = [];
  for (const d of got.decks) made.push({ file: await newDeck(d.name === "Default" ? stem : d.name, d.cards), cards: d.cards.length });
  return made;
}

/**
 * Multipart: import a deck file. JSON actions:
 * grade { deck, id, grade 1-4 } -> the card's next button labels · save { deck, name, cards } · create { name } · delete { deck } · generate { topic, count, deck? }
 */
export async function POST(req: NextRequest) {
  if (req.headers.get("content-type")?.startsWith("multipart/form-data")) {
    try { return NextResponse.json({ decks: await upload(req) }); } catch (e) { return fail(e); }
  }
  const b = await req.json();
  try {
    switch (b.action) {
      case "grade": {
        if (![1, 2, 3, 4].includes(b.grade) || !text(b.id, 40) || !(await deck(b.deck))) throw new Error("Bad grade");
        const s = await gradeCard(b.deck, b.id, b.grade as Grade);
        await logActivity();
        return NextResponse.json({ labels: preview(s, localDate(new Date())) }); // for the card coming back after Again
      }
      case "save": {
        const cards = b.cards;
        if (!text(b.name, 200) || !Array.isArray(cards) || !cards.every((c) => text(c?.front) && text(c?.back))) throw new Error("Bad deck");
        await write(deckPath(b.deck), deckToMd(b.name, cards));
        return NextResponse.json({ ok: true });
      }
      case "create": {
        if (!text(b.name, 200) || !b.name.trim()) throw new Error("Give the deck a name");
        return NextResponse.json({ file: await newDeck(b.name, []) });
      }
      case "delete": {
        deckPath(b.deck);
        await remove(deckPath(b.deck)); // its schedule stays in cards.json, harmless
        return NextResponse.json({ ok: true });
      }
      case "generate": {
        const count = Math.min(50, Math.max(1, Number(b.count) || 15));
        if (!text(b.topic, 2000) || !b.topic.trim()) throw new Error("Give a topic");
        const existing = b.deck ? await deck(b.deck) : null;
        const avoid = existing?.cards.map((c) => `- ${c.front.split("\n")[0]}`).join("\n") || "none";
        const reply = (await claude(await prompt("generate-deck", { topic: b.topic.trim(), count: String(count), existing: avoid }))).text;
        const got = parseDeck("new", files(reply)["deck.md"] ?? reply); // the cards, with or without the file wrapper
        if (!got.cards.length) throw new Error("Claude's reply had no cards:\n\n" + reply.slice(0, 1500));
        if (existing) {
          await write(deckPath(existing.file), deckToMd(existing.name, [...existing.cards, ...got.cards]));
          return NextResponse.json({ file: existing.file, added: got.cards.length });
        }
        return NextResponse.json({ file: await newDeck(got.name === "new" ? b.topic.trim() : got.name, got.cards), added: got.cards.length });
      }
    }
    throw new Error(`Unknown action ${b.action}`);
  } catch (e) {
    return fail(e);
  }
}
