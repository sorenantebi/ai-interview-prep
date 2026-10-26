import copy
import sys

import numpy as np
import pandas as pd

ns = {}
exec(open("attempt.py").read(), ns)
attempt = ns["team_summary"]

REFERENCE = """import pandas as pd

def team_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("team")
        .agg(players=("player", "nunique"), total=("points", "sum"), mean=("points", "mean"), best=("points", "max"))
        .reset_index()
    )
"""
ref_ns = {}
exec(REFERENCE, ref_ns)
reference = ref_ns["team_summary"]

rng = np.random.default_rng(5)
big = pd.DataFrame({
    "team": rng.choice([f"t{i:02d}" for i in range(40)], 40000),
    "player": rng.choice([f"p{i:03d}" for i in range(500)], 40000),
    "points": rng.integers(0, 30, 40000),
})
cases = [
    (pd.DataFrame({"team": ["red", "blue", "red", "red"], "player": ["al", "bo", "cy", "al"], "points": [10, 7, 4, 6]}),),
    (pd.DataFrame({"team": ["x"], "player": ["p"], "points": [3]}),),
    (pd.DataFrame({"team": ["b", "a", "b"], "player": ["q", "q", "q"], "points": [1.5, 2.0, -1.5]}),),
    (pd.DataFrame({"team": ["z", "y", "x"], "player": ["a", "b", "c"], "points": [0, 0, 0]}),),
    (pd.DataFrame({"team": ["t"] * 5, "player": ["a", "b", "a", "b", "c"], "points": [5, 4, 3, 2, 1]}),),
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
