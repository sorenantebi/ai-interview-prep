import copy
import sys

import numpy as np
import pandas as pd

ns = {}
exec(open("attempt.py").read(), ns)
attempt = ns["filter_and_sort"]

REFERENCE = """import pandas as pd

def filter_and_sort(df: pd.DataFrame, min_score: float) -> pd.DataFrame:
    kept = df[df["score"] >= min_score]
    return kept.sort_values(["score", "name"], ascending=[False, True]).reset_index(drop=True)
"""
ref_ns = {}
exec(REFERENCE, ref_ns)
reference = ref_ns["filter_and_sort"]

rng = np.random.default_rng(1)
big = pd.DataFrame({"name": [f"p{i:05d}" for i in range(20000)], "score": rng.integers(0, 100, 20000)})
cases = [
    (pd.DataFrame({"name": ["ana", "ben", "cy", "dee"], "score": [72, 90, 65, 90]}), 70),
    (pd.DataFrame({"name": ["zed", "amy"], "score": [50, 40]}), 60),
    (pd.DataFrame({"name": ["a", "b", "c"], "score": [1.5, 2.5, 2.5]}), 0),
    (pd.DataFrame({"name": ["c", "b", "a"], "score": [5, 5, 5]}), 5),
    (pd.DataFrame({"name": ["x"], "score": [10]}), 10.0),
    (pd.DataFrame({"name": ["neg", "pos"], "score": [-3, 3]}), -3),
    (pd.DataFrame({"name": pd.Series([], dtype=object), "score": pd.Series([], dtype=float)}), 0),
    (big, 50),
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
