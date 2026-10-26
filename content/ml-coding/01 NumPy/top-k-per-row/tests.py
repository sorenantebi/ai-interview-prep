import sys
import time
import numpy as np

# The problem's rules: these helpers would do the work for you, so they raise instead.
def _banned(name):
    def f(*args, **kwargs):
        raise RuntimeError(f"{name} is not allowed in this problem: build it from basic array operations")
    return f

for _mod, _name, _label in [(np, "einsum", "np.einsum"), (np, "tensordot", "np.tensordot"), (np, "convolve", "np.convolve"),
                            (np, "correlate", "np.correlate"), (np.linalg, "norm", "np.linalg.norm"),
                            (np.lib.stride_tricks, "sliding_window_view", "sliding_window_view"),
                            (np.lib.stride_tricks, "as_strided", "as_strided")]:
    setattr(_mod, _name, _banned(_label))
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
top_k_per_row = ns["top_k_per_row"]

def reference(x: np.ndarray, k: int) -> np.ndarray:
    return np.argsort(-x, axis=1, kind="stable")[:, :k]

rng = np.random.default_rng(0)
cases = [
    (np.array([[0.1, 0.9, 0.5], [3.0, 3.0, 1.0]]), 2),
    (np.array([[5.0, 1.0, 5.0, 7.0]]), 3),
    (np.array([[2.0]]), 1),
    (np.array([[1.0, 1.0, 1.0, 1.0]]), 4),
    (np.array([[-1.0, -3.0, -2.0]]), 1),
    (np.array([[0.0, 1.0, 0.0, 1.0, 0.0]]), 3),
    (rng.integers(0, 5, size=(20, 10)).astype(float), 4),
    (rng.normal(size=(50, 30)), 30),
    (rng.integers(0, 50, size=(1000, 1000)).astype(float), 10),
]

TIME_LIMIT = 2.0


def show(a):
    return np.array2string(np.asarray(a), threshold=12, precision=4) if isinstance(a, np.ndarray) else repr(a)


passed = 0
for n, args in enumerate(cases, 1):
    shown = ", ".join(show(a) for a in args)
    try:
        want = reference(*[a.copy() if isinstance(a, np.ndarray) else a for a in args])
        given = [a.copy() if isinstance(a, np.ndarray) else a for a in args]
        start = time.perf_counter()
        got = top_k_per_row(*given)
        elapsed = time.perf_counter() - start
        if not isinstance(got, np.ndarray) or got.shape != want.shape:
            print(f"FAIL case {n}: input={shown}, expected an array of shape {want.shape}, got {type(got).__name__} {getattr(got, 'shape', '')}")
        elif not np.array_equal(got, want):
            print(f"FAIL case {n}: input={shown}, expected={show(want)}, got={show(got)}")
        elif elapsed > TIME_LIMIT:
            print(f"FAIL case {n}: input shape(s) {[getattr(a, 'shape', a) for a in args]} (too slow: {elapsed:.2f}s, expected a vectorised solution)")
        else:
            print(f"PASS case {n}")
            passed += 1
    except Exception as e:
        print(f"FAIL case {n}: input={shown}, got {type(e).__name__}: {e}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)
