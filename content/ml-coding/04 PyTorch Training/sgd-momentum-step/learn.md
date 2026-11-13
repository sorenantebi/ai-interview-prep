# Learn: SGD with Momentum Step

## The idea

- **Training** a neural network means nudging each weight a little in the direction that lowers the loss.
- This task asks you to write one such nudge by hand: the update that `torch.optim.SGD` runs inside every training loop.
- **Gradient** (`grad`): the direction (per weight) in which the loss rises fastest, so we move against it.
- **Learning rate** (`lr`): a small step-size number that scales how far each update moves.
- **Plain gradient descent** moves a weight by `lr · grad`.
- **Momentum**: gives the update a memory, like a ball rolling downhill that keeps some of its earlier speed.
  - If gradients keep pointing the same way, the speed builds up.
  - If they flip sign back and forth, they cancel out.
- **Velocity**: the running total of past gradients that carries the memory.
  - Each step, the old velocity is shrunk by the `momentum` factor (for example 0.9).
  - Then the new gradient is added.
- **Weight decay** (L2 regularisation): gently pulls every weight toward 0 so weights don't grow huge.
  - It works by adding `weight_decay · param` to the gradient before anything else.
- **Learning rate placement**: PyTorch stores the plain gradient sum in the velocity and applies `lr` only when moving the parameter.

## Work it by hand

Example 1: `param = [1.0, -2.0]`, `grad = [0.5, 0.5]`, `velocity = [0.0, 0.0]`, `lr = 0.1`, `momentum = 0.9`, `weight_decay = 0.0`. Every tensor has shape `(2,)`.

| Step | Calculation | Result |
|---|---|---|
| 1. Add decay to the gradient | `0.5 + 0.0 · 1.0`, `0.5 + 0.0 · (-2.0)` | `g = [0.5, 0.5]` |
| 2. New velocity | `0.9 · 0.0 + 0.5` for each entry | `[0.5, 0.5]` |
| 3. Scale by `lr` | `0.1 · [0.5, 0.5]` | `[0.05, 0.05]` |
| 4. Move the parameter | `1.0 - 0.05`, `-2.0 - 0.05` | `[0.95, -2.05]` |

- Result: `[[0.95, -2.05], [0.5, 0.5]]`, which is `[param_new, velocity_new]`.
- `lr` shows up only in step 3, so the stored velocity `[0.5, 0.5]` does not include it.

## Tools you'll need

### Tensor arithmetic (`+`, `-`, `*`)

- Operators on tensors of the same shape work element by element.
- A plain Python number (a scalar) is applied to every element.
- Each operation returns a **new** tensor and leaves the originals alone.

```python
import torch

a = torch.tensor([1.0, 2.0, 3.0])
b = torch.tensor([10.0, 20.0, 30.0])
print(a + 2 * b)  # tensor([21., 42., 63.])
print(a)          # tensor([1., 2., 3.])
```

### In-place operations (`add_`, `mul_`, `-=`): what to avoid

- Methods ending in `_` and operators like `-=` change the tensor itself.
- The problem says not to modify the inputs, so avoid these on `param`, `grad` and `velocity`.

```python
import torch

x = torch.tensor([1.0, 2.0])
y = x
y += 5          # changes x too, since y is the same tensor
print(x)        # tensor([6., 7.])
z = x + 5       # makes a new tensor
print(x, z)     # tensor([6., 7.]) tensor([11., 12.])
```

### Returning several tensors in a list

- The function returns a plain Python list holding two tensors.
- The order is `[param_new, velocity_new]`.

```python
import torch

p = torch.tensor([1.0])
q = torch.tensor([2.0])
out = [p * 3, q * 3]
print(out)           # [tensor([3.]), tensor([6.])]
print(out[1].shape)  # torch.Size([1])
```

### `torch.optim.SGD` (for checking your work)

- PyTorch's built-in optimizer uses this same formula.
- You don't need it in your solution, but it is handy for comparing results on made-up data.

```python
import torch

w = torch.nn.Parameter(torch.tensor([3.0]))
opt = torch.optim.SGD([w], lr=0.1, momentum=0.5)
(w ** 2).sum().backward()   # gradient is 2 * 3 = 6
opt.step()
print(w.data)  # tensor([2.4000])
```

## Common mistakes

- **Putting `lr` inside the velocity.** Some textbooks store `lr · g` in the velocity.
  - PyTorch stores the plain `g` and applies `lr` only on the parameter update.
- **Using the old velocity in the parameter update.** The parameter step must use the new velocity, not the one passed in.
- **Applying weight decay to the wrong thing.** Decay is added to the gradient, using the old `param`.
  - Don't subtract it from the parameter separately.
- **Modifying inputs in place.** `param -= ...` or `velocity.mul_(...)` changes the caller's tensors.
  - Use ordinary `+`, `-`, `*` so new tensors come back.
- **Returning the wrong order.** Return a list with the parameter first, then the velocity.

## Hints

### Hint 1
- Fold weight decay into the gradient.
- Build the new velocity from the old velocity and that adjusted gradient.
- Use the new velocity to move the parameter.
- Return both new tensors in a list.

### Hint 2
- Weight decay: scalar times `param`, added to `grad`. The shape stays the same.
- New velocity: scalar times the old velocity, plus the adjusted gradient. The shape stays the same.
- New parameter: `param` minus a scalar times the new velocity. The shape stays the same.
- No loops are needed; keep the adjusted gradient and new velocity in their own variables so you can reuse them.

### Hint 3
- Adjusted gradient = `grad` + `weight_decay` × current `param`.
- New velocity = `momentum` × old velocity + adjusted gradient.
- New param = old `param` − `lr` × new velocity.
- Check Example 2: adjusted gradient is `0.2 + 0.1 · 1.0 = 0.3`, new velocity is `0.9 · 1.0 + 0.3 = 1.2`, new param is `1.0 - 0.5 · 1.2 = 0.4`.
