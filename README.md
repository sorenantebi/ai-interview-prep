# Interview Prep

A local study app for coding and system design interviews. Everything lives as plain markdown and Python files in `content/`, so you can browse, edit and back them up like any folder.

- **LeetCode**: NeetCode 150 on a roadmap flowchart. Each problem has the question, a hidden solution, your notes and a Python editor. **Run tests** asks Claude to write `tests.py` on the first run, then runs your code locally.
- **Problem page, like LeetCode**: the editor starts from LeetCode's exact Python starter (`starter.py`) and the Solution tab shows NeetCode's solution. **Run** runs your test cases from the Tests tab: you type only the inputs, one box per parameter, and each result shows Input / Output / Expected. Expected comes from running NeetCode's solution. **Submit** runs hidden tests Claude writes on first use, and passing marks the problem solved.
- **Prev / next and shuffle**: every problem page has ← prev / next → in roadmap order. **Shuffle all** or **Shuffle unsolved** on the LeetCode page walks the problems in a random order instead, with the topic hidden so it doesn't give the pattern away. The order is kept in the URL, so prev/next stay consistent.
- **Notes**: text plus a small drawing pad (`drawing.json`). Both show up in the dashboard cheat sheet.
- **System design cheat sheet**: a dashboard tab listing each problem with its solution diagram (from your Obsidian Excalidraw drawings) and your editable notes. The diagrams also appear in each problem's solution section, together with the deep-dive diagram.
- **Patterns**: a dashboard tab with the common patterns and a template for each topic. Hover a card and click **edit** to change its text and code with a live preview (⌘S saves). **+ topic** adds a card. It's stored in `content/patterns.md`.
- **Study plan**: on the Plan page, choose a start date, length, hours per day and what to cover, and Claude plans each day from the problems in this app, skipping what you've solved. It's saved to `content/plan.json` and the prompt is `prompts/study-plan.md`. The dashboard shows today's tasks, earlier unfinished days and progress. Problem tasks tick themselves off when you solve them, and you can tick any task by hand.
- **Streak calendar**: a 26-week activity heatmap on the dashboard with your current and longest streak. Runs, submits, solves, reviews, mock-interview turns and ticked plan tasks count, saved to `content/activity.json`.
- **Usage**: the **usage** button in the top bar shows how much of your Claude plan is left (current session and week, with reset times). It runs Claude Code's own `/usage`, so the app never touches credentials.
- **Mantra**: big text above the dashboard. Click to edit it; it's stored in `content/mantra.txt`.
- **Cat**: a little white pixel cat walks upright along a ledge under the top bar, and sometimes down the side edges or along the bottom. Click it to pet it. The frames are hand-drawn in `src/components/cat-frames.ts`.
- **Repos**: add as many git repos as you like (https/git@ URL or `owner/repo` for GitHub). Each is cloned into `content/repos/<name>`, and you can browse it with folders, the rendered README and highlighted code. **Pull** updates it and **Remove** deletes the local copy. Private repos use your own git login.
- **Jobs**: a spreadsheet of your applications (company, role, stage, applied date, next step, link, notes). Every cell is editable, click a column header to sort, and filter by stage. It's stored in `content/jobs.json`.
- **Timer**: ⏱ in the top bar, with a stopwatch or 15–60 min countdown. It keeps running across pages.
- **System Design**: 32 problems with requirements, scale hints and full solutions. 17 of them embed the Hello Interview video.
- **AI & Interviews**: add a LeetCode problem from a link, generate original problems, add system design problems, and run mock interviews (coding or system design) that you can save as transcripts.
- **Dashboard**: a wide, spreadsheet-style LeetCode cheat sheet of every solved problem, grouped by topic. Columns: problem (difficulty, solved date, review, **Reset code**), your own passing code (saved to `solved.py` each time your tests pass), the reference time/space complexity, and your notes (edit them right in the cell; they are saved to `notes.md`, the same file as the problem page's Notes tab).
- **Spaced repetition**: **Add to reviews** on any solved problem schedules it 1 → 3 → 7 → 14 → 30 → 60 → 120 days out. You can also pick the next review date by hand. Due problems appear at the top of the dashboard. Rate each one **Again** (back to 1 day), **Hard** (same interval), **Good** (next interval) or **Easy** (skip one). The schedule is stored in `progress.json`.
- **Files**: a browser and editor for everything in `content/`, including the AI prompts.

## Requirements

- Node 20+
- Python 3 (runs your solutions)
- [Claude Code](https://claude.com/claude-code), installed and logged in (`claude` on your PATH). The app runs `claude -p` for every AI feature, so it uses your Claude subscription and no API key is needed. Without it, everything except the AI features still works.

## Run

```bash
npm install
npm run dev        # http://localhost:3000 (bound to 127.0.0.1 only)
```

## Content layout

```
content/
  leetcode/<NN Topic>/<problem>/       question.md, solution.md, starter.py, attempt.py, solved.py, testcases.json, tests.py, notes.md, drawing.json
  system-design/<NN Category>/<problem>/ question.md (frontmatter `video:` = YouTube URL), solution.md, notes.md
  interviews/                          saved mock interviews
  notes/, repos/                       your own notes
  prompts/                             the instructions sent to Claude: edit these to change its output
  progress.json                        solved / attempted state
  jobs.json                            your job applications
```

A new topic folder (e.g. `leetcode/19 Strings`) appears automatically. Folders that aren't on the NeetCode roadmap are listed under "Other topics".

## Optional: Google login

Copy `.env.example` to `.env.local` and fill in the `GOOGLE_*` and `NEXTAUTH_SECRET` values. Set `ALLOWED_EMAILS` to limit which accounts can sign in. With the Google values left empty, the app opens without a login.

## Other

- `npm test`: unit tests (path guard, frontmatter parsing, progress, Claude output parsing)
- `npm run import-diagrams [vaultDir]`: copies the Obsidian Excalidraw drawings into each system design problem (`diagram.excalidraw`, `deep-dive.excalidraw`)
- `npm run fetch`: re-downloads LeetCode starters and NeetCode solutions for every problem (github.com/neetcode-gh/leetcode, MIT)
- `npm run seed [vaultDir]`: rebuilds `content/` from an Obsidian vault in the original folder layout (only needed once)
- Solutions run unsandboxed on your machine with a 10-second timeout. That is fine for your own code locally. Don't expose the app on a network.

## Credits

- LeetCode solutions are from [NeetCode](https://neetcode.io) ([neetcode-gh/leetcode](https://github.com/neetcode-gh/leetcode), MIT License). The LeetCode section follows the NeetCode 150 list and roadmap.
- System design videos are by [Hello Interview](https://www.hellointerview.com). Problem links and starter code are from [LeetCode](https://leetcode.com).
- Not affiliated with NeetCode, LeetCode or Hello Interview. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for licenses.

