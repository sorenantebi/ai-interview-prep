import { NextRequest, NextResponse } from "next/server";
import { moveProblem, read, write } from "@/lib/content";
import { testsProblem } from "@/lib/run";
import { codeBlock } from "@/lib/starter";

const FILES = ["question.md", "starter.py", "solution.md", "tests.py"] as const;
const slug = (s: string) => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

/**
 * move { path, group }: puts a problem under another topic.
 * create-ml { group, files, force? }: saves your own ML coding problem; unless `force`, only when its tests work.
 */
export async function POST(req: NextRequest) {
  const b = await req.json();
  try {
    if (b.action === "move") return NextResponse.json({ path: await moveProblem(String(b.path ?? ""), String(b.group ?? "")) });
    if (b.action !== "create-ml") throw new Error(`Unknown action ${b.action}`);
    const group = String(b.group ?? "").trim();
    if (!group || /[/\\]/.test(group) || /^[._]/.test(group)) throw new Error("Pick a topic");
    const f = Object.fromEntries(FILES.map((n) => [n, String(b.files?.[n] ?? "")]));
    const title = f["question.md"].match(/^# (.+)$/m)?.[1].trim() ?? "";
    if (!slug(title) || title.includes("<")) throw new Error("Give the problem a title: the `# Title` line in question.md");
    const dir = `ml-coding/${group}/${slug(title)}`;
    if ((await read(`${dir}/question.md`)) !== null) throw new Error(`${dir} already exists`);
    if (!b.force) {
      const bad = await testsProblem({ reference: codeBlock(f["solution.md"]), starter: f["starter.py"], tests: f["tests.py"] });
      if (bad) return NextResponse.json({ error: bad, canForce: true }, { status: 422 });
    }
    for (const n of FILES) await write(`${dir}/${n}`, f[n]);
    return NextResponse.json({ path: dir });
  } catch (e) {
    return NextResponse.json({ error: (e as Error).message }, { status: 400 });
  }
}
