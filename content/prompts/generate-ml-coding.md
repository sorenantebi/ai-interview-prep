You are writing an ORIGINAL practice problem for the ML coding section of a study app: short, LeetCode-style
exercises in NumPy, pandas and PyTorch, like the ones asked in ML engineer interviews.

Topic: {{topic}}
Difficulty: {{difficulty}}
Extra instructions from the user: {{idea}}

Requirements:
- One task that fits the topic and takes 10-30 minutes: a plain top-level Python function (no class), solvable in
  a few lines to a page. Easy = one or two operations, Medium = a small algorithm or a training step, Hard = several
  steps that must fit together (e.g. a vectorised algorithm, a model piece, a full training loop).
- Use the library the topic names. NumPy topics: the solution uses only basic NumPy (array creation, indexing,
  reshape/transpose, broadcasting, arithmetic, reductions, sort/argsort and `@`), set `NUMPY_ONLY = True` in
  tests.py, and end the Problem section with this paragraph:
  **Rules:** build it from basic NumPy: array creation, indexing (including fancy indexing with index arrays), reshape / transpose, broadcasting, arithmetic, reductions (`sum`, `max`, `mean`, …), `np.sort` / `np.argsort` and `@`. Not allowed: `np.einsum`, `np.tensordot`, `np.convolve`, `np.correlate`, `np.linalg.norm`, `sliding_window_view` / `as_strided`, and other libraries (SciPy, scikit-learn, pandas, PyTorch). The hidden tests reject them.
  Other topics: `NUMPY_ONLY = False`.
- `starter.py` is the imports plus the function signature with `pass`. Every parameter has a type hint
  (`np.ndarray`, `pd.DataFrame`, `pd.Series`, `torch.Tensor`, `int`, `float`, `list[...]`, ...).
- Examples: 2-3, each `Input:` is `name = value` pairs in parameter order, written as Python/JSON literals (arrays
  and tensors as nested lists, a DataFrame as a dict of columns). Outputs: floats with 5 decimals, no spaces, NaN as
  null, a DataFrame as a dict of columns, as in the template. Trace every example through your solution.
- The reference solution in solution.md is the same function, correct and idiomatic. Add `## Complexity` only if it
  says something useful; this section does not grade complexity.
- tests.py: start from the template's tests.py and change only `FUNC`, `NUMPY_ONLY`, `reference` and `CASES`
  (and imports if the topic needs pandas or torch). `reference` is a correct implementation (it may differ from the
  solution, e.g. a slow loop). 8-12 cases: the examples, edge cases (size 1, zeros, ties, NaN where relevant), and
  random seeded inputs. The file must run in a few seconds. The app runs it against your reference solution and
  against the empty starter and rejects the problem unless the first passes and the second fails.
- Be deterministic: seed every random generator (`np.random.default_rng(0)`, `torch.manual_seed(0)`).

Write exactly four files, in the same structure as the template below, with every `<...>` placeholder filled in
(no text outside the file sections):

=== FILE: question.md ===
...
=== FILE: starter.py ===
...
=== FILE: solution.md ===
...
=== FILE: tests.py ===
...
=== END ===

# Template

{{template}}
