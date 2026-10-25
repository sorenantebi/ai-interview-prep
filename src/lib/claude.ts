import { spawn, type ChildProcessWithoutNullStreams, type StdioOptions } from "node:child_process";
import { tmpdir } from "node:os";
import { read, write } from "./content.ts";

/** Loads content/prompts/<name>.md and fills {{vars}}. */
export async function prompt(name: string, vars: Record<string, string> = {}) {
  const tpl = await read(`prompts/${name}.md`);
  if (tpl === null) throw new Error(`Missing prompt file content/prompts/${name}.md`);
  return tpl.replace(/\{\{(\w+)\}\}/g, (_, k) => vars[k] ?? "");
}

const bin = () => process.env.CLAUDE_BIN ?? "claude";
const WIN = process.platform === "win32";

/** Starts the claude CLI. On Windows an npm install is `claude.cmd`, which only runs through the shell, and the shell drops empty args unless quoted. */
// Typed as all-piped: callers only touch the streams they asked to pipe.
function cli(args: string[], stdio: StdioOptions) {
  const child = WIN ? spawn(`"${bin()}"`, args.map((a) => `"${a}"`), { cwd: tmpdir(), stdio, shell: true }) : spawn(bin(), args, { cwd: tmpdir(), stdio });
  return child as ChildProcessWithoutNullStreams;
}

/** Runs the local Claude Code CLI headlessly. Uses whatever account `claude` is logged into. */
/** Models you can pick on the Claude page, by exact model ID ("" = whatever Claude Code itself defaults to). */
export const MODELS: { id: string; label: string; group: string }[] = [
  { id: "", label: "Claude Code default", group: "" },
  { id: "claude-opus-5-5", label: "Claude Opus 5.5", group: "Opus" },
  { id: "claude-opus-5", label: "Claude Opus 5", group: "Opus" },
  { id: "claude-sonnet-5-5", label: "Claude Sonnet 5.5", group: "Sonnet" },
  { id: "claude-sonnet-5", label: "Claude Sonnet 5", group: "Sonnet" },
  { id: "claude-haiku-5-5", label: "Claude Haiku 5.5", group: "Haiku" },
];
const ALIASES: Record<string, string> = { opus: "claude-opus-5-5", sonnet: "claude-sonnet-5-5", haiku: "claude-haiku-5-5" };

/** The model picked on the Claude page (settings.json), or "" for Claude Code's default. Older alias picks map to IDs. */
export async function savedModel(): Promise<string> {
  try {
    const m = JSON.parse((await read("settings.json")) ?? "{}").model ?? "";
    return ALIASES[m] ?? m;
  } catch { return ""; }
}

