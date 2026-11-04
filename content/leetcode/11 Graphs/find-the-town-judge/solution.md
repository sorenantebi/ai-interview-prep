---
topic: "Graphs"
difficulty: Easy
leetcode: https://leetcode.com/problems/find-the-town-judge/
neetcode: https://neetcode.io/problems/find-the-town-judge
---
# Find the Town Judge - Solution

## Intuition

Model the trust relationships as a directed graph where `a -> b` means `a` trusts `b`. The judge is the node with out-degree `0` and in-degree `n - 1`. Tracking a single score per person (in-degree minus out-degree) is enough: only the judge can reach a score of `n - 1`.

## Approach

1. Create a `score` array of size `n + 1`, initialized to `0`.
2. For each pair `[a, b]` in `trust`, decrement `score[a]` (a trusts someone) and increment `score[b]` (b is trusted).
3. Scan labels `1..n` and return the first label whose score equals `n - 1`.
4. If no label has that score, return `-1`.

A person who trusts anyone loses at least one point, so their maximum score is `n - 2`. Hence a score of `n - 1` means trusted by everyone else and trusting nobody. When `n = 1` and `trust` is empty, person `1` has score `0 == n - 1`, so the answer is `1`.

## Code

```python
class Solution:
    def findJudge(self, n: int, trust: List[List[int]]) -> int:
        delta = defaultdict(int)

        for src, dst in trust:
            delta[src] -= 1
            delta[dst] += 1

        for i in range(1, n + 1):
            if delta[i] == n - 1:
                return i
        return -1
```

## Complexity

- **Time:** `O(n + T)` — one pass over the `T` trust pairs and one pass over the `n` people.
- **Space:** `O(n)` — the score array holds one entry per person.

## Other Approaches

- **Separate in/out degree arrays:** count in-degree and out-degree independently and look for in-degree `n - 1` with out-degree `0` — Time `O(n + T)` / Space `O(n)`
- **Set of trusters:** collect everyone who trusts someone; the judge is the only person not in the set, then verify they are trusted by `n - 1` people — Time `O(n + T)` / Space `O(n)`
