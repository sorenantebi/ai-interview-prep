"use client";
import { useEffect, useState } from "react";

/** The theme in effect: your pick if you made one, otherwise the system setting. */
export const isDark = () =>
  document.documentElement.dataset.theme ? document.documentElement.dataset.theme === "dark" : window.matchMedia("(prefers-color-scheme: dark)").matches;

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
    <button onClick={toggle} className="whitespace-nowrap bg-panel px-3 py-1.5 text-lg hover:bg-fg hover:text-panel" aria-label={dark ? "Switch to light mode" : "Switch to dark mode"} title={dark ? "Light mode" : "Dark mode"}>
      {dark === null ? "◐" : dark ? "☀" : "☾"}
    </button>
  );
}
