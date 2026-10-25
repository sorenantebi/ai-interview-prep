import { notFound } from "next/navigation";
import Workspace from "@/components/Workspace";
import { areaStats, localDate, progress, read, write } from "@/lib/content";
import { orderQuery, sequence, type Order } from "@/lib/order";
import { problemHref } from "@/components/ProblemList";
import { codeBlock, parseExamples, starterFrom, strokesOf, type Cases } from "@/lib/starter";

export const dynamic = "force-dynamic";

export default async function ProblemPage({ params, searchParams }: {
  params: Promise<{ group: string; slug: string }>;
  searchParams: Promise<{ order?: string; seed?: string; only?: string; review?: string }>;
}) {
  const { group, slug } = await params;
  const q = await searchParams;
  const path = `leetcode/${decodeURIComponent(group)}/${decodeURIComponent(slug)}`;
  const [question, solution, attempt, notes, starterFile, saved, drawing] = await Promise.all(
    ["question.md", "solution.md", "attempt.py", "notes.md", "starter.py", "testcases.json", "drawing.json"].map((f) => read(`${path}/${f}`)),
  );
  if (question === null) notFound();
  const prog = await progress();
  // A review starts from a blank starter. The dashboard shows solved.py, so a solve from before solved.py existed
  // gets its answer copied there first; the problem stays solved either way.
  const review = q.review === "1";
  if (review && prog[path]?.status === "solved" && attempt !== null && (await read(`${path}/solved.py`)) === null) await write(`${path}/solved.py`, attempt);

  // Prev / next: roadmap order, or a seeded random order (?order=random&seed=…[&only=unsolved]).
  const order: Order = { random: q.order === "random", seed: Number(q.seed) || 1, unsolved: q.only === "unsolved" };
  const lcStats = await areaStats("leetcode");
  const all = lcStats.flatMap((g) => g.problems.map((p) => p.path));
  const solved = new Set(Object.keys(prog).filter((k) => prog[k].status === "solved"));
  const seq = sequence(all, order, solved, path);
  const at = seq.indexOf(path);
  const link = (p?: string) => (p ? problemHref(p) + orderQuery(order) : null);
  const nav = { prev: link(seq[at - 1]), next: link(seq[at + 1]), pos: at + 1, total: seq.length, random: order.random, unsolved: order.unsolved };
  // LeetCode's starter when we have it; otherwise signatures only, taken from the reference solution.
  const starter = starterFile ?? starterFrom(codeBlock(solution ?? ""));
  const examples = parseExamples(question, starter);
  let mine: Cases | null = null;
  try { mine = saved ? JSON.parse(saved) : null; } catch {}
  return (
    <Workspace
      path={path}
      question={order.random ? question.replace(/\*\*Topic:\*\*[^·\n]*·\s*/, "") : question} // shuffle mode hides the topic: it gives the pattern away
      solution={solution ?? ""}
      attempt={attempt}
      fresh={review}
      starter={starter}
      names={examples.names}
      cases={mine?.cases?.length ? mine.cases : examples.cases}
      examples={examples.cases}
      notes={notes ?? ""}
      drawing={strokesOf(drawing)}
      status={prog[path]?.status}
      review={prog[path]?.review}
      today={localDate(new Date())}
      nav={nav}
      topics={lcStats.map((g) => g.group)}
    />
  );
}
