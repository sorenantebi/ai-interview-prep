import { NextRequest, NextResponse } from "next/server";
import { setQuizMark } from "@/lib/quiz";

/** { id, mark: "known" | "again" | null }: your mark for a question-bank question. */
export async function POST(req: NextRequest) {
  const { id, mark } = await req.json();
  if (typeof id !== "string" || !/^[\w-]+\/[\w-]+$/.test(id) || ![null, "known", "again"].includes(mark)) return NextResponse.json({ error: "Bad mark" }, { status: 400 });
  await setQuizMark(id, mark);
  return NextResponse.json({ ok: true });
}
