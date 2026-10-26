import sys
import numpy as np

ns = {}
exec(open("attempt.py").read(), ns)
FN = ns["pca_project"]


def reference(X: np.ndarray, k: int) -> np.ndarray:
    Xc = X - X.mean(axis=0)
    _, _, Vt = np.linalg.svd(Xc, full_matrices=False)
    comps = Vt[:k]
    signs = np.sign(comps[np.arange(k), np.abs(comps).argmax(axis=1)])
    comps = comps * signs[:, None]
    return Xc @ comps.T

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


NAMES = ['X', 'k']
rng = np.random.default_rng(8)

def scaled(n, scales):
    Q, _ = np.linalg.qr(rng.normal(size=(len(scales), len(scales))))
    return (rng.normal(size=(n, len(scales))) * np.array(scales)) @ Q.T + rng.normal(size=len(scales))


cases = [
    (np.array([[1.0, 2.0], [3.0, 3.0], [5.0, 7.0]]), 1),
    (np.array([[2.0, 0.0, 1.0], [0.0, 1.0, 1.0], [4.0, 1.0, 0.0], [2.0, 2.0, 2.0]]), 2),
    (np.array([[0.0, 0.0], [2.0, 0.0], [0.0, 1.0], [2.0, 1.0], [1.0, 0.5]]), 2),
    (np.array([[1.0], [4.0], [2.0]]), 1),
    (scaled(50, [5.0, 2.0, 0.5]), 1),
    (scaled(50, [5.0, 2.0, 0.5]), 3),
    (scaled(200, [10.0, 6.0, 3.0, 1.0, 0.2]), 2),
    (-scaled(30, [4.0, 1.0]), 2),
    (scaled(5000, [9.0, 7.0, 5.0, 3.0, 2.0, 1.5, 1.0, 0.7, 0.4, 0.1]), 3),
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
