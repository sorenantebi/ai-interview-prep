# Learn: Gradient with Autograd

## The idea

- **Gradient**: a list of slopes, one per element of `x`. Entry `i` answers "if I nudge `x[i]` up a tiny bit, how much does `f` change?"
- The gradient always has the same shape as `x`.
- **Autograd**: PyTorch's automatic differentiation. It records each operation while you compute `f`, then replays the record backwards with the chain rule.
- You never write a derivative by hand.
- In ML this is what `loss.backward()` does in every training loop. The loss is a scalar, and the gradient says how to change each weight.
- **Scalar**: a single number, a 0-dimensional tensor. Autograd can only start from a scalar.
- **requires_grad**: a flag on a tensor. PyTorch only records operations on tensors that have it switched on.
- **Leaf tensor**: a tensor you created directly, not the result of an operation. Gradients are asked for with respect to leaves.
- The catch here: `x` doesn't track gradients and you must not change it, so you need a separate copy that does.

## Work it by hand

Take `x = [1.0, 2.0]`. Entry `i` of the gradient is `2·x_i·sin(x_i) + x_i²·cos(x_i) + 2·S`, where `S` is the sum of all of `x`.

- The first two terms come from `x_i² · sin(x_i)` (product rule).
- The last term comes from `(Σx)²`. Every element feeds into the total, so every entry gets `2·S`.

1. Sum: `S = 1 + 2 = 3`, so `2·S = 6`.
2. Entry 0 (`x = 1`):
   - `2·1·sin(1) = 2 · 0.84147 = 1.68294`
   - `1²·cos(1) = 0.54030`
   - Total: `1.68294 + 0.54030 + 6 = 8.22324`
3. Entry 1 (`x = 2`):
   - `2·2·sin(2) = 4 · 0.90930 = 3.63719`
   - `2²·cos(2) = 4 · (−0.41615) = −1.66459`
   - Total: `3.63719 − 1.66459 + 6 = 7.97260`
4. Result: `[8.22324, 7.97260]`, shape `(2,)` like `x`. This matches the expected output.

| i | x_i | 2·x·sin(x) | x²·cos(x) | 2S | total |
|---|-----|-----------|-----------|----|-------|
| 0 | 1.0 | 1.68294 | 0.54030 | 6 | 8.22324 |
| 1 | 2.0 | 3.63719 | −1.66459 | 6 | 7.97260 |

- Autograd reaches the same numbers by working backwards from `f` and multiplying local slopes.

## Tools you'll need

### x.clone(), x.detach(), x.requires_grad_(True)

- `clone()` makes an independent copy, so changing the copy never touches the original.
- `detach()` returns a tensor cut loose from any gradient history.
- `requires_grad_(True)` switches tracking on in place and returns the tensor. The trailing underscore means "in place".

```python
import torch

a = torch.tensor([5.0, 6.0, 7.0])
c = a.clone()
c.requires_grad_(True)
print(a.requires_grad, c.requires_grad, c.is_leaf)  # False True True
y = c * 2
print(y.requires_grad, y.detach().requires_grad)  # True False
```

### Tensor math: `**`, `torch.sin`, `.sum()`

- These work element by element and keep the shape.
- `.sum()` with no arguments collapses everything to a scalar, whatever the shape.
- Order matters: `(t**2).sum()` squares each element and then adds. `t.sum()**2` adds and then squares the total.

```python
import torch

t = torch.tensor([[0.0, 1.0], [2.0, 3.0]])
print((t ** 2).sum())  # tensor(14.)
print(t.sum() ** 2)  # tensor(36.)
print(t.sum().shape)  # torch.Size([])
print(torch.cos(torch.zeros(2)))  # tensor([1., 1.])
```

### torch.autograd.grad(outputs, inputs)

- It returns the gradient of the scalar `outputs` with respect to `inputs`.
- The result is always a **tuple**, one gradient per input, so pick out the element you need.
- The gradient has the same shape as the input and does not require grad itself.

```python
import torch

x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
y = (x ** 3).sum()
grads = torch.autograd.grad(y, x)
print(type(grads))  # <class 'tuple'>
print(grads[0])  # tensor([ 3., 12., 27.])
```

### y.backward() and x.grad

- This is the alternative route: `backward()` fills in `.grad` on every leaf that tracks gradients.
- Calling it again adds to `.grad` instead of replacing it.
- Since `.grad` lives on the tracked copy, check what you return.

```python
import torch

w = torch.tensor([1.0, -2.0], requires_grad=True)
(w ** 2).sum().backward()
print(w.grad)  # tensor([ 2., -4.])
(w ** 2).sum().backward()
print(w.grad)  # tensor([ 4., -8.])
print(w.grad.requires_grad)  # False
```

## Common mistakes

- **Using the original `x` for the gradient.**
  - It was never recorded, so PyTorch raises an error.
  - Make a tracking copy and build `f` from that copy.
- **Modifying the input.**
  - Calling `x.requires_grad_(True)` directly on the argument changes the caller's tensor.
  - Always copy first.
- **Mixing up tensors.**
  - The tensor used in the formula must be the same one you pass to `grad`.
  - A different copy has no link to `f`.
- **Squaring in the wrong place.**
  - The second term is the sum squared, not the sum of squares.
  - `f` must also end as a scalar, or autograd complains.
- **Returning the tuple, or a tracked tensor.**
  - `autograd.grad` returns a tuple, so return the tensor inside it.
  - With `backward()`, make sure what you return doesn't still require grad.

## Hints

### Hint 1
- Make a private copy of the input that tracks gradients.
- Compute `f` from that copy, so it becomes a single number.
- Ask autograd for the gradient of that number with respect to the copy.
- Return the gradient tensor.

### Hint 2
- Copy with `detach()`, `clone()` and `requires_grad_(True)`. The shape stays the same as `x`.
- Build `f` from `**`, `torch.sin` and `.sum()`. The shape becomes a scalar.
- `torch.autograd.grad(f, copy)` returns a tuple holding one tensor shaped like `x`.

### Hint 3
- `f` is two scalars added together.
- The first one: square every element, multiply by the sine of the same element, then sum over everything.
- The second one: sum all the elements first, then square that total.
- Use the tracking copy everywhere `x` appears in the formula.
- The gradient call gives a tuple, so take its first item. That is your answer.
