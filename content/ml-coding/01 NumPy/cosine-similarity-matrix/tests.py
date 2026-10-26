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
cosine_similarity = ns["cosine_similarity"]

def reference(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    na = np.sqrt((a * a).sum(axis=1, keepdims=True))
    nb = np.sqrt((b * b).sum(axis=1, keepdims=True))
    au = a / np.where(na == 0, 1.0, na)
    bu = b / np.where(nb == 0, 1.0, nb)
    return au @ bu.T

rng = np.random.default_rng(0)
cases = [
    (np.array([[1.0, 0.0], [1.0, 1.0]]), np.array([[2.0, 0.0], [0.0, 3.0]])),
    (np.array([[0.0, 0.0], [3.0, 4.0]]), np.array([[-3.0, 4.0]])),
    (np.array([[3.0, 4.0]]), np.array([[-3.0, -4.0]])),
    (np.array([[0.0, 0.0]]), np.array([[0.0, 0.0]])),
    (np.array([[5.0]]), np.array([[-2.0], [7.0]])),
    (np.array([[1.0, 2.0, 3.0]]), np.array([[2.0, 4.0, 6.0]])),
    (rng.normal(size=(6, 4)), rng.normal(size=(3, 4))),
    (np.vstack([rng.normal(size=(9, 8)), np.zeros((1, 8))]), rng.normal(size=(12, 8))),
    (rng.normal(size=(1000, 128)), rng.normal(size=(900, 128))),
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
        got = cosine_similarity(*given)
        elapsed = time.perf_counter() - start
        if not isinstance(got, np.ndarray) or got.shape != want.shape:
            print(f"FAIL case {n}: input={shown}, expected an array of shape {want.shape}, got {type(got).__name__} {getattr(got, 'shape', '')}")
        elif not np.allclose(got, want, rtol=1e-6, atol=1e-8, equal_nan=True):
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
