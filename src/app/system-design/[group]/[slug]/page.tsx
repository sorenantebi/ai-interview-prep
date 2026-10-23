import Link from "next/link";
import { notFound } from "next/navigation";
import Markdown from "@/components/Markdown";
import ExcalidrawView, { parseScene } from "@/components/ExcalidrawView";
import Difficulty from "@/components/Difficulty";
import SolvedToggle from "@/components/SolvedToggle";
import { parse, progress, read } from "@/lib/content";

export const dynamic = "force-dynamic";

const youtubeId = (url?: string) => url?.match(/(?:v=|youtu\.be\/|embed\/)([\w-]{11})/)?.[1];

export default async function SystemDesignProblem({ params }: { params: Promise<{ group: string; slug: string }> }) {
  const { group: g, slug } = await params;
  const group = decodeURIComponent(g);
  const path = `system-design/${group}/${decodeURIComponent(slug)}`;
  const [question, solution, notes, diagramFile, deepDiveFile] = await Promise.all(
    ["question.md", "solution.md", "notes.md", "diagram.excalidraw", "deep-dive.excalidraw"].map((f) => read(`${path}/${f}`)),
  );
  const diagrams = [["Solution diagram", parseScene(diagramFile)], ["Deep dive", parseScene(deepDiveFile)]] as const;
  if (question === null) notFound();
  const { data } = parse(question);
  const vid = youtubeId(data.video);
  const status = (await progress())[path]?.status;

  return (
    <div className="mx-auto max-w-4xl space-y-6">
      <div className="flex flex-wrap items-center gap-2 text-sm">
        <Link href="/system-design" className="text-muted hover:text-fg">← System Design · {group.replace(/^\d+\s*/, "")}</Link>
        <Difficulty level={data.difficulty} />
        <span className="flex-1" />
        <Link href={`/ai?tab=interview&kind=system-design&problem=${encodeURIComponent(path)}`} className="btn-primary">Mock interview</Link>
        <SolvedToggle path={path} status={status} label="Mark done" />
      </div>
      {vid && (
        <div className="card aspect-video overflow-hidden">
          <iframe
            className="h-full w-full"
            src={`https://www.youtube-nocookie.com/embed/${vid}`}
            title={`${data.problem ?? "System design"} video walkthrough`}
            allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; fullscreen"
            allowFullScreen
          />
        </div>
      )}
      <article className="card p-6"><Markdown>{question}</Markdown></article>
      {solution && (
        <details className="card group">
          <summary className="cursor-pointer select-none px-6 py-4 font-medium">Show solution / summary</summary>
          <div className="space-y-6 border-t border-border p-6">
            {diagrams.map(([label, scene]) => scene && (
              <figure key={label} className="space-y-2">
                <figcaption className="tag">{label}</figcaption>
                <div className="overflow-x-auto border border-border">
                  <ExcalidrawView scene={scene} title={`${data.problem ?? "System design"}: ${label}`} className="w-full min-w-[640px]" />
                </div>
              </figure>
            ))}
            <Markdown>{solution}</Markdown>
          </div>
        </details>
      )}
      {notes && (
        <details className="card" open>
          <summary className="cursor-pointer select-none px-6 py-4 font-medium">My notes</summary>
          <div className="border-t border-border p-6"><Markdown>{notes}</Markdown></div>
        </details>
      )}
      <p className="text-xs text-muted">
        Edit these files under <Link className="underline" href={`/files?path=${encodeURIComponent(path)}`}>Files</Link> (add a <code>notes.md</code> for your own summary).
      </p>
    </div>
  );
}
