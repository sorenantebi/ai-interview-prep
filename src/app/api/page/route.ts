import { NextRequest, NextResponse } from "next/server";
import { addFile, chatPage, clearChat, fileUrl, readPage, savePage, undoPage } from "@/lib/page";

const fail = (e: unknown, status = 400) => NextResponse.json({ error: (e as Error).message }, { status });

/** chat { message } · clear-chat · save { html } · undo · upload (multipart form with "file") */
export async function POST(req: NextRequest) {
  try {
    if (req.headers.get("content-type")?.startsWith("multipart/form-data")) {
      const file = (await req.formData()).get("file");
      if (!(file instanceof File)) throw new Error("No file");
      const name = await addFile(file.name, Buffer.from(await file.arrayBuffer()));
      return NextResponse.json({ name, url: fileUrl(name) });
    }
    const b = await req.json();
    if (b.action === "chat") {
      if (!String(b.message ?? "").trim()) throw new Error("Write a message");
      try { return NextResponse.json({ messages: await chatPage(String(b.message)), html: await readPage() }); } catch (e) { return fail(e, 500); }
    }
    if (b.action === "clear-chat") { await clearChat(); return NextResponse.json({ messages: [] }); }
    if (b.action === "save") await savePage(String(b.html ?? ""));
    else if (b.action === "undo") { if (!(await undoPage())) throw new Error("Nothing to undo"); }
    else throw new Error(`Unknown action ${b.action}`);
    return NextResponse.json({ html: await readPage() });
  } catch (e) {
    return fail(e);
  }
}
