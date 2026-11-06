import { NextRequest, NextResponse } from "next/server";
import { logActivity, read, remove, setProgress } from "@/lib/content";
import { completeTasks } from "@/lib/plan";
import { claude, prompt } from "@/lib/claude";
import { AREA, runRepo, saveWork, workingRepo } from "@/lib/repo";

const fence = (files: Record<string, string>) => Object.entries(files).map(([f, c]) => `=== ${f} ===\n\`\`\`python\n${c}\n\`\`\``).join("\n\n");

/**
 * Repo Debugging. Actions, each with { path } (the problem folder):
 * save { files } · run { files } (the visible tests) · submit { files } (plus the hidden tests; passing marks it solved) ·
 * reset (back to the original repo) · assistant { message, files, changed?, sessionId? } (the AI chat: reads files, never edits)
 * `files` is every file of the project as you have it now (added ones included, deleted ones left out).
 */
export async function POST(req: NextRequest) {
  const b = await req.json();
  try {
    const path = String(b.path ?? "");
    if (!path.startsWith(`${AREA}/`) || path.includes("..") || (await read(`${path}/question.md`)) === null) throw new Error("Not a repo problem");
    const files: Record<string, string> | null = b.files && typeof b.files === "object" ? b.files : null;
    const save = () => (files ? saveWork(path, files) : Promise.resolve());
    switch (b.action) {
      case "save":
        await save();
        return NextResponse.json({ ok: true });
      case "run":
      case "submit": {
        await save();
        await logActivity();
        const r = await runRepo(path, (await workingRepo(path)).files, b.action === "submit");
        if (b.action === "submit") {
          await setProgress(path, r.ok ? "solved" : "attempted");
          if (r.ok) await completeTasks(path);
        }
        return NextResponse.json(r);
      }
      case "reset":
        await remove(`${path}/work.json`).catch(() => {});
        return NextResponse.json({ ok: true });
      case "assistant": {
        const message = String(b.message ?? "").slice(0, 20_000);
        const changed = b.changed && typeof b.changed === "object" && Object.keys(b.changed).length ? `\n\n[My current versions of these files (a file shown empty and marked deleted is gone)]\n${fence(b.changed)}` : "";
        if (b.sessionId) return NextResponse.json(await claude(message + changed, { sessionId: String(b.sessionId) }));
        // First message: the task and every file (with the candidate's edits so far); later turns resume this session.
        await save();
        const input = await prompt("repo-assistant", { question: (await read(`${path}/question.md`)) ?? "", files: fence((await workingRepo(path)).files) });
        return NextResponse.json(await claude(`${input}\n\n# The candidate's first message\n\n${message}`));
      }
    }
    throw new Error(`Unknown action ${b.action}`);
  } catch (e) {
    return NextResponse.json({ error: (e as Error).message }, { status: 500 });
  }
}
