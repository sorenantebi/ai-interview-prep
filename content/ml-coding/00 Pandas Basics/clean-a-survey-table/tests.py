import sys
import numpy as np
import pandas as pd

# --- Edit these ------------------------------------------------------------------------------------------------
FUNC = "clean_table"  # the function name from starter.py
NUMPY_ONLY = False      # True: ban SciPy / pandas / PyTorch and NumPy shortcuts (einsum, convolve, ...), as in 01 NumPy


def reference(df, defaults, fixes):
    # Plain-Python version: rebuild each column value by value (fill first, then fix).
    data = {}
    for col in df.columns:
        vals = df[col].tolist()
        if col in defaults:
            vals = [defaults[col] if pd.isna(v) else v for v in vals]
        if col in fixes:
            vals = [fixes[col].get(v, v) if not pd.isna(v) else v for v in vals]
        data[col] = vals
    return pd.DataFrame(data, index=df.index)


rng = np.random.default_rng(0)  # seeded, so the tests are the same every run


def make(n):
    city = [None if rng.random() < 0.2 else str(rng.choice(["cat", "dog", "catt", "dgo"])) for _ in range(n)]
    age = rng.integers(-1, 60, size=n).astype(float)
    age[rng.random(n) < 0.2] = np.nan
    return pd.DataFrame({"city": city, "age": age, "id": np.arange(n)})


CASES = [  # one tuple of arguments per case: the examples, edge cases, then a few random / large ones
    (pd.DataFrame({"city": ["Berlin", "Bon", None, "Bonn"], "age": [25.0, np.nan, 31.0, np.nan]}),
     {"city": "unknown", "age": 30.0}, {"city": {"Bon": "Bonn"}}),
    (pd.DataFrame({"grade": ["A", "a", "B", None], "score": [1.5, 2.5, np.nan, 4.0]}),
     {"grade": "F"}, {"grade": {"a": "A"}}),
    # single row
    (pd.DataFrame({"x": [None]}), {"x": "none"}, {"x": {"nope": "no"}}),
    # no missing values, no typos present
    (pd.DataFrame({"a": ["u", "v"], "b": [1.0, 2.0]}), {"a": "z"}, {"b": {9.0: 0.0}}),
    # default is itself corrected by fixes (fill first, then replace)
    (pd.DataFrame({"c": ["ok", None, "bad"]}), {"c": "N/A"}, {"c": {"N/A": "unknown", "bad": "ok"}}),
    # several replacements in several columns, non-default index
    (pd.DataFrame({"p": ["x", "xx", "y", "yy"], "q": ["m", "mm", None, "m"]}, index=[10, 20, 30, 40]),
     {"q": "m"}, {"p": {"xx": "x", "yy": "y"}, "q": {"mm": "m"}}),
    # numeric sentinel replaced, missing numbers filled
    (pd.DataFrame({"age": [-1.0, 20.0, np.nan, -1.0]}), {"age": 0.0}, {"age": {-1.0: 0.0}}),
    (make(30), {"city": "unknown", "age": 35.0}, {"city": {"catt": "cat", "dgo": "dog"}, "age": {-1.0: 0.0}}),
    (make(200), {"city": "cat", "age": 0.0}, {"city": {"catt": "cat", "dgo": "dog"}}),
    (make(1000), {"age": 30.0}, {"city": {"catt": "cat", "dgo": "dog"}}),
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
