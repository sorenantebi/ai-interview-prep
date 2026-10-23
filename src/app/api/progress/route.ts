import { NextRequest, NextResponse } from "next/server";
import { logActivity, progress, review, setProgress, type ReviewAction } from "@/lib/content";
import { completeTasks } from "@/lib/plan";

const ACTIONS: ReviewAction[] = ["enable", "disable", "again", "hard", "good", "easy", "set"];

export async function GET() {
  return NextResponse.json(await progress());
}

/** { path, status } sets solved/attempted/null; { path, review, due? } runs a spaced-repetition action. */
export async function POST(req: NextRequest) {
  const { path, status, review: action, due } = await req.json();
  try {
    if (action !== undefined) {
      if (!ACTIONS.includes(action)) throw new Error(`Unknown review action ${action}`);
      if (["again", "hard", "good", "easy"].includes(action)) await logActivity();
      return NextResponse.json(await review(path, action, new Date(), due));
    }
    await setProgress(path, status);
    if (status === "solved") await Promise.all([logActivity(), completeTasks(path)]);
    return NextResponse.json(await progress());
  } catch (e) {
    return NextResponse.json({ error: (e as Error).message }, { status: 400 });
  }
}
