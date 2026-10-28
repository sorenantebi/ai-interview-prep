---
topic: "Backtracking"
difficulty: Medium
leetcode: https://leetcode.com/problems/combination-sum-ii/
neetcode: https://neetcode.io/problems/combination-target-sum-ii
---
# Combination Sum II - Solution

**Question:** Combination Sum II - Question · **Difficulty:** Medium

## Intuition

Same backtracking as Combination Sum, but each index is used at most once (recurse with `i + 1`) and duplicates in the input must not produce duplicate combinations. After **sorting**, equal values are adjacent; at a given recursion level, picking the second copy of a value as the *next* element would rebuild exactly the subtrees already explored with the first copy, so skip it.

## Approach

1. Sort `candidates`.
2. `dfs(start, remaining)`: if `remaining == 0`, record a copy of `path`.
3. Loop `i` from `start`:
   - If `i > start` and `candidates[i] == candidates[i - 1]`, skip (same value already tried at this level).
   - If `candidates[i] > remaining`, break (sorted).
   - Append, recurse with `dfs(i + 1, remaining - candidates[i])`, pop.

## Code

```python
class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()

        res = []

        def backtrack(cur, pos, target):
            if target == 0:
                res.append(cur.copy())
                return
            if target <= 0:
                return

            prev = -1
            for i in range(pos, len(candidates)):
                if candidates[i] == prev:
                    continue
                cur.append(candidates[i])
                backtrack(cur, i + 1, target - candidates[i])
                cur.pop()
                prev = candidates[i]

        backtrack([], 0, target)
        return res
```

## Complexity

- **Time:** `O(n * 2^n)` worst case — each index is in or out, plus `O(n)` to copy a result; sorting is `O(n log n)`.
- **Space:** `O(n)` — recursion depth and path (output excluded).

## Other Approaches

- **Generate all and dedupe with a set of tuples:** explore every subset of indices and store sorted tuples — Time `O(n * 2^n)` without pruning benefits, Space `O(2^n)` for the set.
- **Counter-based DFS:** iterate over distinct values with their counts and choose how many copies to take — same worst case, naturally duplicate-free.

## Key Takeaway

Sort + "skip `nums[i] == nums[i-1]` when `i > start`" is the universal trick to deduplicate combination/subset backtracking with repeated input values.

## C++

```cpp
/*
    Given array & a target, find all unique combos that sum to target, nums can only be used once
    Ex. candidates = [10,1,2,7,6,1,5], target = 8 -> [[1,1,6],[1,2,5],[1,7],[2,6]]

    Backtracking, generate all combo sums, push/pop + index checking to explore new combos

    Time: O(2^n)
    Space: O(n)
*/

class Solution {
public:
    vector<vector<int>> combinationSum2(vector<int>& candidates, int target) {
        sort(candidates.begin(), candidates.end());
        
        vector<int> curr;
        vector<vector<int>> result;
        
        dfs(candidates, target, 0, 0, curr, result);
        return result;
    }
private:
    void dfs(vector<int>& candidates, int target, int sum, int start, vector<int>& curr, vector<vector<int>>& result) {
        if (sum > target) {
            return;
        }
        if (sum == target) {
            result.push_back(curr);
            return;
        }
        for (int i = start; i < candidates.size(); i++) {
            if (i > start && candidates[i] == candidates[i - 1]) {
                continue;
            }
            curr.push_back(candidates[i]);
            dfs(candidates, target, sum + candidates[i], i + 1, curr, result);
            curr.pop_back();
        }
    }
};
```
