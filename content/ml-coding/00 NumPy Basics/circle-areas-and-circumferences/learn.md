# Learn: Circle Areas and Circumferences

## The idea

- The task: for every radius in an array, compute two numbers and return them together in one 2-D array.
  - The **area** is the space inside the circle: `pi * r ** 2`.
  - The **circumference** is the length around the edge: `2 * pi * r`.
- You do this for all radii at once, with no Python loop.
- **Element-wise** arithmetic: an operation on a NumPy array is applied to each entry separately.
  - The result is a new array of the same length.
- **Vectorisation** means writing whole-array expressions instead of loops.
  - It is shorter and much faster than a loop.
  - In ML and data work it shows up in feature normalisation, loss computation and evaluation tables.
- **Broadcasting**: a single number combined with an array acts as if it were repeated to match the array's length.
- **Stacking**: joining arrays into one bigger array.
  - Here the two 1-D results become row 0 and row 1 of a 2-D array.
- **Shape** `(2, n)` means 2 rows and `n` columns, one column per circle.

## Work it by hand

Example 1: `radii = [1.0, 2.0]`, shape `(2,)`.

| Step | Result | Shape |
|---|---|---|
| Square each radius | `[1.0, 4.0]` | `(2,)` |
| Multiply by pi (areas) | `[3.14159, 12.56637]` | `(2,)` |
| Multiply each radius by 2 | `[2.0, 4.0]` | `(2,)` |
| Multiply by pi (circumferences) | `[6.28319, 12.56637]` | `(2,)` |
| Stack areas on top of circumferences | see below | `(2, 2)` |

Final answer:

```text
[[ 3.14159, 12.56637],
 [ 6.28319, 12.56637]]
```

- Row 0 is the areas, row 1 is the circumferences.
- Each column belongs to one circle.
- The second column repeats a number: radius 2 gives area 4*pi and circumference 4*pi.

## Tools you'll need

### np.pi

- A constant holding pi as a float.
- It is not a function, so write `np.pi` with no parentheses.

```python
import numpy as np

print(np.pi)       # 3.141592653589793
print(np.pi * 2)   # 6.283185307179586
```

### The `**` operator

- The power operator.
- On an array it raises every element to that power and returns a new array.
- The original array is unchanged.

```python
import numpy as np

a = np.array([1.0, 3.0, 5.0])
print(a ** 3)  # [  1.  27. 125.]
print(a)       # [1. 3. 5.]
```

### Arithmetic with a single number

- Multiplying an array by a plain number applies it to every element (broadcasting).
- Operations can be chained.
  - `**` is evaluated before `*`, as in normal maths.

```python
import numpy as np

v = np.array([2.0, 4.0])
print(10 * v)       # [20. 40.]
print(3 * v ** 2)   # [12. 48.]
```

### np.vstack(tup)

- Stacks arrays **vertically**, so each input becomes a row of the result.
- Pass the arrays inside one list or tuple.
- For 1-D inputs of length `n`, the output has shape `(k, n)`, where `k` is the number of arrays.
  - All inputs must have the same length.

```python
import numpy as np

x = np.array([1, 2, 3])
y = np.array([7, 8, 9])
s = np.vstack([x, y])
print(s)        # [[1 2 3]
                #  [7 8 9]]
print(s.shape)  # (2, 3)
```

## Common mistakes

- **Passing the arrays as separate arguments.**
  - `np.vstack(a, b)` fails.
  - Wrap them in one list: `np.vstack([a, b])`.
- **Swapping the rows.**
  - Areas go in row 0 and circumferences in row 1.
  - Check the order against Example 1.
- **Using `^` for powers.**
  - In Python `^` is bitwise XOR, not exponentiation.
  - Use `**`.
- **Mixing up the formulas.**
  - Only the area squares the radius.
  - Squaring the wrong one gives plausible-looking but wrong numbers.
- **Returning shape `(n, 2)`.**
  - Stacking with `np.column_stack`, or transposing by accident, gives the wrong shape.
  - Print `.shape` and confirm it is `(2, n)`.

## Hints

### Hint 1
- Compute the areas for all radii in one step.
- Compute the circumferences for all radii in a second step.
- Combine the two results into one 2-D array, areas on top.

### Hint 2
- Areas: use `np.pi`, the `**` operator and multiplication on the whole array; the result has shape `(n,)`.
- Circumferences: use `np.pi` and multiplication only; the result also has shape `(n,)`.
- Pass both to `np.vstack` inside a list to get shape `(2, n)`.

### Hint 3
- For each radius `r`, the area is pi times `r` squared.
- The circumference is 2 times pi times `r`.
- Write each formula with the whole array in place of `r`, and keep the two results in two variables.
- Put the areas first in a list, give that list to `np.vstack`, and return what it gives back.
