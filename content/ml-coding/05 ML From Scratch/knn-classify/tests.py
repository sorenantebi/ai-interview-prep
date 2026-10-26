import sys
import numpy as np

ns = {}
exec(open("attempt.py").read(), ns)
FN = ns["knn_classify"]


def reference(X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, k: int) -> np.ndarray:
    d2 = ((X_test[:, None, :] - X_train[None, :, :]) ** 2).sum(axis=2)
    nearest = np.argsort(d2, axis=1, kind="stable")[:, :k]
    votes = y_train[nearest]
    return np.array([np.bincount(row).argmax() for row in votes], dtype=int)

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


NAMES = ['X_train', 'y_train', 'X_test', 'k']
rng = np.random.default_rng(7)

Xa = rng.normal(size=(200, 2))
ya = (Xa[:, 0] > 0).astype(int) + (Xa[:, 1] > 0).astype(int)
Xb = rng.normal(size=(2000, 4))
yb = rng.integers(0, 5, size=2000)
cases = [
    (np.array([[0.0, 0.0], [1.0, 0.0], [5.0, 5.0], [6.0, 5.0]]), np.array([0, 0, 1, 1]), np.array([[0.5, 0.5], [5.5, 4.0]]), 3),
    (np.array([[0.0], [2.0], [3.0], [10.0]]), np.array([4, 1, 4, 1]), np.array([[1.0], [2.5]]), 2),
    (np.array([[0.0], [1.0]]), np.array([7, 3]), np.array([[0.4], [0.6], [0.5]]), 1),
    (np.array([[1.0], [-1.0], [3.0]]), np.array([5, 2, 2]), np.array([[0.0]]), 1),
    (np.array([[1.0], [-1.0], [3.0]]), np.array([5, 2, 9]), np.array([[0.0]]), 2),
    (np.array([[0.0], [1.0], [2.0]]), np.array([1, 0, 1]), np.array([[100.0]]), 3),
    (Xa, ya, rng.normal(size=(50, 2)), 5),
    (Xa, ya, rng.normal(size=(50, 2)), 4),
    (Xb, yb, rng.normal(size=(500, 4)), 7),
    (np.zeros((40, 1)), rng.permutation(40) % 9, np.array([[0.0], [1.0]]), 3),
    (np.repeat(np.arange(5.0), 20)[:, None], rng.integers(0, 6, size=100), np.array([[2.0], [2.5], [-1.0]]), 5),
]


def check(got, want):
    return close(got, want, exact=True)

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
