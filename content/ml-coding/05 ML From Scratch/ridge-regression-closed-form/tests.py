import sys
import numpy as np

ns = {}
exec(open("attempt.py").read(), ns)
FN = ns["ridge_regression"]


def reference(X: np.ndarray, y: np.ndarray, alpha: float) -> np.ndarray:
    A = np.hstack([np.ones((X.shape[0], 1)), X])
    D = alpha * np.eye(A.shape[1])
    D[0, 0] = 0.0
    return np.linalg.solve(A.T @ A + D, A.T @ y)

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


NAMES = ['X', 'y', 'alpha']
rng = np.random.default_rng(12)

Xd = rng.normal(size=(30, 2))
Xd = np.hstack([Xd, Xd])
Xb = rng.normal(size=(2000, 20))
cases = [
    (np.array([[1.0], [2.0], [3.0]]), np.array([3.0, 5.0, 7.0]), 1.0),
    (np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0], [2.0, 2.0]]), np.array([2.0, 1.0, 4.0, 7.0]), 0.5),
    (np.array([[1.0], [2.0], [3.0]]), np.array([3.0, 5.0, 7.0]), 1e-8),
    (np.array([[1.0], [2.0], [3.0], [4.0]]), np.array([10.0, 12.0, 9.0, 11.0]), 1e6),
    (np.array([[2.0]]), np.array([5.0]), 3.0),
    (Xd, Xd @ np.array([1.0, 2.0, 3.0, 4.0]) + 1.0, 0.1),
    (rng.normal(size=(5, 12)), rng.normal(size=5), 2.0),
    (rng.normal(size=(100, 5)) + 3.0, rng.normal(size=100) + 10.0, 10.0),
    (Xb, Xb @ rng.normal(size=20) - 4.0 + rng.normal(size=2000), 25.0),
]


def check(got, want):
    return close(got, want, rtol=1e-5, atol=1e-6)

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
