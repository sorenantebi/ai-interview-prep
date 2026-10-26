import sys
import math
import torch
import torch.nn.functional as F

_cdist = torch.cdist
def _no_cdist(*a, **k):
    raise RuntimeError("torch.cdist is disabled for this problem")
torch.cdist = _no_cdist

ns = {}
exec(open("attempt.py").read(), ns)
attempt = ns["pairwise_distances"]

def reference(a, b):
    return _cdist(a, b, compute_mode="donot_use_mm_for_euclid_dist")


ATOL, RTOL, CHECK_DTYPE = 1e-5, 1e-6, False


def show(x):
    if isinstance(x, torch.Tensor):
        return str(x.tolist()) if x.numel() <= 12 else f"tensor of shape {tuple(x.shape)}"
    if isinstance(x, (list, tuple)):
        s = "[" + ", ".join(show(i) for i in x) + "]"
        return s if len(s) <= 200 else s[:200] + "..."
    return repr(x)


def clone(x):
    if isinstance(x, torch.Tensor):
        return x.clone()
    if isinstance(x, (list, tuple)):
        return type(x)(clone(i) for i in x)
    return x


def mismatch(got, want):
    if isinstance(want, torch.Tensor):
        if not isinstance(got, torch.Tensor):
            return f"expected a tensor, got {type(got).__name__}"
        if tuple(got.shape) != tuple(want.shape):
            return f"expected shape {tuple(want.shape)}, got {tuple(got.shape)}"
        if CHECK_DTYPE and got.dtype != want.dtype:
            return f"expected dtype {want.dtype}, got {got.dtype}"
        if want.dtype in (torch.bool, torch.int64, torch.int32):
            return None if torch.equal(got.to(want.dtype), want) else "wrong values"
        return None if torch.allclose(got.double(), want.double(), rtol=RTOL, atol=ATOL) else "wrong values"
    if isinstance(want, (list, tuple)):
        if not isinstance(got, (list, tuple)) or len(got) != len(want):
            return f"expected a list of {len(want)} items, got {type(got).__name__}"
        for i, (g, w) in enumerate(zip(got, want)):
            m = mismatch(g, w)
            if m:
                return f"item {i}: {m}"
        return None
    if isinstance(want, float):
        if isinstance(got, bool) or not isinstance(got, (int, float)):
            return f"expected a Python float, got {type(got).__name__}"
        return None if abs(got - want) <= ATOL + RTOL * abs(want) else "wrong value"
    return None if got == want else "wrong value"


torch.manual_seed(0)
d = torch.float64
cases = [
    (torch.tensor([[[0.0, 0.0], [3.0, 4.0]]], dtype=d), torch.tensor([[[0.0, 0.0], [6.0, 8.0]]], dtype=d)),
    (torch.tensor([[[1.0]], [[2.0]]], dtype=d), torch.tensor([[[4.0], [0.0]], [[2.0], [-1.0]]], dtype=d)),
    (torch.randn(1, 1, 3, dtype=d), torch.randn(1, 1, 3, dtype=d)),
    (torch.randn(2, 4, 5, dtype=d), torch.randn(2, 6, 5, dtype=d)),
    (torch.randn(3, 7, 1, dtype=d), torch.randn(3, 2, 1, dtype=d)),
    (torch.full((1, 3, 4), 10.0, dtype=d), torch.full((1, 2, 4), 10.0, dtype=d)),
    (torch.randn(2, 5, 8, dtype=d) * 100, torch.randn(2, 5, 8, dtype=d) * 100),
    (torch.randn(4, 500, 64, dtype=d), torch.randn(4, 400, 64, dtype=d)),
]
x = torch.randn(1, 20, 16, dtype=d)
cases.append((x, x.clone()))

passed = 0
for n, args in enumerate(cases, 1):
    try:
        want = reference(*clone(args))
        got = attempt(*clone(args))
        m = mismatch(got, want)
        if m:
            print(f"FAIL case {n}: input={show(list(args))}: {m}; expected={show(want)}, got={show(got)}")
        else:
            print(f"PASS case {n}")
            passed += 1
    except Exception as e:
        print(f"FAIL case {n}: input={show(list(args))}, got {type(e).__name__}: {e}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)
