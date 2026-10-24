import { claude, prompt } from "./claude.ts";

export type Complexity = { time: string; space: string; timeOk: boolean | null; spaceOk: boolean | null; why: string; claimed?: { time: string; space: string }; at?: string };

/** Claude works out the time/space complexity of your code and, when you give yours, says whether it's right. */
export async function checkComplexity(question: string, code: string, claimed?: { time: string; space: string }): Promise<Complexity> {
  const input = await prompt("complexity", { question, code, time: claimed?.time || "not given", space: claimed?.space || "not given" });
  const { text } = await claude(input);
  const json = text.match(/\{[\s\S]*\}/)?.[0];
  let r: Complexity;
  try { r = JSON.parse(json ?? ""); } catch { throw new Error("Couldn't read the complexity from Claude's answer:\n" + text.slice(0, 300)); }
  if (typeof r.time !== "string" || typeof r.space !== "string") throw new Error("Claude's answer had no complexity");
  return { time: r.time, space: r.space, timeOk: claimed?.time ? !!r.timeOk : null, spaceOk: claimed?.space ? !!r.spaceOk : null, why: String(r.why ?? ""), ...(claimed ? { claimed } : {}) };
}
