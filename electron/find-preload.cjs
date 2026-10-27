// Bridge for the Cmd+F bar (find.html): only these calls, nothing else from Node.
const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("finder", {
  search: (text, forward, start) => ipcRenderer.send("find", text, forward, start),
  close: () => ipcRenderer.send("find-close"),
  onResult: (cb) => ipcRenderer.on("find-result", (_, r) => cb(r)),
  onOpen: (cb) => ipcRenderer.on("find-open", (_, theme) => cb(theme)),
});
