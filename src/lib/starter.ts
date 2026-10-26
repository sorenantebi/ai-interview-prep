// Pure helpers shared by the server, the browser and scripts/fetch-neetcode.ts.

/** First ```python block of a markdown file. */
export const codeBlock = (md: string) => md.match(/```python\n([\s\S]*?)```/)?.[1] ?? "";

/** LeetCode snippets leave method bodies empty; give each one a `pass` so the file is valid Python. */
export function fillEmptyBodies(snippet: string): string {
  const lines = snippet.replace(/\s+$/, "").split("\n");
  const out: string[] = [];
  lines.forEach((line, i) => {
    out.push(line.trimEnd());
    const def = line.match(/^(\s*)def .*:\s*$/);
    if (!def) return;
    const next = lines.slice(i + 1).find((l) => l.trim() !== "");
    const indent = (s: string) => s.match(/^\s*/)![0].length;
    if (next === undefined || indent(next) <= def[1].length || next.trim().startsWith("#")) out.push(def[1] + "    pass");
  });
  return out.join("\n") + "\n";
}

/**
 * LeetCode-style starter from a full solution: comments, imports, `class Solution` (or a design class)
 * and its public method signatures only. Helper functions, nested defs and other classes are dropped.
 */
export function starterFrom(code: string): string {
  if (!code.trim()) return "class Solution:\n    pass\n";
  const lines = code.split("\n");
  const classes = [...code.matchAll(/^class (\w+)/gm)].map((m) => m[1]);
  const keep = new Set(classes.includes("Solution") ? ["Solution"] : classes.filter((c) => !/^(ListNode|TreeNode|Node)$/.test(c)));
  const out: string[] = [];
  let inKept = false;
  let bodyIndent = -1;
  for (const line of lines) {
    const indent = line.match(/^\s*/)![0].length;
    const cls = line.match(/^class (\w+)/);
    if (cls) {
      inKept = keep.has(cls[1]);
      bodyIndent = -1;
      if (inKept) out.push(line.trimEnd());
      continue;
    }
    if (indent === 0 && line.trim()) {
      inKept = false;
      if (/^(#|from |import )/.test(line)) out.push(line.trimEnd());
      if (/^(from |import )/.test(line) && !/^(from |import )/.test(lines[lines.indexOf(line) + 1] ?? "")) out.push("");
      continue;
    }
    if (!inKept) continue;
    const def = line.match(/^(\s+)def (\w+)\(/);
    if (def && bodyIndent < 0) bodyIndent = def[1].length;
    if (def && def[1].length === bodyIndent && (!def[2].startsWith("_") || def[2] === "__init__")) {
      out.push("", line.trimEnd(), def[1] + (def[1].includes("\t") ? "\t" : "    ") + "pass");
    }
  }
  return out.join("\n").replace(/\n{3,}/g, "\n\n").replace(/^\n+/, "").replace(/(class \w+.*:)\n\n/g, "$1\n") + "\n";
}

/** Parameter names of the method you implement ([] for design classes, which take calls + args). */
export function paramsOf(starter: string): string[] {
  const classes = [...starter.matchAll(/^class (\w+)/gm)].map((m) => m[1]);
  // A plain function (ML Coding) takes all its parameters; a design class takes calls + args.
  const def = !classes.length ? starter.match(/^def (?!_)\w+\(([^)]*)\)/m)
    : classes.includes("Solution") || classes.includes("Codec") ? starter.match(/^\s+def (?!_)\w+\(self,?\s*([^)]*)\)/m) : null;
  if (!def) return [];
  return def[1].split(",").map((p) => p.split(":")[0].split("=")[0].trim()).filter(Boolean);
}

export type Cases = { names: string[]; cases: string[][] };

/** Top-level bracketed values in a string, e.g. '["A","b"]\n[[1],[2]]' -> two values (brackets inside strings ignored). */
function topLevel(text: string): string[] {
  const out: string[] = [];
  let depth = 0, start = -1, quote = "";
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (quote) { if (c === quote && text[i - 1] !== "\\") quote = ""; continue; }
    if (c === '"' || c === "'") quote = c;
    else if (c === "[") { if (depth++ === 0) start = i; }
    else if (c === "]" && --depth === 0) out.push(text.slice(start, i + 1));
  }
  return out;
}

/** Example inputs from a question.md, as LeetCode testcases: one string per parameter. */
export function parseExamples(question: string, starter: string): Cases {
  const params = paramsOf(starter);
  const cases: string[][] = [];
  let names: string[] | null = null;
  const lines = question.split("\n");
  lines.forEach((line, i) => {
    const m = line.match(/^Input:\s*(.*)$/);
    if (!m) return;
    let text = m[1];
    for (let j = i + 1; j < lines.length && !/^(Output|Explanation|```)/.test(lines[j].trim()); j++) text += "\n" + lines[j];
    text = text.trim();
    // Design problems: the call list, then the argument list.
    const vals = /^\[\s*"/.test(text) && !/^\w+\s*=/.test(text) ? topLevel(text) : [];
    if (vals.length === 2 && !params.length) {
      names = ["calls", "args"];
      cases.push(vals.map((v) => v.replace(/\n\s*/g, "")));
      return;
    }
    const flat = text.replace(/\n\s*/g, "");
    const parts = flat.split(/,\s*(?=[A-Za-z_]\w*\s*=)/).map((p) => p.match(/^([A-Za-z_]\w*)\s*=\s*([\s\S]+)$/));
    if (parts.every(Boolean)) {
      names ??= parts.map((p) => p![1]);
      cases.push(parts.map((p) => p![2].trim()));
    } else cases.push([flat]);
    // Prose like "the same board, but…" is not a testcase.
    if (cases.at(-1)!.some((v) => !/^[\[{"'\-\d]|^(true|false|null|None|True|False)\b/.test(v))) cases.pop();
  });
  return { names: names ?? (params.length ? params : ["input"]), cases: cases.length ? cases : [params.map(() => "")] };
}

/** Strokes from a drawing.json (empty when missing or unreadable). */
export function strokesOf(json: string | null): { d: [number, number][]; w: number; accent?: boolean }[] {
  try { return JSON.parse(json ?? "{}").strokes ?? []; } catch { return []; }
}
