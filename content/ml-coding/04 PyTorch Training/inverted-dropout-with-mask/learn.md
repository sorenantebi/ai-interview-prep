# Learn: Inverted Dropout with a Mask

## The idea

- **Task:** zero out some activations using a ready-made mask, then scale the survivors up so the average signal stays the same.
- **Dropout:** during training, randomly switch off some activations to stop the network leaning on any single one. This helps it generalize.
- **Activation:** a number a layer passes on to the next layer.
- **Where it shows up:** inside the forward pass of almost every deep network's training loop.
- **Side effect of dropping:** the layer's output gets smaller on average.
  - Drop half the values and the total signal is about half as big.
  - At inference nothing is dropped, so the signal would suddenly be bigger than in training.
- **Inverted dropout:** fixes this during training by scaling the survivors by `1 / (1 - p)`.
  - Then each activation has the same average value in training and at inference.
- **`p`:** the drop probability. The keep probability is `1 - p`.
- **Mask:** a tensor shaped like `x`, with `1.0` where a value is kept and `0.0` where it is dropped.
  - Here the mask is given, so there is no randomness.

## Work it by hand

Example 1: `x = [1.0, 2.0, 3.0, 4.0]`, `mask = [1.0, 0.0, 1.0, 0.0]`, `p = 0.5`.

1. Apply the mask position by position. The shape stays `(4,)`.

| position | x | mask | x * mask |
|---|---|---|---|
| 0 | 1.0 | 1.0 | 1.0 |
| 1 | 2.0 | 0.0 | 0.0 |
| 2 | 3.0 | 1.0 | 3.0 |
| 3 | 4.0 | 0.0 | 0.0 |

2. Result of step 1: `[1.0, 0.0, 3.0, 0.0]`.
3. Compute the keep probability: `1 - 0.5 = 0.5`.
4. Compute the scale factor: `1 / 0.5 = 2`.
5. Scale every value: `[2.0, 0.0, 6.0, 0.0]`.
6. This matches the expected output `[2.00000, 0.00000, 6.00000, 0.00000]`.
   - Dropped positions stay zero because zero times anything is zero.

## Tools you'll need

### Element-wise multiplication `a * b`

- On tensors of the same shape, `*` multiplies matching positions. It is not a matrix product.
- It returns a new tensor and leaves the inputs unchanged.

```python
import torch

a = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
b = torch.tensor([[0.0, 1.0], [1.0, 0.0]])
print(a * b)  # tensor([[0., 2.], [3., 0.]])
print((a * b).shape)  # torch.Size([2, 2])
```

### Dividing a tensor by a Python number

- `t / c` divides every element by `c` and gives a float tensor.
- Parentheses let you compute the divisor first, like `t / (1 - q)`.

```python
import torch

t = torch.tensor([3.0, 6.0, 9.0])
print(t / 3)  # tensor([1., 2., 3.])
print(t / (1 - 0.25))  # tensor([ 4.,  8., 12.])
```

### Out-of-place vs in-place

- `a * b` creates a new tensor.
- In-place versions like `a.mul_(b)` or `a *= b` overwrite `a`.
- The problem says not to modify `x`, so use the out-of-place form.

```python
import torch

a = torch.tensor([1.0, 2.0])
b = a * 2
print(a)  # tensor([1., 2.])
a.mul_(2)
print(a)  # tensor([2., 4.])
```

## Common mistakes

- **Dividing by `p` instead of `1 - p`.**
  - With `p = 0.5` both give the same answer, so check against Example 2 (`p = 0.2`, scale `1.25`).
- **Modifying `x` in place.**
  - `x *= mask` or `x.mul_(mask)` changes the caller's tensor. Use `x * mask` instead.
- **Using a matrix product.**
  - `torch.matmul` or `@` is wrong here. You need element-wise `*`.
- **Forgetting to scale.**
  - Without it, Example 1 gives `[1, 0, 3, 0]`, which is wrong.
- **Casting to integers by accident.**
  - Keep tensors as floats. The inputs already are, so don't cast them.

## Hints

### Hint 1
- First, zero out the dropped activations using the mask.
- Then scale everything up to make up for the dropped ones, using the keep probability.

### Hint 2
- Step 1: element-wise multiplication of `x` and `mask`. The shape stays the same as `x`.
- Step 2: divide that tensor by a single Python number. The shape still stays the same.
- Neither step needs a loop.

### Hint 3
- The keep probability is `1 - p`.
- Each output value is `x` at that position, times the mask at that position, divided by `1 - p`.
- Check with Example 2: `-2.0 * 1.0 / 0.8 = -2.5`, and the position with mask `0.0` gives `0.0`.
