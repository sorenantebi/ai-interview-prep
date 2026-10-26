import copy
import sys

import numpy as np
import pandas as pd

ns = {}
exec(open("attempt.py").read(), ns)
attempt = ns["pivot_sales"]

REFERENCE = """import pandas as pd

def pivot_sales(df: pd.DataFrame) -> pd.DataFrame:
    table = df.pivot_table(index="region", columns="month", values="amount", aggfunc="sum", fill_value=0)
    table.columns.name = None
    return table.reset_index()
"""
ref_ns = {}
exec(REFERENCE, ref_ns)
reference = ref_ns["pivot_sales"]

rng = np.random.default_rng(6)
months = [f"2024-{m:02d}" for m in range(1, 13)]
big = pd.DataFrame({
    "region": rng.choice([f"r{i:02d}" for i in range(30)], 30000),
    "month": rng.choice(months, 30000),
    "amount": rng.integers(1, 100, 30000).astype(float),
})
cases = [
    (pd.DataFrame({"region": ["east", "west", "east", "east"], "month": ["2024-02", "2024-01", "2024-01", "2024-02"], "amount": [5.0, 3.0, 2.0, 1.0]}),),
    (pd.DataFrame({"region": ["north"], "month": ["2023-12"], "amount": [9.5]}),),
    (pd.DataFrame({"region": ["b", "a"], "month": ["2024-03", "2023-11"], "amount": [1.0, 2.0]}),),
    (pd.DataFrame({"region": ["a", "a", "a"], "month": ["2024-01", "2024-01", "2024-01"], "amount": [1.0, 2.0, 3.0]}),),
    (pd.DataFrame({"region": ["a", "b", "c"], "month": ["2024-01", "2024-02", "2024-03"], "amount": [1, 2, 3]}),),
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
