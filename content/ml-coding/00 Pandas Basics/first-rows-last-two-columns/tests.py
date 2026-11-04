import sys
import numpy as np
import pandas as pd

# --- Edit these ------------------------------------------------------------------------------------------------
FUNC = "top_left_slice"  # the function name from starter.py
NUMPY_ONLY = False      # True: ban SciPy / pandas / PyTorch and NumPy shortcuts (einsum, convolve, ...), as in 01 NumPy


def reference(df, n):
    # Pick the columns by position through the column Index, then take the first n rows.
    cols = list(df.columns[len(df.columns) - 2:])
    return df[cols].head(n)


rng = np.random.default_rng(0)  # seeded, so the tests are the same every run
CASES = [  # one tuple of arguments per case: the examples, edge cases, then a few random / large ones
    (pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]}), 2),
    (pd.DataFrame({"x": [1.5, 2.5], "y": [0.5, 1.0], "z": [3.0, 4.0], "w": [9.0, 8.0]}), 1),
    (pd.DataFrame({"p": [1, 2, 3, 4], "q": [5, 6, 7, 8]}), 3),
    (pd.DataFrame({"p": [1, 2, 3, 4], "q": [5, 6, 7, 8]}), 0),
    (pd.DataFrame({"p": [1], "q": [2]}), 1),
    (pd.DataFrame({"a": [1, 2, 3, 4], "b": [5.0, np.nan, 7.0, 8.0], "c": ["u", "v", "w", "x"]},
                  index=[10, 20, 30, 40]), 3),
    (pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9], "d": [0, 0, 1]}, index=["r1", "r2", "r3"]), 3),
    (pd.DataFrame({"k": [1, 2, 3], "k2": [4, 5, 6], "k3": [7, 8, 9]}), 5),
    (pd.DataFrame(rng.normal(size=(20, 5)), columns=list("abcde")), 7),
    (pd.DataFrame(rng.integers(0, 100, size=(50, 8)), columns=[f"f{i}" for i in range(8)]), 25),
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
