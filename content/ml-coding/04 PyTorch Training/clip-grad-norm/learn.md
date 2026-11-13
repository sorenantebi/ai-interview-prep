# Learn: Clip Gradient Norm

## The idea

- **Gradient**: a tensor, one per parameter, that says how to nudge that parameter to reduce the loss.
- The task: if all gradients together are "too big", shrink them all by the same factor. Otherwise leave them alone.
- **Exploding gradient**: a gradient that becomes huge, so one update can wreck the model.
- **Gradient clipping**: a safety belt against exploding gradients.
  - It shows up in training loops for RNNs and transformers, right before the optimizer step.
- Intuition: picture all numbers from all tensors as one long arrow.
  - Its length is the **total L2 norm**: square every element, add them all up, take the square root.
  - If the length is above `max_norm`, shrink the whole arrow to about that length.
  - One shared factor keeps the arrow's direction. It only gets shorter.
- That is why the norm covers all tensors at once, not one tensor at a time.
- **Scale factor** (`coef`): the limit divided by the current length.
  - A tiny number (`1e-6`) is added to the length so you never divide by zero.
  - If `coef < 1`, the gradient is too long, so scale. Otherwise leave it.
  - Clipping never makes gradients bigger.

## Work it by hand

Example 1: `grads = [[3.0, 4.0]]`, `max_norm = 1.0`.

| Step | Calculation | Result |
|---|---|---|
| 1. Square each entry | 3², 4² | 9, 16 |
| 2. Add them (over all tensors) | 9 + 16 | 25 |
| 3. Square root | √25 | total = 5 |
| 4. Ratio of limit to length | 1.0 / (5 + 0.000001) | about 0.19999996 |
| 5. Is the ratio below 1? | 0.19999996 < 1 | yes, so scale |
| 6. Multiply each entry | 3 × 0.2, 4 × 0.2 | 0.6, 0.8 |

- Output: `[[0.60000, 0.80000]]`.
- The `1e-6` is so small that the result still rounds to 0.6 and 0.8 at five decimals.
- Check with Example 3: `[[6.0], [8.0]]`, `max_norm = 5`.
  - Squares are 36 and 64. Across both tensors they add to 100, so the norm is 10.
  - The ratio is about 0.5, so the output is 3 and 4.
  - Clipping each tensor on its own would give different numbers.

## Tools you'll need

### `tensor ** 2` and `.sum()`

- `** 2` squares every element and keeps the shape.
- `.sum()` with no arguments adds all elements of any shape into one 0-dimensional tensor.

```python
import torch
t = torch.tensor([[1.0, 2.0], [3.0, 0.0]])
print((t ** 2).shape)   # torch.Size([2, 2])
print((t ** 2).sum())   # tensor(14.)
print(t.sum().shape)    # torch.Size([])
```

### Python's `sum()` over a generator

- Built-in `sum(iterable)` adds items one by one, starting from the integer 0.
  - It works with tensors, because `0 + tensor` is fine.
- A generator expression builds one value per list item.
- Tensors of different shapes are easy to add once each is reduced to a single number.

```python
import torch
parts = [torch.tensor([1.0, 2.0]), torch.tensor([[3.0], [4.0]])]
print(sum(p.sum() for p in parts))  # tensor(10.)
print(sum(len(p) for p in parts))   # 4
```

### `torch.sqrt(x)`

- Takes the square root element-wise.
- It needs a tensor, not a plain Python number. A tensor from `.sum()` is fine.

```python
import torch
x = torch.tensor(49.0)
print(torch.sqrt(x))  # tensor(7.)
```

### Comparing a tensor to a number

- `x < 1` on a 0-dimensional tensor gives a boolean tensor, and `if` turns it into a Python bool.
- Multiplying a tensor by a 0-dimensional tensor (or a number) scales every element and keeps the shape.

```python
import torch
r = torch.tensor(0.4)
if r < 1:
    print("shrink")  # shrink
print(r * torch.tensor([10.0, 20.0]))  # tensor([4., 8.])
```

### `tensor.clone()`

- Makes a copy with its own memory.
- Useful when you must return new tensors but changed nothing.

```python
import torch
a = torch.tensor([1.0, 2.0])
b = a.clone()
b[0] = 99.0
print(a)  # tensor([1., 2.])
print(b)  # tensor([99.,  2.])
```

### `torch.linalg.norm(t)` (an alternative)

- For a flat vector it returns the L2 norm. For a matrix it defaults to the Frobenius norm, which is the same thing over all elements.
- You can use it per tensor, but then you must combine the results correctly (see below).

```python
import torch
print(torch.linalg.norm(torch.tensor([3.0, 4.0])))  # tensor(5.)
print(torch.linalg.norm(torch.tensor([[1.0, 2.0], [2.0, 0.0]])))  # tensor(3.)
```

## Common mistakes

- **Clipping each tensor separately.** The norm must cover every element of every tensor at once.
  - Check with Example 3: the answer is 3 and 4, not 5 and 5.
- **Averaging per-tensor norms.** If you use per-tensor norms, square them, add, then take the square root.
  - Adding or averaging the norms themselves is wrong.
- **Forgetting the "otherwise" case.** When `coef` is 1 or more, return the gradients unchanged.
  - Never scale them up to reach `max_norm`.
- **Modifying inputs in place.** `g *= coef` or `g.mul_(coef)` changes the caller's tensors.
  - Use `g * coef`, and `clone()` for the unchanged case.
- **Skipping the small constant.** Without it, all-zero gradients (total norm 0) divide by zero.

## Hints

### Hint 1
- Find one number that measures the size of all gradients together.
- Turn that number into a scale factor using the limit.
- If the factor is below 1, scale every tensor by it. Otherwise return copies.
- Build new tensors rather than editing the old ones.

### Hint 2
- Square and sum each tensor with `.sum()`: one 0-dimensional value per tensor.
- Add those values across the list with `sum(...)`, then apply `torch.sqrt`: one 0-dimensional total norm.
- Build the ratio from it and test it against 1 with `if`.
- Build the output list with a list comprehension. Each output keeps the shape of its input.

### Hint 3
- The total norm is the square root of the sum of all squared elements, across all tensors.
- The scale factor is `max_norm` divided by (total norm + 0.000001).
- If the factor is less than 1, each output is the input tensor times the factor.
- If not, each output is an independent copy of the input tensor.
- Check yourself on Example 3: total 10, factor about 0.5, outputs 3 and 4.
