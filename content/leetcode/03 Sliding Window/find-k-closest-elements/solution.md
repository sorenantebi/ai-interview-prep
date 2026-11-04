---
topic: "Sliding Window"
difficulty: Medium
leetcode: https://leetcode.com/problems/find-k-closest-elements/
neetcode: https://neetcode.io/problems/find-k-closest-elements
---
# Find K Closest Elements - Solution

## Intuition

Because the array is sorted, the `k` closest elements always form a contiguous window of length `k`. So the task reduces to finding the correct left edge of that window. We can binary search on that left edge instead of scanning.

## Approach

1. The window start `left` lies in `[0, len(arr) - k]`. Set `lo = 0`, `hi = len(arr) - k`.
2. While `lo < hi`, take `mid = (lo + hi) // 2` and compare the window `[mid, mid + k - 1]` with the shifted window `[mid + 1, mid + k]`. The only elements that differ are `arr[mid]` and `arr[mid + k]`.
3. If `x - arr[mid] > arr[mid + k] - x`, then `arr[mid]` is farther from `x` than `arr[mid + k]`, so the window should move right: `lo = mid + 1`.
4. Otherwise (including ties, which favor the smaller value) the window can start at `mid` or earlier: `hi = mid`.
5. Return `arr[lo : lo + k]`.

## Code

```python
# Log(n) + k
# More code but also more intuitive
class Solution:
    def findClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:
        l, r = 0, len(arr) - 1

        # Find index of x or the closest val to x
        val, idx = arr[0], 0
        while l <= r:
            m = (l + r) // 2
            curDiff, resDiff = abs(arr[m] - x), abs(val - x)
            if curDiff < resDiff or (curDiff == resDiff and arr[m] < val):
                val, idx = arr[m], m

            if arr[m] < x:
                l = m + 1
            elif arr[m] > x:
                r = m - 1
            else:
                break

        l = r = idx
        for i in range(k - 1):
            if l == 0:
                r += 1
            elif r == len(arr) - 1 or x - arr[l - 1] <= arr[r + 1] - x:
                l -= 1
            else:
                r += 1
        return arr[l : r + 1]


# Log(n-k) + k
# Elegant but very difficult to understand
class Solution:
    def findClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:
        l, r = 0, len(arr) - k

        while l < r:
            m = (l + r) // 2
            if x - arr[m] > arr[m + k] - x:
                l = m + 1
            else:
                r = m
        return arr[l : l + k]
```

## Complexity

- **Time:** `O(log(n - k) + k)` — binary search over the possible window starts, plus `k` to copy the result.
- **Space:** `O(1)` — extra space besides the output list.

## Other Approaches

- **Sort by distance:** sort elements by `(|a - x|, a)`, take the first `k`, then sort them — Time `O(n log n)` / Space `O(n)`
- **Two pointers (shrink window):** start with the full array and drop the farther endpoint until `k` elements remain — Time `O(n)` / Space `O(1)`
- **Binary search + expand:** find the insertion point of `x`, then expand outward with two pointers for `k` steps — Time `O(log n + k)` / Space `O(1)`
