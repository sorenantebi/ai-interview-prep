---
topic: "Binary Search"
difficulty: Medium
leetcode: https://leetcode.com/problems/search-in-rotated-sorted-array-ii/
neetcode: https://neetcode.io/problems/search-in-rotated-sorted-array-ii
---
# Search in Rotated Sorted Array II - Solution

## Intuition

In a rotated sorted array, at least one half around any midpoint is still sorted. We can check whether the target lies within the sorted half and discard the other half. Duplicates break this only when `nums[lo] == nums[mid] == nums[hi]`: then we cannot tell which half is sorted, so we shrink the window by one from each end and continue.

## Approach

1. Set `lo = 0`, `hi = len(nums) - 1`.
2. While `lo <= hi`, compute `mid`. If `nums[mid] == target`, return `True`.
3. If `nums[lo] == nums[mid] == nums[hi]`, the sorted half is ambiguous: increment `lo` and decrement `hi`, then continue.
4. Else if `nums[lo] <= nums[mid]`, the left half is sorted. If `nums[lo] <= target < nums[mid]`, search left (`hi = mid - 1`); otherwise search right (`lo = mid + 1`).
5. Otherwise the right half is sorted. If `nums[mid] < target <= nums[hi]`, search right (`lo = mid + 1`); otherwise search left (`hi = mid - 1`).
6. If the loop ends, return `False`.

## Code

```python
class Solution:
    def search(self, nums: List[int], target: int) -> bool:
        left,right = 0,len(nums) - 1
        while left <= right:
            mid = left + (right - left) // 2
            if nums[mid] == target:
                return True

            #Left sorted portion
            if nums[left] < nums[mid]:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            #Right sorted portion
            elif nums[left] > nums[mid]:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1
            else:
                left += 1
        return False
```

## Complexity

- **Time:** `O(log n)` on average, `O(n)` worst case — each step halves the range, except when many duplicates force the range to shrink by only two (e.g. `[1,1,1,1,1,1,2,1,1]`). This is the answer to the follow-up: duplicates can degrade the worst case to linear.
- **Space:** `O(1)` — only a few index variables.

## Other Approaches

- **Linear scan:** check every element with `target in nums` — Time `O(n)` / Space `O(1)`
- **Find pivot, then binary search:** locate the rotation point, then binary search the proper half; the pivot search also degrades with duplicates — Time `O(n)` worst case / Space `O(1)`
