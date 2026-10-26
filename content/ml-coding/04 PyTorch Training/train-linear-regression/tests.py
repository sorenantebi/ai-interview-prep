import sys
import torch
import torch.nn.functional as F

ns = {}
exec(open("attempt.py").read(), ns)
attempt = ns["train_linear_regression"]

RTOL, ATOL = 1e-4, 1e-4


def reference(X, y, w, b, lr, steps):
    # Closed-form gradients, no autograd.
    w, b, n = w.clone(), torch.tensor(float(b)), X.shape[0]
    for _ in range(steps):
        r = X @ w + b - y
        w, b = w - lr * (2 / n) * (X.T @ r), b - lr * (2 / n) * r.sum()
    return [w, b]


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
def case(n, d, lr, steps):
    X = torch.randn(n, d)
    return (X, X @ torch.randn(d) + 0.5 + 0.1 * torch.randn(n), torch.zeros(d), 0.0, lr, steps)

X1 = torch.tensor([[1.0], [2.0], [3.0]])
y1 = torch.tensor([2.0, 4.0, 6.0])
cases = [
    (X1, y1, torch.zeros(1), 0.0, 0.1, 1),
    (X1, y1, torch.zeros(1), 0.0, 0.05, 200),
    (torch.tensor([[1.0, 2.0]]), torch.tensor([1.0]), torch.tensor([0.5, 0.5]), 1.0, 0.1, 0),
    (X1, y1, torch.tensor([3.0]), -1.0, 0.01, 5),
    case(1, 1, 0.1, 10),
    case(10, 3, 0.05, 50),
    case(50, 5, 0.05, 200),
    case(200, 2, 0.1, 100),
    case(1000, 20, 0.05, 300),
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
