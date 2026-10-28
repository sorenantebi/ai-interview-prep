---
topic: "Backtracking"
difficulty: Medium
leetcode: https://leetcode.com/problems/combination-sum/
neetcode: https://neetcode.io/problems/combination-target-sum
---
# Combination Sum - Solution

**Question:** Combination Sum - Question · **Difficulty:** Medium

## Intuition

Build combinations in **non-decreasing index order** so each multiset is generated exactly once: at each step we may reuse the current candidate or move on to later ones, but never go back. Sorting the candidates lets us stop exploring as soon as a candidate exceeds the remaining target.

## Approach

1. Sort `candidates`.
2. `dfs(start, remaining)`: if `remaining == 0`, record a copy of `path`.
3. Otherwise for each index `i` from `start`: if `candidates[i] > remaining`, break (all later ones are larger).
4. Append `candidates[i]`, recurse with `dfs(i, remaining - candidates[i])` (same `i` allows reuse), then pop.

## Code

```python
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        res = []

        def dfs(i, cur, total):
            if total == target:
                res.append(cur.copy())
                return
            if i >= len(candidates) or total > target:
                return

            cur.append(candidates[i])
            dfs(i, cur, total + candidates[i])
            cur.pop()
            dfs(i + 1, cur, total)

        dfs(0, [], 0)
        return res
```

## Complexity

- **Time:** `O(N^(T/m + 1))` in the worst case, where `N` = number of candidates, `T` = target, `m` = smallest candidate (depth of the tree is at most `T/m`); pruning makes it much faster in practice.
- **Space:** `O(T/m)` — recursion depth and path length (output excluded).

## Other Approaches

- **Include/exclude binary tree:** at each index either take `candidates[i]` again (stay at `i`) or skip to `i + 1` — same complexity, slightly different tree shape.
- **DP over targets:** `dp[t]` = list of combinations summing to `t`, built candidate by candidate to avoid permutations — Time/Space proportional to the output size times `T`.

## Key Takeaway

To avoid duplicate combinations, only pick candidates at index `>= start`; pass `i` (not `i + 1`) when reuse is allowed, and sort to enable early `break` pruning.

## C++

```cpp
/*
    Given distinct int array & a target, return list of all unique combos that sum to target
    Ex. candidates = [2,3,6,7] target = 7 -> [[2,2,3],[7]]

    Backtracking, generate all combo sums, push/pop + index checking to explore new combos

    Time: O(2^target)
    Space: O(target)
*/

class Solution {
public:
    vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
        std::vector<int> curr;
        std::vector<std::vector<int>> res;
        helper(candidates, target, 0, curr, res);
        return res;
    }
private:
    void helper(std::vector<int>& cands, int target, int i, std::vector<int>& curr,  std::vector<std::vector<int>>& res) {
        if (i >= cands.size() || target < 0)
            return;

        if (target == 0) {
            res.push_back(curr);
            return;
        }

        curr.push_back(cands[i]);
        
        helper(cands, target - cands[i], i, curr, res);

        curr.pop_back();

        helper(cands, target, i + 1, curr, res);
    }
};
```
