---
topic: "Binary Search"
difficulty: Medium
leetcode: https://leetcode.com/problems/search-in-rotated-sorted-array/
neetcode: https://neetcode.io/problems/find-target-in-rotated-sorted-array
---
# Search In Rotated Sorted Array - Solution

**Question:** Search In Rotated Sorted Array - Question · **Difficulty:** Medium

## Intuition

Split the range at `mid`: at least one of the halves `[lo, mid]` or `[mid, hi]` is guaranteed to be sorted. If `target` lies within the value range of the sorted half, search there; otherwise it can only be in the other half. Each step still discards half the range.

## Approach

1. `lo = 0`, `hi = n - 1`; loop while `lo <= hi`.
2. Compute `mid`; return it if `nums[mid] == target`.
3. If `nums[lo] <= nums[mid]` (left half sorted): if `nums[lo] <= target < nums[mid]`, go left (`hi = mid - 1`), else go right.
4. Otherwise the right half is sorted: if `nums[mid] < target <= nums[hi]`, go right (`lo = mid + 1`), else go left.
5. Return `-1` when the range empties.

## Code

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums) - 1

        while l <= r:
            mid = (l + r) // 2
            if target == nums[mid]:
                return mid

            # left sorted portion
            if nums[l] <= nums[mid]:
                if target > nums[mid] or target < nums[l]:
                    l = mid + 1
                else:
                    r = mid - 1
            # right sorted portion
            else:
                if target < nums[mid] or target > nums[r]:
                    r = mid - 1
                else:
                    l = mid + 1
        return -1
```

## Complexity

- **Time:** `O(log n)` — one half is discarded per iteration.
- **Space:** `O(1)`.

## Other Approaches

- **Find pivot, then binary search:** locate the minimum's index (as in Find Minimum in Rotated Sorted Array), then run a normal binary search on the correct sorted side — Time `O(log n)`, Space `O(1)`.
- **Linear scan:** Time `O(n)`, Space `O(1)`.

## Key Takeaway

In a rotated sorted array, one side of `mid` is always sorted — test whether the target falls in that side's range to decide where to go.
