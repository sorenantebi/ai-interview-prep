import sys
import numpy as np

# --- Edit these ------------------------------------------------------------------------------------------------
FUNC = "function_name"  # the function name from starter.py
NUMPY_ONLY = False      # True: ban SciPy / pandas / PyTorch and NumPy shortcuts (einsum, convolve, ...), as in 01 NumPy


def reference(x, k):
    # The correct answer, written independently of attempt.py. With NUMPY_ONLY the banned helpers raise here too.
    ...


rng = np.random.default_rng(0)  # seeded, so the tests are the same every run
CASES = [  # one tuple of arguments per case: the examples, edge cases, then a few random / large ones
    (np.array([[1.0, 2.0], [3.0, 4.0]]), 1),
    (np.array([[0.0]]), 1),
    (rng.normal(size=(50, 8)), 3),
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
