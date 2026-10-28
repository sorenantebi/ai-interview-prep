# Adding your own Quant Dev (C++) problem

Folders starting with `_` (like this one) are ignored by the app.

1. Create `quant-dev/<NN Topic>/<problem-name>/` and copy the four files from this folder into it.
2. Fill in every `<...>` placeholder:

| File | What it's for |
|---|---|
| `question.md` | The problem page. Describe the exact interface (class / function names and signatures). |
| `starter.cpp` | What you start from: includes plus the interface with stub bodies. It must compile against `tests.cpp` and fail it. |
| `solution.md` | Explanation plus the reference solution in a ```` ```cpp ```` block. |
| `tests.cpp` | `#include "qtest.h"`, `#include "attempt.cpp"`, then `EXAMPLE(...)` cases (shown by **Run**) and `CASE(...)` cases (hidden, run by **Submit**). |

Checks: `CHECK(cond)`, `CHECK_EQ(got, expected)`, `CHECK_NEAR(got, expected, eps)`, `CHECK_THROWS(expr)`. Don't define `main` (qtest.h does).
Tests compile with `-std=c++20 -pthread -fsanitize=undefined` and the standard library's bounds checks, and time out after 20 s.

Check it: `node scripts/check-problems.ts "content/quant-dev/<NN Topic>"` (the reference must pass every case, the starter must fail).
