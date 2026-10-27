@echo off
rem Opens prep/ in the browser, starting the server first if it isn't running (rebuilds only when the code changed).
rem The server runs in a minimised "prep server" window; close that window to stop it.
cd /d "%~dp0.."
set URL=http://localhost:3000
curl -s -o nul %URL%/api/progress && goto open

if not exist node_modules call npm install || (echo npm install failed. & pause & exit /b 1)
rem Exit code 1 when there's no build, or src/, public/, package.json or next.config.ts changed since it.
node -e "const f=require('fs'),p=require('path');const b=f.statSync('.next/BUILD_ID',{throwIfNoEntry:false});if(!b)process.exit(1);const n=x=>f.statSync(x).mtimeMs>b.mtimeMs;const w=d=>f.readdirSync(d,{withFileTypes:true}).some(e=>e.isDirectory()?w(p.join(d,e.name)):n(p.join(d,e.name)));process.exit(['src','public'].some(w)||['package.json','next.config.ts'].some(n)?1:0)"
if errorlevel 1 (
  echo Building prep, about a minute...
  call npx next build || (echo Build failed. & pause & exit /b 1)
)
start "prep server" /min cmd /c npx next start -H 127.0.0.1
:wait
timeout /t 1 /nobreak >nul
curl -s -o nul %URL%/api/progress || goto wait

:open
start "" %URL%
