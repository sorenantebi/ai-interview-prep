You are writing an ORIGINAL practice problem for the "AI Assisted" section of a study app. It practises the newer
interview formats where the candidate works in a small, unfamiliar multi-file codebase instead of a blank function:
Stripe-style "bug squash" (failing tests, find the root cause), extending an existing codebase with a feature, and
Meta's AI-enabled coding round (fix a bug → implement the core feature → optimise for large inputs), usually with an AI
chat assistant that can read the files but not edit them.

Kind: {{kind}}
Difficulty: {{difficulty}}
Scenario: {{idea}}

What the kinds mean:
- bug-fix: a working-looking project with 2-3 planted bugs, each in a different file or function. Realistic,
  non-algorithmic bugs: off-by-one, wrong comparison (< vs <=), inclusive/exclusive ranges, mutable default arguments,
  shared state, integer vs float division, wrong dict key, a swallowed exception, a stale cache key, string vs int
  comparison, wrong sort key, timezone-naive maths, a missing `return`. Some visible tests fail because of them.
- extend: a working project plus a feature request (1-2 features). The visible tests for the new feature fail until
  it's built; the existing tests pass. The feature has to fit the existing design (use the existing classes / helpers).
- multi-stage: Meta style, three stages in the question: (1) fix one bug in the existing code, (2) implement the core
  feature (a stub that raises NotImplementedError, ~40-100 lines to write), (3) make it fast: hidden tests include
  large inputs (e.g. 10^5 items) that a naive solution can't finish within the time budget each test asserts.

Requirements for the project:
- Python 3 standard library only. 4-8 files in a small package (e.g. `inventory/models.py`, `inventory/service.py`,
  `inventory/utils.py`, `inventory/__init__.py`) plus `tests/test_<area>.py` files, ~150-400 lines in total. It must
  read like real code: docstrings where a real repo would have them, sensible names, no comments that point at the
  bugs (no "BUG", "TODO: fix", "off by one" or similar hints anywhere).
- Tests: plain functions named `test_*` using `assert` (no pytest, no unittest, no fixtures; the runner imports each
  `tests/test_*.py` from the repo root, so tests do `from inventory.service import ...`). Give each assert a short
  message only when it helps. Visible tests: 6-15, covering the existing behaviour and the task; at least one fails on
  the original repo for every bug / feature. `hidden_tests.py` (at the problem root, it also imports from the repo):
  8-20 more tests with edge cases and, for multi-stage, the large-input tests (assert the time with
  `time.perf_counter()`, budget about 1 second, sized so the optimal solution takes < 0.2 s and a naive one > 3 s).
- Everything deterministic (seed `random.Random(0)`), no network, no files outside the repo, no sleeps. The whole
  hidden run must finish in a few seconds with the solution.
- The solution: `solution/<same path>` for EVERY repo file you change, with the full fixed file (not a diff), plus
  `solution/solution.md`. Change only existing files; don't add files.

question.md format (the candidate sees this first; describe symptoms, never the cause or the location of a bug):
```
---
difficulty: {{difficulty}}
kind: {{kind}}
---
# <Short title>

**Kind:** <Bug fix | Extend the codebase | Multi-stage (AI-enabled round)> · **Difficulty:** {{difficulty}}

## Scenario
<2-4 sentences: what the service does, who uses it, what's going wrong or what's being asked for, like a ticket.>

## Your tasks
1. <task: e.g. "Users report that ... Find and fix the cause (the failing tests show the symptoms).">
2. ...

## Notes
- <a few facts a teammate would tell you: entry points, conventions, constraints>
- Run runs the tests in `tests/`; Submit runs them plus hidden tests. You may use the AI assistant panel like you would
  in an AI-enabled interview: it can read every file but can't edit them.
```

solution.md format:
```
# <Title> - Solution

## Root causes / approach
<per bug: the file and function, what was wrong, why it produced the symptom, the fix. For features / stages: the
design and why it fits the codebase; for the optimisation: the complexity before and after.>

## How to find it
<the debugging path a strong candidate follows: which failing test to read first, what to print or check.>
```

Write exactly these files (paths are relative to the problem folder), with no text outside the file sections:

=== FILE: question.md ===
...
=== FILE: repo/<package>/<file>.py ===
...
=== FILE: repo/tests/test_<area>.py ===
...
=== FILE: hidden_tests.py ===
...
=== FILE: solution/<package>/<changed file>.py ===
...
=== FILE: solution/solution.md ===
...
=== END ===
