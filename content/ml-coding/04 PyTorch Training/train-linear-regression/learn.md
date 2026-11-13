# Learn: Train Linear Regression

## The idea

- The task: start with a straight-line model and nudge its numbers a little, over and over, until its predictions match the data better.
- It shows up as the training loop at the heart of nearly all PyTorch models. Bigger networks use the same loop with more parameters.
- **Linear model**: `pred = X @ w + b`, where each row of `X` is multiplied by the weights `w` and shifted by the bias `b`.
- **Residual**: `pred - y`, how far each prediction is from its target.
- **Mean squared error (MSE)**: square each residual, then average. A small loss means a good fit.
- **Gradient**: for each parameter, how much the loss grows if you nudge that parameter up.
  - To lower the loss, move each parameter a little in the opposite direction.
- **Learning rate** (`lr`): how big that nudge is.
- **Full-batch**: every step uses all rows of `X`, not a random subset.
- **Autograd**: PyTorch's gradient calculator.
  - It records operations on tensors marked `requires_grad=True`.
  - `loss.backward()` then fills each tensor's `.grad`.
- By hand, the gradients are `(2/n) · Xᵀ r` for `w` and `(2/n) · sum(r)` for `b`, where `r` is the residual vector.

## Work it by hand

Example 1: `X = [1, 2, 3]`, `y = [2, 4, 6]`, `w = 0`, `b = 0`, `lr = 0.1`, one step.

| Step | Value |
|---|---|
| Predictions `X*w + b` | `[0, 0, 0]` |
| Residuals `r = pred - y` | `[-2, -4, -6]` |
| Loss (mean of `r²`) | `(4+16+36)/3 = 18.667` |
| `∂L/∂w = (2/n) · Σ x·r` | `(2/3)(-2 - 8 - 18) = (2/3)(-28) = -18.667` |
| `∂L/∂b = (2/n) · Σ r` | `(2/3)(-12) = -8` |
| New `w = w - lr · grad` | `0 - 0.1·(-18.667) = 1.86667` |
| New `b = b - lr · grad` | `0 - 0.1·(-8) = 0.8` |

- Result: `[[1.86667], 0.8]`, matching the expected output.
- Example 3 has `steps = 0`, so the loop never runs and you return the starting values unchanged.

## Tools you'll need

### `requires_grad=True`
- Marks a tensor so autograd tracks operations on it.
- Only floating-point tensors can do this.

```python
import torch
w = torch.tensor([3.0], requires_grad=True)
loss = ((2 * w - 4) ** 2).sum()
loss.backward()
print(w.grad)  # tensor([8.])
```

### `loss.backward()` and `.grad`
- `backward()` needs a single number (a 0-dim tensor), so reduce with `.mean()` or `.sum()` first.
- It **adds** into `.grad`; it does not overwrite.

```python
import torch
w = torch.tensor(1.0, requires_grad=True)
(w * 3).backward()
print(w.grad)  # tensor(3.)
(w * 3).backward()
print(w.grad)  # tensor(6.)
```

### `torch.optim.SGD` and `opt.zero_grad()`
- `SGD([params], lr=...)` holds your parameters.
- `opt.step()` applies `p ← p - lr · p.grad`.
- Call `opt.zero_grad()` every iteration, or gradients pile up as shown above.

```python
import torch
p = torch.tensor([5.0], requires_grad=True)
opt = torch.optim.SGD([p], lr=0.5)
(p ** 2).sum().backward()
opt.step()
print(p)  # tensor([0.], requires_grad=True)
opt.zero_grad()
```

### `torch.no_grad()`
- Inside this block, operations are not recorded by autograd.
- It is needed if you update a parameter by hand instead of using an optimizer.
- Use in-place updates like `-=` so the tensor stays the same object.

```python
import torch
w = torch.tensor([1.0], requires_grad=True)
(w * 2).sum().backward()
with torch.no_grad():
    w -= 0.1 * w.grad
print(w)  # tensor([0.8000], requires_grad=True)
```

### `@`, broadcasting and `.mean()`
- `(n, d) @ (d,)` gives shape `(n,)`.
- Adding a scalar or 0-dim tensor adds it to every element.
- `.mean()` collapses a tensor to one number.

```python
import torch
A = torch.ones(4, 3)
v = torch.tensor([1.0, 2.0, 3.0])
print((A @ v + 1.0).shape)  # torch.Size([4])
t = torch.tensor([1.0, 3.0, 5.0])
print(((t - 2) ** 2).mean())  # tensor(3.6667)
```

### `.detach().clone()`
- `clone()` makes an independent copy, so editing it won't touch the original.
- `detach()` cuts the link to autograd.
- Use both to copy an input and to return a plain result.

```python
import torch
a = torch.tensor([1.0, 2.0], requires_grad=True)
c = a.detach().clone()
c[0] = 9.0
print(a)  # tensor([1., 2.], requires_grad=True)
print(c)  # tensor([9., 2.])
```

### `torch.tensor(x)` for a scalar
- Wrapping a Python float gives a 0-dimensional tensor, which is the shape the answer needs for `b`.

```python
import torch
s = torch.tensor(2.5)
print(s.shape)  # torch.Size([])
print(s.ndim)  # 0
```

## Common mistakes

- **Forgetting to zero gradients.**
  - Gradients accumulate across `backward()` calls, so each step would use old plus new gradients.
  - Zero them every iteration.
- **Modifying the input `w`.**
  - Updating `w` in place changes the caller's tensor.
  - Copy it first with `detach().clone()`.
- **Updating a tracked tensor by hand without `torch.no_grad()`.**
  - A plain `w = w - lr * w.grad` builds a new non-leaf tensor and breaks training.
  - Use `SGD`, or update in place inside `with torch.no_grad():`.
- **Returning tensors that still track gradients.**
  - Return `detach()`ed values.
- **Making `b` the wrong kind of object.**
  - A plain float can't be optimized. It must be a tensor with `requires_grad=True`, and it should stay 0-dimensional, not shape `(1,)`.
- **Using `sum` instead of `mean`.**
  - The loss is a mean, so the gradient carries the factor `2/n`.
  - A sum makes steps `n` times too big.

## Hints

### Hint 1
- Make your own copy of `w`, and turn `b` into a tensor. Both must be tracked by autograd.
- Repeat `steps` times:
  - clear old gradients;
  - compute the loss on all the data;
  - get the gradients;
  - update the parameters.
- At the end, return the values without gradient tracking.

### Hint 2
- Copy `w` with `.detach().clone()` and then switch tracking on with `.requires_grad_(True)`.
- Build `b` with `torch.tensor(...)` and `requires_grad=True`.
- Create `torch.optim.SGD([w, b], lr=lr)`.
- In the loop, call `zero_grad()`.
- Compute the residuals from `X @ w + b - y`, shape `(n,)`.
- Reduce them with `.mean()` to a 0-dim loss, then call `backward()` and `step()`.
- Return both parameters after `detach()`.

### Hint 3
- The loss is: take the residuals `X @ w + b - y`, square each one, and average them.
- `backward()` fills `w.grad` and `b.grad` with the derivatives.
- `step()` subtracts `lr` times each gradient from its parameter.
- To check by hand: `∂L/∂w = (2/n) · Xᵀ r` and `∂L/∂b = (2/n) · sum(r)`.
- With zero steps the loop body never runs, so you return the copies of the starting values.
