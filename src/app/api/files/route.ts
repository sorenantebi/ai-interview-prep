import { NextRequest, NextResponse } from "next/server";
import { mkdir, read, remove, rename, tree, write } from "@/lib/content";

const fail = (e: unknown) => NextResponse.json({ error: (e as Error).message }, { status: 400 });

export async function GET(req: NextRequest) {
  const p = req.nextUrl.searchParams.get("path");
  try {
    if (p === null) return NextResponse.json(await tree());
    const content = await read(p);
    return content === null ? NextResponse.json({ error: "Not found" }, { status: 404 }) : NextResponse.json({ content });
  } catch (e) {
    return fail(e);
  }
}

export async function PUT(req: NextRequest) {
  const { path, content } = await req.json();
  try {
    await write(path, content);
    return NextResponse.json({ ok: true });
  } catch (e) {
    return fail(e);
  }
}

export async function POST(req: NextRequest) {
  const { action, path, to } = await req.json();
  try {
    if (action === "mkdir") await mkdir(path);
    else if (action === "rename") await rename(path, to);
    else return fail(new Error(`Unknown action ${action}`));
    return NextResponse.json({ ok: true });
  } catch (e) {
    return fail(e);
  }
}

export async function DELETE(req: NextRequest) {
  try {
    await remove(req.nextUrl.searchParams.get("path") ?? "");
    return NextResponse.json({ ok: true });
  } catch (e) {
    return fail(e);
  }
}
