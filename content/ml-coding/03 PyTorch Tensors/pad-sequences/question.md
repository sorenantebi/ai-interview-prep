---
topic: "PyTorch Tensors"
difficulty: Medium
---
# Pad Sequences

**Topic:** PyTorch Tensors · **Difficulty:** Medium

## Problem

`seqs` is a non-empty list of token-id sequences (lists of ints) of different lengths, possibly empty. Batch them for a model.

Return a list `[padded, lengths]`:
- `padded`: an int64 tensor of shape `(N, L)` where `L` is the longest sequence's length. Row `i` starts with `seqs[i]` and is filled up to `L` with `pad_value`. If every sequence is empty, the shape is `(N, 0)`.
- `lengths`: an int64 tensor of shape `(N,)` with each sequence's original length.

Reading the Python lists once is fine; try to fill the tensor without a Python loop per row.

## Examples

**Example 1**
```text
Input: seqs = [[1, 2, 3], [4]], pad_value = 0
Output: [[[1,2,3],[4,0,0]],[3,1]]
```

**Example 2**
```text
Input: seqs = [[], [7, 8]], pad_value = -1
Output: [[[-1,-1],[7,8]],[0,2]]
Explanation: The empty first sequence becomes a row of padding with length 0.
```

## Constraints

- `1 <= len(seqs) <= 10^4`
- `0 <= len(seqs[i]) <= 1000`
- Both tensors have dtype `torch.int64`
