// electron-builder hook (runs before signing): copies the staged server and starter content into the app as-is.
// Its own extraResources would drop node_modules, dotfiles and empty folders, which the server and content need.
const fs = require("node:fs");
const path = require("node:path");

exports.default = async ({ appOutDir, electronPlatformName, packager }) => {
  const res = electronPlatformName === "darwin"
    ? path.join(appOutDir, `${packager.appInfo.productFilename}.app`, "Contents", "Resources")
    : path.join(appOutDir, "resources");
  for (const dir of ["server", "content"]) fs.cpSync(path.join(".electron", dir), path.join(res, dir), { recursive: true, verbatimSymlinks: true });
};
