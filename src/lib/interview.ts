// Mock interview length by difficulty. Coding follows the usual round lengths per difficulty; system design gets
// longer because requirements, high-level design and deep dives all need room. Unknown (the interviewer picks
// the problem): a full 45-minute round.
const MINUTES: Record<string, Record<string, number>> = {
  coding: { easy: 15, medium: 30, hard: 45 },
  "system-design": { easy: 35, medium: 45, hard: 60 },
};

export function interviewMinutes(kind: string, difficulty?: string): number {
  return MINUTES[kind === "system-design" ? "system-design" : "coding"][difficulty?.toLowerCase() ?? ""] ?? 45;
}

/** The difficulty from a question.md's frontmatter ("difficulty: Medium"), if any. */
export const difficultyOf = (question: string) => question.match(/^difficulty:\s*["']?(\w+)/m)?.[1];
