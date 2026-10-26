import copy
import sys

import numpy as np
import pandas as pd

ns = {}
exec(open("attempt.py").read(), ns)
attempt = ns["latest_per_user"]

REFERENCE = """import pandas as pd

def latest_per_user(df: pd.DataFrame) -> pd.DataFrame:
    d = df.assign(_t=pd.to_datetime(df["updated_at"]), _pos=range(len(df)))
    d = d.sort_values(["user_id", "_t", "_pos"]).drop_duplicates("user_id", keep="last")
    return d.drop(columns=["_t", "_pos"]).reset_index(drop=True)
"""
ref_ns = {}
exec(REFERENCE, ref_ns)
reference = ref_ns["latest_per_user"]

rng = np.random.default_rng(10)
stamps = pd.Timestamp("2024-01-01") + pd.to_timedelta(rng.integers(0, 500, 30000), unit="h")
big = pd.DataFrame({"user_id": rng.integers(0, 3000, 30000), "updated_at": stamps.strftime("%Y-%m-%d %H:%M:%S"), "email": [f"m{i}" for i in range(30000)]})
cases = [
    (pd.DataFrame({"user_id": [1, 2, 1], "updated_at": ["2024-03-01 10:00:00", "2024-01-05 09:00:00", "2024-02-01 08:00:00"], "email": ["a@new", "b@x", "a@old"]}),),
    (pd.DataFrame({"user_id": [7, 7], "updated_at": ["2024-01-01 00:00:00", "2024-01-01 00:00:00"], "email": ["first", "second"]}),),
    (pd.DataFrame({"user_id": [3], "updated_at": ["2020-01-01 00:00:00"], "email": ["only"]}),),
    (pd.DataFrame({"user_id": [5, 4, 5, 4], "updated_at": ["2024-01-01 12:00:00", "2024-01-02 00:00:00", "2024-01-01 09:00:00", "2023-12-31 23:59:59"], "email": ["p", "q", "r", "s"]}),),
    (pd.DataFrame({"user_id": [2, 2, 2], "updated_at": ["2024-01-01 00:00:01", "2024-01-01 00:00:02", "2024-01-01 00:00:02"], "email": ["x", "y", "z"]}),),
    (pd.DataFrame({"user_id": [1, 1], "updated_at": ["2024-01-10 00:00:00", "2024-01-09 23:59:59"], "email": ["late", "early"]}),),
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
