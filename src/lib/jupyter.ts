import { spawn } from "node:child_process";
import { randomBytes } from "node:crypto";
import { tmpdir } from "node:os";
import path from "node:path";
import { python } from "./run";
import { safePath } from "./content";

type Server = { port: number; token: string };
const g = globalThis as { jupyter?: Promise<Server> };

/** Starts one Jupyter server for content/repos (on first use; it lives as long as the app's server). */
function start(): Promise<Server> {
  const token = randomBytes(24).toString("hex");
  const child = spawn(python(), [
    "-m", "notebook", "--no-browser", "--ip=127.0.0.1", "--port=8899",
    `--ServerApp.root_dir=${safePath("repos")}`, `--IdentityProvider.token=${token}`,
    // Keep Jupyter's .ipynb_checkpoints out of your repos. shortcut: notebooks with the same file name share a checkpoint; fine for "revert".
    `--FileCheckpoints.checkpoint_dir=${path.join(tmpdir(), "prep-jupyter-checkpoints")}`,
    // Let the repo page embed it.
    `--ServerApp.tornado_settings={"headers":{"Content-Security-Policy":"frame-ancestors 'self' http://localhost:* http://127.0.0.1:*"}}`,
  ], { stdio: ["ignore", "ignore", "pipe"] });
  process.once("exit", () => child.kill()); // stop Jupyter with the app
  return new Promise((resolve, reject) => {
    let log = "";
    const fail = (why: string) => { g.jupyter = undefined; reject(new Error(why)); };
    child.on("error", (e) => fail(e.message));
    child.on("exit", () => fail(/No module named notebook/.test(log) ? "Jupyter isn't installed: run `npm run setup-python` once." : `Jupyter stopped:\n${log.slice(-1500)}`));
    child.stderr.on("data", (d) => {
      log += d;
      const port = log.match(/http:\/\/127\.0\.0\.1:(\d+)\//)?.[1]; // the port Jupyter picked (8899, or the next free one)
      if (port) resolve({ port: Number(port), token });
    });
  });
}

/** URL of a notebook (path relative to content/repos), on the same host name the browser uses for the app. */
export async function notebookUrl(rel: string, host: string) {
  const { port, token } = await (g.jupyter ??= start());
  return `http://${host === "127.0.0.1" ? host : "localhost"}:${port}/notebooks/${rel.split("/").map(encodeURIComponent).join("/")}?token=${token}`;
}
