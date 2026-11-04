---
topic: "Advanced Graphs"
difficulty: Hard
leetcode: https://leetcode.com/problems/greatest-common-divisor-traversal/
neetcode: https://neetcode.io/problems/greatest-common-divisor-traversal
---
# Greatest Common Divisor Traversal - Solution

## Intuition

Two numbers are connected exactly when they share a prime factor. Instead of testing all pairs of indices (too slow), connect each number to its prime factors using a Union-Find structure. Numbers sharing a prime end up in the same component. The answer is true iff all indices end up in one component.

## Approach

1. If `len(nums) == 1`, return `True`.
2. If any number equals `1`, return `False` (it has no prime factors, so it cannot connect to anything).
3. Build a smallest-prime-factor (SPF) sieve up to `max(nums)`.
4. Create a Union-Find over `n` index nodes plus extra nodes for each prime value (indexed by the prime itself, offset by `n`).
5. For each index `i`, factorize `nums[i]` with the sieve and union `i` with each of its prime factors.
6. Check that all indices share the same root.

## Code

```python
class UnionFind:
    def __init__(self, n):
        self.par = [i for i in range(n)]
        self.size = [1] * n
        self.count = n

    def find(self, x):
        if self.par[x] != x:
            self.par[x] = self.find(self.par[x])
        return self.par[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return
        if self.size[px] < self.size[py]:
            self.par[px] = py
            self.size[py] += self.size[px]
        else:
            self.par[py] = px
            self.size[px] += self.size[py]
        self.count -=1

class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        uf = UnionFind(len(nums))

        factor_index = {}
        for i, n in enumerate(nums):
            f = 2
            while f * f <= n:
                if n % f == 0:
                    if f in factor_index:
                        uf.union(i, factor_index[f])
                    else:
                        factor_index[f] = i
                    while n % f == 0:
                        n = n // f
                f += 1
            if n > 1:
                if n in factor_index:
                    uf.union(i, factor_index[n])
                else:
                    factor_index[n] = i
        return uf.count == 1
```

## Complexity

- **Time:** `O(M log log M + N log M · α(N + M))` — the sieve costs `O(M log log M)`, and each number has at most `O(log M)` prime factors to union.
- **Space:** `O(N + M)` — the SPF table and the Union-Find array.

## Other Approaches

- **BFS/DFS on a prime-index bipartite graph:** build adjacency between indices and their primes, then traverse from index 0 and check all indices are visited — Time `O(M log log M + N log M)` / Space `O(N + M)`
- **Brute-force pairwise gcd:** compare every pair of indices and union those with `gcd > 1` — Time `O(N² log M)` / Space `O(N)` (too slow for the constraints)
