import sys
import numpy as np

ns = {}
exec(open("attempt.py").read(), ns)
FN = ns["gaussian_nb_predict"]


def reference(X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, eps: float) -> np.ndarray:
    classes = np.unique(y_train)
    mu = np.array([X_train[y_train == c].mean(axis=0) for c in classes])
    var = np.array([X_train[y_train == c].var(axis=0) for c in classes]) + eps
    log_prior = np.log(np.array([(y_train == c).mean() for c in classes]))
    diff = X_test[:, None, :] - mu[None, :, :]
    log_lik = -0.5 * (np.log(2 * np.pi * var)[None] + diff ** 2 / var[None]).sum(axis=2)
    return classes[(log_prior[None] + log_lik).argmax(axis=1)]

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


NAMES = ['X_train', 'y_train', 'X_test', 'eps']
rng = np.random.default_rng(10)

Xa = np.vstack([rng.normal(loc=c, size=(60, 3)) for c in (0.0, 2.0, 4.0)])
ya = np.repeat([0, 1, 2], 60)
Xb = rng.normal(size=(5000, 10)) + rng.integers(0, 4, size=(5000, 1))
yb = (Xb.mean(axis=1) > 1.5).astype(int) * 5
cases = [
    (np.array([[1.0], [2.0], [8.0], [9.0]]), np.array([0, 0, 1, 1]), np.array([[1.5], [7.0], [5.0]]), 1e-9),
    (np.array([[0.0, 1.0], [1.0, 1.0], [5.0, 3.0], [6.0, 3.0], [6.0, 4.0]]), np.array([3, 3, 7, 7, 7]), np.array([[0.5, 1.0], [5.0, 2.0]]), 0.01),
    (np.array([[1.0], [3.0], [1.0], [3.0]]), np.array([2, 2, 1, 1]), np.array([[2.0], [0.0]]), 1e-9),
    (np.array([[5.0, 1.0], [5.0, 2.0], [5.0, 9.0], [5.0, 8.0]]), np.array([0, 0, 1, 1]), np.array([[5.0, 1.5], [6.0, 7.0]]), 1e-6),
    (np.array([[1.0], [2.0], [3.0]]), np.array([4, 4, 4]), np.array([[0.0], [10.0]]), 1e-9),
    (Xa, ya, rng.normal(loc=2.0, scale=2.0, size=(100, 3)), 1e-9),
    (Xa, ya * 10 + 1, Xa[::7].copy(), 0.5),
    (Xb, yb, rng.normal(size=(1000, 10)) + 1.5, 1e-9),
    (rng.normal(size=(6, 2)), np.array([0, 0, 0, 1, 1, 1]), rng.normal(scale=2.0, size=(300, 2)), 1e-9),
    (np.array([[0.0], [2.0], [10.0], [11.0], [13.0], [14.0]]), np.array([0, 0, 1, 1, 1, 1]), np.linspace(-6.0, 6.0, 61)[:, None], 1e-9),
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
