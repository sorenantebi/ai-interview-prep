---
topic: "NumPy Basics"
difficulty: Easy
---
# Roll the Dice and Count the Faces - Solution

## Intuition

A seeded `Generator` makes the rolls reproducible, and `rng.integers(1, 7, size=n)` draws them in one call (the upper bound is exclusive). `np.bincount` counts how often each non-negative integer occurs, so with `minlength=7` it returns counts for the values `0..6`. Face 0 never occurs, so we drop index 0 with a slice.

## Approach

1. Create `rng = np.random.default_rng(seed)`.
2. Draw `rolls = rng.integers(1, 7, size=n)`.
3. Compute `np.bincount(rolls, minlength=7)[1:]` to get the counts of faces 1 to 6.
4. Return `(rolls, counts)`.

## Code

```python
import numpy as np

def roll_dice(n: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    rolls = np.random.default_rng(seed).integers(1, 7, size=n)
    return rolls, np.bincount(rolls, minlength=7)[1:]
```

## Complexity

Time and memory are `O(n)`: one pass to draw the rolls and one to count them.
