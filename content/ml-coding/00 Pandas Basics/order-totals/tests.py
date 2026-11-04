import sys
import numpy as np
import pandas as pd

# --- Edit these ------------------------------------------------------------------------------------------------
FUNC = "add_total"  # the function name from starter.py
NUMPY_ONLY = False      # True: ban SciPy / pandas / PyTorch and NumPy shortcuts (einsum, convolve, ...), as in 01 NumPy


def reference(data):
    # Slow but obviously correct: build the frame, then compute each total with a plain loop.
    df = pd.DataFrame(data)
    totals = []
    for p, q in zip(data["price"], data["quantity"]):
        totals.append(p * q)
    df["total"] = pd.Series(totals, dtype=float)
    return df


rng = np.random.default_rng(0)  # seeded, so the tests are the same every run
_n = 200
_prices = np.round(rng.uniform(0.5, 100.0, size=_n), 2)
_prices[rng.random(_n) < 0.1] = np.nan
_nan = float("nan")
CASES = [  # one tuple of arguments per case: the examples, edge cases, then a few random / large ones
    ({"item": ["pen", "book"], "price": [1.5, 12.0], "quantity": [4, 2]},),
    ({"item": ["tea"], "price": [2.5], "quantity": [0]},),
    ({"item": ["cup", "lid"], "price": [3.0, _nan], "quantity": [2, 5]},),
    ({"item": ["a", "b", "c"], "price": [0.0, 0.0, 0.0], "quantity": [1, 2, 3]},),
    ({"item": ["x"], "price": [_nan], "quantity": [0]},),
    ({"item": ["a", "a", "a"], "price": [2.0, 2.0, 2.0], "quantity": [3, 3, 3]},),
    ({"item": ["big"], "price": [999.99], "quantity": [1000]},),
    ({"item": [f"item{i}" for i in range(_n)], "price": _prices.tolist(),
      "quantity": rng.integers(0, 50, size=_n).tolist()},),
    ({"item": [f"s{i}" for i in range(10)], "price": np.round(rng.uniform(1, 10, size=10), 2).tolist(),
      "quantity": rng.integers(0, 10, size=10).tolist()},),
]
# ---------------------------------------------------------------------------------------------------------------

if NUMPY_ONLY:
    def _banned(name):
        def f(*args, **kwargs):
            raise RuntimeError(f"{name} is not allowed in this problem: build it from basic array operations")
        return f

    for _mod, _name in [(np, "einsum"), (np, "tensordot"), (np, "convolve"), (np, "correlate"), (np.linalg, "norm"),
                        (np.lib.stride_tricks, "sliding_window_view"), (np.lib.stride_tricks, "as_strided")]:
        setattr(_mod, _name, _banned(_name))

    class _NumpyOnly:
        def find_spec(self, name, path=None, target=None):
            if name.split(".")[0] in ("scipy", "sklearn", "pandas", "torch"):
                raise ImportError(f"{name.split('.')[0]} is not allowed in this problem: use NumPy only")

    sys.meta_path.insert(0, _NumpyOnly())

ns = {}
try:
    exec(open("attempt.py").read(), ns)
except ImportError as e:
    print(f"FAIL: {e}")
    print("0/1 passed")
    sys.exit(1)
attempt = ns[FUNC]


def copy(a):
    return a.clone() if hasattr(a, "clone") else a.copy() if hasattr(a, "copy") else a


def same(got, want):
    pd, torch = sys.modules.get("pandas"), sys.modules.get("torch")
    if pd and isinstance(want, (pd.DataFrame, pd.Series)):
        try:
            pd.testing.assert_frame_equal(got, want, check_dtype=False) if isinstance(want, pd.DataFrame) else pd.testing.assert_series_equal(got, want, check_dtype=False)
            return True
        except (AssertionError, TypeError):
            return False
    if torch and isinstance(want, torch.Tensor):
        return isinstance(got, torch.Tensor) and got.shape == want.shape and torch.allclose(got.double(), want.double(), rtol=1e-5, atol=1e-6, equal_nan=True)
    if isinstance(want, np.ndarray):
        return isinstance(got, np.ndarray) and got.shape == want.shape and np.allclose(got, want, rtol=1e-5, atol=1e-6, equal_nan=True)
    if isinstance(want, (list, tuple)):
        return isinstance(got, (list, tuple)) and len(got) == len(want) and all(same(g, w) for g, w in zip(got, want))
    if isinstance(want, float):
        return isinstance(got, (int, float, np.floating)) and abs(got - want) <= 1e-6 + 1e-5 * abs(want)
    return got == want


def show(x):
    s = repr(x)
    return s if len(s) <= 200 else s[:200] + "..."


passed = 0
for n, args in enumerate(CASES, 1):
    try:
        want = reference(*[copy(a) for a in args])
        got = attempt(*[copy(a) for a in args])
        if same(got, want):
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input={show(args)}, expected={show(want)}, got={show(got)}")
    except Exception as e:
        print(f"FAIL case {n}: input={show(args)}, got {type(e).__name__}: {e}")

print(f"{passed}/{len(CASES)} passed")
if passed != len(CASES):
    sys.exit(1)
