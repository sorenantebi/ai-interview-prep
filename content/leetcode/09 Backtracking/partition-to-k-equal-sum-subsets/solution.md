---
topic: "Backtracking"
difficulty: Medium
leetcode: https://leetcode.com/problems/partition-to-k-equal-sum-subsets/
neetcode: https://neetcode.io/problems/partition-to-k-equal-sum-subsets
---
# Partition to K Equal Sum Subsets - Solution

## Intuition

If the total is not divisible by `k`, the answer is false. Otherwise each subset must sum to `target = sum / k`. Since all values are positive, we can fill one bucket at a time: pick unused elements until the bucket reaches `target`, then start the next bucket. With only 16 elements, a bitmask over used elements makes memoization cheap, because the current bucket's partial sum is fully determined by the mask (`sum(used) % target`).

## Approach

1. Compute `total`. If `total % k != 0` or `max(nums) > total // k`, return false.
2. Sort `nums` in descending order so large elements fail fast.
3. Run a DFS over a bitmask `mask` of used elements, with the current bucket's sum `cur`.
4. When `cur == target`, reset `cur` to 0 (a new bucket begins). When all bits are set, return true.
5. For each unused element `i` with `cur + nums[i] <= target`, mark it used and recurse.
6. Memoize failed masks, since `cur` is derived from `mask`, so a mask that failed once always fails.

## Code

```python
class Solution(object):
    def canPartitionKSubsets(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: bool
        """

        if sum(nums) % k != 0:
            return False

        nums.sort(reverse = True)
        target = sum(nums) / k
        visited= set()

        def backtrack(idx, count, currSum):
            if count == k:
                return True

            if target == currSum:
                return backtrack(0, count + 1, 0)

            for i in range(idx, len(nums)):
                
                # skip duplicates if last same number was skipped
                if i > 0 and (i - 1) not in visited and nums[i] == nums[i - 1]:
                    continue

                if i in visited or currSum + nums[i] > target:
                    continue

                visited.add(i)

                if backtrack(i + 1, count, currSum + nums[i]):
                    return True
                
                visited.remove(i)

            return False


        return backtrack(0, 0, 0)
```

## Complexity

- **Time:** `O(2^n * n)` — each mask is expanded at most once thanks to memoization, and each expansion scans `n` elements.
- **Space:** `O(2^n)` — the set of failed masks plus recursion depth of `n`.

## Other Approaches

- **Backtracking over k buckets:** assign each element to one of `k` buckets with pruning (skip equal bucket sums) — Time `O(k^n)` worst case / Space `O(n + k)`
- **Bottom-up bitmask DP:** `dp[mask]` stores the current bucket's partial sum or -1 if unreachable — Time `O(2^n * n)` / Space `O(2^n)`
- **Fill one bucket at a time with start index:** recurse on combinations that reach `target`, then repeat for `k-1` — Time `O(k * 2^n)` / Space `O(n)`
