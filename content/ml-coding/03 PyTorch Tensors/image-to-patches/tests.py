import sys
import math
import torch
import torch.nn.functional as F


ns = {}
exec(open("attempt.py").read(), ns)
attempt = ns["image_to_patches"]

def reference(images: torch.Tensor, patch: int) -> torch.Tensor:
    B, C, H, W = images.shape
    p = patch
    x = images.reshape(B, C, H // p, p, W // p, p)
    x = x.permute(0, 2, 4, 1, 3, 5)
    return x.reshape(B, (H // p) * (W // p), C * p * p)


ATOL, RTOL, CHECK_DTYPE = 0.0, 0.0, True


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
cases = [
    (torch.arange(16).reshape(1, 1, 4, 4), 2),
    (torch.tensor([[[[1, 2], [3, 4]], [[5, 6], [7, 8]]]]), 2),
    (torch.arange(12).reshape(1, 1, 3, 4), 1),
    (torch.randn(2, 3, 4, 6), 2),
    (torch.randn(1, 2, 6, 6), 3),
    (torch.randn(3, 1, 4, 8), 4),
    (torch.arange(2 * 2 * 4 * 4).reshape(2, 2, 4, 4), 4),
    (torch.randn(8, 3, 224, 224), 16),
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
