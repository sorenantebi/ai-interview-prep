import copy
import sys

import numpy as np
import pandas as pd

ns = {}
exec(open("attempt.py").read(), ns)
attempt = ns["top_values"]

REFERENCE = """import pandas as pd

def top_values(s: pd.Series, n: int) -> pd.Series:
    counts = s.value_counts()
    table = pd.DataFrame({"label": counts.index, "count": counts.values})
    table = table.sort_values(["count", "label"], ascending=[False, True]).head(n)
    return pd.Series(table["count"].values, index=table["label"].values)
"""
ref_ns = {}
exec(REFERENCE, ref_ns)
reference = ref_ns["top_values"]

rng = np.random.default_rng(3)
words = np.array([f"w{i:03d}" for i in range(300)])
big = pd.Series(words[rng.integers(0, 300, 50000)])
cases = [
    (pd.Series(["cat", "dog", "cat", "bird", "dog", "cat"]), 2),
    (pd.Series(["b", "a", None, "c", "a", "b"]), 5),
    (pd.Series(["x"]), 1),
    (pd.Series(["c", "b", "a"]), 2),
    (pd.Series(["z", "z", "y", "y", "x"]), 1),
    (pd.Series([None, None, "q"]), 3),
    (pd.Series(["m"] * 4 + ["n"] * 4 + ["o"] * 4), 2),
    (big, 10),
]


def show(x):
    if isinstance(x, (pd.DataFrame, pd.Series)):
        return "\n" + x.to_string() if len(x) <= 8 else f"<{type(x).__name__} with {len(x)} rows>"
    return repr(x)


def mismatch(got, want):
    kind = type(want).__name__
    if not isinstance(got, type(want)):
        return f"expected a {kind}, got {type(got).__name__}"
    if isinstance(want.index, pd.RangeIndex):
        got = got.reset_index(drop=True)
    opts = dict(check_dtype=False, check_names=False, check_index_type=False)
    try:
        if isinstance(want, pd.DataFrame):
            pd.testing.assert_frame_equal(got, want, check_column_type=False, **opts)
        else:
            pd.testing.assert_series_equal(got, want, **opts)
    except AssertionError:
        return f"expected={show(want)}\ngot={show(got)}"
    return None


def changed(before, after):
    return any(isinstance(b, (pd.DataFrame, pd.Series)) and not b.equals(a) for b, a in zip(before, after))


passed = 0
for n, args in enumerate(cases, 1):
    inputs = ", ".join(show(a) for a in args)
    try:
        mine = copy.deepcopy(args)
        got = attempt(*mine)
        want = reference(*copy.deepcopy(args))
        problem = mismatch(got, want)
        if problem is None and changed(args, mine):
            problem = "your function modified its input; return a new frame instead"
        if problem:
            print(f"FAIL case {n}: input={inputs}\n{problem}")
        else:
            print(f"PASS case {n}")
            passed += 1
    except Exception as e:
        print(f"FAIL case {n}: input={inputs}\ngot {type(e).__name__}: {e}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)
