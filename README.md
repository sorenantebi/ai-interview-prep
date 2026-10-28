# prep/

**A local, file-based study app for coding and system design interviews**, with Claude as your interviewer, test writer and study planner.

![Next.js 15](https://img.shields.io/badge/Next.js-15-1e1e1e) ![Python 3](https://img.shields.io/badge/Python-3-1e1e1e) ![Claude Code](https://img.shields.io/badge/AI-Claude%20Code-09aea1) ![Local first](https://img.shields.io/badge/data-local%20files-abbab9)

![Dashboard](docs/dashboard.png)

## Features

| | |
|---|---|
| **LeetCode** | NeetCode 150 on a roadmap flowchart, or one scrollable list by topic. Prev/next and shuffle mode (topic hidden). Solve in **Python or C++** (LeetCode's C++ starters, NeetCode's C++ solutions, the same hidden tests). |
| **ML Coding** | 60 NumPy, pandas and PyTorch exercises for ML interviews (tensors, training steps, ML from scratch), on the same problem page with Run and hidden-test Submit. Have Claude generate more, or add your own from `content/ml-coding/_template/`. |
| **Quant Dev** | 63 C++ problems with hidden C++ tests: C++ basics you compile yourself (pointers, memory, classes), smart pointers, containers and allocators, templates, multithreading, lock-free, low-latency bit tricks and trading systems (order book, matching engine, FIX parser). Plus 165 getcracked-style questions (C++ output and UB, concurrency, OS and networking, low latency, trading, probability) and the trading-systems interview guide as a PDF tab. |
| **Problem page** | LeetCode starter code, a Google-Doc-style editor (no autocomplete), **Run** your own inputs against NeetCode's solution, **Submit** to hidden tests (works without Claude), optionally stating your time and space complexity, which Claude checks against your code. Hints and a complexity check from Claude. Move a problem to any topic. |
| **System design** | 32 problems with solutions, your Excalidraw diagrams, 17 Hello Interview videos, and your own notes canvas. |
| **Mock interviews** | Coding or system design interviews with Claude. The timer starts on its own, and you get feedback and a saved transcript. |
| **Review** | A dashboard cheat sheet of your solved problems (your code, notes, drawings), spaced repetition and a patterns sheet. |
| **Plan** | Claude writes a day-by-day study plan from your progress, including reviews. Streak calendar on the dashboard. |
| **Extras** | Light/dark switch, job application tracker, git repo browser (open and run Jupyter notebooks in place), file browser, timer, Claude model picker and usage, a mantra and a pettable cat. |

![Problem page](docs/problem.png)

## Quick start

Needs **Node 20+** and **Python 3**, plus a **C++ compiler** for C++ answers (Xcode Command Line Tools on macOS, `g++` on Linux and Windows), on macOS, Linux or Windows. For the AI features, [set up Claude](#set-up-claude) too.

```bash
npm start             # installs, builds and opens http://localhost:3000 in your browser (Ctrl+C stops it)
npm run setup-python  # optional: numpy, pandas, torch and Jupyter for ML Coding and notebooks
```

`npm start` only reinstalls or rebuilds when something changed, so after the first time it opens in seconds. Use `npm run dev` while editing the code. Your data stays in `content/`.

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

### How C++ answers are compiled

Each Run or Submit writes your code to a temporary folder and compiles it with your system compiler (`c++`, or `g++` on Windows; set `CXX` to use another), then runs it on your machine.

| Where | Flags | Why |
|---|---|---|
| **Quant Dev** (with its `tests.cpp`, or alone for C++ Basics) | `-std=c++20 -O1 -g -pthread` | C++20, light optimisation and debug info, so crashes and failures point at real lines |
| | `-fsanitize=undefined -fno-sanitize-recover=undefined` | Undefined behaviour (signed overflow, bad shifts, null dereference…) stops the program and fails the test instead of silently "working" |
| | `-D_LIBCPP_HARDENING_MODE=…EXTENSIVE` / `-D_GLIBCXX_ASSERTIONS` | The standard library checks bounds, e.g. `vec[i]` past the end crashes instead of reading garbage |
| **LeetCode in C++** | `-std=c++20 -O2` (plus libc++'s fast bounds checks on macOS) | Speed like LeetCode's judge. Your file is compiled together with a small `main` that the Python tests talk to, plus LeetCode's usual setup: the common headers, `using namespace std`, `ListNode` and `TreeNode` |

A C++ Basics program whose first lines are `// compile: g++ …` commands is built with exactly those, in order, instead; the **Compile It Yourself** exercise practises compiling (`-c`) and linking as two steps.

Compiling takes about a second; a LeetCode answer that hasn't changed isn't compiled again. A Quant Dev program gets 20 seconds to run and a LeetCode run 30 seconds including compiling, so an infinite loop or a deadlock shows up as a timeout. A crash, such as a double free or a dangling pointer, is reported with its signal. AddressSanitizer, which would also catch use-after-free, is off: its programs hang on current macOS. On Windows the sanitizer flags are dropped, since MinGW doesn't support them.

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
| `npm start` | Install and build if needed, start the server and open the browser |
| `npm run dev` | Development server |
| `npm test` | Unit tests |
| `node scripts/generate-tests.ts` | Pre-generate hidden tests for all problems (`--model`, `--jobs`, `--force`) |
| `npm run fetch` | Re-download LeetCode starters and NeetCode solutions |
| `node scripts/fetch-cpp.ts` | Re-download LeetCode's C++ starters and NeetCode's C++ solutions |
| `npm run setup-python` | Install numpy, pandas, torch and Jupyter into `.venv` for ML Coding and notebooks |
| `node scripts/check-problems.ts <dir>` | Check problems (Python or C++): examples run, hidden tests pass with the reference and fail with the starter |

</details>



## Credits

Solutions from [NeetCode](https://neetcode.io) ([neetcode-gh/leetcode](https://github.com/neetcode-gh/leetcode), MIT), following the NeetCode 150 roadmap. Problems and starter code from [LeetCode](https://leetcode.com). System design videos by [Hello Interview](https://www.hellointerview.com). Not affiliated with any of them. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
