import { notFound } from "next/navigation";
import Workspace from "@/components/Workspace";
import { areaStats, localDate, progress, read, write } from "@/lib/content";
import { orderQuery, sequence, type Order } from "@/lib/order";
import { problemHref } from "@/components/ProblemList";
import { codeBlock, parseExamples, starterFrom, strokesOf, type Cases } from "@/lib/starter";

export type ProblemPageProps = {
  params: Promise<{ group: string; slug: string }>;
  searchParams: Promise<{ order?: string; seed?: string; only?: string; review?: string }>;
};

/** The coding problem page of an area ("leetcode", "ml-coding" or "quant-dev"): editor, tests, notes, prev / next. */
export default async function ProblemPage({ area, params, searchParams }: ProblemPageProps & { area: string }) {
  const { group, slug } = await params;
  const q = await searchParams;
  const path = `${area}/${decodeURIComponent(group)}/${decodeURIComponent(slug)}`;
  const [question, solution, attempt, notes, starterFile, saved, drawing, attemptCpp, starterCpp] = await Promise.all(
    ["question.md", "solution.md", "attempt.py", "notes.md", "starter.py", "testcases.json", "drawing.json", "attempt.cpp", "starter.cpp"].map((f) => read(`${path}/${f}`)),
  );
  if (question === null) notFound();
  const prog = await progress();
  // A review starts from a blank starter. The dashboard shows solved.py, so a solve from before solved.py existed
  // gets its answer copied there first; the problem stays solved either way.
  const review = q.review === "1";
  if (review && prog[path]?.status === "solved" && attempt !== null && (await read(`${path}/solved.py`)) === null) await write(`${path}/solved.py`, attempt);

  // Prev / next: roadmap order, or a seeded random order (?order=random&seed=…[&only=unsolved]).
  const order: Order = { random: q.order === "random", seed: Number(q.seed) || 1, unsolved: q.only === "unsolved" };
  const lcStats = await areaStats(area);
  const all = lcStats.flatMap((g) => g.problems.map((p) => p.path));
  const solved = new Set(Object.keys(prog).filter((k) => prog[k].status === "solved"));
  const seq = sequence(all, order, solved, path);
  const at = seq.indexOf(path);
  const link = (p?: string) => (p ? problemHref(p) + orderQuery(order) : null);
  const nav = { prev: link(seq[at - 1]), next: link(seq[at + 1]), pos: at + 1, total: seq.length, random: order.random, unsolved: order.unsolved };
  // LeetCode's starter when we have it; otherwise signatures only, taken from the reference solution.
  // Quant Dev is C++ only (its own tests), ML Coding Python only, LeetCode both when there's a C++ starter.
  const cppOnly = area === "quant-dev";
  const starter = cppOnly ? "" : (starterFile ?? starterFrom(codeBlock(solution ?? "")));
  const examples = cppOnly ? { names: [], cases: [] } : parseExamples(question, starter);
  const langs = cppOnly ? (["cpp"] as const) : starterCpp !== null ? (["python", "cpp"] as const) : (["python"] as const);
  let mine: Cases | null = null;
  try { mine = saved ? JSON.parse(saved) : null; } catch {}
  return (
    <Workspace
      path={path}
      question={order.random ? question.replace(/\*\*Topic:\*\*[^·\n]*·\s*/, "") : question} // shuffle mode hides the topic: it gives the pattern away
      solution={solution ?? ""}
      langs={[...langs]}
      attempts={{ python: attempt, cpp: attemptCpp }}
      fresh={review}
      starters={{ python: starter, cpp: starterCpp ?? "" }}
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
