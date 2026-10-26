import copy
import sys

import numpy as np
import pandas as pd

ns = {}
exec(open("attempt.py").read(), ns)
attempt = ns["fill_with_median"]

REFERENCE = """import pandas as pd

def fill_with_median(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    numeric = out.select_dtypes("number").columns
    out[numeric] = out[numeric].fillna(out[numeric].median())
    return out
"""
ref_ns = {}
exec(REFERENCE, ref_ns)
reference = ref_ns["fill_with_median"]

rng = np.random.default_rng(4)
vals = rng.normal(size=(20000, 3))
vals[rng.random((20000, 3)) < 0.2] = np.nan
big = pd.DataFrame(vals, columns=["a", "b", "c"])
cases = [
    (pd.DataFrame({"age": [30, None, 50, 20], "city": ["a", None, "b", "c"]}),),
    (pd.DataFrame({"x": [1.0, 2.0, None], "y": [None, None, 4.0]}),),
    (pd.DataFrame({"x": [np.nan, np.nan]}),),
    (pd.DataFrame({"x": [1.0, 3.0, np.nan, 10.0, np.nan]}),),
    (pd.DataFrame({"k": [1, 2, 3]}),),
    (pd.DataFrame({"name": ["a", None], "v": [None, 7.5]}),),
    (pd.DataFrame({"x": pd.Series([], dtype=float)}),),
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
