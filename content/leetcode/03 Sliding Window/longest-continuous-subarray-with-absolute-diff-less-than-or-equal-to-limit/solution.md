---
topic: "Sliding Window"
difficulty: Medium
leetcode: https://leetcode.com/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/
neetcode: https://neetcode.io/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit
---
# Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit - Solution

## Intuition

Every pair in a window differs by at most `limit` exactly when `max - min <= limit`. So we only need to track the window's maximum and minimum. If the window is valid, growing it on the right may break it, and shrinking it from the left can only help, which makes this a classic sliding window. Monotonic deques give the current max and min in O(1).

## Approach

1. Keep two deques of indices: `max_q` (values decreasing) and `min_q` (values increasing). Their fronts are the window's max and min.
2. For each right index `r`, pop from the back of each deque while the new value dominates the back element, then push `r`.
3. While `nums[max_q[0]] - nums[min_q[0]] > limit`, advance the left pointer `l`. Drop deque fronts whose index is now `< l`.
4. The window `[l, r]` is valid; update the best length with `r - l + 1`.
5. Return the best length.

## Code

```python
from typing import List, Optional
from collections import deque

class Solution:
    def longestSubarray(self, nums: List[int], limit: int) -> int:
        max_q = deque()
        min_q = deque()
        l = 0
        best = 0
        for r, x in enumerate(nums):
            while max_q and nums[max_q[-1]] <= x:
                max_q.pop()
            max_q.append(r)
            while min_q and nums[min_q[-1]] >= x:
                min_q.pop()
            min_q.append(r)
            while nums[max_q[0]] - nums[min_q[0]] > limit:
                l += 1
                # expire indices that left the window
                if max_q[0] < l:
                    max_q.popleft()
                if min_q[0] < l:
                    min_q.popleft()
            best = max(best, r - l + 1)
        return best
```

## Complexity

- **Time:** `O(n)` — each index is pushed and popped at most once per deque, and `l` and `r` each move at most `n` steps.
- **Space:** `O(n)` — the deques can hold up to `n` indices (for example, a monotonic input).

## Other Approaches

- **Two heaps with lazy deletion:** a max-heap and a min-heap of `(value, index)`, discarding stale tops when they fall outside the window — Time `O(n log n)` / Space `O(n)`
- **Sorted multiset / balanced BST:** insert and remove window values and read the min and max — Time `O(n log n)` / Space `O(n)`
- **Brute force:** check the max and min of every subarray — Time `O(n^2)` / Space `O(1)`
