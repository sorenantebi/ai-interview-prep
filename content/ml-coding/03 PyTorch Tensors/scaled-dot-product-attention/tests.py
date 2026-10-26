import sys
import math
import torch
import torch.nn.functional as F

def _disabled(*a, **k):
    raise RuntimeError("this function is disabled for this problem")
F.scaled_dot_product_attention = _disabled
torch.nn.MultiheadAttention = _disabled

ns = {}
exec(open("attempt.py").read(), ns)
attempt = ns["attention"]

def reference(q: torch.Tensor, k: torch.Tensor, v: torch.Tensor, mask: torch.Tensor = None) -> torch.Tensor:
    scores = q @ k.transpose(-2, -1) / math.sqrt(q.shape[-1])
    if mask is not None:
        scores = scores.masked_fill(~mask, float("-inf"))
    weights = torch.nan_to_num(torch.softmax(scores, dim=-1), nan=0.0)
    return weights @ v


ATOL, RTOL, CHECK_DTYPE = 1e-5, 1e-4, False


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
def rand(B, Tq, Tk, d, dv, scale=1.0):
    return torch.randn(B, Tq, d) * scale, torch.randn(B, Tk, d), torch.randn(B, Tk, dv)
causal = torch.ones(2, 5, 5, dtype=torch.bool).tril()
none_row = torch.ones(1, 3, 4, dtype=torch.bool)
none_row[0, 1] = False
cases = [
    (torch.tensor([[[1.0, 0.0]]]), torch.tensor([[[1.0, 0.0], [0.0, 1.0]]]), torch.tensor([[[10.0], [20.0]]]), torch.tensor([[[True, True]]])),
    (torch.tensor([[[1.0, 0.0], [0.0, 1.0]]]), torch.tensor([[[1.0, 0.0], [0.0, 1.0]]]), torch.tensor([[[10.0], [20.0]]]), torch.tensor([[[True, False], [False, False]]])),
    (*rand(1, 1, 1, 1, 1), None),
    (*rand(2, 3, 4, 8, 5), None),
    (*rand(2, 5, 5, 4, 3), causal),
    (*rand(1, 3, 4, 6, 2), none_row),
    (*rand(2, 4, 6, 8, 8, scale=1000.0), None),
    (*rand(2, 4, 6, 8, 8, scale=1000.0), torch.rand(2, 4, 6) > 0.5),
    (*rand(3, 7, 2, 16, 1), torch.zeros(3, 7, 2, dtype=torch.bool)),
    (*rand(8, 256, 256, 64, 64), torch.ones(8, 256, 256, dtype=torch.bool).tril()),
]

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
