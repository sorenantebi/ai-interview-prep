import sys
import torch
import torch.nn.functional as F

ns = {}
exec(open("attempt.py").read(), ns)
attempt = ns["mlp_backward"]

RTOL, ATOL = 1e-4, 1e-5


def reference(x, y, W1, b1, W2, b2):
    params = [p.clone().requires_grad_(True) for p in (W1, b1, W2, b2)]
    W1, b1, W2, b2 = params
    out = torch.relu(x @ W1.T + b1) @ W2.T + b2
    ((out - y) ** 2).mean().backward()
    return [p.grad for p in params]


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
def case(n, d, h, k):
    return (torch.randn(n, d), torch.randn(n, k), torch.randn(h, d), torch.randn(h), torch.randn(k, h), torch.randn(k))

cases = [
    (torch.tensor([[1.0, -1.0]]), torch.tensor([[0.0]]), torch.eye(2), torch.zeros(2), torch.tensor([[1.0, 1.0]]), torch.zeros(1)),
    (torch.tensor([[1.0, 2.0], [0.5, -1.0]]), torch.tensor([[1.0], [0.0]]), torch.tensor([[0.5, -0.5], [1.0, 1.0]]),
     torch.tensor([0.1, -0.2]), torch.tensor([[1.0, -1.0]]), torch.tensor([0.5])),
    (torch.randn(3, 2), torch.randn(3, 1), torch.randn(4, 2), torch.full((4,), -100.0), torch.randn(1, 4), torch.randn(1)),
    case(1, 1, 1, 1),
    case(2, 3, 4, 2),
    case(8, 5, 16, 3),
    case(32, 10, 64, 10),
    case(1000, 64, 256, 32),
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
