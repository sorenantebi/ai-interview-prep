import sys
import numpy as np

ns = {}
exec(open("attempt.py").read(), ns)
FN = ns["k_fold_indices"]


def reference(n: int, k: int) -> list:
    sizes = [n // k + (1 if i < n % k else 0) for i in range(k)]
    folds, start = [], 0
    for size in sizes:
        val = list(range(start, start + size))
        train = list(range(0, start)) + list(range(start + size, n))
        folds.append([train, val])
        start += size
    return folds

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


NAMES = ['n', 'k']
rng = np.random.default_rng(4)

cases = [(5, 2), (7, 3), (6, 3), (3, 3), (4, 1), (1, 1), (10, 4), (2, 2), (100, 7), (2000, 10)]


def as_lists(x):
    return [[[int(i) for i in part] for part in pair] for pair in x]


def check(got, want):
    try:
        g = as_lists(got)
        if len(g) != len(want) or any(len(p) != 2 for p in g):
            raise ValueError
    except (TypeError, ValueError):
        return f"expected a list of {len(want)} [train, val] pairs, got {short(got)}"
    for i, (gp, wp) in enumerate(zip(g, as_lists(want))):
        if gp != wp:
            return f"fold {i}: expected train={short(wp[0])}, val={short(wp[1])}, got train={short(gp[0])}, val={short(gp[1])}"

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
