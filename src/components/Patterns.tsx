"use client";
import { useState } from "react";
import Markdown from "./Markdown";
import { putFile } from "@/lib/client";

type Section = { title: string; body: string };

const split = (md: string) => {
  const [intro, ...rest] = md.split(/^## /m);
  return { intro, sections: rest.map((s): Section => { const [title, ...body] = s.split("\n"); return { title: title.trim(), body: body.join("\n").trim() }; }) };
};
const join = (intro: string, sections: Section[]) => intro.trimEnd() + "\n\n" + sections.map((s) => `## ${s.title}\n\n${s.body.trim()}\n`).join("\n");

/** patterns.md as one card per "## Topic"; each card can be edited in place (title, text and code). */
export default function Patterns({ markdown }: { markdown: string }) {
  const parsed = split(markdown);
  const [sections, setSections] = useState(parsed.sections);
  const [editing, setEditing] = useState<number | null>(null);
  const [draft, setDraft] = useState<Section>({ title: "", body: "" });
  const [error, setError] = useState("");
  const [isNew, setIsNew] = useState(false); // an added topic that was never saved disappears on Cancel

  async function persist(next: Section[]) {
    try {
      await putFile("patterns.md", join(parsed.intro, next));
      setSections(next);
      setEditing(null);
      setIsNew(false);
      setError("");
    } catch (e) {
      setError((e as Error).message);
    }
  }
  const edit = (i: number) => { setEditing(i); setDraft(sections[i]); setIsNew(false); };
  const save = () => persist(sections.map((s, i) => (i === editing ? { title: draft.title.trim() || "Untitled", body: draft.body } : s)));
  const addTopic = () => { const next = [...sections, { title: "New topic", body: "**Use when:** …\n\n- pattern\n\n```python\n# template\n```" }]; setSections(next); setEditing(next.length - 1); setDraft(next[next.length - 1]); setIsNew(true); };
  const remove = (i: number) => confirm(`Delete "${sections[i].title}"?`) && persist(sections.filter((_, k) => k !== i));

  return (
    <div className="card max-h-[80vh] overflow-y-auto">
      <nav className="sticky top-0 z-10 flex flex-wrap gap-1 border-b border-border bg-panel p-2" aria-label="Pattern topics">
        {sections.map((s, i) => (
          <a key={i} href={`#pattern-${i}`} className="border border-border px-2 py-0.5 font-mono text-xs hover:bg-fg hover:text-panel">{s.title}</a>
        ))}
        <span className="flex-1" />
        <button onClick={addTopic} className="px-2 py-0.5 font-mono text-xs text-muted hover:text-fg">+ topic</button>
      </nav>
      {error && <p className="p-2 text-sm text-hard" role="alert">{error}</p>}
      <div className="grid gap-px bg-border md:grid-cols-2 xl:grid-cols-3">
        {sections.map((s, i) => (
          <section key={i} id={`pattern-${i}`} className={`group scroll-mt-14 bg-panel p-4 [&_.md]:text-sm [&_pre]:text-xs ${editing === i ? "md:col-span-2 xl:col-span-3" : ""}`}>
            {editing === i ? (
              <div className="space-y-2">
                <input className="input font-display text-lg" value={draft.title} onChange={(e) => setDraft({ ...draft, title: e.target.value })} aria-label="Topic title" />
                <div className="grid gap-3 lg:grid-cols-2">
                  <textarea
                    className="input min-h-80 resize-y font-mono text-[13px] leading-relaxed"
                    value={draft.body}
                    onChange={(e) => setDraft({ ...draft, body: e.target.value })}
                    onKeyDown={(e) => {
                      if (e.key === "Tab") { // insert spaces instead of leaving the box, so code stays indented
                        e.preventDefault();
                        const t = e.currentTarget, a = t.selectionStart;
                        setDraft({ ...draft, body: t.value.slice(0, a) + "    " + t.value.slice(t.selectionEnd) });
                        requestAnimationFrame(() => t.setSelectionRange(a + 4, a + 4));
                      }
                      if (e.key === "s" && (e.metaKey || e.ctrlKey)) { e.preventDefault(); save(); }
                    }}
                    spellCheck={false}
                    aria-label="Topic text and code (markdown)"
                  />
                  <div className="max-h-[32rem] overflow-y-auto border border-border p-3">
                    <div className="mb-2 font-mono text-[11px] text-muted">preview</div>
                    <Markdown>{draft.body}</Markdown>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <button className="btn-primary" onClick={save}>Save</button>
                  <button className="btn" onClick={() => { if (isNew) setSections((ss) => ss.filter((_, k) => k !== i)); setEditing(null); setIsNew(false); }}>Cancel</button>
                  <span className="font-mono text-[11px] text-muted">Markdown · code in ```python blocks · ⌘S saves</span>
                  <button className="ml-auto font-mono text-xs text-muted hover:text-hard" onClick={() => remove(i)}>delete topic</button>
                </div>
              </div>
            ) : (
              <>
                <div className="mb-2 flex items-baseline gap-2">
                  <h3 className="font-display text-lg font-medium tracking-tight">{s.title}</h3>
                  <button className="ml-auto font-mono text-xs text-muted opacity-0 hover:text-fg focus:opacity-100 group-hover:opacity-100" onClick={() => edit(i)}>edit</button>
                </div>
                <Markdown>{s.body}</Markdown>
              </>
            )}
          </section>
        ))}
      </div>
    </div>
  );
}
