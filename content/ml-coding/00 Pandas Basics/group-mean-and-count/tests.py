import sys
import numpy as np
import pandas as pd

# --- Edit these ------------------------------------------------------------------------------------------------
FUNC = "group_mean_count"  # the function name from starter.py
NUMPY_ONLY = False      # True: ban SciPy / pandas / PyTorch and NumPy shortcuts (einsum, convolve, ...), as in 01 NumPy


def reference(df, key, value):
    # Slow, explicit version: one boolean mask per distinct label.
    labels = sorted(set(df[key].tolist()))
    means, counts = [], []
    for lab in labels:
        sub = df[df[key] == lab][value]
        means.append(float(sub.sum()) / len(sub))
        counts.append(len(sub))
    return pd.DataFrame({"mean": means, "count": counts}, index=pd.Index(labels, name=key))


rng = np.random.default_rng(0)  # seeded, so the tests are the same every run
_names = np.array(["red", "green", "blue", "gold", "teal"])
_big = pd.DataFrame({"g": rng.choice(_names, size=500), "x": rng.normal(size=500), "other": rng.integers(0, 9, size=500)})
_ints = pd.DataFrame({"k": rng.integers(0, 6, size=200), "y": rng.uniform(-5, 5, size=200)})
CASES = [  # one tuple of arguments per case: the examples, edge cases, then a few random / large ones
    (pd.DataFrame({"team": ["a", "b", "a", "b", "a"], "score": [1.0, 2.0, 3.0, 6.0, 5.0]}), "team", "score"),
    (pd.DataFrame({"city": ["x", "x"], "price": [10.0, 20.0]}), "city", "price"),
    (pd.DataFrame({"city": ["b", "a", "b"], "v": [2.0, 4.0, 6.0]}), "city", "v"),
    (pd.DataFrame({"k": ["only"], "v": [7.5]}), "k", "v"),
    (pd.DataFrame({"k": ["a", "b", "c"], "v": [0.0, 0.0, 0.0]}), "k", "v"),
    (pd.DataFrame({"k": [3, 1, 2, 1, 3, 3], "v": [1.0, -1.0, 2.0, 3.0, 5.0, 0.5]}), "k", "v"),
    (pd.DataFrame({"o": [1, 2, 3, 4], "k": ["u", "v", "u", "v"], "v": [-2.0, 4.0, 2.0, -4.0]}), "k", "v"),
    (_big, "g", "x"),
    (_ints, "k", "y"),
    (_big, "g", "other"),
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
