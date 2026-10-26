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
nms = ns["nms"]

def reference(boxes: np.ndarray, scores: np.ndarray, iou_threshold: float) -> np.ndarray:
    areas = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
    order = np.argsort(-scores, kind="stable")
    keep = []
    while order.size:
        i, rest = order[0], order[1:]
        keep.append(i)
        w = np.clip(np.minimum(boxes[i, 2], boxes[rest, 2]) - np.maximum(boxes[i, 0], boxes[rest, 0]), 0, None)
        h = np.clip(np.minimum(boxes[i, 3], boxes[rest, 3]) - np.maximum(boxes[i, 1], boxes[rest, 1]), 0, None)
        inter = w * h
        union = areas[i] + areas[rest] - inter
        iou = np.divide(inter, union, out=np.zeros_like(inter, dtype=float), where=union > 0)
        order = rest[iou <= iou_threshold]
    return np.array(keep, dtype=int)

rng = np.random.default_rng(0)
def boxes(k, size):
    xy = rng.uniform(0, size, size=(k, 2))
    wh = rng.uniform(1, size / 8, size=(k, 2))
    return np.hstack([xy, xy + wh])


many = boxes(3000, 1000)
cases = [
    (np.array([[0.0, 0.0, 2.0, 2.0], [0.1, 0.0, 2.0, 2.0], [3.0, 3.0, 4.0, 4.0]]), np.array([0.9, 0.8, 0.7]), 0.5),
    (np.array([[0.0, 0.0, 1.0, 1.0], [0.0, 0.0, 1.0, 1.0], [0.5, 0.0, 1.5, 1.0]]), np.array([0.5, 0.5, 0.9]), 0.3),
    (np.zeros((0, 4)), np.zeros(0), 0.5),
    (np.array([[1.0, 1.0, 2.0, 2.0]]), np.array([0.1]), 0.5),
    (np.array([[0.0, 0.0, 2.0, 2.0], [0.0, 0.0, 2.0, 1.0]]), np.array([0.6, 0.9]), 0.5),
    (np.array([[0.0, 0.0, 2.0, 2.0], [1.0, 0.0, 3.0, 2.0]]), np.array([0.9, 0.8]), 1.0 / 3.0),
    (np.array([[0.0, 0.0, 1.0, 1.0], [0.0, 0.0, 1.0, 1.0], [0.0, 0.0, 1.0, 1.0]]), np.array([0.2, 0.2, 0.2]), 0.0),
    (boxes(40, 50), rng.random(40), 0.4),
    (boxes(200, 100), rng.integers(0, 5, size=200).astype(float), 0.2),
    (many, rng.random(3000), 0.5),
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
        got = nms(*given)
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
