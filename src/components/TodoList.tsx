"use client";
import { useState } from "react";
import { putFile } from "@/lib/client";

export type Todo = { id: string; text: string; done: boolean };

/** Your own small to-do list on the dashboard, saved to content/todos.json. */
export default function TodoList({ initial }: { initial: Todo[] }) {
  const [todos, setTodos] = useState(initial);
  const [text, setText] = useState("");
  const [error, setError] = useState("");
  function update(next: Todo[]) {
    setTodos(next);
    putFile("todos.json", JSON.stringify(next, null, 2)).then(() => setError(""), (e) => setError((e as Error).message));
  }
  function add(e: React.FormEvent) {
    e.preventDefault();
    if (text.trim()) update([...todos, { id: crypto.randomUUID(), text: text.trim(), done: false }]);
    setText("");
  }
  const done = todos.filter((t) => t.done).length;

  return (
    // Attached to the streak card's right edge; contain:size lets the streak card alone set the height, so a long list scrolls.
    <section className="card flex flex-col p-4 max-sm:-mt-px sm:-ml-px sm:w-60 sm:[contain:size]">
      <div className="mb-2 flex items-baseline justify-between gap-2">
        <h2 className="font-medium">To-do</h2>
        {done > 0 && <button className="font-mono text-xs text-muted hover:text-fg" onClick={() => update(todos.filter((t) => !t.done))}>clear {done} done</button>}
      </div>
      <form onSubmit={add} className="mb-2">
        <input className="input text-sm" value={text} onChange={(e) => setText(e.target.value)} placeholder="Add a to-do + Enter" />
      </form>
      <ul className="min-h-0 flex-1 space-y-0.5 overflow-y-auto">
        {todos.map((t) => (
          <li key={t.id} className="group flex items-start gap-2 text-sm">
            <input type="checkbox" className="mt-1 accent-[var(--accent)]" checked={t.done} aria-label={t.text}
              onChange={() => update(todos.map((x) => (x.id === t.id ? { ...x, done: !x.done } : x)))} />
            <span className={`flex-1 break-words ${t.done ? "text-muted line-through" : ""}`}>{t.text}</span>
            <button className="text-muted opacity-0 hover:text-hard group-hover:opacity-100 focus:opacity-100" aria-label={`Remove ${t.text}`}
              onClick={() => update(todos.filter((x) => x.id !== t.id))}>×</button>
          </li>
        ))}
        {!todos.length && <li className="text-sm text-muted">Nothing yet.</li>}
      </ul>
      {error && <p className="mt-1 text-xs text-hard">{error}</p>}
    </section>
  );
}
