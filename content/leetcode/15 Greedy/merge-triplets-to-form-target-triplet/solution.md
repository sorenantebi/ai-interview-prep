---
topic: "Greedy"
difficulty: Medium
leetcode: https://leetcode.com/problems/merge-triplets-to-form-target-triplet/
neetcode: https://neetcode.io/problems/merge-triplets-to-form-target
---
# Merge Triplets to Form Target Triplet - Solution

**Question:** Merge Triplets to Form Target Triplet - Question · **Difficulty:** Medium

## Intuition

Merging takes element-wise maxima, so values can only grow. Any triplet with a coordinate **larger** than the target's can never be used (it would overshoot permanently). Among the remaining "safe" triplets, merging all of them is harmless, so we just need each target coordinate to be matched exactly by at least one safe triplet.

## Approach

1. Keep a set `found` of coordinate indices matched so far.
2. For each triplet `t`: skip it if any `t[k] > target[k]`.
3. Otherwise, for each `k` with `t[k] == target[k]`, add `k` to `found`.
4. Return `len(found) == 3`.

## Code

```python
class Solution:
    def mergeTriplets(self, triplets: List[List[int]], target: List[int]) -> bool:
        good = set()

        for t in triplets:
            if t[0] > target[0] or t[1] > target[1] or t[2] > target[2]:
                continue
            for i, v in enumerate(t):
                if v == target[i]:
                    good.add(i)
        return len(good) == 3
```

## Complexity

- **Time:** `O(n)` — one pass over the triplets.
- **Space:** `O(1)` — the set holds at most 3 indices.

## Other Approaches

- **Merge all safe triplets:** element-wise max of all safe triplets and compare to `target` — Time `O(n)`, Space `O(1)`; equivalent formulation.

## Key Takeaway

With monotone (max-only) merge operations, discard anything that exceeds the goal, then check whether the safe items together cover every component.
