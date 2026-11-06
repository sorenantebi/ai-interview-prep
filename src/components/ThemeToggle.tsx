"use client";
import { useEffect, useState } from "react";

/** Dark only when you picked it; light is the default. */
export const isDark = () => document.documentElement.dataset.theme === "dark";

/** Light/dark switch in the top bar; the choice is remembered in this browser. */
export default function ThemeToggle() {
  const [dark, setDark] = useState<boolean | null>(null);
  useEffect(() => setDark(isDark()), []);
  function toggle() {
    const next = isDark() ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem("theme", next); } catch {}
    setDark(next === "dark");
    window.dispatchEvent(new Event("prep-theme")); // lets the code editor switch its colours too
  }
  return (
    <button onClick={toggle} className="flex h-8 cursor-pointer items-center whitespace-nowrap bg-panel px-3 text-[15px] hover:bg-fg hover:text-panel" aria-label={dark ? "Switch to light mode" : "Switch to dark mode"} title={dark ? "Light mode" : "Dark mode"}>
      <svg viewBox="0 0 16 16" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
        {dark === null ? null : dark ? (
          <><circle cx="8" cy="8" r="3" /><path d="M8 1.5v1.2M8 13.3v1.2M1.5 8h1.2M13.3 8h1.2M3.4 3.4l.85.85M11.75 11.75l.85.85M3.4 12.6l.85-.85M11.75 4.25l.85-.85" /></>
        ) : (
          <path d="M13.5 9.6A5.8 5.8 0 0 1 6.4 2.5a5.8 5.8 0 1 0 7.1 7.1Z" />
        )}
      </svg>
    </button>
  );
}
