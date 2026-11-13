# Learn: MLP Manual Backward

## The idea

- **Task:** compute, by hand, how much the loss changes when each of the four parameters (`W1`, `b1`, `W2`, `b2`) changes a tiny bit.
- You return four tensors, each with exactly the shape of its parameter.
- **Where it shows up:** inside every training loop. `loss.backward()` does exactly this work, and an optimizer then uses the results to update the weights.
- **Gradient:** for one parameter, the rate at which the loss `L` changes when that parameter changes.
  - A positive gradient means "lower this parameter to lower the loss".
- **Chain rule:** if `L` depends on `out`, and `out` depends on `W`, then the effect of `W` on `L` is the product of the two effects.
- **Backpropagation:** apply the chain rule one step at a time, starting at the loss and walking backward.
  - At each step you receive a gradient from the step after it and turn it into gradients for that step's inputs.
- **Forward pass first:** the backward pass reuses values from the forward pass, so compute and keep them.
- **MSE** (mean squared error): the mean of `(out - y)²` over all `n·k` elements.
  - Its derivative for each output element is `2 · (out - y) / (n·k)`.
- **ReLU:** `relu(z) = max(z, 0)`.
  - Its derivative is 1 where `z > 0` and 0 elsewhere, so it lets gradient through only for "active" units.
- **Linear layer rules:** for `out = a @ W.T + b`, with incoming gradient `g` of shape `(n, outputs)`:
  - Weights: `g.T @ a` (same shape as `W`).
  - Bias: sum of `g` over the batch rows.
  - Input (passed further back): `g @ W`.

## Work it by hand

Example 1: `x = [[1, -1]]`, `y = [[0]]`, `W1 = [[1,0],[0,1]]`, `b1 = [0,0]`, `W2 = [[1,1]]`, `b2 = [0]`. Sizes: `n=1, d=2, h=2, k=1`.

1. **Forward, layer 1:** `z1 = x @ W1.T + b1 = [[1, -1]]`, shape `(1, 2)`.
2. **ReLU:** `a1 = [[1, 0]]`, shape `(1, 2)`.
3. **Forward, layer 2:** `out = 1·1 + 0·1 + 0 = [[1]]`, shape `(1, 1)`.
4. **Loss gradient:** `dout = 2·(1 - 0)/(1·1) = [[2]]`, shape `(1, 1)`.
5. **Second layer, weights:** `dW2 = dout.T @ a1 = [[2]] · [[1, 0]] = [[2, 0]]`, shape `(1, 2)`.
6. **Second layer, bias:** `db2 = [2]`, shape `(1,)`.
7. **Second layer, input:** `da1 = dout @ W2 = [[2, 2]]`, shape `(1, 2)`.
8. **Through ReLU:** the mask `z1 > 0` is `[[1, 0]]`, so `dz1 = [[2, 0]]`, shape `(1, 2)`.
9. **First layer, weights:** `dW1 = dz1.T @ x = [[2],[0]] · [[1, -1]] = [[2, -2],[0, 0]]`, shape `(2, 2)`.
10. **First layer, bias:** `db1 = [2, 0]`, shape `(2,)`.

- Result: `[[[2,-2],[0,0]], [2,0], [[2,0]], [2]]`, which matches the expected output.
- The second hidden unit was inactive (`z1 = -1`), so its row of `dW1` and its `db1` entry are 0.

## Tools you'll need

### `A @ B` and `.T`
- `@` is matrix multiplication; the inner sizes must match: `(a, b) @ (b, c)` gives `(a, c)`.
- `.T` transposes a 2-D tensor.

```python
import torch
A = torch.tensor([[1., 2., 3.], [4., 5., 6.]])
B = torch.tensor([[1., 0.], [0., 1.], [1., 1.]])
print((A @ B).shape)  # torch.Size([2, 2])
print(A.T.shape)  # torch.Size([3, 2])
print(A @ B)  # tensor([[ 4.,  5.], [10., 11.]])
```

### `t.sum(0)`
- Sums over dimension 0 and removes it: one value per column.

```python
import torch
g = torch.tensor([[1., 2.], [3., 4.], [5., 6.]])
print(g.sum(0))  # tensor([ 9., 12.])
print(g.sum(0).shape)  # torch.Size([2])
```

### Comparison masks: `z > 0`
- Comparing a tensor with a number gives a boolean tensor.
- Multiplying by it keeps values where it is True and zeroes the rest.

```python
import torch
z = torch.tensor([[-1., 2.], [3., 0.]])
m = z > 0
print(m)  # tensor([[False,  True], [ True, False]])
print(torch.tensor([[5., 5.], [5., 5.]]) * m)  # tensor([[0., 5.], [5., 0.]])
```

### `torch.relu(z)` and `t.numel()`
- `torch.relu` zeroes negative entries.
- `numel()` returns the total number of elements, which is `n·k` for an `(n, k)` tensor.

```python
import torch
z = torch.tensor([[-2., 1., 3.], [0., -1., 4.]])
print(torch.relu(z))  # tensor([[0., 1., 3.], [0., 0., 4.]])
print(z.numel())  # 6
```

### Broadcasting a bias
- Adding a `(h,)` vector to an `(n, h)` matrix adds it to every row.

```python
import torch
M = torch.zeros(2, 3)
b = torch.tensor([1., 2., 3.])
print(M + b)  # tensor([[1., 2., 3.], [1., 2., 3.]])
```

## Common mistakes

- **Forgetting the `1/(n·k)` factor.** The loss is a mean over all `n·k` elements, not only over `n`.
  - Divide by `out.numel()`.
- **Wrong transpose order.** A weight gradient must have the weight's shape.
  - `W1` is `(h, d)`, so you need `(h, n) @ (n, d)`, not the reverse. Check shapes first.
- **Summing the bias gradient over the wrong axis.** The bias is shared by all samples, so sum over the batch axis (0), not the feature axis.
- **ReLU mask on the wrong tensor.** Use the pre-activation `z1`, not `a1`.
  - Use `z1 > 0` so that `z1 == 0` gives derivative 0, as the problem requires.
- **Using autograd or `requires_grad`.** The task forbids it.
  - Plain tensor arithmetic is enough, and the returned tensors then carry no gradient history.

## Hints

### Hint 1
- Run the forward pass and keep the intermediate values.
- Start backward with the gradient of the loss at the network output.
- Handle the second layer: its weights, its bias, and the gradient sent back to the hidden activations.
- Pass that gradient through ReLU.
- Handle the first layer: its weights and its bias.

### Hint 2
- The output gradient has shape `(n, k)`.
- The second layer gives `dW2` and `db2`, plus a gradient for the hidden activations of shape `(n, h)`.
- ReLU is an element-wise product with a boolean mask built from `z1`; the shape stays `(n, h)`.
- The first layer then gives `dW1` of shape `(h, d)` and `db1` of shape `(h,)`.
- Matrix products and `sum(0)` cover everything.

### Hint 3
- The output gradient is two times `(out - y)`, divided by the number of elements `n·k`.
- For a linear layer with incoming gradient `g` and input `a`:
  - The weight gradient is `g` transposed, times `a`.
  - The bias gradient is the column sum of `g`.
  - The gradient sent back to the input is `g` times the weight matrix (no transpose).
- Between the layers, multiply the hidden gradient element-wise by 1 where `z1 > 0` and 0 elsewhere.
