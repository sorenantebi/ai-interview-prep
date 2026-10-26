import sys
import numpy as np

ns = {}
exec(open("attempt.py").read(), ns)
FN = ns["roc_auc"]


def reference(y_true: np.ndarray, scores: np.ndarray) -> float:
    order = np.argsort(scores, kind="stable")
    s = scores[order]
    ranks = np.empty(len(s))
    i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and s[j + 1] == s[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2 + 1  # average rank of the tied run
        i = j + 1
    pos = y_true == 1
    P, N = int(pos.sum()), int((~pos).sum())
    U = ranks[pos].sum() - P * (P + 1) / 2
    return float(U / (P * N))

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


NAMES = ['y_true', 'scores']
rng = np.random.default_rng(9)

y_r = rng.integers(0, 2, size=500)
y_r[:2] = [0, 1]
y_b = rng.integers(0, 2, size=20000)
cases = [
    (np.array([0, 0, 1, 1]), np.array([0.1, 0.4, 0.35, 0.8])),
    (np.array([1, 0, 1, 0]), np.array([0.5, 0.5, 0.9, 0.2])),
    (np.array([0, 1]), np.array([0.2, 0.9])),
    (np.array([0, 1]), np.array([0.9, 0.2])),
    (np.array([0, 1, 0, 1]), np.array([0.3, 0.3, 0.3, 0.3])),
    (np.array([1, 1, 1, 0]), np.array([3.0, 1.0, 2.0, 2.0])),
    (y_r, rng.normal(size=500) + y_r),
    (y_r, np.round(rng.normal(size=500), 1)),
    (y_b, np.round(rng.normal(size=20000) + 0.5 * y_b, 2)),
]


def check(got, want):
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
