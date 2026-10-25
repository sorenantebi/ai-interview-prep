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
PIDFILE="$DIST/prep.pid"
# Only ever stops the server this launcher started (checked to still be a next process), never a `npm run dev` one.
stop() {
  local pid; pid=$(cat "$PIDFILE" 2>/dev/null) || return 1
  rm -f "$PIDFILE"
  ps -p "$pid" -o command= | grep -q next && { pkill -P "$pid"; kill "$pid"; }
}
if [ "$1" = stop ]; then stop; exit 0; fi

# Restart that server if the code changed since its build.
if up && stale && stop; then
  for _ in $(seq 10); do up || break; sleep 0.5; done
fi

if ! up; then
  say "Starting… (rebuilding after code changes takes about a minute)"
  if stale; then
    node_modules/.bin/next build >"$LOG" 2>&1 || { say "Build failed, see $LOG"; exit 1; }
  fi
  nohup node_modules/.bin/next start -H 127.0.0.1 -p "$PORT" >>"$LOG" 2>&1 &
  echo $! >"$PIDFILE"
  for _ in $(seq 60); do up && break; sleep 1; done
fi
if [ "$MAC" ]; then open "$URL"; else xdg-open "$URL"; fi
