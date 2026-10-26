import sys
import numpy as np

ns = {}
exec(open("attempt.py").read(), ns)
FN = ns["precision_recall_f1"]


def reference(y_true: np.ndarray, y_pred: np.ndarray) -> list:
    tp = int(np.sum((y_pred == 1) & (y_true == 1)))
    fp = int(np.sum((y_pred == 1) & (y_true == 0)))
    fn = int(np.sum((y_pred == 0) & (y_true == 1)))
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return [precision, recall, f1]

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


NAMES = ['y_true', 'y_pred']
rng = np.random.default_rng(2)

cases = [
    (np.array([1, 0, 1, 1, 0]), np.array([1, 1, 0, 1, 0])),
    (np.array([0, 0, 1]), np.array([0, 0, 0])),
    (np.array([0, 0, 0]), np.array([1, 0, 1])),
    (np.array([0, 0, 0]), np.array([0, 0, 0])),
    (np.array([1, 1, 0, 0]), np.array([1, 1, 0, 0])),
    (np.array([1, 1, 0, 0]), np.array([0, 0, 1, 1])),
    (np.array([1]), np.array([1])),
    (np.array([1, 1, 1, 1]), np.array([1, 0, 0, 0])),
    (rng.integers(0, 2, size=1000), rng.integers(0, 2, size=1000)),
    (rng.integers(0, 2, size=100000), rng.integers(0, 2, size=100000)),
]


def check(got, want):
    if not isinstance(got, (list, tuple)) or len(got) != 3:
        return f"expected a list [precision, recall, f1], got {short(got)}"
    return close(got, want, rtol=1e-9, atol=1e-9)

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
