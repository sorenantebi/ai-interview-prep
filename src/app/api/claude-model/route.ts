import { NextRequest, NextResponse } from "next/server";
import { saveModel } from "@/lib/claude";

/** Saves the model the app's AI features use ({ model: one of MODELS' ids }). */
export async function POST(req: NextRequest) {
  try {
    await saveModel(String((await req.json()).model ?? ""));
    return NextResponse.json({ ok: true });
  } catch (e) {
    return NextResponse.json({ error: (e as Error).message }, { status: 400 });
  }
}
