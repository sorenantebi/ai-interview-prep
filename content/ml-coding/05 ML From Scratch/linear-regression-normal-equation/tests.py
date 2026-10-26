import sys
import numpy as np

ns = {}
exec(open("attempt.py").read(), ns)
FN = ns["fit_linear_regression"]


def reference(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    A = np.hstack([np.ones((X.shape[0], 1)), X])
    w, *_ = np.linalg.lstsq(A, y, rcond=None)
    return w

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


NAMES = ['X', 'y']
rng = np.random.default_rng(3)

X_big = rng.normal(size=(2000, 10))
X_dup = rng.normal(size=(20, 2))
X_dup = np.hstack([X_dup, X_dup[:, :1]])
cases = [
    (np.array([[1.0], [2.0], [3.0]]), np.array([3.0, 5.0, 7.0])),
    (np.array([[0.0, 1.0], [1.0, 0.0], [1.0, 1.0], [2.0, 1.0]]), np.array([1.0, 2.0, 2.5, 4.0])),
    (np.array([[1.0], [2.0]]), np.array([1.0, 1.0])),
    (np.array([[2.0]]), np.array([4.0])),
    (np.array([[1.0, 2.0], [1.0, 2.0], [1.0, 2.0]]), np.array([1.0, 2.0, 3.0])),
    (X_dup, X_dup @ np.array([1.0, -2.0, 3.0]) + 0.5),
    (rng.normal(size=(3, 5)), rng.normal(size=3)),
    (rng.normal(size=(50, 3)), rng.normal(size=50)),
    (X_big, X_big @ rng.normal(size=10) + 2.0 + rng.normal(scale=0.1, size=2000)),
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
