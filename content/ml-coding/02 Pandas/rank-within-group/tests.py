import copy
import sys

import numpy as np
import pandas as pd

ns = {}
exec(open("attempt.py").read(), ns)
attempt = ns["rank_in_department"]

REFERENCE = """import pandas as pd

def rank_in_department(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["rank"] = out.groupby("dept")["salary"].rank(method="dense", ascending=False).astype(int)
    return out
"""
ref_ns = {}
exec(REFERENCE, ref_ns)
reference = ref_ns["rank_in_department"]

rng = np.random.default_rng(8)
big = pd.DataFrame({"dept": rng.choice(["a", "b", "c", "d"], 30000), "name": [f"e{i}" for i in range(30000)], "salary": rng.integers(50, 80, 30000)})
cases = [
    (pd.DataFrame({"dept": ["eng", "eng", "ops", "eng"], "name": ["a", "b", "c", "d"], "salary": [100, 120, 90, 100]}),),
    (pd.DataFrame({"dept": ["x", "x", "x"], "name": ["p", "q", "r"], "salary": [9, 9, 7]}),),
    (pd.DataFrame({"dept": ["solo"], "name": ["z"], "salary": [1]}),),
    (pd.DataFrame({"dept": ["a", "b", "a", "b"], "name": ["w", "x", "y", "z"], "salary": [1.5, 1.5, 2.5, 0.5]}),),
    (pd.DataFrame({"dept": ["a"] * 4, "name": ["p", "q", "r", "s"], "salary": [3, 3, 3, 3]}),),
    (pd.DataFrame({"dept": ["a", "a"], "name": ["p", "q"], "salary": [5, 6]}, index=[10, 20]),),
    (pd.DataFrame({"dept": pd.Series([], dtype=object), "name": pd.Series([], dtype=object), "salary": pd.Series([], dtype=int)}),),
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
