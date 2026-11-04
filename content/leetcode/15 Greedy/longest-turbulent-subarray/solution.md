---
topic: "Greedy"
difficulty: Medium
leetcode: https://leetcode.com/problems/longest-turbulent-subarray/
neetcode: https://neetcode.io/problems/longest-turbulent-subarray
---
# Longest Turbulent Subarray - Solution

## Intuition

A turbulent subarray is a run of adjacent comparisons whose signs strictly alternate (`<`, `>`, `<`, ...). So we only need to track the current window and decide, at each step, whether it can be extended or must restart. When the sign of the latest comparison differs from the previous one, we extend. When the elements are equal, the window collapses to a single element. When the sign repeats, a new window starts from the previous element (length 2).

## Approach

1. Keep `best` (answer) and `cur` (length of the turbulent window ending at the current index), both starting at 1.
2. Keep `prev_sign`, the sign of the previous comparison (`0` initially).
3. For each `i` from 1 to `n - 1`, compute `sign` of `arr[i] - arr[i - 1]` (`1`, `-1`, or `0`).
4. If `sign == 0`, reset `cur = 1`.
5. Else if `sign == -prev_sign`, the sign flipped, so `cur += 1`.
6. Else the sign repeated (or this is the first comparison), so `cur = 2`.
7. Set `prev_sign = sign` and update `best = max(best, cur)`.
8. Return `best`.

## Code

```python
class Solution:
    def maxTurbulenceSize(self, arr: List[int]) -> int:
        l, r = 0, 1
        res, prev = 1, ""

        while r < len(arr):
            if arr[r - 1] > arr[r] and prev != ">":
                res = max(res, r - l + 1)
                r += 1
                prev = ">"
            elif arr[r - 1] < arr[r] and prev != "<":
                res = max(res, r - l + 1)
                r += 1
                prev = "<"
            else:
                r = r + 1 if arr[r] == arr[r - 1] else r
                l = r - 1
                prev = ""
        return res
```

## Complexity

- **Time:** `O(n)` — a single pass over the array with constant work per element.
- **Space:** `O(1)` — only a few integer variables are kept.

## Other Approaches

- **Two-pointer window:** move `r` and restart `l` whenever the alternation breaks — Time `O(n)` / Space `O(1)`
- **Dynamic programming:** keep `up[i]` and `down[i]` arrays for the longest turbulent run ending at `i` — Time `O(n)` / Space `O(n)` (reducible to `O(1)`)
