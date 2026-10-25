import { NextRequest, NextResponse } from "next/server";
import fs from "node:fs/promises";
import { mkdir, read, remove, rename, safePath, tree, write } from "@/lib/content";

const stat = (p: string) => fs.stat(safePath(p)).catch(() => null);

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

const MAX_UPLOAD = 50 * 1024 * 1024;

/** Saves an uploaded file into content/misc/ under a safe name, never overwriting (adds " (2)" etc.). */
async function upload(req: NextRequest) {
  const file = (await req.formData()).get("file");
  if (!(file instanceof File)) throw new Error("No file");
  if (file.size > MAX_UPLOAD) throw new Error("Files up to 50 MB");
  const clean = file.name.replace(/[^\w.\- ()]+/g, "_").replace(/^\.+/, "").slice(-120) || "upload";
  const dot = clean.lastIndexOf(".");
  const [stem, ext] = dot > 0 ? [clean.slice(0, dot), clean.slice(dot)] : [clean, ""];
  for (let n = 1; ; n++) {
    const p = `misc/${n === 1 ? stem : `${stem} (${n})`}${ext}`;
    if ((await stat(p)) === null) { await write(p, new Uint8Array(await file.arrayBuffer())); return p; }
  }
}

export async function POST(req: NextRequest) {
  if (req.headers.get("content-type")?.startsWith("multipart/form-data")) {
    try { return NextResponse.json({ path: await upload(req) }); } catch (e) { return fail(e); }
  }
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
