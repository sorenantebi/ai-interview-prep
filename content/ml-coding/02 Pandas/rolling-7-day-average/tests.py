import copy
import sys

import numpy as np
import pandas as pd

ns = {}
exec(open("attempt.py").read(), ns)
attempt = ns["rolling_7_day_average"]

REFERENCE = """import pandas as pd

def rolling_7_day_average(df: pd.DataFrame) -> pd.DataFrame:
    d = df.assign(ts=pd.to_datetime(df["date"])).sort_values("ts")
    d["avg_7d"] = d.rolling("7D", on="ts")["sales"].mean()
    return d[["date", "sales", "avg_7d"]].reset_index(drop=True)
"""
ref_ns = {}
exec(REFERENCE, ref_ns)
reference = ref_ns["rolling_7_day_average"]

rng = np.random.default_rng(9)
days = pd.date_range("2020-01-01", periods=6000, freq="D")
keep = np.sort(rng.choice(6000, 4000, replace=False))
big = pd.DataFrame({"date": days[keep].strftime("%Y-%m-%d"), "sales": rng.random(4000) * 100}).sample(frac=1, random_state=1).reset_index(drop=True)
cases = [
    (pd.DataFrame({"date": ["2024-01-03", "2024-01-01", "2024-01-02"], "sales": [30.0, 10.0, 20.0]}),),
    (pd.DataFrame({"date": ["2024-01-01", "2024-01-07", "2024-01-08"], "sales": [7.0, 1.0, 4.0]}),),
    (pd.DataFrame({"date": ["2024-05-05"], "sales": [3.0]}),),
    (pd.DataFrame({"date": ["2024-02-28", "2024-03-01", "2024-02-29"], "sales": [1.0, 3.0, 2.0]}),),
    (pd.DataFrame({"date": ["2023-12-31", "2024-01-10"], "sales": [5.0, 6.0]}),),
    (pd.DataFrame({"date": [f"2024-01-{d:02d}" for d in range(1, 15)], "sales": [float(d) for d in range(1, 15)]}),),
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
