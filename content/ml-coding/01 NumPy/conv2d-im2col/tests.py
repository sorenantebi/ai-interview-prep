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
conv2d = ns["conv2d"]

def reference(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    H, W = image.shape
    kh, kw = kernel.shape
    oh, ow = H - kh + 1, W - kw + 1
    rows = np.arange(oh)[:, None] + np.arange(kh)[None, :]  # (oh, kh): image rows each output row touches
    cols = np.arange(ow)[:, None] + np.arange(kw)[None, :]  # (ow, kw)
    patches = image[rows[:, None, :, None], cols[None, :, None, :]]  # (oh, ow, kh, kw)
    cols_matrix = patches.reshape(oh * ow, kh * kw)  # im2col: one row per output pixel
    return (cols_matrix @ kernel.reshape(-1)).reshape(oh, ow)

rng = np.random.default_rng(0)
cases = [
    (np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]), np.array([[1.0, 0.0], [0.0, -1.0]])),
    (np.array([[1.0, 2.0, 3.0, 4.0]]), np.array([[1.0, 1.0, 1.0]])),
    (np.array([[5.0]]), np.array([[2.0]])),
    (np.arange(12.0).reshape(3, 4), np.ones((3, 4))),
    (np.arange(16.0).reshape(4, 4), np.array([[0.0, 1.0], [2.0, 3.0]])),
    (np.arange(10.0).reshape(5, 2), np.array([[1.0], [-1.0]])),
    (rng.normal(size=(20, 15)), rng.normal(size=(3, 5))),
    (rng.normal(size=(1200, 1200)), rng.normal(size=(3, 3))),
]

TIME_LIMIT = 0.5


def show(a):
    return np.array2string(np.asarray(a), threshold=12, precision=4) if isinstance(a, np.ndarray) else repr(a)


passed = 0
for n, args in enumerate(cases, 1):
    shown = ", ".join(show(a) for a in args)
    try:
        want = reference(*[a.copy() if isinstance(a, np.ndarray) else a for a in args])
        given = [a.copy() if isinstance(a, np.ndarray) else a for a in args]
        start = time.perf_counter()
        got = conv2d(*given)
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
