// Copies Obsidian Excalidraw drawings ("<Name> - Diagram.excalidraw.md", "<Name> - Deep Dive Diagram.excalidraw.md")
// into content/system-design/<category>/<slug>/diagram.excalidraw and deep-dive.excalidraw as plain Excalidraw JSON.
// Usage: node scripts/import-excalidraw.mjs [vaultDir]
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import LZString from "lz-string";

const vault = process.argv[2] ?? path.join(os.homedir(), "Documents/Obsidian Vault/ML Prep");
const root = path.join(vault, "System Design/General System Design");
const out = path.join(process.cwd(), "content/system-design");
const slug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

function decode(file) {
  const src = fs.readFileSync(file, "utf8");
  const compressed = src.match(/```compressed-json\n([\s\S]*?)```/)?.[1];
  const plain = src.match(/```json\n([\s\S]*?)```/)?.[1];
  const data = compressed ? JSON.parse(LZString.decompressFromBase64(compressed.replace(/\s+/g, ""))) : JSON.parse(plain);
  // The Obsidian plugin sometimes merges earlier labels into one text ("A ^id\n\nB"): only the last chunk is real.
  const clean = (t) => (typeof t === "string" && /\^\w+\s*\n\n/.test(t) ? t.split(/\^\w+\s*\n\n/).pop() : t);
  const elements = data.elements.filter((e) => !e.isDeleted).map((e) => (e.type === "text" ? { ...e, text: clean(e.text), originalText: clean(e.originalText) } : e));
  return { type: "excalidraw", version: 2, source: "obsidian", elements, appState: { viewBackgroundColor: "#ffffff" }, files: data.files ?? {} };
}

let n = 0;
const missing = [];
for (const cat of fs.readdirSync(root).filter((d) => /^\d\d /.test(d))) {
  for (const p of fs.readdirSync(path.join(root, cat)).filter((d) => !d.endsWith(".md"))) {
    const dest = path.join(out, cat, slug(p));
    if (!fs.existsSync(dest)) { missing.push(`${cat}/${p} (no problem folder)`); continue; }
    for (const [kind, name] of [["Diagram", "diagram.excalidraw"], ["Deep Dive Diagram", "deep-dive.excalidraw"]]) {
      const f = path.join(root, cat, p, `${p} - ${kind}.excalidraw.md`);
      if (!fs.existsSync(f)) continue;
      try {
        fs.writeFileSync(path.join(dest, name), JSON.stringify(decode(f)));
        n++;
      } catch (e) {
        missing.push(`${p} ${kind}: ${e.message}`);
      }
    }
  }
}
console.log(`imported ${n} drawings`);
if (missing.length) console.log(missing.join("\n"));
