"use client";
import { useState } from "react";
import { putFile } from "@/lib/client";

/** Big motivational line above the dashboard; click to edit, saved to content/mantra.txt. */
export default function Mantra({ initial }: { initial: string }) {
  const [text, setText] = useState(initial);
  const [editing, setEditing] = useState(false);
  const save = async (value: string) => {
    setEditing(false);
    const v = value.trim();
    if (v === text) return;
    setText(v);
    await putFile("mantra.txt", v + "\n");
  };
  const big = "font-display text-5xl font-semibold uppercase leading-[0.95] tracking-[-0.04em] md:text-7xl xl:text-8xl";
  return editing ? (
    <textarea
      autoFocus
      defaultValue={text}
      rows={Math.max(1, text.split("\n").length)}
      className={`${big} w-full resize-none border-b-2 border-fg bg-transparent outline-none`}
      onBlur={(e) => save(e.target.value)}
      onKeyDown={(e) => {
        if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); save(e.currentTarget.value); }
        if (e.key === "Escape") setEditing(false);
      }}
      aria-label="Mantra"
    />
  ) : (
    <button onClick={() => setEditing(true)} className={`${big} block w-full whitespace-pre-line text-left hover:opacity-80`} title="Click to edit your mantra">
      {text || "click to write your mantra"}
    </button>
  );
}
