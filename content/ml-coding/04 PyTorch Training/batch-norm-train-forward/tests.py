import sys
import torch
import torch.nn.functional as F

ns = {}
exec(open("attempt.py").read(), ns)
attempt = ns["batch_norm_train"]

RTOL, ATOL = 1e-4, 1e-4


def reference(x, gamma, beta, running_mean, running_var, momentum, eps):
    rm, rv = running_mean.clone(), running_var.clone()
    y = F.batch_norm(x, rm, rv, gamma, beta, training=True, momentum=momentum, eps=eps)
    return [y, rm, rv]


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
def case(n, d, momentum=0.1, eps=1e-5, scale=1.0):
    return (torch.randn(n, d) * scale, torch.randn(d), torch.randn(d), torch.randn(d), torch.rand(d) + 0.5, momentum, eps)

cases = [
    (torch.tensor([[1.0, 2.0], [3.0, 6.0]]), torch.ones(2), torch.zeros(2), torch.zeros(2), torch.ones(2), 0.1, 1e-5),
    (torch.tensor([[0.0], [0.0], [3.0]]), torch.tensor([2.0]), torch.tensor([1.0]), torch.tensor([1.0]), torch.tensor([0.5]), 0.5, 1e-5),
    (torch.full((4, 3), 2.0), torch.ones(3), torch.zeros(3), torch.zeros(3), torch.ones(3), 0.1, 1e-3),
    case(2, 1),
    case(5, 4, 0.0),
    case(5, 4, 1.0),
    case(16, 8, 0.3, 1e-4, 50.0),
    case(64, 32),
    case(4096, 256),
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
