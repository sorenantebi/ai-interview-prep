import { NextRequest, NextResponse } from "next/server";
import { logActivity, remove } from "@/lib/content";
import { generatePlan, readPlan, savePlan } from "@/lib/plan";

const fail = (e: unknown, status = 400) => NextResponse.json({ error: (e as Error).message }, { status });

/** generate { start, weeks, hours, focus[], notes } · toggle { date, index, done } */
export async function POST(req: NextRequest) {
  const b = await req.json();
  try {
    if (b.action === "generate") {
      if (!/^\d{4}-\d{2}-\d{2}$/.test(b.start ?? "")) throw new Error("Pick a start date");
      const plan = await generatePlan({ start: b.start, weeks: Number(b.weeks) || 4, hours: Number(b.hours) || 2, focus: Array.isArray(b.focus) ? b.focus.map(String) : [], notes: String(b.notes ?? "") });
      await savePlan(plan);
      return NextResponse.json(plan);
    }
    if (b.action === "toggle") {
      const plan = await readPlan();
      const task = plan?.days.find((d) => d.date === b.date)?.tasks[Number(b.index)];
      if (!plan || !task) throw new Error("No such task");
      task.done = typeof b.done === "boolean" ? b.done : !task.done; // explicit value, so unticking a solved problem sticks
      await savePlan(plan);
      if (task.done) await logActivity();
      return NextResponse.json(plan);
    }
    throw new Error(`Unknown action ${b.action}`);
  } catch (e) {
    return fail(e, b.action === "generate" ? 500 : 400);
  }
}

export async function DELETE() {
  await remove("plan.json").catch(() => {});
  return NextResponse.json({ ok: true });
}
