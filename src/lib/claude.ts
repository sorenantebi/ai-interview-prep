import { spawn } from "node:child_process";
import { read } from "./content.ts";

/** Loads content/prompts/<name>.md and fills {{vars}}. */
export async function prompt(name: string, vars: Record<string, string> = {}) {
  const tpl = await read(`prompts/${name}.md`);
  if (tpl === null) throw new Error(`Missing prompt file content/prompts/${name}.md`);
  return tpl.replace(/\{\{(\w+)\}\}/g, (_, k) => vars[k] ?? "");
}

/** Runs the local Claude Code CLI headlessly. Uses whatever account `claude` is logged into. */
export function claude(input: string, opts: { sessionId?: string; tools?: string[] } = {}): Promise<{ text: string; sessionId: string }> {
  // Only the listed tools exist (e.g. WebFetch); the app writes all files itself.
  // Empty setting sources + strict MCP keep the user's own hooks/plugins/MCP servers out.
  const args = ["-p", "--output-format", "json", "--tools", (opts.tools ?? []).join(","), "--setting-sources", "", "--strict-mcp-config"];
  if (opts.tools?.length) args.push("--allowedTools", opts.tools.join(","));
  if (opts.sessionId) args.push("--resume", opts.sessionId);

  return new Promise((resolve, reject) => {
    const child = spawn(process.env.CLAUDE_BIN ?? "claude", args, { cwd: process.env.TMPDIR ?? "/tmp", stdio: ["pipe", "pipe", "pipe"] });
    let out = "", err = "";
    child.stdout.on("data", (d) => (out += d));
    child.stderr.on("data", (d) => (err += d));
    child.on("error", (e) => reject(new Error(`Could not start claude CLI: ${e.message}. Is Claude Code installed?`)));
    child.on("close", (code) => {
      try {
        const res = JSON.parse(out);
        if (res.is_error) return reject(new Error(res.result || "Claude returned an error"));
        resolve({ text: res.result, sessionId: res.session_id });
      } catch {
        reject(new Error(`claude exited ${code}: ${err || out}`.slice(0, 2000)));
      }
    });
    const timer = setTimeout(() => child.kill(), 5 * 60_000);
    child.on("close", () => clearTimeout(timer));
    child.stdin.end(input);
  });
}

/** Pulls `=== FILE: name ===` sections out of a model reply. */
export function files(text: string): Record<string, string> {
  const out: Record<string, string> = {};
  const re = /^=== FILE: (.+?) ===\n([\s\S]*?)(?=^=== FILE: |^=== END ===|(?![\s\S]))/gm;
  for (const m of text.matchAll(re)) out[m[1].trim()] = m[2].trim() + "\n";
  return out;
}

export type Limit = { label: string; used: number; resets: string | null };

/** Lines like "Current session: 60% used · resets Oct 23 at 11:19pm (Europe/Berlin)" from Claude Code's /usage. */
export function parseUsage(report: string): Limit[] {
  return [...report.matchAll(/^(Current [^:\n]+):\s*(\d+)% used(?:\s*·\s*resets ([^\n]+))?$/gm)].map((m) => ({ label: m[1].trim(), used: Number(m[2]), resets: m[3]?.trim() ?? null }));
}

/** Your plan's limits, read by running Claude Code's own `/usage` command (the app never touches credentials). */
export function planUsage(): Promise<{ limits: Limit[]; raw: string }> {
  return new Promise((resolve, reject) => {
    const child = spawn(process.env.CLAUDE_BIN ?? "claude", ["-p", "/usage", "--setting-sources", "", "--strict-mcp-config"], { cwd: process.env.TMPDIR ?? "/tmp", stdio: ["ignore", "pipe", "pipe"] });
    let out = "", err = "";
    child.stdout.on("data", (d) => (out += d));
    child.stderr.on("data", (d) => (err += d));
    child.on("error", (e) => reject(new Error(`Could not start claude CLI: ${e.message}`)));
    const timer = setTimeout(() => child.kill(), 60_000);
    child.on("close", () => { clearTimeout(timer); resolve({ limits: parseUsage(out), raw: (out || err).trim() }); });
  });
}
