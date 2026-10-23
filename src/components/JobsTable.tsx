"use client";
import { useEffect, useMemo, useRef, useState } from "react";
import { putFile } from "@/lib/client";

export type Job = { id: string; company: string; role: string; stage: string; applied: string; next: string; link: string; notes: string };

export const STAGES = ["Wishlist", "Applied", "Online assessment", "Recruiter screen", "Technical screen", "Onsite", "Offer", "Rejected", "Withdrawn"];
const ACTIVE = new Set(["Applied", "Online assessment", "Recruiter screen", "Technical screen", "Onsite"]);
const stageColor = (s: string) => (s === "Offer" ? "bg-easy text-white" : s === "Rejected" || s === "Withdrawn" ? "bg-fg/10 text-muted" : ACTIVE.has(s) ? "bg-accent/20" : "bg-panel");

const COLS: { key: keyof Job; label: string; width: string }[] = [
  { key: "company", label: "Company", width: "minmax(140px,1fr)" },
  { key: "role", label: "Role", width: "minmax(160px,1.2fr)" },
  { key: "stage", label: "Stage", width: "170px" },
  { key: "applied", label: "Applied", width: "140px" },
  { key: "next", label: "Next step", width: "140px" },
  { key: "link", label: "Link", width: "minmax(120px,0.8fr)" },
  { key: "notes", label: "Notes", width: "minmax(220px,2fr)" },
];
const GRID = { gridTemplateColumns: COLS.map((c) => c.width).join(" ") + " 36px" };

const today = () => new Date().toLocaleDateString("en-CA");
const blank = (): Job => ({ id: crypto.randomUUID(), company: "", role: "", stage: "Applied", applied: today(), next: "", link: "", notes: "" });

/** Spreadsheet of job applications, saved to content/jobs.json. */
export default function JobsTable({ initial }: { initial: Job[] }) {
  const [jobs, setJobs] = useState(initial);
  const [sort, setSort] = useState<{ key: keyof Job; dir: 1 | -1 }>({ key: "applied", dir: -1 });
  const [filter, setFilter] = useState("all");
  const [saved, setSaved] = useState(true);
  const first = useRef(true);
  const focusId = useRef<string | null>(null);

  useEffect(() => {
    if (first.current) { first.current = false; return; }
    setSaved(false);
    const t = setTimeout(() => putFile("jobs.json", JSON.stringify(jobs, null, 2)).then(() => setSaved(true), () => alert("Could not save jobs.json")), 600);
    return () => clearTimeout(t);
  }, [jobs]);

  const set = (id: string, key: keyof Job, value: string) => setJobs((js) => js.map((j) => (j.id === id ? { ...j, [key]: value } : j)));
  const add = () => { const j = blank(); focusId.current = j.id; setJobs((js) => [j, ...js]); setFilter("all"); };
  const remove = (j: Job) => { if (confirm(`Delete ${j.company || "this row"}?`)) setJobs((js) => js.filter((x) => x.id !== j.id)); };

  const counts = useMemo(() => STAGES.map((s) => [s, jobs.filter((j) => j.stage === s).length] as const).filter(([, n]) => n), [jobs]);
  const rows = useMemo(() => {
    const rank = (j: Job) => (sort.key === "stage" ? String(STAGES.indexOf(j.stage)).padStart(2, "0") : String(j[sort.key]).toLowerCase());
    return jobs
      .filter((j) => filter === "all" || (filter === "active" ? ACTIVE.has(j.stage) : j.stage === filter))
      .sort((a, b) => (rank(a) < rank(b) ? -sort.dir : rank(a) > rank(b) ? sort.dir : 0));
  }, [jobs, sort, filter]);

  const cellInput = "w-full bg-transparent px-2 py-1.5 text-sm outline-none focus:bg-accent/10";
  const chip = (active: boolean) => `px-2 py-0.5 font-mono text-xs ${active ? "bg-fg text-panel" : "border border-border bg-panel hover:border-fg"}`;

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap items-center gap-1">
        <button className="btn-primary mr-2" onClick={add}>+ Add application</button>
        <button className={chip(filter === "all")} onClick={() => setFilter("all")}>All {jobs.length}</button>
        <button className={chip(filter === "active")} onClick={() => setFilter("active")}>In progress {jobs.filter((j) => ACTIVE.has(j.stage)).length}</button>
        {counts.map(([s, n]) => <button key={s} className={chip(filter === s)} onClick={() => setFilter(s)}>{s} {n}</button>)}
        <span className="ml-auto font-mono text-[11px] text-muted">{saved ? "saved to jobs.json" : "saving…"}</span>
      </div>
      <div className="card overflow-x-auto">
        <div className="min-w-[1100px]">
          <div className="sticky top-0 grid border-b border-fg bg-panel font-mono text-[11px] uppercase tracking-wide text-muted" style={GRID}>
            {COLS.map((c) => (
              <button key={c.key} className="border-l border-border px-2 py-2 text-left first:border-l-0 hover:text-fg" onClick={() => setSort((s) => ({ key: c.key, dir: s.key === c.key ? (-s.dir as 1 | -1) : 1 }))}>
                {c.label} {sort.key === c.key ? (sort.dir === 1 ? "↑" : "↓") : ""}
              </button>
            ))}
            <span />
          </div>
          {rows.length === 0 && <p className="p-4 text-sm text-muted">{jobs.length ? "No applications in this stage." : "No applications yet. Add your first one."}</p>}
          {rows.map((j) => (
            <div key={j.id} className="grid border-b border-border hover:bg-fg/[0.03]" style={GRID}>
              <div className="border-l border-border first:border-l-0">
                <input className={`${cellInput} font-medium`} value={j.company} placeholder="Company" aria-label="Company" onChange={(e) => set(j.id, "company", e.target.value)} autoFocus={focusId.current === j.id} />
              </div>
              <div className="border-l border-border"><input className={cellInput} value={j.role} placeholder="Role" aria-label="Role" onChange={(e) => set(j.id, "role", e.target.value)} /></div>
              <div className="border-l border-border p-1">
                <select className={`w-full px-1.5 py-1 text-sm outline-none ${stageColor(j.stage)}`} value={j.stage} aria-label="Stage" onChange={(e) => set(j.id, "stage", e.target.value)}>
                  {STAGES.map((s) => <option key={s}>{s}</option>)}
                </select>
              </div>
              <div className="border-l border-border"><input type="date" className={`${cellInput} font-mono`} value={j.applied} aria-label="Applied date" onChange={(e) => set(j.id, "applied", e.target.value)} /></div>
              <div className="border-l border-border"><input type="date" className={`${cellInput} font-mono ${j.next && j.next <= today() ? "text-hard" : ""}`} value={j.next} aria-label="Next step date" onChange={(e) => set(j.id, "next", e.target.value)} /></div>
              <div className="flex items-center border-l border-border">
                <input className={`${cellInput} min-w-0`} value={j.link} placeholder="https://…" aria-label="Link" onChange={(e) => set(j.id, "link", e.target.value)} />
                {/^https?:\/\//.test(j.link) && <a href={j.link} target="_blank" rel="noreferrer" className="px-1.5 text-muted hover:text-fg" aria-label="Open link">↗</a>}
              </div>
              <div className="border-l border-border">
                <textarea className={`${cellInput} block resize-y`} rows={1} value={j.notes} placeholder="Notes" aria-label="Notes" onChange={(e) => set(j.id, "notes", e.target.value)} />
              </div>
              <button className="border-l border-border text-muted hover:text-hard" onClick={() => remove(j)} aria-label={`Delete ${j.company || "row"}`}>×</button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
