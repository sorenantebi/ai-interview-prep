import sys
import math
import torch
import torch.nn.functional as F


ns = {}
exec(open("attempt.py").read(), ns)
attempt = ns["positional_encoding"]

def reference(seq_len: int, d_model: int) -> torch.Tensor:
    pos = torch.arange(seq_len, dtype=torch.float64).unsqueeze(1)
    freq = 10000.0 ** (-torch.arange(0, d_model, 2, dtype=torch.float64) / d_model)
    angle = pos * freq
    pe = torch.zeros(seq_len, d_model, dtype=torch.float64)
    pe[:, 0::2] = torch.sin(angle)
    pe[:, 1::2] = torch.cos(angle)
    return pe.float()


ATOL, RTOL, CHECK_DTYPE = 1e-4, 1e-4, True


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


cases = [(1, 2), (2, 4), (3, 2), (5, 6), (10, 16), (1, 512), (50, 64), (128, 128), (512, 256)]

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
