# Learn: Celsius to Fahrenheit

## The idea

- The task: convert every temperature in an array from Celsius to Fahrenheit, then round each result to 1 decimal.
  - For one number the formula is `F = C * 9 / 5 + 32`.
  - The output must have the same shape as the input, whatever that shape is.
- This pattern shows up all the time in data work: converting units, rescaling features in a pipeline, normalising values before training.
- **Vectorised arithmetic**: writing `+`, `-`, `*` or `/` on an array applies the operation to every element at once.
  - No Python loop is needed.
  - It is shorter and much faster on large arrays.
- **Element-wise**: an operation that changes each value on its own and keeps the shape.
- **Shape**: the size along each dimension. `(2, 3)` means 2 rows and 3 columns.
- **Scalar**: a plain number such as `9`. NumPy applies it to every element of the array (a simple case of broadcasting).

## Work it by hand

- Example 1: `celsius = [0.0, 100.0, -40.0, 37.0]`, shape `(4,)`.
- Each step acts on all four values together, and the shape stays `(4,)`.

| Step | Operation | Result |
|---|---|---|
| 1 | multiply by 9 | `[0, 900, -360, 333]` |
| 2 | divide by 5 | `[0, 180, -72, 66.6]` |
| 3 | add 32 | `[32, 212, -40, 98.6]` |
| 4 | round to 1 decimal | `[32.0, 212.0, -40.0, 98.6]` |

- Check one value by hand: for 37, `37 * 9 = 333`, `333 / 5 = 66.6`, `66.6 + 32 = 98.6`.
- Rounding changes nothing here, because every value already has at most 1 decimal.
- Final output: `[32.0, 212.0, -40.0, 98.6]`.
  - The expected output shows 5 decimals (`32.00000`), which is only print formatting.

## Tools you'll need

### Arithmetic operators on arrays (`+`, `-`, `*`, `/`)

- Each operator works element-wise and returns a **new** array, so the original is untouched.
- A scalar is applied to every element.

```python
import numpy as np

a = np.array([[1.0, 2.0], [3.0, 4.0]])
b = a * 10 - 1
print(b)
# [[ 9. 19.]
#  [29. 39.]]
print(b.shape)  # (2, 2)
print(a)
# [[1. 2.]
#  [3. 4.]]
```

### Operator precedence

- `*` and `/` bind tighter than `+` and `-`.
- Parentheses override this, and equal-precedence operators go left to right.

```python
import numpy as np

v = np.array([2.0, 4.0, 6.0])
print(v + 1 * 2)    # [4. 6. 8.]
print((v + 1) * 2)  # [ 6. 10. 14.]
```

### `/` always gives floats

- In Python 3, `/` is true division.
- Even on an `int64` array the result is `float64`, so no decimals are lost.

```python
import numpy as np

n = np.array([1, 2, 3])
print(n / 2)          # [0.5 1.  1.5]
print((n / 2).dtype)  # float64
```

### np.round(a, decimals)

- Rounds each element to `decimals` decimal places.
- `decimals` defaults to 0.
- Returns a new array with the same shape.

```python
import numpy as np

x = np.array([[1.234, 5.678], [9.0, 0.449]])
print(np.round(x, 2))
# [[1.23 5.68]
#  [9.   0.45]]
print(np.round(x))
# [[1. 6.]
#  [9. 0.]]
```

### In-place operators (`+=`, `*=`, ...) — avoid here

- These modify the existing array instead of making a new one.
- Anyone else holding that array sees the change.

```python
import numpy as np

x = np.array([1.0, 2.0])
y = x
y *= 2
print(x)  # [2. 4.]
```

## Common mistakes

- **Writing a loop or list comprehension.** The problem forbids them, so apply the operators to the whole array.
- **Modifying the input in place.** `celsius *= 9` changes the caller's array. Plain `*`, `/`, `+` build new arrays, so use those.
- **Rounding the wrong thing.** Round the final Fahrenheit values, not the Celsius input, or the answers will be off.
- **Using `//` instead of `/`.** Floor division drops decimals (`333 // 5` is `66`), so use `/`.
- **Getting the order wrong.** `C * 9 / 5 + 32` is correct. Adding 32 before multiplying gives a different result.

## Hints

### Hint 1
- Work in two stages.
- First, apply the conversion formula to the whole array.
- Second, round that result to 1 decimal place.
- Return the new array.

### Hint 2
- Write the formula with `*`, `/` and `+` directly on the array. The result is a new array with the same shape.
- Pass that result to `np.round` and ask for 1 decimal.

### Hint 3
- Take the array, multiply by 9, divide by 5, then add 32.
- Hand that whole expression to `np.round` as its first argument, and give `1` as the second argument.
- Every operator creates a new array, so the input stays untouched and the shape is preserved.
