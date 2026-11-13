# Learn: Sinusoidal Positional Encoding

## The idea

- **Task:** build a table of numbers with one row per token position and one column per feature.
  - Each row is a unique "address" for its position.
  - The values come from fixed sine and cosine waves, so nothing is learned.
- **Why it exists:** a Transformer reads all tokens at once, so it has no built-in sense of order.
  - The positional encoding is added to each token's embedding to tell it "I am at position 0, 1, 2...".
  - It shows up in the first layer of nearly every Transformer model.
- **Column pairs:** columns come in pairs `(2i, 2i+1)`, and each pair shares one wave speed.
  - The even column holds `sin(angle)`, the odd column holds `cos(angle)` of the same angle.
  - `angle = position * frequency`.
- **Frequency:** how fast a wave oscillates, here `1 / 10000^(2i / d_model)`.
  - Early pairs wave fast, later pairs wave slowly.
- **Broadcasting:** PyTorch stretches size-1 dimensions to match another tensor.
  - A `(3, 1)` tensor times a `(1, 2)` tensor gives a `(3, 2)` grid.
- **Strided slice:** `x[:, 0::2]` means "every second column, starting at column 0".
- **dtype:** the number type of a tensor, such as `float32` or `float64`.

## Work it by hand

Example 1: `seq_len = 2`, `d_model = 4`.

1. Positions are `[0, 1]`. As a column, shape `(2, 1)`.
2. The values `2i` are `0, 2`, so there are `d_model/2 = 2` pairs.
   - Frequencies are `10000^(-2i/4)`: `10000^0 = 1` and `10000^(-0.5) = 0.01`.
   - As a row, shape `(1, 2)`.
3. Angles by broadcasting, shape `(2, 2)`:

| position | freq 1 | freq 0.01 |
|---|---|---|
| 0 | 0 | 0 |
| 1 | 1 | 0.01 |

4. Sine of the angles, shape `(2, 2)`: row 0 is `[0, 0]`, row 1 is `[0.84147, 0.01000]`.
5. Cosine of the angles, shape `(2, 2)`: row 0 is `[1, 1]`, row 1 is `[0.54030, 0.99995]`.
6. Interleave into a `(2, 4)` tensor: sines go to columns 0 and 2, cosines to columns 1 and 3.

```text
row 0: [0.00000, 1.00000, 0.00000, 1.00000]
row 1: [0.84147, 0.54030, 0.01000, 0.99995]
```

- This matches the expected output.

## Tools you'll need

### torch.arange(start, end, step, dtype=...)

- Makes a 1-D tensor of evenly spaced numbers, with `end` excluded.
- Pass `dtype` to choose float or int.

```python
import torch
a = torch.arange(1, 10, 3, dtype=torch.float32)
print(a)  # tensor([1., 4., 7.])
print(a.shape)  # torch.Size([3])
```

### tensor.unsqueeze(dim)

- Inserts a new size-1 dimension at `dim`.
- Handy for turning a vector into a column or a row.

```python
import torch
v = torch.tensor([5.0, 6.0, 7.0])
print(v.unsqueeze(1).shape)  # torch.Size([3, 1])
print(v.unsqueeze(0).shape)  # torch.Size([1, 3])
```

### Broadcasting with `*`

- A `(n, 1)` tensor times a `(m,)` or `(1, m)` tensor gives an `(n, m)` grid of all products.

```python
import torch
col = torch.tensor([[1.0], [2.0], [3.0]])
row = torch.tensor([10.0, 100.0])
print((col * row).shape)  # torch.Size([3, 2])
print(col * row)
# tensor([[ 10., 100.],
#         [ 20., 200.],
#         [ 30., 300.]])
```

### Power with `**` and negative exponents

- `base ** tensor` works element-wise.
- A negative exponent means a reciprocal.
- Use a float base and a float tensor.

```python
import torch
e = torch.tensor([0.0, 1.0, 2.0])
print(2.0 ** (-e))  # tensor([1.0000, 0.5000, 0.2500])
```

### torch.sin / torch.cos

- Apply sine or cosine (in radians) to every element.
- The shape is unchanged.

```python
import torch
x = torch.tensor([0.0, 3.14159265 / 2])
print(torch.sin(x))  # tensor([0., 1.])
print(torch.cos(x).shape)  # torch.Size([2])
```

### Strided slice assignment: `t[:, start::2] = ...`

- `0::2` means every second column from 0, and `1::2` means every second column from 1.
- You can assign a tensor of matching shape into that slice.

```python
import torch
t = torch.zeros(2, 6)
t[:, 0::2] = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
print(t.shape)  # torch.Size([2, 6])
print(t[0])  # tensor([1., 0., 2., 0., 3., 0.])
```

### tensor.float() and dtype

- `.float()` casts to `float32`.
- Creating a tensor with `dtype=torch.float64` gives more precision for intermediate work.

```python
import torch
x = torch.tensor([1.5, 2.5], dtype=torch.float64)
print(x.dtype)  # torch.float64
print(x.float().dtype)  # torch.float32
```

## Common mistakes

- **Integer positions or exponents:** `torch.arange(5)` is an integer tensor.
  - Raising it to a negative power fails or truncates.
  - Pass `dtype=torch.float32` (or float64), or use a float base.
- **Wrong frequency exponent:** the exponent uses `2i / d_model`, where `2i` runs over `0, 2, 4, ...`.
  - That is `arange(0, d_model, 2)`, not `arange(d_model/2)` unless you multiply by 2.
- **Shape mismatch on assignment:** each of the even and odd slices has `d_model/2` columns.
  - That must match the angle grid's second dimension, so check `.shape` on a size error.
- **Swapping sin and cos:** even columns get sine, odd columns get cosine.
  - Position 0 must come out as `[0, 1, 0, 1, ...]`.
- **Wrong dtype or a loop:** the result must be `float32`, with no Python loops.
  - Use broadcasting instead.
  - Cast at the end, and compute in float64 first to keep large-position angles accurate.

## Hints

### Hint 1

- Build the positions as a column.
- Build the frequencies as a row, one per column pair.
- Multiply them to get one angle for every position and every pair.
- Take sine and cosine of that grid.
- Place sines in the even columns and cosines in the odd columns of the final tensor.
- Make sure the result is `float32`.

### Hint 2

- Positions: `arange` then `unsqueeze(1)`, shape `(seq_len, 1)`.
- Frequencies: a power of 10000 over `arange(0, d_model, 2)`, shape `(d_model/2,)`.
- Angle: their product, shape `(seq_len, d_model/2)`.
- Output: `zeros(seq_len, d_model)`, filled through the slices `0::2` and `1::2`.
- Finish with a cast to `float32`.

### Hint 3

- The frequency for pair `i` is `10000` raised to the power `-(2i) / d_model`.
- The values `2i` are `0, 2, 4, ...` up to `d_model - 2`, which is exactly what `arange(0, d_model, 2)` gives.
- So divide that range by `d_model`, negate it, and use it as the exponent of the float `10000.0`.
- Multiply by the position column to get the angle grid.
- Write the sine of the grid into the columns starting at 0 with step 2.
- Write the cosine into the columns starting at 1 with step 2.
- Finally cast to `float32`.
