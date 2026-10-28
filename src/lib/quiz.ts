import fs from "node:fs/promises";
import { read, safePath, write } from "./content.ts";

export type QuizQuestion = { id: string; title: string; difficulty: string; body: string; answer: string };
export type QuizTopic = { file: string; name: string; intro: string; questions: QuizQuestion[] };
export type QuizMarks = Record<string, { mark: "known" | "again"; at: string }>; // id -> your last mark

const slug = (s: string) => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

/** One question-bank file: `## Title · Difficulty`, the question, then `### Answer` (see content/quant-questions/README.md). */
export function parseQuiz(file: string, md: string): QuizTopic {
  const body = md.replace(/^---\n[\s\S]*?\n---\n/, "");
  const [head, ...parts] = body.split(/^## /m);
  const name = head.match(/^# (.+)$/m)?.[1].trim() ?? file.replace(/^\d+\s*|\.md$/g, "");
  const intro = head.replace(/^# .+$/m, "").trim();
  const topic = slug(file.replace(/\.md$/, ""));
  const questions = parts.map((p) => {
    const [first, ...rest] = p.split("\n");
    const [title, difficulty = ""] = first.split(" · ").map((x) => x.trim());
    const [q, a = ""] = rest.join("\n").split(/^### Answer\s*$/m);
    return { id: `${topic}/${slug(title)}`, title, difficulty, body: q.trim(), answer: a.trim() };
  });
  return { file, name, intro, questions };
}

/** Every topic file in content/quant-questions, in file-name order. */
export async function quizTopics(): Promise<QuizTopic[]> {
  const files = (await fs.readdir(safePath("quant-questions")).catch(() => [])).filter((f) => f.endsWith(".md") && f !== "README.md").sort();
  return Promise.all(files.map(async (f) => parseQuiz(f, (await read(`quant-questions/${f}`)) ?? "")));
}

export async function quizMarks(): Promise<QuizMarks> {
  try { return JSON.parse((await read("quiz.json")) ?? "{}"); } catch { return {}; }
}

/** Your "got it" / "again" mark for a question (null clears it). */
export async function setQuizMark(id: string, mark: "known" | "again" | null) {
  const marks = await quizMarks();
  if (mark) marks[id] = { mark, at: new Date().toISOString() };
  else delete marks[id];
  await write("quiz.json", JSON.stringify(marks, null, 1));
}
