#!/bin/bash
# Opens prep/ in the browser, starting the server first if it isn't running (rebuilds only when the code changed).
# `launch.sh stop` stops the server this launcher started (prep.app runs it on Quit). Works on macOS and Linux.
cd "$(dirname "$0")/.." || exit 1
# Apps opened from the Dock get a bare PATH; add the usual node / claude locations.
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$HOME/.npm-global/bin:$PATH"
PORT=${PORT:-3000}; DIST=${NEXT_DIST_DIR:-.next}
URL=http://localhost:$PORT
MAC=$([ "$(uname)" = Darwin ] && echo 1)
LOG=$([ "$MAC" ] && echo "$HOME/Library/Logs/prep.log" || echo "${TMPDIR:-/tmp}/prep.log")
say() { if [ "$MAC" ]; then osascript -e "display notification \"$1\" with title \"prep\""; else notify-send prep "$1"; fi 2>/dev/null; }

up() { curl -s -o /dev/null "$URL/api/progress"; }

stale() { [ ! -f "$DIST/BUILD_ID" ] || [ -n "$(find src public package.json next.config.ts -newer "$DIST/BUILD_ID" -print -quit)" ]; }
PIDFILE=".prep-$PORT.pid"  # outside .next, which a build wipes
# Only ever stops the server this launcher started (checked to still be a next process), never a `npm run dev` one.
stop() {
  local pid; pid=$(cat "$PIDFILE" 2>/dev/null) || return 1
  rm -f "$PIDFILE"
  ps -p "$pid" -o command= | grep -q next && { pkill -P "$pid"; kill "$pid"; }
}
if [ "$1" = stop ]; then stop; exit 0; fi

# One launch at a time: a second click while one is building or starting waits for it, then just opens the browser.
LOCK=".prep-$PORT.lock"
for _ in $(seq 300); do mkdir "$LOCK" 2>/dev/null && break; sleep 1; done
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

# Restart that server if the code changed since its build.
if up && stale && stop; then
  for _ in $(seq 40); do up || break; sleep 0.5; done
fi

if ! up; then
  say "Starting… (rebuilding after code changes takes about a minute)"
  [ -d node_modules ] || npm install >"$LOG" 2>&1 || { say "npm install failed, see $LOG"; exit 1; }
  if stale; then
    node_modules/.bin/next build >"$LOG" 2>&1 || { say "Build failed, see $LOG"; exit 1; }
  fi
  nohup node_modules/.bin/next start -H 127.0.0.1 -p "$PORT" >>"$LOG" 2>&1 &
  started=$!
  for _ in $(seq 60); do up && break; sleep 1; done
  # Remember the process that actually serves the port (only if this launch's server is the one running).
  listener=$(lsof -tiTCP:"$PORT" -sTCP:LISTEN 2>/dev/null | head -1)
  if kill -0 "$started" 2>/dev/null; then echo "${listener:-$started}" >"$PIDFILE"; fi
fi
if [ "$MAC" ]; then open "$URL"; else xdg-open "$URL"; fi
