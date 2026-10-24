import fs from "node:fs/promises";
import path from "node:path";
import { read, safePath, write } from "./content.ts";
import { claude, prompt } from "./claude.ts";

// The customizable page: content/page/page.html, its pictures in content/page/files/, older versions in history/.
const MAX_HISTORY = 20;
export const IMAGE_TYPES: Record<string, string> = { png: "image/png", jpg: "image/jpeg", jpeg: "image/jpeg", gif: "image/gif", webp: "image/webp", svg: "image/svg+xml" };

/** Your page, or the starter page (default.html, kept in git) until you change it. */
export const readPage = async () => (await read("page/page.html")) ?? (await read("page/default.html")) ?? "<!doctype html><html><body></body></html>";

/** Saves a new version, keeping the previous one in history/ so it can be undone. */
export async function savePage(html: string) {
  await write(`page/history/${Date.now()}.html`, await readPage());
  const dir = safePath("page/history");
  const old = (await fs.readdir(dir)).sort().slice(0, -MAX_HISTORY);
  await Promise.all(old.map((f) => fs.rm(path.join(dir, f))));
  await write("page/page.html", html);
}

/** Restores the newest saved version. Returns false when there is nothing to undo. */
export async function undoPage(): Promise<boolean> {
  const dir = safePath("page/history");
  const last = (await fs.readdir(dir).catch(() => [] as string[])).filter((f) => f.endsWith(".html")).sort().pop();
  if (!last) return false;
  await write("page/page.html", await fs.readFile(path.join(dir, last), "utf8"));
  await fs.rm(path.join(dir, last));
  return true;
}

export async function pageFiles(): Promise<string[]> {
  return (await fs.readdir(safePath("page/files")).catch(() => [] as string[])).filter((f) => !f.startsWith("."));
}
export const fileUrl = (name: string) => `/api/page/file/${encodeURIComponent(name)}`;

/**
 * Splits Claude's answer into the chat reply and the page. The page is found by its own boundaries
 * (<!doctype html> or <html> ... the last </html>), not by ``` fences, because pages often contain ``` themselves
 * (code blocks in notes), which used to cut the page short.
 */
export function splitReply(text: string): { reply: string; page: string | null; complete: boolean } {
  const start = text.search(/<!doctype html|<html[\s>]/i);
  if (start < 0) return { reply: text.trim() || "…", page: null, complete: false };
  const end = text.toLowerCase().lastIndexOf("</html>");
  const page = end > start ? text.slice(start, end + "</html>".length).trim() : text.slice(start).trim();
  const reply = text.slice(0, start).replace(/```html\s*$/i, "").trim() || "Done.";
  return { reply, page, complete: end > start };
}

export type ChatMessage = { role: "you" | "claude"; text: string; changed?: boolean; at: string };

export async function readChat(): Promise<ChatMessage[]> {
  try { return JSON.parse((await read("page/chat.json")) ?? "[]"); } catch { return []; }
}
export const clearChat = () => write("page/chat.json", "[]");

/**
 * One chat turn: Claude sees the recent conversation and the page as it is now (so undo and manual edits count),
 * replies, and returns a new page when the message asked for a change. Claude has no tools: it only returns text.
 */
export async function chatPage(message: string): Promise<ChatMessage[]> {
  const [chat, files, html] = await Promise.all([readChat(), pageFiles(), readPage()]);
  const input = await prompt("page", {
    history: chat.slice(-12).map((m) => `${m.role === "you" ? "User" : "You"}: ${m.text}`).join("\n") || "(new conversation)",
    request: message,
    files: files.length ? files.map((f) => `- ${fileUrl(f)} (${f})`).join("\n") : "(none)",
    html,
  });
  const { text } = await claude(input);
  const { reply, page, complete } = splitReply(text);
  const changed = complete;
  if (changed) await savePage(page + "\n");
  const now = new Date().toISOString();
  const next: ChatMessage[] = [...chat, { role: "you", text: message, at: now }, { role: "claude", text: page && !changed ? reply + "\n\n(The page I wrote was incomplete, so nothing changed. Try again.)" : reply, changed, at: now }];
  await write("page/chat.json", JSON.stringify(next.slice(-200), null, 1));
  return next;
}

/** Stores an uploaded picture under a safe, unique name. */
export async function addFile(name: string, data: Buffer): Promise<string> {
  const ext = name.split(".").pop()?.toLowerCase() ?? "";
  if (!IMAGE_TYPES[ext]) throw new Error("Only images can be added (png, jpg, gif, webp, svg)");
  if (data.length > 10 * 1024 * 1024) throw new Error("Pictures can be at most 10 MB");
  const base = name.replace(/\.[^.]+$/, "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "picture";
  const existing = new Set(await pageFiles());
  let file = `${base}.${ext}`;
  for (let i = 2; existing.has(file); i++) file = `${base}-${i}.${ext}`;
  await fs.mkdir(safePath("page/files"), { recursive: true });
  await fs.writeFile(safePath(`page/files/${file}`), data);
  return file;
}
