#!/bin/bash
# Creates /Applications/prep.app, which runs scripts/launch.sh. Drag it to the Dock; Quit it to stop the server.
# An AppleScript app (not a bare script bundle) so macOS can ask for access when the repo is in Desktop/Documents.
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APP="/Applications/prep.app"
chmod +x "$ROOT/scripts/launch.sh"
rm -rf "$APP"
LAUNCH="quoted form of \"$ROOT/scripts/launch.sh\""
osacompile -s -o "$APP" \
  -e "on run" -e "do shell script $LAUNCH & \" >/dev/null 2>&1 &\"" -e "end run" \
  -e "on reopen" -e "run" -e "end reopen" \
  -e "on quit" -e "do shell script $LAUNCH & \" stop >/dev/null 2>&1\"" -e "continue quit" -e "end quit"
# scripts/app-icon.png: 1024px, already shaped to the macOS icon grid.
SET="$(mktemp -d)/prep.iconset"; mkdir "$SET"
for n in 16 32 128 256 512; do
  sips -z $n $n "$ROOT/scripts/app-icon.png" --out "$SET/icon_${n}x${n}.png" >/dev/null
  sips -z $((n*2)) $((n*2)) "$ROOT/scripts/app-icon.png" --out "$SET/icon_${n}x${n}@2x.png" >/dev/null
done
iconutil -c icns "$SET" -o "$APP/Contents/Resources/applet.icns"
# osacompile's Assets.car icon wins over applet.icns, so drop it.
rm -f "$APP/Contents/Resources/Assets.car"
/usr/libexec/PlistBuddy -c "Delete :CFBundleIconName" "$APP/Contents/Info.plist"
codesign --force -s - "$APP" 2>/dev/null  # editing the bundle breaks osacompile's signature
touch "$APP"
echo "Created $APP. Drag it from Finder to your Dock; Quit it to stop the server."
