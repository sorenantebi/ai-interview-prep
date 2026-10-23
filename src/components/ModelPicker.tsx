"use client";
import { useState } from "react";
import { api } from "@/lib/client";

/** Picks the model for every AI feature in the app (saved to content/settings.json). */
export default function ModelPicker({ models, initial, defaultName }: { models: { id: string; label: string; group: string }[]; initial: string; defaultName: string | null }) {
  const [model, setModel] = useState(initial);
  const [error, setError] = useState("");
  // Keep an older pick visible even though it's no longer in the list.
  const shown = models.filter((m) => m.id).concat(model && !models.some((m) => m.id === model) ? [{ id: model, label: model, group: "Other" }] : []);
  async function pick(id: string) {
    const before = model;
    setModel(id);
    setError("");
    try { await api("/api/claude-model", { model: id }); } catch (e) { setModel(before); setError((e as Error).message); }
  }
  return (
    <section className="card space-y-3 p-4">
      <h2 className="font-medium">Model</h2>
      <div className="flex flex-wrap items-center gap-3">
        <select className="input w-auto min-w-72 py-2 text-base" value={model} onChange={(e) => pick(e.target.value)} aria-label="Model used by the app">
          <option value="">{`Claude Code default${defaultName ? ` (${defaultName})` : ""}`}</option>
          {[...new Set(shown.map((m) => m.group))].map((g) => (
            <optgroup key={g} label={g}>
              {shown.filter((m) => m.group === g).map((m) => <option key={m.id} value={m.id}>{m.label}</option>)}
            </optgroup>
          ))}
        </select>
        <code className="font-mono text-xs text-muted">{model || "no --model flag"}</code>
      </div>
      <p className="font-mono text-[11px] text-muted">Used for problems, tests, hints, mock interviews and study plans.{error && <span className="text-hard"> {error}</span>}</p>
    </section>
  );
}
