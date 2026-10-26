import Link from "next/link";
import MlProblemForm from "@/components/MlProblemForm";
import { groups, read } from "@/lib/content";

export const dynamic = "force-dynamic";

/** Write your own ML coding problem, starting from content/ml-coding/_template. */
export default async function NewMlProblem() {
  const names = ["question.md", "starter.py", "solution.md", "tests.py"];
  const template = Object.fromEntries(await Promise.all(names.map(async (n) => [n, (await read(`ml-coding/_template/${n}`)) ?? ""])));
  return (
    <div className="mx-auto max-w-6xl space-y-4">
      <Link href="/ml-coding" className="font-mono text-xs text-muted hover:text-fg">← ML Coding</Link>
      <h1 className="page-title">Add your own problem</h1>
      <p className="max-w-3xl text-sm text-muted">
        Fill in the four files, starting from the skeleton. On save, the app checks that your solution passes your tests and the empty starter fails them.
        Or let Claude write one: <Link href="/ai?tab=ml-coding" className="underline">Generate ML coding problem</Link>.
      </p>
      <MlProblemForm groups={await groups("ml-coding")} template={template} />
    </div>
  );
}
