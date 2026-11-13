# Learn: Causal Mask

## The idea

- **The task:** build a `(t, t)` grid of numbers that is `0.0` where a token may look and `-inf` where it may not.
- **Why it exists:** a decoder (like GPT) predicts the next token, so token `i` may only see itself and earlier tokens.
  - If it could see later tokens, it could just read the answer.
- **Where it shows up:** every transformer decoder, in both training and generation.
  - You build the mask once per sequence length and reuse it.
- **Query / key:** row `i` is the query (the token asking), and column `j` is the key (the token being looked at).
- **Attention scores:** a `(t, t)` grid of numbers saying how much each query cares about each key.
- **Softmax:** the step that turns a row of scores into weights that are positive and sum to 1.
- **Additive mask:** a grid you add to the scores before the softmax.
  - Adding `0.0` changes nothing.
  - Adding `-inf` makes the score `-inf`, and `exp(-inf) = 0`, so that key gets exactly zero weight.
- **Main diagonal:** the entries where `i == j`, running from top-left to bottom-right.
  - The `-inf` entries are exactly the ones strictly above it.

## Work it by hand

Take `t = 3`. Entry `[i, j]` is `0.0` if `j <= i`, and `-inf` if `j > i`.

| row i | j=0 | j=1 | j=2 |
|---|---|---|---|
| 0 | 0.0 (0<=0) | -inf (1>0) | -inf (2>0) |
| 1 | 0.0 (0<=1) | 0.0 (1<=1) | -inf (2>1) |
| 2 | 0.0 (0<=2) | 0.0 (1<=2) | 0.0 (2<=2) |

1. The shape is `(3, 3)` and the dtype is `float32`.
2. The diagonal (`i == j`) is `0.0`, because a token may see itself.
3. Below the diagonal (`j < i`) is `0.0`, because the past is visible.
4. Above the diagonal (`j > i`) is `-inf`, because the future is hidden.
5. Read off the rows to get the final answer:

```text
[[0.0, -inf, -inf],
 [0.0,  0.0, -inf],
 [0.0,  0.0,  0.0]]
```

## Tools you'll need

### torch.full(size, fill_value)

- Makes a tensor of the given shape with every entry set to one value.
- The dtype is inferred from the value, so a Python float gives `float32`.

```python
import torch

a = torch.full((2, 4), 7.5)
print(a.shape)  # torch.Size([2, 4])
print(a.dtype)  # torch.float32
print(a[0])     # tensor([7.5000, 7.5000, 7.5000, 7.5000])
```

### float("-inf")

- Python's negative infinity, a valid float that PyTorch stores as `-inf`.
- `exp(-inf)` is `0`, which is why it works as a "block this" value in a softmax.

```python
import torch

x = torch.tensor([1.0, float("-inf")])
print(x)            # tensor([1., -inf])
print(torch.exp(x)) # tensor([2.7183, 0.0000])
print(torch.softmax(torch.tensor([0.0, float("-inf")]), dim=0))  # tensor([1., 0.])
```

### tensor.triu(diagonal=0) and tensor.tril(diagonal=0)

- `triu` ("upper triangle") keeps entries on and above a diagonal and sets the rest to **0**.
- `tril` ("lower triangle") keeps entries on and below it, and sets the rest to **0**.
- `diagonal` picks the border: `0` is the main diagonal, positive values move up and negative values move down.
- The shape does not change.

```python
import torch

m = torch.arange(1, 10, dtype=torch.float32).reshape(3, 3)
print(m.triu())    # tensor([[1., 2., 3.],
                   #         [0., 5., 6.],
                   #         [0., 0., 9.]])
print(m.triu(2))   # tensor([[0., 0., 3.],
                   #         [0., 0., 0.],
                   #         [0., 0., 0.]])
print(m.tril(-1))  # tensor([[0., 0., 0.],
                   #         [4., 0., 0.],
                   #         [7., 8., 0.]])
```

### torch.arange(n) and broadcasting

- `arange(n)` gives `[0, 1, ..., n-1]`.
- **Broadcasting** means PyTorch stretches a size-1 dimension to match the other operand.
  - A column `(n, 1)` compared with a row `(1, n)` gives an `(n, n)` grid.

```python
import torch

r = torch.arange(4).reshape(4, 1)
c = torch.arange(4).reshape(1, 4)
print((r - c).shape)  # torch.Size([4, 4])
print((r < c)[0])     # tensor([False,  True,  True,  True])
```

### torch.where(cond, a, b)

- Picks `a` where the condition is true and `b` elsewhere.
- `a` and `b` can be Python scalars, and the result's dtype follows them.
- This is an alternative route: build a boolean grid, then choose a value per entry.

```python
import torch

cond = torch.tensor([[True, False], [False, True]])
out = torch.where(cond, 5.0, -5.0)
print(out)        # tensor([[ 5., -5.],
                  #         [-5.,  5.]])
print(out.dtype)  # torch.float32
```

## Common mistakes

- **Off-by-one on the diagonal.** The diagonal must be `0.0`, because a token sees itself.
  - Check that your border starts one step above the main diagonal, not on it. Test with `t = 3`.
- **Wrong filler for the wrong region.** `triu` and `tril` turn the part they drop into `0`.
  - Decide which region should hold `-inf` and which should hold zeros, then pick the tool that keeps the right one.
- **Multiplying by `-inf`.** `0 * -inf` is `nan`, not `0`.
  - Choose values instead of multiplying a 0/1 grid by `-inf`.
- **Wrong dtype.** Integer or boolean tensors can't hold `-inf` as you need.
  - Check that the result is `float32`.
- **Python loops.** They are forbidden here and slow, since `t = 4096` means about 16 million entries.

## Hints

### Hint 1
- Start with a square grid where every entry is `-inf`.
- Keep the `-inf` only in the region strictly above the diagonal.
- Turn everything else (the diagonal and below) into `0.0`.
- Use a tool that works on the triangles of a matrix, so no loops are needed.

### Hint 2
- Use `torch.full` to make the `(t, t)` grid of `-inf`. The shape is `(t, t)` and the dtype is `float32`.
- Apply a triangle method (`triu` or `tril`) to that grid. The shape stays `(t, t)`.
- Remember that the method sets the dropped entries to `0`, which is exactly the value you want in the allowed region.

### Hint 3
- `triu(k)` keeps entry `[i, j]` when `j - i >= k`, and sets all other entries to 0.
- You want to keep `-inf` where `j > i`, which is the same as `j - i >= 1`.
- So choose `k` equal to one: the kept region then starts one column to the right of the main diagonal.
- The diagonal and everything below it become `0.0` automatically.
