# Learn: Adam Step

## The idea

- **The task:** compute one Adam update by hand: new parameter, new `m`, new `v`.
- **Where it shows up:** it is the default optimiser in most training loops. `torch.optim.Adam(...).step()` does exactly this for every parameter.
- **Gradient descent** moves each parameter by `lr · grad` against the gradient to lower the loss.
- Adam improves on this in two ways:
  - It smooths the gradient over time.
  - It gives each parameter its own step size.
- **Exponential moving average (EMA):** with decay `beta`, keep `beta` of the old value and mix in `1 - beta` of the new one.
- **First moment `m`:** an EMA of the gradient.
  - It acts like momentum: noisy gradients cancel, steady ones add up.
- **Second moment `v`:** an EMA of the squared gradient.
  - It measures how large the gradients typically are.
- **Optimiser state:** `m` and `v`, kept per parameter between steps.
- **Per-parameter step size:** the step is roughly `m / sqrt(v)`.
  - Big or noisy gradients make `sqrt(v)` large, so the step shrinks.
  - Small, steady gradients keep the step near `lr`.
- **Bias correction:** `m` and `v` start at 0, so early values are too small.
  - Dividing by `1 - beta^t` undoes this.
  - At `t = 1` it divides by `1 - beta`, which exactly cancels the shrinkage.
  - As `t` grows, `beta^t` goes to 0 and the correction fades away.
- **`eps`:** a tiny number added so you never divide by zero.

## Work it by hand

Example 1: `param = [1.0, 2.0]`, `grad = [0.1, -0.2]`, `m = v = [0, 0]`, `t = 1`, `lr = 0.001`, `beta1 = 0.9`, `beta2 = 0.999`. Every tensor has shape `(2,)` and every step is element by element.

| Step | Element 0 | Element 1 |
|---|---|---|
| `m_new = 0.9·0 + 0.1·grad` | 0.01 | -0.02 |
| `grad²` | 0.01 | 0.04 |
| `v_new = 0.999·0 + 0.001·grad²` | 0.00001 | 0.00004 |
| `1 - beta1^1 = 0.1`, so `m_hat = m_new / 0.1` | 0.1 | -0.2 |
| `1 - beta2^1 = 0.001`, so `v_hat = v_new / 0.001` | 0.01 | 0.04 |
| `sqrt(v_hat)` | 0.1 | 0.2 |
| `m_hat / (sqrt(v_hat) + eps)` | ≈ 1 | ≈ -1 |
| `lr ·` that | 0.001 | -0.001 |
| `param_new = param - ...` | 0.999 | 2.001 |

- **Result:** `[[0.999, 2.001], [0.01, -0.02], [0.00001, 0.00004]]`.
- On step 1, `m_hat = grad` and `sqrt(v_hat) = |grad|`.
  - So each parameter moves by about `lr` against its gradient's sign, whatever the gradient's size.
- The returned `m` and `v` are the uncorrected ones.
  - The corrected values are used only for the step.

## Tools you'll need

### Element-wise tensor arithmetic
- `+`, `-`, `*`, `/` and `**` work element by element between tensors of the same shape.
- A plain float is applied to every element.

```python
import torch

x = torch.tensor([1.0, -2.0, 3.0])
print(0.5 * x + 1)  # tensor([1.5000, 0.0000, 2.5000])
print(x ** 2)       # tensor([1., 4., 9.])
print(x / (x ** 2 + 1e-8))  # tensor([ 1.0000, -0.5000,  0.3333])
```

### Python scalar powers
- `t` is a plain int and `beta` a plain float, so `beta ** t` is ordinary Python maths.
- The result is a float, not a tensor.

```python
print(1 - 0.5 ** 3)  # 0.875
print(type(0.5 ** 3).__name__)  # float
```

### torch.sqrt(tensor)
- Element-wise square root.
- Returns a new tensor of the same shape.

```python
import torch

a = torch.tensor([4.0, 9.0, 0.25])
print(torch.sqrt(a))  # tensor([2.0000, 3.0000, 0.5000])
print(torch.sqrt(a).shape)  # torch.Size([3])
```

### Out-of-place vs in-place operations
- `w - 0.5` builds a new tensor and leaves `w` alone.
- Methods ending in `_` (like `sub_`) change the tensor itself.
- The problem forbids modifying inputs, so use the plain operators.

```python
import torch

w = torch.tensor([1.0, 2.0])
w2 = w - 0.5
print(w)   # tensor([1., 2.])
print(w2)  # tensor([0.5000, 1.5000])
w.sub_(0.5)
print(w)   # tensor([0.5000, 1.5000])
```

### torch.no_grad()
- If an input has `requires_grad=True`, arithmetic on it is tracked and results carry a graph.
- An optimiser step should not be tracked.
- Inside `with torch.no_grad():` results are plain tensors; `.detach()` does the same for one tensor.

```python
import torch

p = torch.tensor([1.0, 2.0], requires_grad=True)
print((p * 2).requires_grad)  # True
with torch.no_grad():
    print((p * 2).requires_grad)  # False
print((p * 2).detach().requires_grad)  # False
```

## Common mistakes

- **Modifying inputs in place.** `m *= beta1` or `param -= ...` changes the caller's tensors.
  - Build new tensors, e.g. `m_new = beta1 * m + ...`.
- **Returning the corrected moments.** `m_hat` and `v_hat` are only for the step.
  - Return the uncorrected `m_new` and `v_new`, or the next step's state is wrong.
- **Misplacing `eps`.** It goes after the square root: `sqrt(v_hat) + eps`, not `sqrt(v_hat + eps)`.
- **Misusing `t`.** `t` starts at 1, and the factor is `beta1 ** t`, not `beta1 * t`.
- **Leaking the graph.** If `param` or `grad` track gradients, the results would too.
  - Compute inside `torch.no_grad()` or call `.detach()`.

## Hints

### Hint 1
- Update the two running averages from the old `m`, `v` and the gradient.
- Correct both for bias using `t`.
- Compute the per-element step and subtract it from the parameter.
- Return the new parameter and the two uncorrected averages in a list.

### Hint 2
- Everything is element-wise arithmetic, so every intermediate has the same shape as `param`.
- The only function you need is `torch.sqrt`.
- The bias factors `1 - beta1 ** t` and `1 - beta2 ** t` are single floats.

### Hint 3
- `m_new` is `beta1` times the old `m`, plus `(1 - beta1)` times the gradient.
- `v_new` is the same with `beta2` and the squared gradient.
- Divide `m_new` by `1 - beta1^t` and `v_new` by `1 - beta2^t` to get `m_hat` and `v_hat`.
- The step is `lr` times `m_hat`, divided by (the square root of `v_hat`, plus `eps`).
- Subtract that from `param`, then return `[param_new, m_new, v_new]`.
