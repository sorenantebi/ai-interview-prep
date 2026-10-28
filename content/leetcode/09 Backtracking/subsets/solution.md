---
topic: "Backtracking"
difficulty: Medium
leetcode: https://leetcode.com/problems/subsets/
neetcode: https://neetcode.io/problems/subsets
---
# Subsets - Solution

**Question:** Subsets - Question · **Difficulty:** Medium

## Intuition

Each element is independently either **in** or **out** of a subset, so the subsets are the leaves of a binary decision tree of depth `n`. Backtracking walks this tree with one shared `path` list: choose to include `nums[i]`, recurse, undo the choice, then recurse without it.

## Approach

1. Define `dfs(i)` which decides about `nums[i]` given the current `path`.
2. If `i == len(nums)`, record a copy of `path` as a subset.
3. Otherwise: append `nums[i]`, call `dfs(i + 1)`, pop it (backtrack), and call `dfs(i + 1)` again to skip it.
4. Start with `dfs(0)` and return the collected subsets.

## Code

```python
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res = []

        subset = []

        def dfs(i):
            if i >= len(nums):
                res.append(subset.copy())
                return
            # decision to include nums[i]
            subset.append(nums[i])
            dfs(i + 1)
            # decision NOT to include nums[i]
            subset.pop()
            dfs(i + 1)

        dfs(0)
        return res
```

## Complexity

- **Time:** `O(n * 2^n)` — `2^n` subsets, each copied in `O(n)`.
- **Space:** `O(n)` recursion stack and path (output of size `O(n * 2^n)` not counted).

## Other Approaches

- **Iterative cascading:** start with `[[]]`; for each number, append it to a copy of every existing subset — Time `O(n * 2^n)`, Space same output.
- **Bitmask enumeration:** for `mask` in `0..2^n - 1`, include `nums[j]` when bit `j` is set — Time `O(n * 2^n)`, Space `O(1)` extra.

## Key Takeaway

The include/exclude backtracking template (append, recurse, pop, recurse) is the foundation for subsets, combinations, and many "choose some items" problems.

## C++

```cpp
/*
    Given an integer array of unique elements, return all possible subsets (the power set)
    Ex. nums = [1,2,3] -> [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]

    Backtracking, generate all combinations, push/pop + index checking to explore new combos

    Time: O(n x 2^n)
    Space: O(n)
*/

class Solution {
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        vector<int> curr;
        vector<vector<int>> result;
        dfs(nums, 0, curr, result);
        return result;
    }
private:
    void dfs(vector<int>& nums, int start, vector<int>& curr, vector<vector<int>>& result) {
        result.push_back(curr);
        for (int i = start; i < nums.size(); i++) {
            curr.push_back(nums[i]);
            dfs(nums, i + 1, curr, result);
            curr.pop_back();
        }
    }
};
```
