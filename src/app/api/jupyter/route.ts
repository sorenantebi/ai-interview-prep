import { NextRequest, NextResponse } from "next/server";
import fs from "node:fs/promises";
import { safePath } from "@/lib/content";
import { notebookUrl } from "@/lib/jupyter";

/** Opens a repo notebook in the app's Jupyter server. Body: { path } relative to content/repos. */
export async function POST(req: NextRequest) {
  const { path } = await req.json();
  try {
    if (typeof path !== "string" || !path.endsWith(".ipynb")) throw new Error("Not a notebook");
    await fs.access(safePath(`repos/${path}`));
    return NextResponse.json({ url: await notebookUrl(path, req.nextUrl.hostname) });
  } catch (e) {
    return NextResponse.json({ error: (e as Error).message }, { status: 500 });
  }
}
