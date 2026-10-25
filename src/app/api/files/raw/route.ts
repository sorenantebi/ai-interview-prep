import fs from "node:fs/promises";
import { NextRequest, NextResponse } from "next/server";
import { safePath } from "@/lib/content";

const RAW_TYPES: Record<string, string> = {
  pdf: "application/pdf", png: "image/png", jpg: "image/jpeg", jpeg: "image/jpeg", gif: "image/gif", webp: "image/webp", svg: "image/svg+xml", avif: "image/avif",
};

/** Serves PDFs and images from content/ for the dashboard and the Files viewer. Other types aren't served. */
export async function GET(req: NextRequest) {
  const rel = req.nextUrl.searchParams.get("path") ?? "";
  const type = RAW_TYPES[rel.split(".").pop()?.toLowerCase() ?? ""];
  if (!type) return NextResponse.json({ error: "Only PDFs and images" }, { status: 400 });
  try {
    const data = await fs.readFile(safePath(rel));
    const headers: Record<string, string> = { "Content-Type": type, "X-Content-Type-Options": "nosniff" };
    if (type === "image/svg+xml") headers["Content-Security-Policy"] = "default-src 'none'; style-src 'unsafe-inline'; sandbox"; // an uploaded SVG can't run scripts
    return new NextResponse(new Uint8Array(data), { headers });
  } catch {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }
}
