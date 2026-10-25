import { NextRequest, NextResponse } from "next/server";
import { logActivity, remove } from "@/lib/content";
import { addTask, generatePlan, readPlan, removeTask, savePlan } from "@/lib/plan";

const fail = (e: unknown, status = 400) => NextResponse.json({ error: (e as Error).message }, { status });

/** generate { start, weeks, focus[], notes, previous? } · toggle { date, index, done } · add { date, path, problem? } · remove { date, index } */
export async function POST(req: NextRequest) {
  const b = await req.json();
  try {
    if (b.action === "generate") {
      if (!/^\d{4}-\d{2}-\d{2}$/.test(b.start ?? "")) throw new Error("Pick a start date");
      const settings = { start: b.start, weeks: Number(b.weeks) || 4, focus: Array.isArray(b.focus) ? b.focus.map(String) : [], notes: String(b.notes ?? ""), previous: b.previous === true };
      // Streams one JSON line per update ({progress} … then {plan} or {error}), so the page can show what Claude is doing.
      const enc = new TextEncoder();
      return new Response(new ReadableStream({
        async start(ctrl) {
          const send = (o: object) => { try { ctrl.enqueue(enc.encode(JSON.stringify(o) + "\n")); } catch {} };
          let last = 0, phase = "";
          try {
            const plan = await generatePlan(settings, (p) => {
              if (p.phase === phase && Date.now() - last < 200) return; // a few updates a second is plenty
              last = Date.now();
              phase = p.phase;
              send({ progress: p });
            });
            await savePlan(plan);
            send({ plan });
          } catch (e) {
            send({ error: (e as Error).message });
          }
          ctrl.close();
        },
      }), { headers: { "Content-Type": "application/x-ndjson", "Cache-Control": "no-store" } });
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
    if (b.action === "add") return NextResponse.json(await addTask(String(b.date), String(b.path), b.problem ? String(b.problem) : undefined));
    if (b.action === "remove") return NextResponse.json(await removeTask(String(b.date), Number(b.index)));
    throw new Error(`Unknown action ${b.action}`);
  } catch (e) {
    return fail(e, b.action === "generate" ? 500 : 400);
  }
}

export async function DELETE() {
  await remove("plan.json").catch(() => {});
  return NextResponse.json({ ok: true });
}
