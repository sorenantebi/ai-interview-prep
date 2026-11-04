import sys
import numpy as np

# --- Edit these ------------------------------------------------------------------------------------------------
FUNC = "aggregate_stats"  # the function name from starter.py
NUMPY_ONLY = True         # True: ban SciPy / pandas / PyTorch and NumPy shortcuts (einsum, convolve, ...), as in 01 NumPy


def reference(x):
    # Slow, loop-based version, written independently of the vectorised solution.
    n, d = x.shape
    row_sums = np.zeros(n)
    for i in range(n):
        for j in range(d):
            row_sums[i] += x[i, j]
    col_means = np.zeros(d)
    best = np.zeros(d, dtype=np.int64)
    overall = float(x[0, 0])
    for j in range(d):
        total = 0.0
        for i in range(n):
            total += x[i, j]
            if x[i, j] > x[best[j], j]:
                best[j] = i
            if x[i, j] > overall:
                overall = float(x[i, j])
        col_means[j] = total / n
    return row_sums, col_means, overall, best


rng = np.random.default_rng(0)  # seeded, so the tests are the same every run
CASES = [  # one tuple of arguments per case: the examples, edge cases, then a few random / large ones
    (np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]),),
    (np.array([[3.0, -1.0], [0.0, 7.0], [3.0, 2.0]]),),
    (np.array([[-2.5]]),),
    (np.zeros((4, 3)),),
    (np.array([[5.0, 1.0, 9.0, -3.0]]),),
    (np.array([[5.0], [1.0], [9.0], [9.0]]),),
    (-np.abs(rng.normal(size=(6, 5))) - 1.0,),
    (rng.normal(size=(10, 4)),),
    (rng.integers(0, 3, size=(8, 6)).astype(float),),
    (rng.normal(size=(200, 50)) * 100,),
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
