# Learn: Scatter-Add Counts

## The idea

- **Class prototype**: the average embedding of all samples that share a label, i.e. the "typical" vector of that class.
- The task: turn `N` labelled vectors into `num_classes` average vectors, with no Python loops.
- Where it shows up:
  - Few-shot learning (prototypical networks) classify by distance to prototypes.
  - Nearest-centroid classifiers.
  - Evaluation reports that compare classes in embedding space.
- **Mean**: sum divided by count, so you need two numbers per class.
  - The sum of its rows, shape `(num_classes, D)`.
  - The number of its rows, shape `(num_classes,)`.
- **Scatter**: copy many source rows into destination rows picked by an index tensor.
  - Several sources can land in the same destination, and they are added together.
  - That is exactly a per-class sum.
- **Empty class**: sum 0 and count 0, so `0 / 0` gives `nan`. The task wants zeros instead.
- **Broadcasting**: PyTorch stretches a smaller tensor across a bigger one when the shapes are compatible.
  - A `(3, 1)` tensor divides a `(3, 2)` tensor by repeating its one column across both columns.

## Work it by hand

Example 1: `x = [[1,2],[3,4],[10,0]]`, `labels = [0,0,2]`, `num_classes = 3`.

1. Start with a zero sums tensor of shape `(3, 2)`: `[[0,0],[0,0],[0,0]]`.
2. Scatter the rows by label:
   - Row 0 of `x`, `[1,2]`, goes to row `labels[0] = 0`.
   - Row 1, `[3,4]`, goes to row 0.
   - Row 2, `[10,0]`, goes to row 2.
   - Sums: `[[4,6],[0,0],[10,0]]`, shape `(3, 2)`.
3. Count the labels: class 0 twice, class 1 never, class 2 once.
   - Counts: `[2,0,1]`, shape `(3,)`.
4. Replace counts of 0 by 1 so nothing divides by zero.
   - Safe counts: `[2,1,1]`.
5. Add a trailing axis: `[[2],[1],[1]]`, shape `(3, 1)`.
6. Divide each sum row by its count:
   - Row 0: `[4,6] / 2 = [2,3]`.
   - Row 1: `[0,0] / 1 = [0,0]`.
   - Row 2: `[10,0] / 1 = [10,0]`.
7. Result: `[[2,3],[0,0],[10,0]]`, which matches the expected output.

## Tools you'll need

### `torch.zeros(rows, cols, dtype=...)`

- Makes a tensor filled with zeros.
- Pass the dtype of your data so later operations don't hit a type mismatch.

```python
import torch
a = torch.zeros(2, 3, dtype=torch.float64)
print(a.shape)  # torch.Size([2, 3])
print(a.dtype)  # torch.float64
```

### `tensor.index_add_(dim, index, source)`

- Adds rows of `source` into `tensor` along `dim`: row `i` of `source` goes to position `index[i]`.
- The trailing underscore means it changes the tensor in place (and returns it).
- `index` must be a 1-D int tensor, and repeated indices accumulate.

```python
import torch
dest = torch.zeros(2, 2)
src = torch.tensor([[1., 1.], [2., 2.], [5., 5.]])
idx = torch.tensor([1, 0, 1])
dest.index_add_(0, idx, src)
print(dest)  # tensor([[2., 2.], [6., 6.]])
```

### `torch.bincount(input, minlength=0)`

- Counts how often each non-negative integer appears in a 1-D int tensor.
- The output length is `max(input) + 1`, or `minlength` if that is larger.
- The result is int64.

```python
import torch
v = torch.tensor([0, 3, 3, 1])
print(torch.bincount(v))               # tensor([1, 1, 0, 2])
print(torch.bincount(v, minlength=6))  # tensor([1, 1, 0, 2, 0, 0])
```

### `tensor.clamp(min=...)`

- Limits values to a lower (and/or upper) bound.
- Handy for turning zeros into ones while leaving other values alone.

```python
import torch
c = torch.tensor([0, 4, 0, 2])
print(c.clamp(min=1))  # tensor([1, 4, 1, 2])
```

### `tensor.unsqueeze(dim)` and `tensor.to(dtype)`

- `unsqueeze` inserts a new axis of size 1 at `dim`, so `(3,)` becomes `(3, 1)` for `dim=1`.
- `.to(dtype)` converts types, for example int counts to float before dividing float sums.

```python
import torch
c = torch.tensor([2, 5, 1])
col = c.unsqueeze(1).to(torch.float32)
print(col.shape)  # torch.Size([3, 1])
print(col.dtype)  # torch.float32
```

### `tensor.scatter_add_(dim, index, src)` (alternative)

- Same idea, but `index` must have the same shape as `src` and picks the destination element by element.
- For whole rows you would first have to expand the index to 2-D, so `index_add_` is simpler here.

```python
import torch
t = torch.zeros(3)
t.scatter_add_(0, torch.tensor([0, 0, 2]), torch.tensor([1., 2., 3.]))
print(t)  # tensor([3., 0., 3.])
```

## Common mistakes

- **Dividing by zero counts.** Empty classes give `0/0 = nan`.
  - Clamp counts to at least 1 before dividing.
- **Forgetting the trailing axis.** Dividing `(C, D)` by `(C,)` lines the counts up with the wrong axis, or errors.
  - Reshape counts to `(C, 1)`.
- **Dtype mismatch.** `bincount` returns int64, and `index_add_` needs the destination and source to share a dtype.
  - Create the zeros with `x`'s dtype and convert the counts to it.
- **Missing `minlength`.** If the highest classes have no samples, `bincount` returns a tensor that is too short.
  - Always pass `minlength=num_classes`.
- **Integer division.** Dividing integer tensors would not give true means.
  - Make sure both sides are floats.

## Hints

### Hint 1

- Compute two things per class: the sum of its embeddings and the number of samples.
- Make empty classes safe, so they don't divide by zero.
- Divide the sums by the counts.

### Hint 2

- Make a zero tensor of shape `(num_classes, D)`, then use `index_add_` along dim 0 to get the sums, still `(num_classes, D)`.
- Use `bincount` with `minlength` to get counts, shape `(num_classes,)`.
- Convert counts to float and clamp them to at least 1, still `(num_classes,)`.
- Add a trailing axis so the counts have shape `(num_classes, 1)`, then divide the sums by them.

### Hint 3

- `index_add_(0, labels, x)` means: for every `i`, add `x[i]` into row `labels[i]` of the destination.
- After that, row `c` holds the sum of all embeddings of class `c`.
- The mean of row `c` is `sum[c] / max(count[c], 1)`.
- For an empty class the sum row is all zeros, so zeros divided by 1 stay zeros and no `nan` appears.
