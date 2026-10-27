# prep/

**A local, file-based study app for coding and system design interviews**, with Claude as your interviewer, test writer and study planner.

![Next.js 15](https://img.shields.io/badge/Next.js-15-1e1e1e) ![Python 3](https://img.shields.io/badge/Python-3-1e1e1e) ![Claude Code](https://img.shields.io/badge/AI-Claude%20Code-09aea1) ![Local first](https://img.shields.io/badge/data-local%20files-abbab9)

**Download:** [macOS (Apple silicon)](https://github.com/sorenantebi/prep-app/releases/latest/download/prep-mac-arm64.dmg) · [Windows](https://github.com/sorenantebi/prep-app/releases/latest/download/prep-windows-setup.exe) · [Linux](https://github.com/sorenantebi/prep-app/releases/latest/download/prep-linux.AppImage) · or [run from source](#run-from-source)

![Dashboard](docs/dashboard.png)

## Features

| | |
|---|---|
| **LeetCode** | NeetCode 150 on a roadmap flowchart, or one scrollable list by topic. Prev/next and shuffle mode (topic hidden). |
| **ML Coding** | 60 NumPy, pandas and PyTorch exercises for ML interviews (tensors, training steps, ML from scratch), on the same problem page with Run and hidden-test Submit. Have Claude generate more, or add your own from `content/ml-coding/_template/`. |
| **Problem page** | LeetCode starter code, a Google-Doc-style editor (no autocomplete), **Run** your own inputs against NeetCode's solution, **Submit** to hidden tests (works without Claude), optionally stating your time and space complexity, which Claude checks against your code. Hints and a complexity check from Claude. Move a problem to any topic. |
| **System design** | 32 problems with solutions, your Excalidraw diagrams, 17 Hello Interview videos, and your own notes canvas. |
| **Mock interviews** | Coding or system design interviews with Claude. The timer starts on its own, and you get feedback and a saved transcript. |
| **Review** | A dashboard cheat sheet of your solved problems (your code, notes, drawings), spaced repetition and a patterns sheet. |
| **Plan** | Claude writes a day-by-day study plan from your progress, including reviews. Streak calendar on the dashboard. |
| **Extras** | Light/dark switch, job application tracker, git repo browser (open and run Jupyter notebooks in place), file browser, timer, Claude model picker and usage, a mantra and a pettable cat. |

![Problem page](docs/problem.png)

## Desktop app

| macOS (Apple silicon) | Windows | Linux |
|---|---|---|
| [prep-mac-arm64.dmg](https://github.com/sorenantebi/prep-app/releases/latest/download/prep-mac-arm64.dmg) | [prep-windows-setup.exe](https://github.com/sorenantebi/prep-app/releases/latest/download/prep-windows-setup.exe) | [prep-linux.AppImage](https://github.com/sorenantebi/prep-app/releases/latest/download/prep-linux.AppImage) |

Install it and open **prep**; no Node needed. Your problems, progress and notes live in **Documents/prep** (Help → Show data folder).
For ML Coding and notebooks, install Python 3, then use Help → Install Python packages. For the AI features, [set up Claude](#set-up-claude).

The app isn't signed with a paid certificate, so the first launch is blocked once:
- **macOS:** open System Settings → Privacy & Security and click **Open Anyway** next to prep.
- **Windows:** in the SmartScreen warning, click **More info → Run anyway**.
- **Linux:** make the file executable (`chmod +x prep-linux.AppImage`), then run it.

Older versions are on the [Releases page](https://github.com/sorenantebi/prep-app/releases). To build the installer yourself: `npm install && npm run dist` (output in `dist/`).
New releases are built by GitHub Actions when you push a version tag: `git tag v0.1.0 && git push origin v0.1.0`.

## Run from source

Needs **Node 20+** and **Python 3**, on macOS, Linux or Windows. For the AI features, [set up Claude](#set-up-claude) too.

```bash
npm install
npm run app           # builds, then serves at http://localhost:3000
npm run setup-python  # optional: numpy, pandas, torch and Jupyter for ML Coding and notebooks
```

Use `npm run dev` instead of `npm run app` while editing the code. Your data stays in `content/`.

## Set up Claude

The AI features (adding and generating problems, hidden tests, hints, mock interviews, study plans and the Claude page) run through **Claude Code** on your machine. Everything else works without it.

1. **Install Claude Code**
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```
   Other install options are in the [Claude Code docs](https://docs.claude.com/en/docs/claude-code/setup).

2. **Log in once**: run `claude auth login` and finish signing in in your browser. Or open the app's **claude** page and click **Log in to Claude**, which opens a terminal with that command for you on macOS, Windows or Linux. A Claude Pro or Max subscription works, and so does an Anthropic API key (`ANTHROPIC_API_KEY`).

3. **Check it works**
   ```bash
   claude -p "say hi"
   ```
   If that prints a reply, the app can use Claude. The **claude** page also shows whether Claude Code is connected, lets you pick the model, and shows how much of your plan is used.

> If `claude` isn't on your `PATH`, point the app at it in `.env.local`: `CLAUDE_BIN=/full/path/to/claude`.
> The app uses whatever account Claude Code is logged into. It never asks for or stores a key, and usage counts against that account. Check how much is used with the **claude** button.

## How it works

- **Your data is plain files** in `content/`: markdown, Python and JSON you can open, edit or back up. Your progress, notes, plans and jobs are git-ignored.
- **AI runs through your local Claude Code** (`claude -p`), with no tools that can change files. The app writes everything itself.
- **Prompts are editable** in `content/prompts/`, to change how Claude writes problems, tests, plans and interviews.
- **Runs only on your machine** (127.0.0.1). Your code runs unsandboxed with a 10-second limit, so don't expose the app on a network.

```
content/
├── leetcode/<topic>/<problem>/      question · solution · starter · tests · your code & notes
├── system-design/<category>/<problem>/   question · solution · diagrams · your notes
├── prompts/                          what the app asks Claude
└── patterns.md · plan.json · jobs.json · progress.json · …
```

<details>
<summary><b>Scripts</b></summary>

| Command | What it does |
|---|---|
| `npm run app` | Production build + server (fast) |
| `npm run dev` | Development server |
| `npm run dist` | Build the desktop app installer for this OS into `dist/` (uses Documents/prep for your data) |
| `npm run electron` | Build and open the desktop app without packaging it |
| `npm test` | Unit tests |
| `node scripts/generate-tests.ts` | Pre-generate hidden tests for all problems (`--model`, `--jobs`, `--force`) |
| `npm run fetch` | Re-download LeetCode starters and NeetCode solutions |
| `npm run setup-python` | Install numpy, pandas, torch and Jupyter into `.venv` for ML Coding and notebooks |
| `node scripts/check-problems.ts <dir>` | Check problems: examples run, hidden tests pass with the reference and fail with the starter |

</details>



## Credits

Solutions from [NeetCode](https://neetcode.io) ([neetcode-gh/leetcode](https://github.com/neetcode-gh/leetcode), MIT), following the NeetCode 150 roadmap. Problems and starter code from [LeetCode](https://leetcode.com). System design videos by [Hello Interview](https://www.hellointerview.com). Not affiliated with any of them. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
