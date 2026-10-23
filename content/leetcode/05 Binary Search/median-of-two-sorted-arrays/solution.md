---
topic: "Binary Search"
difficulty: Hard
leetcode: https://leetcode.com/problems/median-of-two-sorted-arrays/
neetcode: https://neetcode.io/problems/median-of-two-sorted-arrays
---
# Median of Two Sorted Arrays - Solution

**Question:** Median of Two Sorted Arrays - Question · **Difficulty:** Hard

## Intuition

The median splits the merged array into a left half and a right half of (almost) equal size. If we take `i` elements from `nums1` and `j = half - i` from `nums2` for the left half, the partition is correct exactly when `A[i-1] <= B[j]` and `B[j-1] <= A[i]`. Since `i` determines `j`, we binary search `i` over the shorter array.

## Approach

1. Let `A` be the shorter array (swap if needed), `total = m + n`, `half = (total + 1) // 2`.
2. Binary search `i` in `[0, len(A)]`; set `j = half - i`.
3. Read the four boundary values, using `-inf`/`+inf` when an index is out of range: `Aleft = A[i-1]`, `Aright = A[i]`, `Bleft = B[j-1]`, `Bright = B[j]`.
4. If `Aleft <= Bright` and `Bleft <= Aright`, the partition is valid: return `max(Aleft, Bleft)` for odd `total`, else the average of `max(Aleft, Bleft)` and `min(Aright, Bright)`.
5. If `Aleft > Bright`, take fewer from `A` (`hi = i - 1`); otherwise take more (`lo = i + 1`).

## Code

```python
# Time: log(min(n, m))


class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        A, B = nums1, nums2
        total = len(nums1) + len(nums2)
        half = total // 2

        if len(B) < len(A):
            A, B = B, A

        l, r = 0, len(A) - 1
        while True:
            i = (l + r) // 2  # A
            j = half - i - 2  # B

            Aleft = A[i] if i >= 0 else float("-infinity")
            Aright = A[i + 1] if (i + 1) < len(A) else float("infinity")
            Bleft = B[j] if j >= 0 else float("-infinity")
            Bright = B[j + 1] if (j + 1) < len(B) else float("infinity")

            # partition is correct
            if Aleft <= Bright and Bleft <= Aright:
                # odd
                if total % 2:
                    return min(Aright, Bright)
                # even
                return (max(Aleft, Bleft) + min(Aright, Bright)) / 2
            elif Aleft > Bright:
                r = i - 1
            else:
                l = i + 1
```

## Complexity

- **Time:** `O(log(min(m, n)))` — binary search over the shorter array only.
- **Space:** `O(1)`.

## Other Approaches

- **Merge then pick:** two-pointer merge up to the middle index — Time `O(m + n)`, Space `O(1)` if you only track the last two values.
- **k-th smallest by elimination:** recursively discard `k/2` elements from one array — Time `O(log(m + n))`, Space `O(log(m + n))` recursion.

## Key Takeaway

Binary search a partition, not a value: choose how many elements come from the shorter array and validate with the cross-boundary conditions, padding edges with ±infinity.
