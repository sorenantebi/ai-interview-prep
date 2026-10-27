// Desktop app: starts the built Next.js server on a free local port and shows it in a window.
// Your data lives in Documents/prep (copied from the bundled starter content on first launch).
const { app, BrowserWindow, Menu, MenuItem, Notification, WebContentsView, dialog, ipcMain, shell, utilityProcess } = require("electron");
const { execFileSync, spawn } = require("node:child_process");
const fs = require("node:fs");
const net = require("node:net");
const path = require("node:path");

const WIN = process.platform === "win32";
// Packaged: inside the app's Resources; `npm run electron`: the staged build in this repo.
const RES = app.isPackaged ? process.resourcesPath : path.join(__dirname, "..", ".electron");
const DATA = process.env.PREP_DATA ?? path.join(app.getPath("documents"), "prep");
const CONTENT = path.join(DATA, "content");
const VENV = path.join(DATA, ".venv");
let server, win, url, finder;

// Apps started from the Dock / Finder get a bare PATH; ask the login shell for the real one so `claude`, `git` and `python3` are found.
function loginPath() {
  if (WIN) return process.env.PATH;
  try {
    const out = execFileSync(process.env.SHELL || "/bin/zsh", ["-ilc", "echo __PATH__$PATH"], { encoding: "utf8", timeout: 5000 });
    return out.split("__PATH__").pop().split("\n")[0].trim(); // interactive shells may print more after it
  } catch {
    return [process.env.PATH, "/opt/homebrew/bin", "/usr/local/bin", path.join(app.getPath("home"), ".local/bin")].join(":");
  }
}

const freePort = () => new Promise((resolve, reject) => {
  const s = net.createServer().once("error", reject).listen(0, "127.0.0.1", () => { const { port } = s.address(); s.close(() => resolve(port)); });
});

async function start() {
  if (!fs.existsSync(CONTENT)) fs.cpSync(path.join(RES, "content"), CONTENT, { recursive: true });
  const port = await freePort();
  const env = {
    ...process.env, PATH: loginPath(), PORT: String(port), HOSTNAME: "127.0.0.1", NODE_ENV: "production",
    CONTENT_DIR: CONTENT, VENV_DIR: VENV, PYTHON_SETUP_HINT: "use the menu Help → Install Python packages",
  };
  const dir = path.join(RES, "server");
  server = utilityProcess.fork(path.join(dir, "server.js"), [], { cwd: dir, env, stdio: "pipe" });
  let log = "";
  server.stdout.on("data", (d) => { log = (log + d).slice(-4000); });
  server.stderr.on("data", (d) => { log = (log + d).slice(-4000); });
  server.on("exit", (code) => { if (!app.isQuitting) { dialog.showErrorBox("prep stopped", `The server exited (${code}).\n\n${log}`); app.quit(); } });
  url = `http://localhost:${port}`;
  for (let i = 0; i < 100; i++) {
    try { if ((await fetch(`${url}/api/progress`)).ok) return; } catch {}
    await new Promise((r) => setTimeout(r, 150));
  }
  throw new Error(`The server didn't start.\n\n${log}`);
}

function open() {
  win = new BrowserWindow({ width: 1440, height: 920, title: "prep", show: false });
  win.once("ready-to-show", () => win.show());
  // Links to other sites (LeetCode, YouTube, GitHub…) open in your browser; the app's own pages stay in the window.
  const external = (u) => !u.startsWith(url);
  win.webContents.setWindowOpenHandler(({ url: u }) => {
    if (external(u)) { shell.openExternal(u); return { action: "deny" }; }
    return { action: "allow" };
  });
  win.webContents.on("will-navigate", (e, u) => { if (external(u)) { e.preventDefault(); shell.openExternal(u); } });
  win.on("closed", () => { win = null; finder = null; });
  win.loadURL(url);

  // Cmd+F: a small find bar in the top-right corner.
  finder = new WebContentsView({ webPreferences: { preload: path.join(__dirname, "find-preload.cjs") } });
  finder.setBackgroundColor("#00000000");
  finder.setVisible(false);
  finder.webContents.loadFile(path.join(__dirname, "find.html"));
  win.contentView.addChildView(finder);
  const place = () => { const [w] = win.getContentSize(); finder.setBounds({ x: w - 380, y: 12, width: 360, height: 38 }); };
  place();
  win.on("resize", place);
  win.webContents.on("before-input-event", (_, i) => { if (i.type === "keyDown" && i.key === "Escape") closeFind(); });
  win.webContents.on("found-in-page", (_, r) => finder?.webContents.send("find-result", r));
  win.webContents.on("did-start-navigation", (_, __, inPlace, isMain) => { if (isMain && !inPlace) closeFind(); });
}

