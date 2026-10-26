import sys
import torch
import torch.nn.functional as F

ns = {}
exec(open("attempt.py").read(), ns)
attempt = ns["adam_step"]

RTOL, ATOL = 1e-4, 1e-5


def reference(param, grad, m, v, t, lr, beta1, beta2, eps):
    # Same formula in float64, then back to float32.
    p, g, m, v = (x.double() for x in (param, grad, m, v))
    m = beta1 * m + (1 - beta1) * g
    v = beta2 * v + (1 - beta2) * g * g
    step = lr * (m / (1 - beta1 ** t)) / ((v / (1 - beta2 ** t)).sqrt() + eps)
    return [(p - step).float(), m.float(), v.float()]


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
def case(shape, t, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
    return (torch.randn(*shape), torch.randn(*shape), torch.randn(*shape) * 0.1, torch.rand(*shape) * 0.01, t, lr, beta1, beta2, eps)

cases = [
    (torch.tensor([1.0, 2.0]), torch.tensor([0.1, -0.2]), torch.zeros(2), torch.zeros(2), 1, 0.001, 0.9, 0.999, 1e-8),
    (torch.tensor([0.5]), torch.tensor([1.0]), torch.tensor([0.2]), torch.tensor([0.05]), 10, 0.01, 0.9, 0.999, 1e-8),
    (torch.randn(4), torch.zeros(4), torch.zeros(4), torch.zeros(4), 1, 0.001, 0.9, 0.999, 1e-8),
    case((5,), 1),
    case((5,), 2),
    case((3, 4), 100, 0.01),
    case((3, 4), 1000000, 0.001, 0.8, 0.99, 1e-6),
    case((2, 2, 2), 7, 0.1, 0.0, 0.5, 1e-3),
    case((1000, 1000), 50),
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
