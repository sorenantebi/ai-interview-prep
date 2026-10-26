import copy
import sys

import numpy as np
import pandas as pd

ns = {}
exec(open("attempt.py").read(), ns)
attempt = ns["sessionize"]

REFERENCE = """import pandas as pd

def sessionize(df: pd.DataFrame, gap_minutes: int) -> pd.DataFrame:
    d = df.assign(_t=pd.to_datetime(df["ts"]), _pos=range(len(df))).sort_values(["user", "_t", "_pos"])
    gap = d.groupby("user")["_t"].diff()
    starts = gap.isna() | (gap > pd.Timedelta(minutes=gap_minutes))
    d["session"] = starts.cumsum().astype(int)
    return d[["user", "ts", "session"]].reset_index(drop=True)
"""
ref_ns = {}
exec(REFERENCE, ref_ns)
reference = ref_ns["sessionize"]

rng = np.random.default_rng(12)
stamps = pd.Timestamp("2024-01-01") + pd.to_timedelta(rng.integers(0, 60 * 24 * 20, 30000), unit="m")
big = pd.DataFrame({"user": rng.choice([f"u{i:03d}" for i in range(300)], 30000), "ts": stamps.strftime("%Y-%m-%d %H:%M:%S")})
cases = [
    (pd.DataFrame({"user": ["u1", "u1", "u2", "u1"], "ts": ["2024-01-01 10:00:00", "2024-01-01 10:20:00", "2024-01-01 09:00:00", "2024-01-01 11:00:00"]}), 30),
    (pd.DataFrame({"user": ["a", "a"], "ts": ["2024-01-01 00:30:00", "2024-01-01 00:00:00"]}), 30),
    (pd.DataFrame({"user": ["a", "a"], "ts": ["2024-01-01 00:00:00", "2024-01-01 00:30:01"]}), 30),
    (pd.DataFrame({"user": ["z"], "ts": ["2024-06-01 12:00:00"]}), 5),
    (pd.DataFrame({"user": ["b", "a", "b", "a"], "ts": ["2024-01-01 00:00:00", "2024-01-01 00:00:00", "2024-01-01 00:00:00", "2024-01-02 00:00:00"]}), 60),
    (pd.DataFrame({"user": ["a"] * 4, "ts": ["2024-01-01 00:00:00", "2024-01-01 00:10:00", "2024-01-01 00:20:00", "2024-01-01 00:30:00"]}), 10),
    (pd.DataFrame({"user": ["a"] * 3, "ts": ["2024-01-01 00:00:00", "2024-01-01 02:00:00", "2024-01-01 04:00:00"]}), 1),
    (pd.DataFrame({"user": pd.Series([], dtype=object), "ts": pd.Series([], dtype=object)}), 30),
    (big, 45),
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
