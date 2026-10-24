import fs from "node:fs/promises";
import { NextRequest, NextResponse } from "next/server";
import { safePath } from "@/lib/content";

/** Serves PDFs from content/ (e.g. the dashboard's cheat sheet) for the browser's own PDF viewer. Only PDFs. */
export async function GET(req: NextRequest) {
  const rel = req.nextUrl.searchParams.get("path") ?? "";
  if (!rel.toLowerCase().endsWith(".pdf")) return NextResponse.json({ error: "Only PDFs" }, { status: 400 });
  try {
    const data = await fs.readFile(safePath(rel));
    return new NextResponse(new Uint8Array(data), { headers: { "Content-Type": "application/pdf", "X-Content-Type-Options": "nosniff" } });
  } catch {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }
}
