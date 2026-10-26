import sys
import torch
import torch.nn.functional as F

ns = {}
exec(open("attempt.py").read(), ns)
attempt = ns["layer_norm"]

RTOL, ATOL = 1e-4, 1e-4


def reference(x, gamma, beta, eps):
    return F.layer_norm(x, (x.shape[-1],), gamma, beta, eps)


def show(a):
    if isinstance(a, torch.Tensor):
        a = a.detach()
        return repr(a.tolist()) if a.numel() <= 12 else f"<tensor of shape {tuple(a.shape)}>"
    if isinstance(a, (list, tuple)):
        return "[" + ", ".join(show(i) for i in a) + "]"
    return repr(a)


def clone(a):
    if isinstance(a, torch.Tensor):
        return a.clone()
    if isinstance(a, (list, tuple)):
        return type(a)(clone(i) for i in a)
    return a


def values(x):
    return list(x) if isinstance(x, (list, tuple)) else [x]


def compare(got, want):
    if got is None:
        return "got None"
    g, w = values(got), values(want)
    if len(g) != len(w):
        return f"expected {len(w)} value(s), got {len(g)}"
    for i, (a, b) in enumerate(zip(g, w), 1):
        if not isinstance(a, torch.Tensor):
            try:
                a = torch.tensor(a, dtype=b.dtype)
            except Exception:
                return f"value {i}: expected a tensor, got {type(a).__name__}"
        if tuple(a.shape) != tuple(b.shape):
            return f"value {i}: expected shape {tuple(b.shape)}, got {tuple(a.shape)}"
        if not torch.allclose(a.detach().double(), b.detach().double(), rtol=RTOL, atol=ATOL):
            return f"value {i}: expected {show(b)}, got {show(a)}"
    return None


torch.manual_seed(0)
def case(n, d, eps=1e-5, scale=1.0):
    return (torch.randn(n, d) * scale, torch.randn(d), torch.randn(d), eps)

cases = [
    (torch.tensor([[1.0, 2.0, 3.0]]), torch.ones(3), torch.zeros(3), 1e-5),
    (torch.tensor([[2.0, 2.0], [0.0, 4.0]]), torch.tensor([2.0, 1.0]), torch.tensor([0.5, -0.5]), 1e-5),
    (torch.tensor([[5.0]]), torch.tensor([3.0]), torch.tensor([1.0]), 1e-5),
    (torch.full((2, 4), 7.0), torch.ones(4), torch.zeros(4), 1e-3),
    case(1, 8),
    case(4, 3, 0.1),
    case(6, 16, 1e-5, 100.0),
    case(32, 64, 1e-6, 0.01),
    case(4096, 512),
]

passed = 0
for n, args in enumerate(cases, 1):
    try:
        want = reference(*clone(args))
        got = attempt(*clone(args))
        err = compare(got, want)
        if err is None:
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input={show(list(args))}, {err}")
    except Exception as e:
        print(f"FAIL case {n}: input={show(list(args))}, got {type(e).__name__}: {e}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)
