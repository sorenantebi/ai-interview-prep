---
topic: "2-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/last-stone-weight-ii/
neetcode: https://neetcode.io/problems/last-stone-weight-ii
---
# Last Stone Weight II - Solution

## Intuition

Whatever order the smashes happen in, the final stone's weight equals the sum of some stones minus the sum of the others, i.e. each stone ends up with a `+` or `-` sign. So the task is to split the stones into two groups whose sums are as close as possible. This is a 0/1 knapsack (subset sum) problem: find the largest achievable subset sum not exceeding `total // 2`.

## Approach

1. Compute `total = sum(stones)` and `target = total // 2`.
2. Maintain a boolean array `dp` of size `target + 1`, where `dp[s]` says whether some subset sums to `s`. Start with `dp[0] = True`.
3. For each stone, update `dp` from high to low sums so each stone is used at most once: `dp[s] |= dp[s - stone]`.
4. Find the largest `s <= target` with `dp[s]` true.
5. The answer is `total - 2 * s`.

## Code

```python
class Solution:
    def lastStoneWeightII(self, stones: List[int]) -> int:
        # Memoization
        stoneSum = sum(stones)
        target = ceil(stoneSum / 2)

        def dfs(i, total):
            if total >= target or i == len(stones):
                return abs(total - (stoneSum - total))
            if (i, total) in dp:
                return dp[(i, total)]

            dp[(i, total)] = min(dfs(i + 1, total),
                                 dfs(i + 1, total + stones[i]))
            return dp[(i, total)]

        dp = {}
        return dfs(0, 0)
```

## Complexity

- **Time:** `O(n * S)` — `n` stones, each processed over up to `S = sum(stones) / 2` sums (at most about 1500).
- **Space:** `O(S)` — one boolean array of size `S + 1`.

## Other Approaches

- **Top-down memoization:** recurse on `(index, current sum)` and minimize `|total - 2 * subset|` — Time `O(n * S)` / Space `O(n * S)`
- **Bitset DP:** keep reachable sums as bits in one integer and OR in `bits << stone` per stone — Time `O(n * S / w)` / Space `O(S / w)`
- **Brute force:** enumerate all `2^n` sign assignments — Time `O(2^n)` / Space `O(n)`
