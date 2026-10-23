/** "a/b" + "../c/./d" -> "a/c/d"; a leading ".." means it escaped the root. (No node:path: this also runs in the browser.) */
function join(dir: string, rel: string): string {
  const out: string[] = [];
  for (const part of `${dir}/${rel}`.split("/")) {
    if (!part || part === ".") continue;
    if (part === "..") { if (!out.length || out[out.length - 1] === "..") out.push(".."); else out.pop(); }
    else out.push(part);
  }
  return out.join("/") || ".";
}

/**
 * Rewrites a relative link or image in a repo's markdown so it works in the app:
 * links -> /repos/<name>/<path>, images -> /api/repos/raw?path=repos/<name>/<path>. Absolute URLs, anchors and links
 * that would climb out of the repo are left alone (the latter become "#").
 */
export function resolveRepoUrl(url: string, key: string, repo: { name: string; dir: string }): string {
  if (!url || /^([a-z][a-z0-9+.-]*:|\/\/|#|\/)/i.test(url)) return url;
  const [rawPath, hash = ""] = url.split("#");
  const [p, query] = rawPath.split("?");
  const rel = join(repo.dir, decodeURIComponent(p));
  if (rel.startsWith("..")) return "#";
  const clean = rel === "." ? "" : rel.replace(/\/$/, "");
  if (key === "src") return `/api/repos/raw?path=${encodeURIComponent(`repos/${repo.name}/${clean}`)}`;
  const href = `/repos/${[repo.name, ...clean.split("/").filter(Boolean)].map(encodeURIComponent).join("/")}`;
  return href + (query ? `?${query}` : "") + (hash ? `#${hash}` : "");
}