async function openFind() {
  if (!win || !finder) return;
  const theme = await win.webContents.executeJavaScript("document.documentElement.dataset.theme || ''").catch(() => "");
  finder.setVisible(true);
  finder.webContents.focus();
  finder.webContents.send("find-open", theme);
}
function closeFind() {
  if (!finder?.getVisible()) return;
  win?.webContents.stopFindInPage("clearSelection");
  finder.setVisible(false);
  win?.webContents.focus();
}
let lastQuery = "";
ipcMain.on("find", (_, text, forward, start) => {
  lastQuery = text;
  if (!text) return win?.webContents.stopFindInPage("clearSelection");
  win?.webContents.findInPage(text, { forward, findNext: start });
});
ipcMain.on("find-close", closeFind);
// Cmd+G / Shift+Cmd+G: next / previous match without focusing the bar.
const findAgain = (forward) => { if (lastQuery && finder?.getVisible()) win?.webContents.findInPage(lastQuery, { forward, findNext: false }); };

// Creates Documents/prep/.venv with the ML Coding / Jupyter packages (torch is a large download).
function installPython() {
  const py = path.join(VENV, WIN ? "Scripts/python.exe" : "bin/python");
  const env = { ...process.env, PATH: loginPath() };
  const say = (body) => new Notification({ title: "prep", body }).show();
  const step = (cmd, args, next) => {
    const p = spawn(cmd, args, { env, stdio: ["ignore", "ignore", "pipe"] });
    let err = "";
    p.stderr.on("data", (d) => { err = (err + d).slice(-1500); });
    p.on("error", (e) => dialog.showErrorBox("Python setup failed", `${e.message}\n\nIs Python 3 installed?`));
    p.on("exit", (code) => (code === 0 ? next() : dialog.showErrorBox("Python setup failed", err)));
  };
  say("Installing numpy, pandas, torch and Jupyter… this takes a few minutes.");
  const pip = () => step(py, ["-m", "pip", "install", "--upgrade", "numpy", "pandas", "torch", "notebook"], () => say("Python packages installed."));
  fs.existsSync(py) ? pip() : step(WIN ? "python" : "python3", ["-m", "venv", VENV], pip);
}

if (!app.requestSingleInstanceLock()) app.quit();
app.on("second-instance", () => { if (win) { if (win.isMinimized()) win.restore(); win.focus(); } });
app.on("before-quit", () => { app.isQuitting = true; server?.kill(); });
// macOS keeps the app (and server) running with no window, like other Mac apps; clicking the Dock icon reopens it.
app.on("window-all-closed", () => { if (process.platform !== "darwin") app.quit(); });
app.on("activate", () => { if (!win && url) open(); });

app.whenReady().then(async () => {
  const menu = Menu.getApplicationMenu();
  const edit = menu?.items.find((i) => i.role?.toLowerCase() === "editmenu");
  edit?.submenu.append(new MenuItem({ type: "separator" }));
  edit?.submenu.append(new MenuItem({ label: "Find…", accelerator: "CmdOrCtrl+F", click: openFind }));
  edit?.submenu.append(new MenuItem({ label: "Find Next", accelerator: "CmdOrCtrl+G", click: () => findAgain(true) }));
  edit?.submenu.append(new MenuItem({ label: "Find Previous", accelerator: "Shift+CmdOrCtrl+G", click: () => findAgain(false) }));
  const help = menu?.items.find((i) => i.role?.toLowerCase() === "help");
  help?.submenu.append(new MenuItem({ label: "Install Python packages", click: installPython }));
  help?.submenu.append(new MenuItem({ label: "Show data folder", click: () => shell.openPath(DATA) }));
  Menu.setApplicationMenu(menu);
  try {
    await start();
    open();
  } catch (e) {
    dialog.showErrorBox("prep couldn't start", String(e.message ?? e));
    app.quit();
  }
});
