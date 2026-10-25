#!/bin/bash
# Adds "prep" to your Linux app menu (pin it to your dock from there). Right-click it → "Stop server" to stop it.
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIR="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
mkdir -p "$DIR"
chmod +x "$ROOT/scripts/launch.sh"
cat >"$DIR/prep.desktop" <<DESKTOP
[Desktop Entry]
Type=Application
Name=prep
Comment=Interview prep
Exec="$ROOT/scripts/launch.sh"
Icon=$ROOT/scripts/app-icon.png
Terminal=false
Actions=stop;

[Desktop Action stop]
Name=Stop server
Exec="$ROOT/scripts/launch.sh" stop
DESKTOP
echo "Added $DIR/prep.desktop. Find prep in your app menu and pin it to your dock."
