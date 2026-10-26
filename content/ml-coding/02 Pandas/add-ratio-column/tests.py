import copy
import sys

import numpy as np
import pandas as pd

ns = {}
exec(open("attempt.py").read(), ns)
attempt = ns["add_ctr"]

REFERENCE = """import numpy as np
import pandas as pd

def add_ctr(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["ctr"] = df["clicks"] / df["views"].replace(0, np.nan)
    return out
"""
ref_ns = {}
exec(REFERENCE, ref_ns)
reference = ref_ns["add_ctr"]

rng = np.random.default_rng(2)
views = rng.integers(0, 50, 30000)
big = pd.DataFrame({"clicks": (views * rng.random(30000)).astype(int), "views": views})
cases = [
    (pd.DataFrame({"clicks": [3, 0, 5], "views": [10, 4, 0]}),),
    (pd.DataFrame({"clicks": [0, 7], "views": [0, 7]}),),
    (pd.DataFrame({"clicks": [1], "views": [3]}),),
    (pd.DataFrame({"clicks": [0, 0, 0], "views": [0, 0, 0]}),),
    (pd.DataFrame({"clicks": [2, 4], "views": [8, 8], "campaign": ["a", "b"]}),),
    (pd.DataFrame({"clicks": pd.Series([], dtype=int), "views": pd.Series([], dtype=int)}),),
    (big,),
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
