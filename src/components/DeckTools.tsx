"use client";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { api } from "@/lib/client";

/** Import from Anki, generate with Claude, or start an empty deck. */
export default function DeckTools({ decks }: { decks: { file: string; name: string }[] }) {
  const router = useRouter();
  const [busy, setBusy] = useState<string | null>(null);
  const [msg, setMsg] = useState<{ ok: boolean; text: string } | null>(null);
  const [topic, setTopic] = useState("");
  const [count, setCount] = useState(15);
  const [into, setInto] = useState("");
  const [name, setName] = useState("");

  async function go(label: string, work: () => Promise<string>) {
    setBusy(label);
    setMsg(null);
    try {
      setMsg({ ok: true, text: await work() });
      router.refresh();
    } catch (e) {
      setMsg({ ok: false, text: (e as Error).message });
    } finally {
      setBusy(null);
    }
  }

  async function upload(file: File) {
    const form = new FormData();
    form.append("file", file);
    const res = await fetch("/api/cards", { method: "POST", body: form });
    const data = await res.json();
    if (!res.ok || data.error) throw new Error(data.error ?? `Import failed (${res.status})`);
    return "Imported " + data.decks.map((d: { file: string; cards: number }) => `${d.file} (${d.cards} cards)`).join(", ");
  }

  return (
    <div className="grid gap-4 md:grid-cols-3">
      <section className="card space-y-3 p-4">
        <h2 className="font-medium">Import from Anki</h2>
        <p className="text-sm text-muted">An <code>.apkg</code> (File → Export → Anki Deck Package) or a plain-text export. Each Anki deck becomes a deck here, with its images. Anki&apos;s review history isn&apos;t imported: cards start as new.</p>
        <label className={`btn inline-block cursor-pointer ${busy ? "pointer-events-none opacity-50" : ""}`}>
          Choose file…
          <input type="file" accept=".apkg,.colpkg,.txt,.tsv" className="hidden" onChange={(e) => { const f = e.target.files?.[0]; e.target.value = ""; if (f) go("Importing…", () => upload(f)); }} />
        </label>
      </section>
      <form className="card space-y-3 p-4" onSubmit={(e) => { e.preventDefault(); go("Claude is writing cards…", async () => { const r = await api("/api/cards", { action: "generate", topic, count, deck: into || undefined }); setTopic(""); return `Added ${r.added} cards to ${r.file}`; }); }}>
        <h2 className="font-medium">Generate with Claude</h2>
        <textarea className="input" rows={2} required value={topic} onChange={(e) => setTopic(e.target.value)} placeholder="e.g. C++ move semantics, or: Kafka partitions and consumer groups" />
        <div className="flex flex-wrap gap-2">
          <label className="flex items-center gap-1 text-sm text-muted">Cards <input type="number" min={1} max={50} className="input w-16 py-1" value={count} onChange={(e) => setCount(Number(e.target.value))} /></label>
          <select className="input flex-1 py-1" value={into} onChange={(e) => setInto(e.target.value)} aria-label="Deck">
            <option value="">New deck</option>
            {decks.map((d) => <option key={d.file} value={d.file}>Add to {d.name}</option>)}
          </select>
        </div>
        <button className="btn-primary" disabled={!!busy}>Generate</button>
      </form>
      <form className="card space-y-3 p-4" onSubmit={(e) => { e.preventDefault(); go("Creating…", async () => { const r = await api("/api/cards", { action: "create", name }); router.push(`/cards/${encodeURIComponent(r.file)}`); return `Created ${r.file}`; }); }}>
        <h2 className="font-medium">New deck</h2>
        <input className="input" required value={name} onChange={(e) => setName(e.target.value)} placeholder="Deck name" />
        <button className="btn" disabled={!!busy}>Create and edit</button>
      </form>
      {(busy || msg) && (
        <p className={`md:col-span-3 whitespace-pre-wrap font-mono text-xs ${busy ? "text-muted" : msg?.ok ? "text-easy" : "text-hard"}`}>{busy ?? msg?.text}</p>
      )}
    </div>
  );
}
