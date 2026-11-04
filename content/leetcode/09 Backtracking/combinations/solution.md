---
topic: "Backtracking"
difficulty: Medium
leetcode: https://leetcode.com/problems/combinations/
neetcode: https://neetcode.io/problems/combinations
---
# Combinations - Solution

## Intuition

A combination is a set, so we can avoid duplicates by always picking numbers in increasing order. Build each combination one number at a time, and only consider numbers larger than the last one chosen. When the partial combination has `k` numbers, record it.

## Approach

1. Keep a `path` list for the current partial combination and a `start` value for the smallest number still allowed.
2. If `len(path) == k`, append a copy of `path` to the results and return.
3. Otherwise, loop `i` from `start` up to `n`, push `i`, recurse with `start = i + 1`, then pop `i` (backtrack).
4. Prune: if fewer than `k - len(path)` numbers remain from `i` to `n`, no valid combination can be completed, so stop the loop early.

## Code

```python
class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        res = []
        def helper(start, comb):
            if len(comb) == k:
                res.append(comb.copy())
                return
            for i in range(start, n+1):
                comb.append(i)
                helper(i+1, comb)
                comb.pop()
        helper(1, [])
        return res
```

## Complexity

- **Time:** `O(k * C(n, k))` — there are `C(n, k)` combinations and copying each into the result costs `O(k)`; pruning keeps the search from visiting dead branches.
- **Space:** `O(k)` — recursion depth and `path` hold at most `k` elements, excluding the output.

## Other Approaches

- **Backtracking without pruning:** same recursion but loops `i` up to `n`, exploring dead-end branches — Time `O(k * C(n, k))` worst case with extra overhead / Space `O(k)`
- **Iterative (lexicographic generation):** maintain a sorted index array and advance it to the next combination — Time `O(k * C(n, k))` / Space `O(k)`
- **Include/exclude recursion:** for each number decide to take it or skip it — Time `O(k * C(n, k))` or worse without pruning / Space `O(n)` recursion depth

## C++

```cpp
class Solution {
private:
    void backtrack(int start, int n, int k, vector<int> &combination, vector<vector<int>> &res){
            //base case, when size of combination is k, we wanna stop
            if(combination.size() == k){
                res.push_back(combination);
                return;
            }

            for(int i = start; i<=n; i++){
                combination.push_back(i);
                backtrack(i+1, n, k, combination, res);
                combination.pop_back();
            }
        }
public:
    vector<vector<int>> combine(int n, int k) {
        vector<vector<int>> res;

        //initial empty list to pass to the backtrack function
        vector<int> emptyCombination;

        backtrack(1, n, k, emptyCombination, res);

        return res;
    }
};
```
