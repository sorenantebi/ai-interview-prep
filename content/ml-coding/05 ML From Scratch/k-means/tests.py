import sys
import numpy as np

ns = {}
exec(open("attempt.py").read(), ns)
FN = ns["k_means"]


def reference(X: np.ndarray, centroids: np.ndarray, iterations: int) -> list:
    C = np.array(centroids, dtype=float)
    labels = np.zeros(X.shape[0], dtype=int)
    for _ in range(iterations):
        d2 = ((X[:, None, :] - C[None, :, :]) ** 2).sum(axis=2)
        labels = d2.argmin(axis=1)
        for j in range(C.shape[0]):
            members = X[labels == j]
            if len(members):
                C[j] = members.mean(axis=0)
    return [C, labels]

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


NAMES = ['X', 'centroids', 'iterations']
rng = np.random.default_rng(6)

blobs = np.vstack([rng.normal(loc=c, scale=0.6, size=(75, 2)) for c in [(0, 0), (5, 5), (0, 6), (6, -1)]])
big = rng.normal(size=(5000, 3))
cases = [
    (np.array([[0.0, 0.0], [0.0, 1.0], [10.0, 10.0], [10.0, 11.0]]), np.array([[0.0, 0.0], [10.0, 10.0]]), 1),
    (np.array([[1.0], [2.0], [9.0], [12.0]]), np.array([[0.0], [5.0], [100.0]]), 2),
    (np.array([[1.0], [3.0]]), np.array([[2.0], [2.0]]), 1),
    (np.array([[0.0], [2.0], [4.0]]), np.array([[1.0], [3.0]]), 1),
    (np.array([[1.0, 1.0], [2.0, 2.0], [3.0, 3.0]]), np.array([[0.0, 0.0]]), 3),
    (np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]), np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]), 2),
    (blobs, blobs[[0, 80, 160, 240]].copy(), 10),
    (blobs, np.array([[0.0, 0.0], [1.0, 1.0], [50.0, 50.0]]), 5),
    (big, big[:8].copy(), 20),
]


def check(got, want):
    if not isinstance(got, (list, tuple)) or len(got) != 2:
        return f"expected a list [centroids, labels], got {short(got)}"
    err = close(got[1], want[1], exact=True)
    if err:
        return "labels: " + err
    err = close(got[0], want[0])
    if err:
        return "centroids: " + err

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
