import fs from "node:fs/promises";
import Link from "next/link";
import { notFound } from "next/navigation";
import Markdown from "@/components/Markdown";
import { safePath } from "@/lib/content";

export const dynamic = "force-dynamic";

const MAX = 512 * 1024;
const LANG: Record<string, string> = { ts: "typescript", tsx: "typescript", js: "javascript", jsx: "javascript", mjs: "javascript", py: "python", rb: "ruby", go: "go", rs: "rust", java: "java", kt: "kotlin", c: "c", h: "c", cpp: "cpp", cc: "cpp", hpp: "cpp", cs: "csharp", swift: "swift", sh: "bash", zsh: "bash", yml: "yaml", yaml: "yaml", json: "json", toml: "ini", sql: "sql", html: "xml", xml: "xml", css: "css", scss: "scss", dockerfile: "dockerfile", ipynb: "json" };

export default async function RepoBrowser({ params }: { params: Promise<{ name: string; path?: string[] }> }) {
  const { name, path = [] } = await params;
  const parts = [decodeURIComponent(name), ...path.map(decodeURIComponent)];
  const rel = `repos/${parts.join("/")}`;
  const abs = safePath(rel);
  const stat = await fs.stat(abs).catch(() => null);
  if (!stat) notFound();
  const href = (n: number) => "/repos/" + parts.slice(0, n).map(encodeURIComponent).join("/");

  let body: React.ReactNode;
  if (stat.isDirectory()) {
    const entries = (await fs.readdir(abs, { withFileTypes: true })).filter((e) => e.name !== ".git").sort((a, b) => Number(b.isDirectory()) - Number(a.isDirectory()) || a.name.localeCompare(b.name));
    const readme = entries.find((e) => e.isFile() && /^readme(\.md)?$/i.test(e.name));
    body = (
      <>
        <ul className="card divide-y divide-border font-mono text-sm">
          {parts.length > 1 && <li><Link href={href(parts.length - 1)} className="block px-4 py-1.5 text-muted hover:bg-fg/5">..</Link></li>}
          {entries.map((e) => (
            <li key={e.name}>
              <Link href={`${href(parts.length)}/${encodeURIComponent(e.name)}`} className="flex gap-2 px-4 py-1.5 hover:bg-fg/5">
                <span className="w-4 text-muted">{e.isDirectory() ? "▸" : ""}</span>{e.name}{e.isDirectory() ? "/" : ""}
              </Link>
            </li>
          ))}
        </ul>
        {readme && (
          <article className="card p-6">
            <div className="tag mb-4">{readme.name}</div>
            <Markdown repo={{ name: parts[0], dir: parts.slice(1).join("/") }}>{await fs.readFile(`${abs}/${readme.name}`, "utf8")}</Markdown>
          </article>
        )}
      </>
    );
  } else if (stat.size > MAX) {
    body = <p className="card p-4 text-sm text-muted">This file is {(stat.size / 1024 / 1024).toFixed(1)} MB, too large to show here.</p>;
  } else {
    const buf = await fs.readFile(abs);
    const file = parts.at(-1)!;
    const ext = (file.toLowerCase() === "dockerfile" ? "dockerfile" : file.split(".").pop() ?? "").toLowerCase();
    if (buf.subarray(0, 8000).includes(0)) body = <p className="card p-4 text-sm text-muted">Binary file ({stat.size.toLocaleString()} bytes).</p>;
    else if (ext === "md") body = <article className="card p-6"><Markdown repo={{ name: parts[0], dir: parts.slice(1, -1).join("/") }}>{buf.toString("utf8")}</Markdown></article>;
    else {
      const text = buf.toString("utf8");
      const fence = "`".repeat(Math.max(3, ...(text.match(/`+/g) ?? [""]).map((m) => m.length + 1)));
      body = (
        <div className="card overflow-hidden [&_.md_pre]:m-0 [&_.md_pre]:max-h-none">
          <div className="border-b border-border px-4 py-2 font-mono text-xs text-muted">{text.split("\n").length} lines · {stat.size.toLocaleString()} bytes</div>
          <Markdown>{`${fence}${LANG[ext] ?? ""}\n${text}\n${fence}`}</Markdown>
        </div>
      );
    }
  }

  return (
    <div className="space-y-4">
      <nav className="flex flex-wrap items-center gap-1 font-mono text-sm" aria-label="Breadcrumb">
        <Link href="/repos" className="text-muted hover:text-fg">repos</Link>
        {parts.map((p, i) => (
          <span key={i} className="flex items-center gap-1">
            <span className="text-muted">/</span>
            {i === parts.length - 1 ? <span className="font-medium">{p}</span> : <Link href={href(i + 1)} className="hover:underline">{p}</Link>}
          </span>
        ))}
      </nav>
      {body}
    </div>
  );
}
