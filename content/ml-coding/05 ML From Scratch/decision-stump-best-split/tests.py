import sys
import numpy as np

ns = {}
exec(open("attempt.py").read(), ns)
FN = ns["best_split"]


def reference(X: np.ndarray, y: np.ndarray) -> list:
    n, d = X.shape
    onehot = (y[:, None] == np.unique(y)[None, :]).astype(float)
    total = onehot.sum(axis=0)

    def gini(counts, size):
        return 1.0 - ((counts / size[:, None]) ** 2).sum(axis=1)

    best = [-1, 0.0, float(1.0 - ((total / n) ** 2).sum())]
    best_score = np.inf
    for f in range(d):
        order = np.argsort(X[:, f], kind="stable")
        v = X[order, f]
        cuts = np.nonzero(v[:-1] < v[1:])[0]
        if len(cuts) == 0:
            continue
        left = np.cumsum(onehot[order], axis=0)[cuts]
        n_left = (cuts + 1).astype(float)
        n_right = n - n_left
        scores = (n_left * gini(left, n_left) + n_right * gini(total - left, n_right)) / n
        thresholds = (v[cuts] + v[cuts + 1]) / 2
        for s, t in zip(scores, thresholds):
            if s < best_score - 1e-12:
                best_score, best = s, [f, float(t), float(s)]
    return best

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
rng = np.random.default_rng(11)

Xs = rng.integers(0, 4, size=(60, 3)).astype(float)
ys = rng.integers(0, 3, size=60)
Xf = rng.normal(size=(300, 4))
yf = (Xf[:, 2] > 0.3).astype(int)
yf[rng.integers(0, 300, size=30)] = 2
cases = [
    (np.array([[1.0], [2.0], [3.0], [4.0]]), np.array([0, 0, 1, 1])),
    (np.array([[1.0, 5.0], [2.0, 5.0], [3.0, 6.0], [4.0, 6.0], [5.0, 7.0]]), np.array([0, 1, 0, 1, 1])),
    (np.array([[3.0], [3.0]]), np.array([0, 1])),
    (np.array([[1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [4.0, 4.0]]), np.array([0, 0, 1, 1])),
    (np.array([[1.0], [2.0], [3.0], [4.0]]), np.array([5, 5, 5, 5])),
    (np.array([[2.0], [1.0], [2.0], [1.0]]), np.array([1, 0, 1, 0])),
    (np.array([[7.0]]), np.array([0])),
    (np.array([[0.0, 1.0], [0.0, 2.0], [0.0, 3.0]]), np.array([1, 0, 1])),
    (Xs, ys),
    (Xf, yf),
    (rng.normal(size=(2000, 20)), rng.integers(0, 4, size=2000)),
]


def check(got, want):
    if not isinstance(got, (list, tuple)) or len(got) != 3:
        return f"expected a list [feature, threshold, score], got {short(got)}"
    try:
        same_feature = int(got[0]) == want[0]
    except (TypeError, ValueError):
        same_feature = False
    if not same_feature or close(got[1], want[1], rtol=1e-9, atol=1e-9) or close(got[2], want[2], rtol=1e-9, atol=1e-9):
        return f"expected {short(want)}, got {short(got)}"

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
