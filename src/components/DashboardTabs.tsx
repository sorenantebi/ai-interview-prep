"use client";
import { useState, type ReactNode } from "react";

/** Switches between the dashboard's cheat sheet views; both are rendered on the server. */
export default function DashboardTabs({ tabs, initial = 0 }: { tabs: { label: string; content: ReactNode }[]; initial?: number }) {
  const [active, setActive] = useState(initial);
  return (
    <section>
      <div className="mb-3 flex flex-wrap gap-1" role="tablist">
        {tabs.map((t, i) => (
          <button key={t.label} role="tab" aria-selected={active === i} onClick={() => setActive(i)} className={`px-4 py-2 text-base font-medium ${active === i ? "bg-fg text-panel" : "bg-panel text-fg hover:bg-fg hover:text-panel"}`}>
            {t.label}
          </button>
        ))}
      </div>
      {tabs.map((t, i) => <div key={t.label} hidden={active !== i}>{t.content}</div>)}
    </section>
  );
}