/** The exact name of Claude Code's own default model, e.g. "Opus 5.5" (from `/model`); null if it can't be read. */
export function defaultModelName(): Promise<string | null> {
  return new Promise((resolve) => {
    const child = cli(["-p", "/model", "--setting-sources", "", "--strict-mcp-config"], ["ignore", "pipe", "ignore"]);
    let out = "";
    child.stdout.on("data", (d) => (out += d));
    child.on("error", () => resolve(null));
    const timer = setTimeout(() => child.kill(), 30_000);
    child.on("close", () => { clearTimeout(timer); resolve(out.match(/Current model: `([^`(]+?)\s*(?:\(default\))?`/)?.[1]?.trim() ?? null); });
  });
}

export async function saveModel(model: string) {
  if (!MODELS.some((m) => m.id === model)) throw new Error(`Unknown model ${model}`);
  let settings: Record<string, unknown> = {};
  try { settings = JSON.parse((await read("settings.json")) ?? "{}"); } catch {}
  await write("settings.json", JSON.stringify({ ...settings, model }, null, 2));
}

export async function claude(input: string, opts: { sessionId?: string; tools?: string[]; model?: string } = {}): Promise<{ text: string; sessionId: string }> {
  const model = opts.model ?? (await savedModel());
  // Only the listed tools exist (e.g. WebFetch); the app writes all files itself.
  // Empty setting sources + strict MCP keep the user's own hooks/plugins/MCP servers out.
  const args = ["-p", "--output-format", "json", "--tools", (opts.tools ?? []).join(","), "--setting-sources", "", "--strict-mcp-config"];
  if (opts.tools?.length) args.push("--allowedTools", opts.tools.join(","));
  if (opts.sessionId) args.push("--resume", opts.sessionId);
  if (model) args.push("--model", model);

  return new Promise((resolve, reject) => {
    const child = cli(args, ["pipe", "pipe", "pipe"]);
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
    const timer = setTimeout(() => child.kill(), 10 * 60_000); // safety limit; long jobs use claudeStream
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
    const child = cli(["-p", "/usage", "--setting-sources", "", "--strict-mcp-config"], ["ignore", "pipe", "pipe"]);
    let out = "", err = "";
    child.stdout.on("data", (d) => (out += d));
    child.stderr.on("data", (d) => (err += d));
    child.on("error", (e) => reject(new Error(`Could not start claude CLI: ${e.message}`)));
    const timer = setTimeout(() => child.kill(), 60_000);
    child.on("close", () => { clearTimeout(timer); resolve({ limits: parseUsage(out), raw: (out || err).trim() }); });
  });
}


/** Whether Claude Code is logged in, and how. Only these three fields leave the server (no email or org). */
export function authStatus(): Promise<{ installed: boolean; loggedIn: boolean; method?: string; plan?: string }> {
  return new Promise((resolve) => {
    const child = cli(["auth", "status", "--json"], ["ignore", "pipe", "ignore"]);
    let out = "";
    child.stdout.on("data", (d) => (out += d));
    child.on("error", () => resolve({ installed: false, loggedIn: false }));
    child.on("close", () => {
      try {
        const s = JSON.parse(out);
        resolve({ installed: true, loggedIn: !!s.loggedIn, method: s.authMethod, plan: s.subscriptionType });
      } catch {
        resolve({ installed: true, loggedIn: false });
      }
    });
  });
}

const LINUX_TERMINALS: [string, string[]][] = [
  ["x-terminal-emulator", ["-e"]], ["gnome-terminal", ["--"]], ["konsole", ["-e"]], ["xfce4-terminal", ["-x"]],
  ["kitty", []], ["alacritty", ["-e"]], ["xterm", ["-e"]],
];

/** The program + args that open a terminal window running `claude auth login` on this OS (null: none found). */
export function loginTerminal(platform: string, has: (cmd: string) => boolean, claudeBin = bin()): { cmd: string; args: string[] } | null {
  const login = `${claudeBin} auth login`;
  if (platform === "darwin")
    return { cmd: "osascript", args: ["-e", `tell application "Terminal" to do script ${JSON.stringify(login)}`, "-e", 'tell application "Terminal" to activate'] };
  if (platform === "win32") return { cmd: "cmd.exe", args: ["/c", "start", "Claude login", "cmd.exe", "/k", login] };
  const t = LINUX_TERMINALS.find(([name]) => has(name));
  return t ? { cmd: t[0], args: [...t[1], claudeBin, "auth", "login"] } : null;
}

/** Opens a terminal window where you log in to Claude Code yourself; the app never sees credentials. */
export async function openLogin(): Promise<{ opened: boolean; command: string }> {
  const { execFileSync } = await import("node:child_process");
  const has = (cmd: string) => { try { execFileSync("which", [cmd], { stdio: "ignore" }); return true; } catch { return false; } };
  const t = loginTerminal(process.platform, has);
  const command = `${bin()} auth login`;
  if (!t) return { opened: false, command };
  const child = spawn(t.cmd, t.args, { detached: true, stdio: "ignore" });
  child.on("error", () => {});
  child.unref();
  return { opened: true, command };
}

export type StreamEvent = { kind: "thinking" } | { kind: "text"; text: string } | { kind: "tokens"; input: number; output: number };

/**
 * Like claude(), but streams: onEvent gets "thinking" when Claude starts reasoning and each piece of text as it's
 * written, so long jobs can show live progress. Uses Claude Code's stream-json output.
 */
export async function claudeStream(input: string, onEvent: (e: StreamEvent) => void, opts: { model?: string; timeoutMs?: number } = {}): Promise<{ text: string; sessionId: string }> {
  const model = opts.model ?? (await savedModel());
  const args = ["-p", "--output-format", "stream-json", "--verbose", "--include-partial-messages", "--tools", "", "--setting-sources", "", "--strict-mcp-config"];
  if (model) args.push("--model", model);
  return new Promise((resolve, reject) => {
    const child = cli(args, ["pipe", "pipe", "pipe"]);
    let buf = "", err = "", result: { text: string; sessionId: string } | null = null, failure = "";
    // Input tokens come with message_start; output is only reported at the end, so estimate it live (~4 chars a token).
    let tokensIn = 0, tokensOut = 0, chars = 0;
    child.stdout.on("data", (d) => {
      buf += d;
      let nl;
      while ((nl = buf.indexOf("\n")) >= 0) {
        const line = buf.slice(0, nl);
        buf = buf.slice(nl + 1);
        let ev;
        try { ev = JSON.parse(line); } catch { continue; }
        const e = ev.event;
        if (ev.type === "stream_event" && e?.type === "message_start") {
          const u = e.message?.usage ?? {};
          tokensIn = (u.input_tokens ?? 0) + (u.cache_creation_input_tokens ?? 0) + (u.cache_read_input_tokens ?? 0);
          onEvent({ kind: "tokens", input: tokensIn, output: tokensOut });
        } else if (ev.type === "stream_event" && e?.type === "content_block_start" && e.content_block?.type === "thinking") onEvent({ kind: "thinking" });
        else if (ev.type === "stream_event" && e?.type === "content_block_delta") {
          chars += (e.delta?.text ?? e.delta?.thinking ?? "").length;
          tokensOut = Math.max(tokensOut, Math.round(chars / 4));
          if (e.delta?.type === "text_delta") onEvent({ kind: "text", text: e.delta.text });
          onEvent({ kind: "tokens", input: tokensIn, output: tokensOut });
        } else if (ev.type === "stream_event" && e?.type === "message_delta" && e.usage?.output_tokens) {
          tokensOut = e.usage.output_tokens;
          onEvent({ kind: "tokens", input: tokensIn, output: tokensOut });
        }
        else if (ev.type === "result") {
          if (ev.is_error) failure = ev.result || "Claude returned an error";
          else result = { text: ev.result, sessionId: ev.session_id };
        }
      }
    });
    child.stderr.on("data", (d) => (err += d));
    child.on("error", (e) => reject(new Error(`Could not start claude CLI: ${e.message}. Is Claude Code installed?`)));
    const limit = opts.timeoutMs ?? 30 * 60_000;
    const timer = setTimeout(() => { failure = `Stopped after ${Math.round(limit / 60_000)} minutes`; child.kill(); }, limit);
    child.on("close", (code) => {
      clearTimeout(timer);
      if (result) resolve(result);
      else reject(new Error(failure || `claude exited ${code}: ${err}`.slice(0, 2000)));
    });
    child.stdin.end(input);
  });
}
