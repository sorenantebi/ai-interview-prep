import copy
import sys

import numpy as np
import pandas as pd

ns = {}
exec(open("attempt.py").read(), ns)
attempt = ns["join_orders"]

REFERENCE = """import pandas as pd

def join_orders(orders: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    out = orders.merge(customers, on="customer_id", how="left")
    out[["name", "country"]] = out[["name", "country"]].fillna("unknown")
    return out
"""
ref_ns = {}
exec(REFERENCE, ref_ns)
reference = ref_ns["join_orders"]

rng = np.random.default_rng(7)
cust_ids = np.arange(0, 2000, 2)
customers_big = pd.DataFrame({"customer_id": cust_ids, "name": [f"c{i}" for i in cust_ids], "country": rng.choice(["DE", "FR", "US"], len(cust_ids))})
orders_big = pd.DataFrame({"order_id": np.arange(30000), "customer_id": rng.integers(0, 2000, 30000), "amount": rng.random(30000)})
no_customers = pd.DataFrame({"customer_id": pd.Series([], dtype=int), "name": pd.Series([], dtype=object), "country": pd.Series([], dtype=object)})
cases = [
    (pd.DataFrame({"order_id": [1, 2, 3], "customer_id": [10, 99, 10], "amount": [5.0, 7.5, 2.0]}), pd.DataFrame({"customer_id": [10, 11], "name": ["ana", "ben"], "country": ["DE", "FR"]})),
    (pd.DataFrame({"order_id": [4], "customer_id": [11], "amount": [1.0]}), pd.DataFrame({"customer_id": [11], "name": ["ben"], "country": ["FR"]})),
    (pd.DataFrame({"order_id": [5, 6], "customer_id": [3, 2], "amount": [1.0, 2.0]}), no_customers),
    (pd.DataFrame({"order_id": [9, 8, 7], "customer_id": [1, 2, 1], "amount": [3.0, 2.0, 1.0]}), pd.DataFrame({"customer_id": [2, 1], "name": ["bo", "al"], "country": ["UK", "US"]})),
    (pd.DataFrame({"order_id": pd.Series([], dtype=int), "customer_id": pd.Series([], dtype=int), "amount": pd.Series([], dtype=float)}), pd.DataFrame({"customer_id": [1], "name": ["al"], "country": ["US"]})),
    (orders_big, customers_big),
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
