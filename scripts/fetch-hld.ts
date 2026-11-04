// Downloads Hello Interview's diagrams for each system design problem: the last one under "High-Level Design" -> hld.<ext>,
// the one under "Final Design" -> final-design.<ext>. They're Hello Interview's work, so they're git-ignored (for your own study).
// Usage: node scripts/fetch-hld.ts [only-this-folder]
import fs from "node:fs";
import path from "node:path";

const root = path.join(process.cwd(), "content/system-design");
const BASE = "https://www.hellointerview.com";
const only = process.argv[2];
// Our folder name -> Hello Interview's slug, where they differ.
const SLUG: Record<string, string> = {
  "news-aggregator": "google-news",
  "local-delivery-service": "gopuff",
  "price-tracking-service": "camelcamelcamel",
  "youtube-top-k": "top-k",
  "rate-limiter": "distributed-rate-limiter",
};

/** The page's headings and images in order -> the HLD and final design image URLs. */
function pickDiagrams(html: string) {
  let section = "", hld: string | undefined, final: string | undefined;
  for (const m of html.matchAll(/<h([1-4])[^>]*>([\s\S]*?)<\/h\1>|<img[^>]*?src="([^"]+)"[^>]*>/g)) {
    if (m[2] !== undefined) {
      const text = m[2].replace(/<[^>]+>/g, "").trim();
      if (m[1] <= "2" || /^(High-Level Design|Potential Deep Dives|Final Design|What is Expected)/i.test(text)) section = text;
    } else if (/\.(svg|png|webp|jpe?g)(\?|$)/i.test(m[3]) && !m[3].startsWith("/assets/")) {
      const src = m[3].replaceAll("&amp;", "&");
      if (/^High-Level Design/i.test(section)) hld = src;
      else if (/^Final Design/i.test(section)) final ??= src;
    }
  }
  return { hld, final };
}

async function save(dir: string, name: string, src: string) {
  const res = await fetch(new URL(src, BASE), { headers: { "User-Agent": "Mozilla/5.0" } });
  if (!res.ok) throw new Error(`${name}: HTTP ${res.status}`);
  const ext = new URL(src, BASE).pathname.match(/\.(\w+)$/)![1].toLowerCase();
  for (const f of fs.readdirSync(dir)) if (f.startsWith(`${name}.`)) fs.rmSync(path.join(dir, f)); // an older copy in another format
  fs.writeFileSync(path.join(dir, `${name}.${ext}`), Buffer.from(await res.arrayBuffer()));
}

const report = { saved: [] as string[], missing: [] as string[], failed: [] as string[] };
for (const group of fs.readdirSync(root).filter((d) => !/ML System Design/.test(d) && fs.statSync(path.join(root, d)).isDirectory())) {
  for (const p of fs.readdirSync(path.join(root, group))) {
    const dir = path.join(root, group, p);
    if (!fs.existsSync(path.join(dir, "question.md")) || (only && p !== only)) continue;
    try {
      const res = await fetch(`${BASE}/learn/system-design/problem-breakdowns/${SLUG[p] ?? p}`, { headers: { "User-Agent": "Mozilla/5.0" } });
      if (!res.ok) throw new Error(`page HTTP ${res.status}`);
      const { hld, final } = pickDiagrams(await res.text());
      if (hld) await save(dir, "hld", hld);
      if (final) await save(dir, "final-design", final);
      (hld && final ? report.saved : report.missing).push(`${p}${hld ? "" : " (no HLD)"}${final ? "" : " (no final design)"}`);
    } catch (e) {
      report.failed.push(`${p}: ${(e as Error).message}`);
    }
    await new Promise((r) => setTimeout(r, 500)); // be polite
  }
}
console.log(JSON.stringify(report, null, 1));
