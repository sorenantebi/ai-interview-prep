# Learn: Array Attributes

## The idea

- **The task:** read four facts that every NumPy array already stores about itself, and return them together as one tuple.
- **Order matters:** number of dimensions, shape, total element count, dtype name.
- **Where it shows up:** most errors in a training loop or feature pipeline are shape or dtype errors.
  - Example: "cannot multiply (32, 10) by (32, 10)".
  - Example: "expected float32, got int64".
  - Printing these four facts is the first debugging step.
- **Dimensions (ndim):** how many axes the array has.
  - A list of numbers has 1, a table has 2, a stack of tables has 3.
  - A single number wrapped as an array has 0.
- **Shape:** a tuple with the length of each axis.
  - A table with 2 rows and 3 columns has shape `(2, 3)`.
- **Size:** the total count of elements, equal to the product of the shape entries.
- **dtype:** the data type of the elements, such as `float64`, `int64` or `bool`.
  - All elements of one array share the same dtype.

## Work it by hand

Take Example 1: `[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]`, turned into an array.

| Step | Question | Look at | Answer |
|---|---|---|---|
| 1 | How many axes? | Two levels of nested brackets: rows, then columns | `2` |
| 2 | How long is each axis? | 2 rows, each holding 3 numbers | `(2, 3)` |
| 3 | How many elements? | 2 × 3 | `6` |
| 4 | What type? | Python floats become 64-bit floats | `"float64"` |

- Put the four answers in order and you get the expected output:

```text
(2, (2, 3), 6, "float64")
```

- Nothing was computed from the values themselves; every answer came from the structure of the array.

## Tools you'll need

### Array attributes: `.ndim`, `.shape`, `.size`

- These are attributes, not methods, so write them without parentheses.
- `.ndim` is an int, `.shape` is a tuple of ints, `.size` is the total element count.
- A 1-D array has a one-element shape tuple like `(5,)`. An empty axis has length 0, so the size is 0 too.

```python
import numpy as np

a = np.zeros((4, 1, 5))
print(a.ndim)   # 3
print(a.shape)  # (4, 1, 5)
print(a.size)   # 20

b = np.array([7, 8, 9])
print(b.shape)  # (3,)

c = np.zeros((0, 3))
print(c.size)   # 0
```

### `.dtype` and `.dtype.name`

- `.dtype` is a dtype object; printing it can look like a string, but it is not one.
- That object has a `.name` attribute that gives a real `str`.

```python
import numpy as np

a = np.array([1.5, 2.5], dtype=np.float32)
print(a.dtype)       # float32
print(a.dtype.name)  # float32
print(type(a.dtype.name))  # <class 'str'>

b = np.array([True, False])
print(b.dtype.name)  # bool
```

### Returning several values

- `return a, b, c, d` packs the values into a tuple.
- No extra parentheses or `tuple(...)` call are needed.

```python
def pair():
    return 1, "x"

print(pair())  # (1, 'x')
print(type(pair()))  # <class 'tuple'>
```

### `np.array(...)` (for experimenting)

- Build arrays from nested lists to try things out; the nesting depth gives `ndim`.
- NumPy picks the dtype from the values.
- The default integer dtype is `int64` on most 64-bit platforms, but it can differ on some systems.

```python
import numpy as np

a = np.array([[1, 2], [3, 4], [5, 6]])
print(a.shape)       # (3, 2)
print(a.dtype.name)  # int64
b = np.array(5.0)
print(b.ndim, b.shape)  # 0 ()
```

## Common mistakes

- **Writing parentheses.** `x.shape()` fails because a tuple is not callable.
  - These four are attributes, so write `x.ndim`, `x.shape`, `x.size`.
- **Returning the dtype object.** `x.dtype` is not a `str`, so a comparison with `"float64"` may behave oddly.
  - Go through `.name` to get a real string.
- **Confusing `size` with `len` or `shape`.** `len(x)` gives only the length of the first axis.
  - A `(2, 3)` array has `len` 2 but `size` 6.
- **Forgetting the 0-D case.** A 0-D array has `ndim` 0 and shape `()`, an empty tuple, but its `size` is still 1.
  - No special case is needed.
- **Wrong order.** The order is ndim, shape, size, dtype name; check it against the problem statement.

## Hints

### Hint 1
- All four facts are already stored on the array, so there is nothing to compute and no loop.
- Read each fact in the order the problem lists them.
- Return them together as one tuple.

### Hint 2
- Number of dimensions, shape and element count: use the attributes of the same names on `x`.
- Type name: go through the dtype object on `x` to its name.
- All four already have the types the problem wants (`int`, `tuple`, `int`, `str`).

### Hint 3
- The only slightly tricky part is the dtype: `x.dtype` prints like `dtype('float64')` but is an object, so ask it for its `name` attribute to get the plain string.
- Then write a single `return` line with the four values separated by commas.
- Keep the order: ndim, shape, size, dtype name.
