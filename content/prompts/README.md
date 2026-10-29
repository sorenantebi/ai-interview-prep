# Prompts

These are the instructions the app sends to Claude Code (`claude -p`). Edit them to change how problems, tests, plans and interviews are generated.

`{{name}}` placeholders are filled by the app; keep them when you edit. Prompts that create files must answer with `=== FILE: <name> ===` sections, which the app parses and writes itself. `complexity.md` and `study-plan.md` must answer with JSON.

| File | Used by |
|---|---|
| `_leetcode-format.md` | Shared file format for the two LeetCode prompts below |
| `add-leetcode-from-link.md` | AI → Add LeetCode from link |
| `generate-leetcode.md` | AI → Generate LeetCode problem |
| `generate-ml-coding.md` | AI → Generate ML coding problem (its file format is `ml-coding/_template/`) |
| `system-design.md` | AI → Add system design |
| `generate-tests.md` | Problem page → Submit (first submit, or "regenerate them") and `scripts/generate-tests.ts` |
| `hint.md` | Problem page → Hint |
| `complexity.md` | Problem page → Complexity, and the check after a passing Submit |
| `study-plan.md` | Plan → Make plan |
| `interview-coding.md` | Mock interview (coding) |
| `interview-system-design.md` | Mock interview (system design, including ML) |
| `generate-deck.md` | Cards → Generate with Claude (a new deck, or more cards for one) |
