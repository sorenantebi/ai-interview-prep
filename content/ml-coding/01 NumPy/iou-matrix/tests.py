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
iou_matrix = ns["iou_matrix"]

def reference(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    area_a = (a[:, 2] - a[:, 0]) * (a[:, 3] - a[:, 1])
    area_b = (b[:, 2] - b[:, 0]) * (b[:, 3] - b[:, 1])
    x1 = np.maximum(a[:, None, 0], b[None, :, 0])
    y1 = np.maximum(a[:, None, 1], b[None, :, 1])
    x2 = np.minimum(a[:, None, 2], b[None, :, 2])
    y2 = np.minimum(a[:, None, 3], b[None, :, 3])
    inter = np.clip(x2 - x1, 0, None) * np.clip(y2 - y1, 0, None)
    union = area_a[:, None] + area_b[None, :] - inter
    return np.divide(inter, union, out=np.zeros_like(inter, dtype=float), where=union > 0)

rng = np.random.default_rng(0)
def boxes(k, size):
    xy = rng.uniform(0, size, size=(k, 2))
    wh = rng.uniform(0, size / 3, size=(k, 2))
    return np.hstack([xy, xy + wh])


cases = [
    (np.array([[0.0, 0.0, 2.0, 2.0]]), np.array([[1.0, 1.0, 3.0, 3.0], [5.0, 5.0, 6.0, 6.0]])),
    (np.array([[0.0, 0.0, 4.0, 4.0], [0.0, 0.0, 1.0, 1.0]]), np.array([[0.0, 0.0, 4.0, 4.0]])),
    (np.array([[0.0, 0.0, 1.0, 1.0]]), np.array([[1.0, 0.0, 2.0, 1.0]])),
    (np.array([[2.0, 2.0, 2.0, 2.0]]), np.array([[2.0, 2.0, 2.0, 2.0]])),
    (np.array([[0.0, 0.0, 0.0, 5.0]]), np.array([[0.0, 0.0, 3.0, 3.0]])),
    (np.array([[1.0, 1.0, 3.0, 2.0]]), np.array([[0.0, 0.0, 4.0, 4.0]])),
    (boxes(10, 20), boxes(7, 20)),
    (boxes(1500, 10_000), boxes(1500, 10_000)),
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
        got = iou_matrix(*given)
        elapsed = time.perf_counter() - start
        if not isinstance(got, np.ndarray) or got.shape != want.shape:
            print(f"FAIL case {n}: input={shown}, expected an array of shape {want.shape}, got {type(got).__name__} {getattr(got, 'shape', '')}")
        elif not np.allclose(got, want, rtol=1e-7, atol=1e-9, equal_nan=True):
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
