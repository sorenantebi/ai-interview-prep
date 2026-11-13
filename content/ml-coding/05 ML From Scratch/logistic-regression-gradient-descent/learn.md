# Learn: Logistic Regression with Gradient Descent

## The idea

- **Logistic regression** answers a yes/no question with a probability between 0 and 1.
  - It takes a weighted sum of the features, then squashes it into that range.
- **Logit**: the weighted sum `z = X @ w + b`, one number per sample.
- **Bias** `b`: a constant added to every logit, so the model isn't forced through zero.
- **Sigmoid**: the squashing function `1 / (1 + exp(-z))`.
  - Big positive `z` gives a probability near 1, big negative gives near 0, and `z = 0` gives exactly 0.5.
- **Probability** `p`: the model's belief that the label is 1.
- **Mean binary cross-entropy**: a score for how wrong the predictions are.
  - It is small when `p` is close to the true label and large when the model is confidently wrong.
- **Gradient**: the slope of the loss with respect to a parameter.
  - It tells you which direction makes the loss grow.
- **Gradient descent**: repeat "compute the gradient, then step the opposite way".
- **Learning rate** `lr`: the size of each step.
- **Full-batch**: every step uses all `n` samples, not a random subset.
- Key fact: for this loss, the slope with respect to the logit is just `p - y` (the prediction error).
  - The problem already gives the final gradient formulas, so you only need to implement them.
- Where it shows up: this is the core of nearly every classifier training loop.
  - Neural networks do the same thing with more layers.

## Work it by hand

Example 1: `X = [[0],[1]]`, `y = [0, 1]`, `w = [0]`, `b = 0`, `lr = 1`, `steps = 1`. Here `n = 2` and `d = 1`.

| Step | Calculation | Result | Shape |
|---|---|---|---|
| Logits | `X @ w + b` = `[0*0+0, 1*0+0]` | `[0, 0]` | `(2,)` |
| Probabilities | sigmoid(0) = 1 / (1 + 1) | `[0.5, 0.5]` | `(2,)` |
| Error `p - y` | `[0.5-0, 0.5-1]` | `[0.5, -0.5]` | `(2,)` |
| `grad_w` | `Xᵀ (p-y) / n` = `(0*0.5 + 1*(-0.5)) / 2` | `[-0.25]` | `(1,)` |
| `grad_b` | mean of `[0.5, -0.5]` | `0.0` | scalar |
| New `w` | `0 - 1 * (-0.25)` | `[0.25]` | `(1,)` |
| New `b` | `0 - 1 * 0.0` | `0.0` | scalar |

- The result is `[[0.25], 0.0]`, which matches the expected output.
- Why the weight went up: the sample with feature 1 has label 1, so a bigger weight pushes its probability up.

## Tools you'll need

### `A @ v` and `A.T`

- `@` is matrix multiplication.
  - A `(n, d)` matrix times a `(d,)` vector gives an `(n,)` vector.
- `.T` transposes, so a `(d, n)` matrix times an `(n,)` vector gives a `(d,)` vector.

```python
import numpy as np
A = np.array([[1., 2.], [3., 4.], [5., 6.]])
print((A @ np.array([1., -1.])).shape)  # (3,)
print(A.T.shape)  # (2, 3)
print(A.T @ np.array([1., 0., 1.]))  # [6. 8.]
```

### `np.exp(x)`

- Computes e to the power x, element by element, on scalars or arrays.
- You need it for the sigmoid.

```python
import numpy as np
print(np.exp(0.0))  # 1.0
print(round(float(np.exp(-1.0)), 3))  # 0.368
```

### `.mean()`

- Averages all elements, or along an `axis` if you give one.
- On a 1-D array it returns a single number.

```python
import numpy as np
a = np.array([[1., 2.], [3., 6.]])
print(a.mean())  # 3.0
print(a.mean(axis=0))  # [2. 4.]
```

### `np.array(x, dtype=float)`

- Makes a new float array, so the caller's array is not changed.
- It also avoids integer-dtype surprises.

```python
import numpy as np
orig = np.array([1, 2, 3])
c = np.array(orig, dtype=float)
c[0] = 9.5
print(orig)  # [1 2 3]
print(c)  # [9.5 2.  3. ]
```

## Common mistakes

- **Changing the input `w` in place.**
  - `w -= ...` modifies the caller's array, and on an integer array it can fail or truncate.
  - Copy `w` to a float array first.
- **Forgetting to divide by `n`.**
  - The gradient is the mean over samples, not the sum.
  - Without `/ n`, steps are `n` times too big and training can blow up.
- **Updating `w` and `b` from different predictions.**
  - Compute `p` once per step, derive both gradients from it, then update.
  - Don't recompute `p` between the two updates.
- **Wrong sign on the update.**
  - Gradient descent subtracts: `w - lr * grad_w`.
- **Returning the wrong types or step count.**
  - Return `w` as a `(d,)` array and `b` as a plain float, in a list `[w, b]`.
  - Run exactly `steps` iterations, including zero when `steps = 0`.

## Hints

### Hint 1

- Make float copies of the starting weights and bias.
- Loop `steps` times.
- Inside the loop, predict probabilities for all samples.
- Measure the error against the labels.
- Turn the error into one gradient for the weights and one for the bias.
- Update both.
- After the loop, return the weights and bias in a list.

### Hint 2

- Logits come from `X @ w + b`, shape `(n,)`.
- Apply the sigmoid with `np.exp` to get `p`, shape `(n,)`.
- Subtract `y` to get the error, shape `(n,)`.
- The weight gradient uses `X.T @ error`, shape `(d,)`.
- The bias gradient uses `.mean()` on the error, a scalar.

### Hint 3

- The sigmoid is one divided by (one plus e to the minus z).
- The weight gradient is the transposed `X` times the error vector, divided by `n`.
  - This gives one number per feature: the sum over samples of feature value times error, averaged.
- The bias gradient is the plain average of the error.
- Both updates have the form "old value minus `lr` times gradient".
  - Use the same `p` from the start of the step for both.
