import { NextResponse } from "next/server";
import fs from "node:fs/promises";
import path from "node:path";

// Serves the installed Monaco editor, so the code editor works offline (by default it loads from a CDN).
const ROOT = path.join(process.cwd(), "node_modules/monaco-editor/min/vs");
const TYPES: Record<string, string> = { ".js": "text/javascript", ".css": "text/css", ".ttf": "font/ttf", ".json": "application/json" };

export async function GET(_: Request, { params }: { params: Promise<{ path: string[] }> }) {
  const file = path.join(ROOT, ...(await params).path);
  if (!file.startsWith(ROOT + path.sep)) return new NextResponse("Not found", { status: 404 });
  try {
    return new NextResponse(new Uint8Array(await fs.readFile(file)), {
      headers: { "Content-Type": TYPES[path.extname(file)] ?? "application/octet-stream", "Cache-Control": "public, max-age=604800" },
    });
  } catch {
    return new NextResponse("Not found", { status: 404 });
  }
}
