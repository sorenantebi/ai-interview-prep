"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import Timer from "./Timer";
import ThemeToggle from "./ThemeToggle";

const links = [
  ["/", "Dashboard"],
  ["/plan", "Plan"],
  ["/leetcode", "LeetCode"],
  ["/ml-coding", "ML Coding"],
  ["/system-design", "System Design"],
  ["/ai", "AI & Interviews"],
  ["/jobs", "Jobs"],
  ["/repos", "Repos"],
  ["/files", "Files"],
];

const box = "whitespace-nowrap px-2.5 py-1 text-[15px]";

/** Top bar of square boxes; the current section is inverted. */
export default function Nav({ authEnabled }: { authEnabled: boolean }) {
  const path = usePathname();
  const active = (href: string) => (href === "/" ? path === "/" : path.startsWith(href));
  return (
    <header className="sticky top-0 z-50 bg-bg/90 backdrop-blur">
      <nav className="mx-auto flex max-w-[1400px] flex-wrap items-center gap-1 px-4 py-2 md:px-8" aria-label="Main">
        <Link href="/" className={`${box} mr-3 bg-panel font-mono text-sm font-medium`}>prep/</Link>
        {links.map(([href, label]) => (
          <Link key={href} href={href} aria-current={active(href) ? "page" : undefined} className={`${box} ${active(href) ? "bg-fg text-panel" : "bg-panel hover:bg-fg hover:text-panel"}`}>
            {label}
          </Link>
        ))}
        <Link href="/claude" aria-current={active("/claude") ? "page" : undefined} className={`${box} ml-auto font-mono text-sm ${active("/claude") ? "bg-fg text-panel" : "bg-panel hover:bg-fg hover:text-panel"}`} title="Claude: connection, model and usage">
          claude
        </Link>
        <Timer />
        <ThemeToggle />
        {authEnabled && (
          <Link href="/api/auth/signout" prefetch={false} className={`${box} bg-panel text-muted hover:text-fg`}>Sign out</Link>
        )}
      </nav>
    </header>
  );
}
