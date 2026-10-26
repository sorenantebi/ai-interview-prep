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
replace_outliers = ns["replace_outliers"]

def reference(x: np.ndarray) -> np.ndarray:
    mean = x.mean(axis=0)
    std = x.std(axis=0)
    median = np.median(x, axis=0)
    mask = np.abs(x - mean) > 3 * std
    return np.where(mask, median, x).astype(float)

rng = np.random.default_rng(0)
spiky = rng.normal(size=(200, 5))
spiky[[3, 50, 120], [0, 2, 4]] = [40.0, -35.0, 60.0]
cases = [
    (np.array([[1.0, 5.0], [1.0, 6.0], [1.0, 5.0], [1.0, 6.0], [1.0, 5.0], [1.0, 6.0], [1.0, 5.0], [1.0, 6.0], [1.0, 5.0], [1.0, 6.0], [100.0, 5.0]]),),
    (np.array([[1.0, 2.0], [3.0, 4.0]]),),
    (np.array([[7.0]]),),
    (np.array([[2.0], [2.0], [2.0]]),),
    (np.array([[0.0]] * 19 + [[-50.0]]),),
    (spiky,),
    (rng.normal(size=(30, 4)),),
    (np.where(rng.random((1000, 1000)) < 0.001, 100.0, rng.normal(size=(1000, 1000))),),
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
        got = replace_outliers(*given)
        elapsed = time.perf_counter() - start
        if not isinstance(got, np.ndarray) or got.shape != want.shape:
            print(f"FAIL case {n}: input={shown}, expected an array of shape {want.shape}, got {type(got).__name__} {getattr(got, 'shape', '')}")
        elif not np.allclose(got, want, rtol=1e-9, atol=1e-9, equal_nan=True):
            print(f"FAIL case {n}: input={shown}, expected={show(want)}, got={show(got)}")
        elif any(isinstance(a, np.ndarray) and not np.array_equal(a, g, equal_nan=True) for a, g in zip(args, given)):
            print(f"FAIL case {n}: your function modified its input array; return a new array instead")
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
