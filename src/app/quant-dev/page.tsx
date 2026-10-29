import Link from "next/link";
import fs from "node:fs/promises";
import ProblemList, { problemHref } from "@/components/ProblemList";
import PdfPages from "@/components/PdfPages";
import QuizBank from "@/components/QuizBank";
import { orderQuery, sequence } from "@/lib/order";
import { areaStats, progress, safePath } from "@/lib/content";
import { quizMarks, quizTopics } from "@/lib/quiz";

export const dynamic = "force-dynamic";
const BOOK = "misc/trading-systems-developer-interview-guide.pdf"; // your copy (git-ignored); the tab shows it when it exists

const RESOURCES = [
  ["getcracked.io", "https://www.getcracked.io/questions", "C++, OS, concurrency, low-latency and probability questions, plus coding exercises"],
  ["NeetCode", "https://neetcode.io", "the LeetCode roadmap (also in this app, now in C++ too)"],
  ["quantquestions.io", "https://quantquestions.io/", "mainly for quant interviews, worth a look for firm-specific prep"],
  ["Codility", "https://app.codility.com/programmers/", "timed coding tests like the online screens"],
  ["HackerRank algorithms", "https://www.hackerrank.com/domains/algorithms", "the platform many firms use for the first screen"],
  ["GeeksforGeeks algorithms", "https://www.geeksforgeeks.org/fundamentals-of-algorithms/", "reference for classic algorithms"],
  ["Project Euler", "https://projecteuler.net/", "maths-heavy programming puzzles"],
  ["Effective C++ (Scott Meyers)", "https://www.oreilly.com/library/view/effective-c-55/0321334876/", "the classic many trading-firm engineers still recommend; take a newer edition"],
  ["Glassdoor and Reddit", "https://www.glassdoor.com/Interview/index.htm", "search for firm-specific questions and processes from past candidates"],
] as const;

export default async function QuantDevPage({ searchParams }: { searchParams: Promise<{ tab?: string; topic?: string }> }) {
  const { tab = "coding", topic } = await searchParams;
  const tabs = [["coding", "Coding (C++)"], ["questions", "Questions"], ["book", "Book & resources"]] as const;

  return (
    <div className="mx-auto max-w-6xl space-y-6">
      <h1 className="page-title">Quant Dev</h1>
      <div className="flex flex-wrap gap-1 border-b border-border" role="tablist">
        {tabs.map(([t, label]) => (
          <Link key={t} role="tab" aria-selected={tab === t} href={`/quant-dev?tab=${t}`} scroll={false} className={`-mb-px border-b-2 px-3 py-2 text-sm ${tab === t ? "border-fg font-medium" : "border-transparent text-muted hover:text-fg"}`}>
            {label}
          </Link>
        ))}
      </div>
      {tab === "questions" ? <Questions topic={topic} /> : tab === "book" ? <Book /> : <Coding topic={topic} />}
    </div>
  );
}

async function Coding({ topic }: { topic?: string }) {
  const [stats, prog] = await Promise.all([areaStats("quant-dev"), progress()]);
  const selected = stats.find((s) => s.group === topic) ?? stats[0];
  const solved = stats.reduce((a, s) => a + s.solved, 0);
  const total = stats.reduce((a, s) => a + s.total, 0);
  const seed = Math.floor(Math.random() * 1e9);
  const all = stats.flatMap((g) => g.problems.map((p) => p.path));
  const solvedSet = new Set(Object.keys(prog).filter((k) => prog[k].status === "solved"));
  const first = sequence(all, { random: true, seed, unsolved: true }, solvedSet)[0];
  return (
    <>
      <div className="flex flex-wrap items-center justify-end gap-3">
        <div className="flex items-center gap-2">
          <span className="mr-2 text-sm tabular-nums text-muted">{solved} / {total} solved</span>
          {first && <Link href={problemHref(first) + orderQuery({ random: true, seed, unsolved: true })} className="btn-primary">⤮ Shuffle unsolved</Link>}
        </div>
      </div>
      <div className="flex flex-wrap gap-2 text-sm">
        {stats.map((s) => (
          <Link key={s.group} href={`/quant-dev?topic=${encodeURIComponent(s.group)}`} scroll={false} className={`btn ${s.group === selected?.group ? "border-accent" : ""}`}>
            {s.name} <span className="text-muted">{s.solved}/{s.total}</span>
          </Link>
        ))}
      </div>
      {selected && (
        <section className="card">
          <div className="flex items-center justify-between border-b border-border px-4 py-3">
            <h2 className="font-medium">{selected.name}</h2>
            <span className="text-sm tabular-nums text-muted">{selected.solved} / {selected.total}</span>
          </div>
          <ProblemList problems={selected.problems} progress={prog} />
        </section>
      )}
    </>
  );
}

async function Questions({ topic }: { topic?: string }) {
  const [topics, marks] = await Promise.all([quizTopics(), quizMarks()]);
  const selected = topics.find((t) => t.file === topic) ?? topics[0];
  if (!selected) return <p className="card p-4 text-sm text-muted">No questions yet: add Markdown files to quant-questions/ (see its README).</p>;
  const known = (t: (typeof topics)[number]) => t.questions.filter((q) => marks[q.id]?.mark === "known").length;
  return (
    <>
      <div className="flex flex-wrap gap-2 text-sm">
        {topics.map((t) => (
          <Link key={t.file} href={`/quant-dev?tab=questions&topic=${encodeURIComponent(t.file)}`} scroll={false} className={`btn ${t.file === selected.file ? "border-accent" : ""}`}>
            {t.name} <span className="text-muted">{known(t)}/{t.questions.length}</span>
          </Link>
        ))}
      </div>
      <QuizBank key={selected.file} questions={selected.questions} initial={marks} />
    </>
  );
}

async function Book() {
  const hasBook = await fs.access(safePath(BOOK)).then(() => true, () => false);
  return (
    <>
      <section className="card p-4">
        <h2 className="mb-2 font-medium">Resources</h2>
        <ul className="space-y-1.5 text-sm">
          {RESOURCES.map(([name, url, what]) => (
            <li key={name}><a href={url} target="_blank" rel="noreferrer" className="underline decoration-accent decoration-2 underline-offset-2">{name}</a> <span className="text-muted">· {what}</span></li>
          ))}
        </ul>
      </section>
      <section className="space-y-2">
        <h2 className="font-medium">Trading Systems Developer Interview Guide (C++ Edition)</h2>
        {hasBook ? (
          <PdfPages title="Trading Systems Developer Interview Guide" src={`/api/files/raw?path=${encodeURIComponent(BOOK)}`} />
        ) : (
          <p className="card p-4 text-sm text-muted">Put your copy of the PDF at <code>content/{BOOK}</code> (Files → Upload into misc, then rename) and it shows here.</p>
        )}
      </section>
    </>
  );
}
