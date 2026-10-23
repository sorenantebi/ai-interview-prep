import Link from "next/link";
import Difficulty from "./Difficulty";
import type { Problem, Progress } from "@/lib/content";

export const problemHref = (p: string) => "/" + p.split("/").map(encodeURIComponent).join("/");

export default function ProblemList({ problems, progress }: { problems: Problem[]; progress: Progress }) {
  if (!problems.length) return <p className="p-4 text-sm text-muted">No problems yet. Add one on the AI page.</p>;
  return (
    <ul className="divide-y divide-border">
      {problems.map((p) => {
        const status = progress[p.path]?.status;
        return (
          <li key={p.path} className="flex items-center gap-3 px-4 py-2 text-sm">
            <span className={`w-4 text-center ${status === "solved" ? "text-easy" : "text-medium"}`} title={status ?? "not started"}>
              {status === "solved" ? "✓" : status === "attempted" ? "•" : ""}
            </span>
            <Link href={problemHref(p.path)} className="flex-1 truncate hover:underline decoration-accent decoration-2 underline-offset-2">{p.title}</Link>
            {p.video && <span className="text-xs text-muted" title="Has video">▶</span>}
            <Difficulty level={p.difficulty} />
            {p.leetcode && <a href={p.leetcode} target="_blank" rel="noreferrer" className="text-xs text-muted hover:underline decoration-accent decoration-2 underline-offset-2">LeetCode ↗</a>}
            {p.neetcode && <a href={p.neetcode} target="_blank" rel="noreferrer" className="text-xs text-muted hover:underline decoration-accent decoration-2 underline-offset-2 max-sm:hidden">NeetCode ↗</a>}
          </li>
        );
      })}
    </ul>
  );
}
