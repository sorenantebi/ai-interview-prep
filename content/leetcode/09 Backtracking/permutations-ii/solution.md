---
topic: "Backtracking"
difficulty: Medium
leetcode: https://leetcode.com/problems/permutations-ii/
neetcode: https://neetcode.io/problems/permutations-ii
---
# Permutations II - Solution

## Intuition

Build permutations position by position, as in the classic permutations problem. Duplicates cause repeated results only when the same value is chosen more than once at the same position. If we track how many copies of each distinct value remain and try each distinct value at most once per position, every permutation is generated exactly once.

## Approach

1. Count the occurrences of each distinct value with a `Counter`.
2. Use a recursive `backtrack` function that appends to a `path` list.
3. When `path` has length `len(nums)`, record a copy of it.
4. Otherwise, for each distinct value whose remaining count is positive: decrement the count, append the value, recurse, then undo both.
5. Because the loop iterates over distinct values rather than indices, duplicate branches are never created.

## Code

```python
import collections


class Solution:

    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        result = []
        counter = collections.Counter(nums)

        def backtrack(perm, counter):
            if len(perm) == len(nums):
                result.append(perm.copy())

            for n in counter:
                if counter[n] == 0:
                    continue
                perm.append(n)
                counter[n] -= 1
                backtrack(perm, counter)
                perm.pop()
                counter[n] += 1

        backtrack([], counter)

        return result
```

## Complexity

- **Time:** `O(n * n!)` — in the worst case (all values distinct) there are `n!` permutations, and copying each takes `O(n)`. With duplicates there are fewer.
- **Space:** `O(n)` — recursion depth, the `path`, and the counter are all `O(n)`, excluding the output.

## Other Approaches

- **Sort + used array:** sort `nums`, then skip `nums[i]` if it equals `nums[i-1]` and `nums[i-1]` is not currently used — Time `O(n * n!)` / Space `O(n)`
- **Swap-based backtracking with a per-level set:** swap elements into position and use a set to skip values already tried at that level — Time `O(n * n!)` / Space `O(n)`
