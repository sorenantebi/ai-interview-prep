---
topic: "Backtracking"
difficulty: Medium
leetcode: https://leetcode.com/problems/permutations/
neetcode: https://neetcode.io/problems/permutations
---
# Permutations - Solution

**Question:** Permutations - Question · **Difficulty:** Medium

## Intuition

A permutation is built position by position: at each step choose any element not yet used. Backtracking explores this tree with a `used` marker per element — mark, recurse, unmark. The leaves (paths of length `n`) are exactly the `n!` permutations.

## Approach

1. Keep `path` and a boolean array `used`.
2. `dfs()`: if `len(path) == n`, record a copy.
3. Otherwise, for each index `i` not used: mark it, append `nums[i]`, recurse, then pop and unmark.

## Code

```python
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        res = []

        # base case
        if len(nums) == 1:
            return [nums[:]]  # nums[:] is a deep copy

        for i in range(len(nums)):
            n = nums.pop(0)
            perms = self.permute(nums)

            for perm in perms:
                perm.append(n)
            res.extend(perms)
            nums.append(n)
        return res
```

## Complexity

- **Time:** `O(n * n!)` — `n!` permutations, each copied in `O(n)` (each node also scans `n` indices).
- **Space:** `O(n)` — recursion depth, `path`, and `used` (output excluded).

## Other Approaches

- **In-place swapping:** at depth `d`, swap each `nums[i]` (`i >= d`) into position `d`, recurse, swap back — Time `O(n * n!)`, Space `O(n)` recursion, no `used` array.
- **Insertion build-up:** for each new number, insert it into every position of every permutation built so far — Time `O(n * n!)`, Space output-sized.

## Key Takeaway

Permutations = backtracking over positions with a `used` set (or swap-in-place); unlike combinations there is no `start` index because order matters.

## C++

```cpp
/*
    Given array of distinct integers, return all the possible permutations
    Ex. nums = [1,2,3] -> [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

    Permute by swapping i/start, DFS from this point, backtrack to undo swap

    Time: O(n x n!)
    Space: O(n!)
*/

class Solution {
public:
    vector<vector<int>> permute(vector<int>& nums) {
        vector<vector<int>> result;
        dfs(nums, 0, result);
        return result;
    }
private:
    void dfs(vector<int>& nums, int start, vector<vector<int>>& result) {
        if (start == nums.size()) {
            result.push_back(nums);
            return;
        }
        for (int i = start; i < nums.size(); i++) {
            swap(nums[i], nums[start]);
            dfs(nums, start + 1, result);
            swap(nums[i], nums[start]);
        }
    }
};
```
