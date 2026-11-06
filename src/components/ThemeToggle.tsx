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
      {dark === null ? "◐" : dark ? "☀" : "☾"}
    </button>
  );
}
