import sys
import torch
import torch.nn.functional as F

ns = {}
exec(open("attempt.py").read(), ns)
attempt = ns["dropout"]

RTOL, ATOL = 1e-4, 1e-5


def reference(x, mask, p):
    return torch.where(mask.bool(), x / (1 - p), torch.zeros_like(x))


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
def case(shape, p):
    return (torch.randn(*shape), (torch.rand(*shape) >= p).float(), p)

cases = [
    (torch.tensor([1.0, 2.0, 3.0, 4.0]), torch.tensor([1.0, 0.0, 1.0, 0.0]), 0.5),
    (torch.tensor([[1.0, -2.0], [0.5, 4.0]]), torch.tensor([[1.0, 1.0], [0.0, 1.0]]), 0.2),
    (torch.randn(5), torch.ones(5), 0.0),
    (torch.randn(5), torch.zeros(5), 0.3),
    (torch.randn(3, 3), torch.ones(3, 3), 0.9),
    case((8,), 0.5),
    case((4, 6), 0.1),
    case((2, 3, 4), 0.75),
    case((512, 512), 0.3),
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
