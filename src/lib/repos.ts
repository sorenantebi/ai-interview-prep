import { execFile } from "node:child_process";
import fs from "node:fs/promises";
import path from "node:path";
import { safePath } from "./content.ts";

const git = (args: string[], cwd?: string, timeout = 300_000) =>
  new Promise<string>((resolve, reject) => {
    // No shell, no prompts: a private repo without credentials fails instead of hanging.
    execFile("git", args, { cwd, timeout, maxBuffer: 1 << 20, env: { ...process.env, GIT_TERMINAL_PROMPT: "0" } }, (err, stdout, stderr) =>
      err ? reject(new Error((stderr || err.message).trim())) : resolve(stdout.trim()),
    );
  });

/** Accepts https://host/owner/repo(.git), git@host:owner/repo(.git) or GitHub shorthand owner/repo. */
export function normalizeUrl(input: string): { url: string; name: string } {
  const s = input.trim();
  const url = /^[\w-][\w.-]*\/[\w-][\w.-]*$/.test(s) ? `https://github.com/${s}.git` : s;
  if (!/^(https:\/\/[\w.-]+(:\d+)?\/[\w./~-]+|git@[\w.-]+:[\w./~-]+)$/.test(url) || url.includes(".."))
    throw new Error("Use an https:// or git@ URL, or owner/repo for GitHub");
  const name = url.replace(/\/+$/, "").split(/[/:]/).pop()!.replace(/\.git$/, "").replace(/[^\w.-]/g, "-");
  if (!name || name.startsWith(".")) throw new Error("Could not work out a folder name from that URL");
  return { url, name };
}

export async function addRepo(input: string) {
  const { url, name } = normalizeUrl(input);
  const dest = safePath(`repos/${name}`);
  if (await fs.stat(dest).catch(() => null)) throw new Error(`repos/${name} already exists`);
  await fs.mkdir(path.dirname(dest), { recursive: true });
  await git(["clone", "--depth", "1", "--", url, dest]);
  return name;
}

export const pullRepo = (name: string) => git(["pull", "--ff-only"], safePath(`repos/${name}`), 120_000);

export async function removeRepo(name: string) {
  if (!name || name.includes("/") || name.startsWith(".")) throw new Error("Bad repo name");
  await fs.rm(safePath(`repos/${name}`), { recursive: true, force: true });
}

export type RepoInfo = { name: string; url: string; branch: string; commit: string; subject: string; when: string };

export async function listRepos(): Promise<RepoInfo[]> {
  const dir = safePath("repos");
  const entries = (await fs.readdir(dir, { withFileTypes: true }).catch(() => [])).filter((e) => e.isDirectory() && !e.name.startsWith("."));
  return Promise.all(
    entries.map(async (e) => {
      const cwd = path.join(dir, e.name);
      const [url, branch, log] = await Promise.all([
        git(["remote", "get-url", "origin"], cwd, 10_000).catch(() => ""),
        git(["rev-parse", "--abbrev-ref", "HEAD"], cwd, 10_000).catch(() => ""),
        git(["log", "-1", "--format=%h%x00%s%x00%cr"], cwd, 10_000).catch(() => ""),
      ]);
      const [commit = "", subject = "", when = ""] = log.split("\0");
      return { name: e.name, url, branch, commit, subject, when };
    }),
  );
}
