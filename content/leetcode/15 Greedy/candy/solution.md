---
topic: "Greedy"
difficulty: Hard
leetcode: https://leetcode.com/problems/candy/
neetcode: https://neetcode.io/problems/candy
---
# Candy - Solution

## Intuition

Each child's constraint involves two neighbors, which is hard to satisfy in a single pass. Split it into two independent one-sided rules: a child must beat the left neighbor if rated higher, and must beat the right neighbor if rated higher. Satisfy each rule with its own sweep, then take the max per child, which satisfies both rules with the fewest candies.

## Approach

1. Initialize `candies` with 1 for every child.
2. Sweep left to right: if `ratings[i] > ratings[i-1]`, set `candies[i] = candies[i-1] + 1`.
3. Sweep right to left: if `ratings[i] > ratings[i+1]`, set `candies[i] = max(candies[i], candies[i+1] + 1)`.
4. Return the sum of `candies`.

## Code

```python
class Solution:
    def candy(self, ratings: List[int]) -> int:
        n = len(ratings)
        # Initialize with one candy becuase each child must have at least one candy.
        candies = [1] * n 

        # Iterate from left to right 
        for i in range(1, n):
            # Check if current rating is greater than left neighbor
            if ratings[i] > ratings[i - 1]:
                # Rating is higher so deserves more candy than left neighbor
                candies[i] = candies[i - 1] + 1

        # Iterate from right to left
        for i in range(n - 2, -1, -1):
            # Check if current rating is greater than right neighbor
            if ratings[i] > ratings[i + 1]:
                # Take max to check if the value is already greater than its right neighbor + 1.
                candies[i] = max(candies[i], candies[i + 1] + 1)
        
        return sum(candies)
```

## Complexity

- **Time:** `O(n)` — two linear passes plus a sum.
- **Space:** `O(n)` — the `candies` array.

## Other Approaches

- **Single pass with slope counting:** track the lengths of the current increasing and decreasing runs and add candies per run, adjusting for the peak — Time `O(n)` / Space `O(1)`
- **Brute-force relaxation:** repeatedly scan and fix violated neighbor constraints until nothing changes — Time `O(n^2)` / Space `O(n)`
