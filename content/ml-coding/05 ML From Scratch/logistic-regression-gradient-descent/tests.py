import sys
import numpy as np

ns = {}
exec(open("attempt.py").read(), ns)
FN = ns["logistic_regression_gd"]


def reference(X: np.ndarray, y: np.ndarray, w: np.ndarray, b: float, lr: float, steps: int) -> list:
    w = np.array(w, dtype=float)
    b = float(b)
    n = X.shape[0]
    for _ in range(steps):
        p = 1.0 / (1.0 + np.exp(-(X @ w + b)))
        err = p - y
        grad_w = X.T @ err / n
        grad_b = err.mean()
        w = w - lr * grad_w
        b = b - lr * grad_b
    return [w, float(b)]

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


NAMES = ['X', 'y', 'w', 'b', 'lr', 'steps']
rng = np.random.default_rng(5)

X_r = rng.normal(size=(100, 3))
y_r = (X_r @ np.array([1.0, -2.0, 0.5]) + rng.normal(scale=0.5, size=100) > 0).astype(int)
X_big = rng.normal(size=(5000, 5))
y_big = (X_big @ rng.normal(size=5) > 0).astype(int)
cases = [
    (np.array([[0.0], [1.0]]), np.array([0, 1]), np.array([0.0]), 0.0, 1.0, 1),
    (np.array([[1.0, 2.0], [2.0, 0.0], [0.0, 1.0]]), np.array([1, 0, 1]), np.array([0.1, -0.1]), 0.5, 0.5, 3),
    (np.array([[1.0, 2.0]]), np.array([1]), np.array([0.3, 0.2]), -0.1, 0.1, 0),
    (np.array([[1.0], [2.0], [3.0]]), np.array([1, 1, 1]), np.array([0.0]), 0.0, 0.1, 10),
    (np.array([[1.0], [-1.0]]), np.array([0, 0]), np.array([0.5]), 0.5, 0.2, 5),
    (X_r, y_r, np.zeros(3), 0.0, 0.1, 200),
    (X_r, y_r, np.array([0.5, 0.5, -0.5]), -1.0, 0.05, 50),
    (X_big, y_big, np.zeros(5), 0.0, 0.5, 100),
]


def check(got, want):
    if not isinstance(got, (list, tuple)) or len(got) != 2:
        return f"expected a list [w, b], got {short(got)}"
    err = close(got[0], want[0])
    if err:
        return "w: " + err
    err = close(got[1], want[1])
    if err:
        return "b: " + err

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
