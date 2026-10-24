import { NextRequest, NextResponse } from "next/server";
import { moveProblem } from "@/lib/content";

/** move { path, group }: puts a problem under another topic. */
export async function POST(req: NextRequest) {
  const b = await req.json();
  try {
    if (b.action !== "move") throw new Error(`Unknown action ${b.action}`);
    return NextResponse.json({ path: await moveProblem(String(b.path ?? ""), String(b.group ?? "")) });
  } catch (e) {
    return NextResponse.json({ error: (e as Error).message }, { status: 400 });
  }
}
