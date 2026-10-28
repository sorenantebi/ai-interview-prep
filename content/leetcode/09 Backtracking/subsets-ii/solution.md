---
topic: "Backtracking"
difficulty: Medium
leetcode: https://leetcode.com/problems/subsets-ii/
neetcode: https://neetcode.io/problems/subsets-ii
---
# Subsets II - Solution

**Question:** Subsets II - Question · **Difficulty:** Medium

## Intuition

Sort so equal values are adjacent, then use the "pick the next element" backtracking form where every node of the tree is a subset. At a given depth, choosing the second copy of a value as the next element would produce exactly the same subtrees as the first copy, so skip equal neighbors at the same level (`i > start and nums[i] == nums[i-1]`).

## Approach

1. Sort `nums`.
2. `dfs(start)`: record a copy of `path` (every node is a valid subset).
3. For `i` from `start` to `n - 1`: skip if `i > start` and `nums[i] == nums[i - 1]`; otherwise append `nums[i]`, recurse with `dfs(i + 1)`, pop.

## Code

```python
class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        res = []
        nums.sort()

        def backtrack(i, subset):
            if i == len(nums):
                res.append(subset[::])
                return

            # All subsets that include nums[i]
            subset.append(nums[i])
            backtrack(i + 1, subset)
            subset.pop()
            # All subsets that don't include nums[i]
            while i + 1 < len(nums) and nums[i] == nums[i + 1]:
                i += 1
            backtrack(i + 1, subset)

        backtrack(0, [])
        return res
```

## Complexity

- **Time:** `O(n * 2^n)` — at most `2^n` subsets, each copied in `O(n)`; sorting is `O(n log n)`.
- **Space:** `O(n)` — recursion depth and path (output excluded).

## Other Approaches

- **Include/exclude with skip:** if you exclude `nums[i]`, also skip all following copies of the same value — same complexity.
- **Generate all subsets and dedupe via a set of sorted tuples:** Time `O(n * 2^n)`, Space `O(n * 2^n)` for the set.

## Key Takeaway

Duplicates in subsets/combinations: sort first, then skip `nums[i] == nums[i-1]` when `i > start` — this prunes duplicate branches instead of filtering duplicate results.

## C++

```cpp
/*
    Given an integer array of unique elements, return all possible subsets (the power set)
    Ex. nums = [1,2,2] -> [[],[1],[1,2],[1,2,2],[2],[2,2]]

    Backtracking, generate all combos, push/pop + to explore new combos, skip duplicates

    Time: O(n x 2^n)
    Space: O(n)
*/

class Solution {
public:
    vector<vector<int>> subsetsWithDup(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        
        vector<int> curr;
        vector<vector<int>> result;
        
        dfs(nums, 0, curr, result);
        return result;
    }
private:
    void dfs(vector<int>& nums, int start, vector<int>& curr, vector<vector<int>>& result) {
        result.push_back(curr);
        for (int i = start; i < nums.size(); i++) {
            if (i > start && nums[i] == nums[i - 1]) {
                continue;
            }
            curr.push_back(nums[i]);
            dfs(nums, i + 1, curr, result);
            curr.pop_back();
        }
    }
};
```
