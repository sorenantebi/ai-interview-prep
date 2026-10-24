import fs from "node:fs/promises";
import { NextResponse } from "next/server";
import { safePath } from "@/lib/content";
import { IMAGE_TYPES } from "@/lib/page";

/** Serves the page's pictures. Images only; SVG is sandboxed so it can't run scripts. */
export async function GET(_: Request, { params }: { params: Promise<{ name: string }> }) {
  const name = decodeURIComponent((await params).name);
  const type = IMAGE_TYPES[name.split(".").pop()?.toLowerCase() ?? ""];
  if (!type || name.includes("/") || name.startsWith(".")) return NextResponse.json({ error: "Not a picture" }, { status: 400 });
  try {
    const data = await fs.readFile(safePath(`page/files/${name}`));
    return new NextResponse(new Uint8Array(data), { headers: { "Content-Type": type, "X-Content-Type-Options": "nosniff", "Content-Security-Policy": "default-src 'none'; style-src 'unsafe-inline'; sandbox" } });
  } catch {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }
}
