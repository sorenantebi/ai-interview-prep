import sys
import numpy as np

ns = {}
exec(open("attempt.py").read(), ns)
FN = ns["confusion_matrix"]


def reference(y_true: np.ndarray, y_pred: np.ndarray, num_classes: int) -> np.ndarray:
    cm = np.zeros((num_classes, num_classes), dtype=int)
    np.add.at(cm, (y_true, y_pred), 1)
    return cm

def short(x, limit=300):
    s = np.array2string(x, threshold=12, precision=5) if isinstance(x, np.ndarray) else repr(x)
    s = " ".join(s.split())
    return s if len(s) <= limit else s[:limit] + "..."


def copy(a):
    return a.copy() if isinstance(a, np.ndarray) else a


def close(got, want, rtol=1e-5, atol=1e-6, exact=False):
    try:
        g = np.asarray(got, dtype=float)
    except (TypeError, ValueError):
        return f"expected {short(np.asarray(want))}, got {short(got)}"
    w = np.asarray(want, dtype=float)
    if g.shape != w.shape:
        return f"expected shape {w.shape}, got {type(got).__name__} with shape {g.shape}"
    ok = np.array_equal(g, w) if exact else np.allclose(g, w, rtol=rtol, atol=atol)
    return None if ok else f"expected {short(w)}, got {short(g)}"


NAMES = ['y_true', 'y_pred', 'num_classes']
rng = np.random.default_rng(1)

cases = [
    (np.array([0, 1, 2, 1]), np.array([0, 2, 2, 1]), 3),
    (np.array([1, 1, 0]), np.array([0, 0, 0]), 2),
    (np.array([0, 1, 2]), np.array([0, 1, 2]), 3),
    (np.array([0, 0, 1, 1]), np.array([1, 1, 0, 0]), 2),
    (np.array([0, 2, 2]), np.array([2, 0, 2]), 4),
    (np.array([0]), np.array([0]), 1),
    (np.array([3]), np.array([1]), 5),
    (np.array([1, 1, 1, 1]), np.array([1, 1, 1, 1]), 2),
    (rng.integers(0, 10, size=5000), rng.integers(0, 10, size=5000), 10),
    (rng.integers(0, 3, size=100000), rng.integers(0, 3, size=100000), 3),
]


def check(got, want):
    err = close(got, want, exact=True)
    if err:
        return err
    if not np.issubdtype(np.asarray(got).dtype, np.integer):
        return f"expected an integer array, got dtype {np.asarray(got).dtype}"

passed = 0
for n, args in enumerate(cases, 1):
    shown = ", ".join(f"{k}={short(v)}" for k, v in zip(NAMES, args))
    try:
        want = reference(*[copy(a) for a in args])
        got = FN(*[copy(a) for a in args])
        err = check(got, want)
        if err:
            print(f"FAIL case {n}: input {shown}; {err}")
        else:
            print(f"PASS case {n}")
            passed += 1
    except Exception as e:
        print(f"FAIL case {n}: input {shown}; got {type(e).__name__}: {e}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)
