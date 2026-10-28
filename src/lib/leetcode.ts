import { fillEmptyBodies } from "./starter.ts";

/** Problem number and Python / C++ starters from LeetCode's public GraphQL API (no starters for premium problems). */
export async function leetcodeInfo(slug: string): Promise<{ id: string; paid: boolean; starter: string | null; cppStarter: string | null }> {
  const res = await fetch("https://leetcode.com/graphql", {
    method: "POST",
    headers: { "Content-Type": "application/json", Referer: "https://leetcode.com" },
    body: JSON.stringify({
      query: "query q($s: String!) { question(titleSlug: $s) { questionFrontendId isPaidOnly codeSnippets { langSlug code } } }",
      variables: { s: slug },
    }),
  });
  const q = (await res.json())?.data?.question;
  if (!q) throw new Error(`LeetCode has no problem "${slug}"`);
  const snippet = (lang: string): string | undefined => q.codeSnippets?.find((s: { langSlug: string }) => s.langSlug === lang)?.code;
  const py = snippet("python3"), cpp = snippet("cpp");
  return { id: q.questionFrontendId, paid: q.isPaidOnly, starter: py ? fillEmptyBodies(py) : null, cppStarter: cpp ? cpp.trimEnd() + "\n" : null };
}

let ncFiles: Promise<string[]> | null = null;

/** NeetCode's Python (or C++) solution for a LeetCode problem number, from github.com/neetcode-gh/leetcode (MIT). */
export async function neetcodeSolution(id: string, lang: "python" | "cpp" = "python"): Promise<string | null> {
  ncFiles ??= fetch("https://api.github.com/repos/neetcode-gh/leetcode/git/trees/main?recursive=1")
    .then((r) => r.json())
    .then((t) => (t.tree ?? []).map((f: { path: string }) => f.path));
  const file = (await ncFiles).find((p) => p.startsWith(`${lang}/${id.padStart(4, "0")}-`));
  if (!file) return null;
  const res = await fetch(`https://raw.githubusercontent.com/neetcode-gh/leetcode/main/${file}`);
  return res.ok ? (await res.text()).replace(/\s+$/, "") + "\n" : null;
}

export const slugOf = (url?: string) => url?.match(/leetcode\.com\/problems\/([\w-]+)/)?.[1];
