import fs from "node:fs/promises";
import { NextRequest, NextResponse } from "next/server";
import { safePath } from "@/lib/content";

const TYPES: Record<string, string> = { png: "image/png", jpg: "image/jpeg", jpeg: "image/jpeg", gif: "image/gif", webp: "image/webp", svg: "image/svg+xml", ico: "image/x-icon", avif: "image/avif" };

/** Serves images from cloned repos for their READMEs. Only image types; SVG is sandboxed so it can't run scripts. */
export async function GET(req: NextRequest) {
  const rel = req.nextUrl.searchParams.get("path") ?? "";
  const type = TYPES[rel.split(".").pop()?.toLowerCase() ?? ""];
  if (!rel.startsWith("repos/") || !type) return NextResponse.json({ error: "Not an image in a repo" }, { status: 400 });
  try {
    const data = await fs.readFile(safePath(rel));
    return new NextResponse(new Uint8Array(data), {
      headers: { "Content-Type": type, "X-Content-Type-Options": "nosniff", "Content-Security-Policy": "default-src 'none'; style-src 'unsafe-inline'; sandbox" },
    });
  } catch {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }
}
