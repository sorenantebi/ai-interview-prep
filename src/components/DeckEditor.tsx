"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import Markdown from "./Markdown";
import { api } from "@/lib/client";

type Draft = { front: string; back: string };

/** Edit a deck's cards (Markdown front and back), add and delete them; Save writes decks/<deck>.md. */
export default function DeckEditor({ file, name: initialName, cards: initial }: { file: string; name: string; cards: Draft[] }) {
  const router = useRouter();
  const [name, setName] = useState(initialName);
  const [cards, setCards] = useState(initial.length ? initial : [{ front: "", back: "" }]);
  const [saved, setSaved] = useState(JSON.stringify([initialName, initial]));
  const [preview, setPreview] = useState(false);
  const [error, setError] = useState("");
  const dirty = JSON.stringify([name, cards.filter((c) => c.front.trim())]) !== saved;
  const set = (i: number, k: keyof Draft, v: string) => setCards((cs) => cs.map((c, j) => (j === i ? { ...c, [k]: v } : c)));

  async function save() {
    try {
      const kept = cards.filter((c) => c.front.trim());
      await api("/api/cards", { action: "save", deck: file, name, cards: kept });
      setSaved(JSON.stringify([name, kept]));
      setError("");
      router.refresh();
    } catch (e) {
      setError((e as Error).message);
    }
  }
  async function del() {
    if (!confirm(`Delete the deck "${name}" and all its cards?`)) return;
    await api("/api/cards", { action: "delete", deck: file });
    router.push("/cards");
  }

  return (
    <div className="mx-auto max-w-5xl space-y-4">
      <Link href="/cards" className="font-mono text-xs text-muted hover:text-fg">← Cards</Link>
      <div className="flex flex-wrap items-center gap-2">
        <input className="input flex-1 font-display text-2xl font-medium" value={name} onChange={(e) => setName(e.target.value)} aria-label="Deck name" />
        <button className="btn" onClick={() => setPreview((p) => !p)}>{preview ? "Edit" : "Preview"}</button>
        <button className="btn-primary" disabled={!dirty} onClick={save}>{dirty ? "Save" : "Saved"}</button>
        <Link href={`/cards/review?deck=${encodeURIComponent(file)}`} className="btn">Review</Link>
        <button className="btn text-hard" onClick={del}>Delete deck</button>
      </div>
      {error && <p className="font-mono text-xs text-hard">{error}</p>}
      <p className="font-mono text-[11px] text-muted">{cards.filter((c) => c.front.trim()).length} cards · Markdown works on both sides · a card with an empty front is dropped on save · editing a front starts that card&apos;s schedule over</p>
      <ol className="space-y-2">
        {cards.map((c, i) => (
          <li key={i} className="card grid gap-2 p-3 md:grid-cols-[1fr_1fr_auto]">
            {preview ? (
              <>
                <div className="min-w-0 text-sm"><Markdown>{c.front}</Markdown></div>
                <div className="min-w-0 border-border text-sm md:border-l md:pl-3"><Markdown>{c.back}</Markdown></div>
              </>
            ) : (
              <>
                <textarea className="input resize-y text-sm" rows={Math.min(8, Math.max(2, c.front.split("\n").length))} value={c.front} onChange={(e) => set(i, "front", e.target.value)} placeholder="Front" aria-label={`Card ${i + 1} front`} />
                <textarea className="input resize-y text-sm" rows={Math.min(8, Math.max(2, c.back.split("\n").length))} value={c.back} onChange={(e) => set(i, "back", e.target.value)} placeholder="Back" aria-label={`Card ${i + 1} back`} />
              </>
            )}
            <button className="self-start px-2 text-muted hover:text-hard" onClick={() => setCards((cs) => cs.filter((_, j) => j !== i))} aria-label={`Delete card ${i + 1}`}>×</button>
          </li>
        ))}
      </ol>
      <button className="btn" onClick={() => { setPreview(false); setCards((cs) => [...cs, { front: "", back: "" }]); }}>+ card</button>
    </div>
  );
}
