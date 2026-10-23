# Prompts

These are the instructions the app sends to Claude Code (`claude -p`). Edit them to change how questions, tests and interviews are generated.

`{{name}}` placeholders are filled by the app. Prompts that create files must answer with `=== FILE: <name> ===` sections. The app parses those and writes the files itself.

| File | Used by |
|---|---|
| `add-leetcode-from-link.md` | AI → Add LeetCode from link |
| `generate-leetcode.md` | AI → Generate LeetCode problem |
| `system-design.md` | AI → Add / generate system design problem |
| `generate-tests.md` | Problem page → Run tests (first run) |
| `hint.md` | Problem page → Hint / review |
| `interview-coding.md` | Mock interview (coding) |
| `interview-system-design.md` | Mock interview (system design) |
