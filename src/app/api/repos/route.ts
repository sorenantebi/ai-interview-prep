import { NextRequest, NextResponse } from "next/server";
import { addRepo, pullRepo, removeRepo } from "@/lib/repos";

const fail = (e: unknown) => NextResponse.json({ error: (e as Error).message }, { status: 400 });

export async function POST(req: NextRequest) {
  const { action, url, name } = await req.json();
  try {
    if (action === "add") return NextResponse.json({ name: await addRepo(url) });
    if (action === "pull") return NextResponse.json({ output: await pullRepo(name) });
    return fail(new Error(`Unknown action ${action}`));
  } catch (e) {
    return fail(e);
  }
}

export async function DELETE(req: NextRequest) {
  try {
    await removeRepo(req.nextUrl.searchParams.get("name") ?? "");
    return NextResponse.json({ ok: true });
  } catch (e) {
    return fail(e);
  }
}
