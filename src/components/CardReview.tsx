"use client";
import Link from "next/link";
import { useCallback, useEffect, useRef, useState } from "react";
import Markdown from "./Markdown";
import { api } from "@/lib/client";

type Item = { deck: string; id: string; front: string; back: string; labels: string[] };
const GRADES = [["Again", "text-hard"], ["Hard", "text-medium"], ["Good", "text-easy"], ["Easy", "text-accent"]] as const;

/** Anki-style session: front, Show answer (space), then grade 1-4. Again puts the card back at the end of the session. */
export default function CardReview({ queue: initial, title, back }: { queue: Item[]; title: string; back: string }) {
  const [queue, setQueue] = useState(initial);
  const [shown, setShown] = useState(false);
  const [done, setDone] = useState(0);
  const [error, setError] = useState("");
  const card = queue[0];
  const busy = useRef(false); // one grade at a time: a key pressed while saving would grade the same card twice

  const grade = useCallback(async (g: number) => {
    if (!card || busy.current) return;
    busy.current = true;
    try {
      const { labels } = await api("/api/cards", { action: "grade", deck: card.deck, id: card.id, grade: g });
      setQueue((q) => (g === 1 ? [...q.slice(1), { ...card, labels }] : q.slice(1)));
      if (g !== 1) setDone((n) => n + 1);
      setShown(false);
      setError("");
    } catch (e) {
      setError((e as Error).message);
    } finally {
      busy.current = false;
    }
  }, [card]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLElement && e.target.closest("input, textarea, select")) return;
      if (!shown && (e.key === " " || e.key === "Enter")) { e.preventDefault(); setShown(true); }
      else if (shown && ["1", "2", "3", "4"].includes(e.key)) grade(Number(e.key));
      else if (shown && e.key === " ") { e.preventDefault(); grade(3); }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [shown, grade]);

  return (
    <div className="mx-auto max-w-3xl space-y-4">
      <div className="flex items-center justify-between">
        <Link href={back} className="font-mono text-xs text-muted hover:text-fg">← {title}</Link>
        <span className="font-mono text-xs tabular-nums text-muted">{done} done · {queue.length} left</span>
      </div>
      {!card ? (
        <div className="card space-y-3 p-8 text-center">
          <p className="font-display text-2xl font-medium">{initial.length ? "All done for today" : "Nothing due today"}</p>
          <Link href={back} className="btn inline-block">Back</Link>
        </div>
      ) : (
        <div className="card space-y-4 p-6">
          {title === "All decks" && <div className="tag">{card.deck}</div>}
          <div className="text-lg"><Markdown>{card.front}</Markdown></div>
          {shown ? (
            <>
              <div className="border-t border-border pt-4"><Markdown>{card.back}</Markdown></div>
              <div className="grid grid-cols-4 gap-2">
                {GRADES.map(([label, color], i) => (
                  <button key={label} className="btn flex flex-col items-center py-2" onClick={() => grade(i + 1)}>
                    <span className={`font-medium ${color}`}>{label}</span>
                    <span className="font-mono text-[11px] text-muted">{card.labels[i]} · {i + 1}</span>
                  </button>
                ))}
              </div>
            </>
          ) : (
            <button className="btn-primary w-full" onClick={() => setShown(true)}>Show answer <span className="font-mono text-xs opacity-70">space</span></button>
          )}
          {error && <p className="font-mono text-xs text-hard">{error}</p>}
        </div>
      )}
    </div>
  );
}
