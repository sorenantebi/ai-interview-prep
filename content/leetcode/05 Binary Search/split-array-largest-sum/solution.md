---
topic: "Binary Search"
difficulty: Hard
leetcode: https://leetcode.com/problems/split-array-largest-sum/
neetcode: https://neetcode.io/problems/split-array-largest-sum
---
# Split Array Largest Sum - Solution

## Intuition

The answer lies between `max(nums)` (every element must fit somewhere) and `sum(nums)` (one single subarray). Given a candidate limit, we can greedily check whether the array can be split into at most `k` subarrays each with sum at most that limit. Feasibility is monotonic: if a limit works, any larger limit works too. That makes it a binary search on the answer.

## Approach

1. Set `lo = max(nums)` and `hi = sum(nums)`.
2. While `lo < hi`, take `mid = (lo + hi) // 2`.
3. Greedily count the subarrays needed: extend the current subarray while its sum stays `<= mid`, otherwise start a new one.
4. If the count is `<= k`, `mid` is feasible, so set `hi = mid`. Otherwise set `lo = mid + 1`.
5. Return `lo`.

Needing fewer than `k` subarrays is fine, since any subarray can be split further without increasing the largest sum (`k <= len(nums)`), so the count `<= k` check is correct.

## Code

```python
class Solution:
    def splitArray(self, nums: List[int], m: int) -> int:
        def canSplit(largest):
            subarray = 0
            curSum = 0
            for n in nums:
                curSum += n
                if curSum > largest:
                    subarray += 1
                    curSum = n
            return subarray + 1 <= m

        l, r = max(nums), sum(nums)
        res = r
        while l <= r:
            mid = l + ((r - l) // 2)
            if canSplit(mid):
                res = mid
                r = mid - 1
            else:
                l = mid + 1
        return res
```

## Complexity

- **Time:** `O(n log S)` — binary search over the range up to `S = sum(nums)`, with an `O(n)` greedy check per step.
- **Space:** `O(1)` — only a few counters are used.

## Other Approaches

- **Dynamic programming:** `dp[i][j]` is the best largest sum splitting the first `i` elements into `j` parts, using prefix sums — Time `O(k n^2)` / Space `O(k n)`
- **Recursion with memoization:** try every cut point for the first part and recurse on the rest — Time `O(k n^2)` / Space `O(k n)`
