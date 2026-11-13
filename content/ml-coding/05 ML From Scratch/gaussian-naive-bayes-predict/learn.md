# Learn: Gaussian Naive Bayes

## The idea

- **Classifier**: given a point, decide which class it most likely belongs to.
- Naive Bayes asks the reverse question for each class: "if a point came from class `c`, how typical would it look?"
  - It combines that with how common the class is, then picks the best class.
- **Prior**: the fraction of training samples in a class, `P(c)`.
  - Example: 2 of 4 samples in class 0 gives a prior of 0.5.
- **Naive**: within one class, assume the features are independent.
  - So a point's likelihood is the product of one-feature likelihoods.
- **Gaussian**: each feature in a class follows a bell curve.
  - The curve is described by a **mean** and a **variance** (the average squared distance from the mean).
- Fitting is just computing, per class, a prior, a mean per feature and a variance per feature.
  - No training loop is needed, which makes it a fast baseline on tabular data.
- **Log score**: multiplying many small probabilities underflows to 0, so we add logs instead.
  - A higher score means a more likely class.
- **Population variance**: divide by the count `n`, not `n - 1`.
- **eps**: a tiny number added to the variance so a constant feature never gives variance 0 (division by zero).
- **Broadcasting**: NumPy stretches size-1 axes so arrays of different shapes can be combined.
  - Example: `(q, 1, d)` minus `(1, c, d)` gives `(q, c, d)`.
- **Tie**: two classes with exactly equal scores; the smallest label wins.

## Work it by hand

Example 1: `X_train = [1, 2, 8, 9]`, `y_train = [0, 0, 1, 1]`, `X_test = [1.5, 7.0, 5.0]`, `eps = 1e-9`.

1. Find the classes: `[0, 1]`.
2. Fit each class:

| class | samples | prior | mean | variance (÷ count) |
|---|---|---|---|---|
| 0 | 1, 2 | 2/4 = 0.5 | 1.5 | (0.25 + 0.25) / 2 = 0.25 |
| 1 | 8, 9 | 0.5 | 8.5 | 0.25 |

3. `eps = 1e-9` is negligible, so the variance stays 0.25.
4. With variance 0.25, the penalty `(x - μ)² / (2σ²)` is `2·(x - μ)²`.
5. Both classes share the same prior and variance, so they share the constant `log 0.5 - ½·log(2π·0.25) ≈ -0.693 - 0.226 = -0.919`.
6. Score each test point (score = constant minus penalty):

| x | class 0: diff, penalty | class 1: diff, penalty | scores (0, 1) |
|---|---|---|---|
| 1.5 | 0, 0 | -7, 98 | -0.919, -98.919 |
| 7.0 | 5.5, 60.5 | -1.5, 4.5 | -61.419, -5.419 |
| 5.0 | 3.5, 24.5 | -3.5, 24.5 | -25.419, -25.419 |

7. Pick the best class per row:
   - 1.5: class 0 wins.
   - 7.0: class 1 wins.
   - 5.0: exact tie, so the smaller label, 0.
8. Result: `[0, 1, 0]`.

- Shapes in the general method:
  - means and variances: `(c, d)`
  - priors: `(c,)`
  - score matrix: `(q, c)`
  - output: `(q,)`

## Tools you'll need

### np.unique(a)
- Returns the sorted distinct values; these are your class labels.

```python
import numpy as np
a = np.array([5, 3, 5, 9, 3])
print(np.unique(a))  # [3 5 9]
```

### Boolean mask indexing
- `X[y == c]` keeps only the rows where the condition is True.

```python
import numpy as np
X = np.array([[1, 2], [3, 4], [5, 6]])
y = np.array([1, 0, 1])
print(X[y == 1])  # [[1 2]
                  #  [5 6]]
print(X[y == 1].shape)  # (2, 2)
```

### .mean(axis=0) and .var(axis=0)
- `axis=0` collapses the rows, giving one value per column (feature).
- `var` divides by the count by default, which is the population variance this problem wants.

```python
import numpy as np
B = np.array([[1.0, 4.0], [3.0, 8.0]])
print(B.mean(axis=0))  # [2. 6.]
print(B.var(axis=0))  # [1. 4.]
```

### np.log and np.pi
- `np.log` is the natural log, applied element by element.
- `np.pi` is π.

```python
import numpy as np
print(np.log(np.array([1.0, np.e])))  # [0. 1.]
```

### Adding an axis with None, and broadcasting
- `a[:, None, :]` inserts a size-1 axis.
- Subtracting arrays then compares every row of one with every row of the other.

```python
import numpy as np
a = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
m = np.array([[0.0, 0.0], [1.0, 1.0]])
d = a[:, None, :] - m[None, :, :]
print(d.shape)  # (3, 2, 2)
print(d[0])  # [[1. 2.]
             #  [0. 1.]]
```

### .sum(axis=k)
- Adds along one axis and removes it.
- Use it to add up the per-feature terms.

```python
import numpy as np
t = np.arange(8).reshape(2, 2, 2)
print(t.sum(axis=2))  # [[ 1  5]
                      #  [ 9 13]]
print(t.sum(axis=2).shape)  # (2, 2)
```

### .argmax(axis=1)
- Returns the index of the largest value in each row.
- On ties it returns the first one.

```python
import numpy as np
s = np.array([[1, 5, 5], [7, 2, 7]])
print(s.argmax(axis=1))  # [1 0]
```

### Indexing with an index array
- Turns column positions back into real labels.

```python
import numpy as np
labels = np.array([3, 7, 9])
print(labels[np.array([2, 0, 0])])  # [9 3 3]
```

## Common mistakes

- **Returning the argmax index instead of the label.**
  - Labels can be `[3, 7]`, so index 1 means label 7. Map back through the sorted class array.
- **Using sample variance.**
  - Divide by the count (NumPy's default, `ddof=0`), not count − 1.
- **Forgetting `eps`, or adding it in the wrong place.**
  - Add it to the variance once, then use that value in both the log term and the division.
- **Wrong axis.**
  - Mean and variance run over samples (`axis=0`).
  - The feature sum runs over `d`, the last axis of the `(q, c, d)` array.
- **Forgetting the prior, or not taking its log.**
  - Add `log P(c)` once per class, not once per feature, and take the log of the fraction rather than the fraction itself.

## Hints

### Hint 1
- Find the distinct classes in sorted order.
- For each class, take its rows and compute the prior, the per-feature mean and the per-feature variance plus `eps`.
- Score every test point against every class: log prior plus the sum of per-feature Gaussian log densities.
- Pick the best class per test point and convert back to labels.

### Hint 2
- `np.unique` gives the classes.
- `X_train[y_train == c]` gives each class's rows; `.mean(axis=0)` and `.var(axis=0)` give `(d,)` vectors.
  - Stack them into `(c, d)` arrays.
- Build the differences with `X_test[:, None, :]` and `mu[None]`, giving `(q, c, d)`.
- Sum over the last axis to get `(q, c)`, then use `argmax(axis=1)`.

### Hint 3
- For one test point `x` and class `c`, the log-likelihood is the sum over features `j` of `-½·(log(2π·var[c, j]) + (x_j - mu[c, j])² / var[c, j])`.
- Add `log(prior[c])` to that sum.
- Do all pairs at once by letting broadcasting line up the test, class and feature axes, then sum over the feature axis only.
- The `argmax` result is a position in the sorted class array, so index that array to get the label.
- Because classes are sorted and `argmax` takes the first maximum, ties go to the smallest label automatically.
