---
topic: "Binary Search"
difficulty: Easy
leetcode: https://leetcode.com/problems/binary-search/
neetcode: https://neetcode.io/problems/binary-search
---
# Binary Search - Solution

**Question:** Binary Search - Question · **Difficulty:** Easy

## Intuition

Because the array is sorted, comparing `target` with the middle element tells us which half can contain it, so we discard half of the remaining range on each step.

## Approach

1. Set `lo = 0`, `hi = n - 1` (inclusive bounds).
2. While `lo <= hi`: compute `mid`.
3. If `nums[mid] == target` return `mid`; if smaller, search right (`lo = mid + 1`); otherwise search left (`hi = mid - 1`).
4. If the loop ends, return `-1`.

## Code

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums) - 1

        while l <= r:
            m = l + ((r - l) // 2)  # (l + r) // 2 can lead to overflow
            if nums[m] > target:
                r = m - 1
            elif nums[m] < target:
                l = m + 1
            else:
                return m
        return -1
```

## Complexity

- **Time:** `O(log n)` — the search range halves every iteration.
- **Space:** `O(1)` — only a few indices.

## Other Approaches

- **Linear scan:** check every element — Time `O(n)`, Space `O(1)`.
- **`bisect_left`:** find the insertion point and check if it holds `target` — Time `O(log n)`, Space `O(1)`.

## Key Takeaway

Pick an invariant (here: inclusive `[lo, hi]` with `lo <= hi`) and keep the updates consistent with it (`mid ± 1`) to avoid off-by-one bugs and infinite loops.
