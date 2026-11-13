# Learn: MSE Loss

## The idea

- **Loss**: a single number saying how wrong a model's predictions are. Small is good, zero is perfect.
- **Mean squared error (MSE)**: for each element, measure how far the prediction is from the target, square that distance, then average everything.
- Squaring does two jobs:
  - It makes every miss positive, so over- and under-predictions can't cancel.
  - It punishes big misses much more than small ones (a miss of 2 costs 4, a miss of 0.5 costs 0.25).
- In plain maths: `mean((pred - target) ** 2)`.
- Every element counts once, so the **shape doesn't matter**: a vector of 3 and a 2x2 grid are handled the same way.
- **Scalar (0-dimensional tensor)**: a single number with shape `()`, which is what you return.
- Where it shows up:
  - In a training loop, the loss is computed after each forward pass, and the optimizer tries to push it down.
  - In an evaluation report, as a quick score for regression models (predicting numbers).
- **Element-wise**: an operation applied to each position separately, so the result keeps the same shape.

## Work it by hand

Example 1: `pred = [1.0, 2.0, 3.0]`, `target = [1.0, 2.0, 5.0]`.

| Step | Result | Shape |
|---|---|---|
| 1. Difference `pred - target` | `[0.0, 0.0, -2.0]` | `(3,)` |
| 2. Square each element | `[0.0, 0.0, 4.0]` | `(3,)` |
| 3. Add them up | `4.0` | `()` |
| 4. Divide by the element count (3) | `4 / 3 = 1.33333` | `()` |

- Only the last element is wrong, by 2.
- The difference is `-2.0`, but its square is `+4.0`, so the sign disappears.
- Spread over 3 elements, the loss is `1.33333`, matching the expected output.

## Tools you'll need

### `a - b` (element-wise subtraction)

- Subtracts matching positions of two tensors with the same shape.
- The result has the same shape as the inputs.

```python
import torch

a = torch.tensor([[5.0, 1.0], [2.0, 8.0]])
b = torch.tensor([[1.0, 1.0], [4.0, 3.0]])
print(a - b)
# tensor([[ 4.,  0.],
#         [-2.,  5.]])
print((a - b).shape)  # torch.Size([2, 2])
```

### `x ** 2` (squaring)

- Raises every element to a power; the shape stays the same.
- Equivalent forms: `x.pow(2)` and `torch.square(x)`.

```python
import torch

x = torch.tensor([-3.0, 0.5, 4.0])
print(x ** 2)  # tensor([ 9.0000,  0.2500, 16.0000])
print(torch.square(x))  # tensor([ 9.0000,  0.2500, 16.0000])
```

### `.mean()`

- With no arguments, it averages over all elements, however many dimensions there are, and returns a 0-dimensional tensor.
- With `dim=...`, it averages only along that axis, which would leave a vector. Not what you want here.

```python
import torch

m = torch.tensor([[1.0, 2.0], [3.0, 10.0]])
print(m.mean())  # tensor(4.)
print(m.mean().shape)  # torch.Size([])
print(m.mean(dim=0))  # tensor([2., 6.])
```

### `.sum()` and `.numel()`

- `.sum()` adds all elements; `.numel()` gives the element count.
- Together they are what `.mean()` does under the hood.

```python
import torch

t = torch.tensor([[2.0, 4.0, 6.0], [8.0, 10.0, 12.0]])
print(t.sum())  # tensor(42.)
print(t.numel())  # 6
print(t.sum() / t.numel())  # tensor(7.)
```

## Common mistakes

- **Averaging along one axis.** `.mean(dim=0)` or `.mean(dim=1)` returns a vector, not a scalar. Call `.mean()` with no arguments.
- **Forgetting to square.** Without squaring, positive and negative errors cancel and the average can be 0 for bad predictions.
- **Using `abs` instead of squaring.** That is a different loss (MAE) and gives different numbers on Example 2.
- **Dividing by the wrong count.** The divisor is the total number of elements, not the size of the first dimension. For a 2x2 tensor that is 4, not 2.
- **Using the banned helpers.** `F.mse_loss` and `nn.MSELoss` are not allowed, so build the loss from basic tensor operations.

## Hints

### Hint 1
- Find how far each prediction is from its target, element by element.
- Make those distances non-negative by squaring them.
- Collapse everything into one number by averaging.

### Hint 2
- Subtract the two tensors: the result has the same shape as the inputs.
- Square with `**`: the shape is unchanged.
- Call `.mean()` with no `dim` argument: the shape becomes `()`.

### Hint 3
- For every element, take `pred - target` and multiply it by itself.
- Add up all those squares across all dimensions, then divide by the total number of elements. `.mean()` does both of these at once.
- Check against Example 2: the squared differences are 0.25, 0, 1, 1, which add to 2.25, and 2.25 / 4 = 0.5625.
