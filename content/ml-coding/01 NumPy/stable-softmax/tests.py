import sys
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
softmax = ns["softmax"]


def reference(x):
    z = x - x.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)


rng = np.random.default_rng(0)
cases = [
    np.array([[1.0, 2.0, 3.0]]),
    np.array([[1000.0, 1000.0], [0.0, -1000.0]]),
    np.array([[0.0]]),
    np.array([[-5.0, -5.0, -5.0, -5.0]]),
    np.array([[10000.0, -10000.0, 0.0]]),
    rng.normal(size=(4, 7)),
    rng.normal(scale=50, size=(30, 12)),
    rng.uniform(-1e4, 1e4, size=(1000, 1000)),
]

passed = 0
for n, x in enumerate(cases, 1):
    try:
        got = softmax(x.copy())
        want = reference(x)
        if not isinstance(got, np.ndarray) or got.shape != want.shape:
            print(f"FAIL case {n}: input shape {x.shape}, expected an array of shape {want.shape}, got {type(got).__name__} {getattr(got, 'shape', '')}")
        elif not np.allclose(got, want, rtol=1e-6, atol=1e-9):
            print(f"FAIL case {n}: input={np.array2string(x, threshold=12)}, expected={np.array2string(want, threshold=12)}, got={np.array2string(got, threshold=12)}")
        else:
            print(f"PASS case {n}")
            passed += 1
    except Exception as e:
        print(f"FAIL case {n}: input shape {x.shape}, got {type(e).__name__}: {e}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)
