import Link from "next/link";
import type { ReactNode } from "react";

/** Dashboard cheat sheet tabs as links: the server only builds the tab you are on, which keeps the page light. */
export default function DashboardTabs({ tabs, active, children }: { tabs: { label: string; href: string }[]; active: number; children: ReactNode }) {
  return (
    <section>
      <div className="mb-3 flex flex-wrap gap-1" role="tablist">
        {tabs.map((t, i) => (
          <Link key={t.label} href={t.href} scroll={false} role="tab" aria-selected={active === i} className={`px-4 py-2 text-base font-medium ${active === i ? "bg-fg text-panel" : "bg-panel text-fg hover:bg-fg hover:text-panel"}`}>
            {t.label}
          </Link>
        ))}
      </div>
      {children}
    </section>
  );
}
