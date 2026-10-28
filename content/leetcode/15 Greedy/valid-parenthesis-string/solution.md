---
topic: "Greedy"
difficulty: Medium
leetcode: https://leetcode.com/problems/valid-parenthesis-string/
neetcode: https://neetcode.io/problems/valid-parenthesis-string
---
# Valid Parenthesis String - Solution

**Question:** Valid Parenthesis String - Question · **Difficulty:** Medium

## Intuition

Instead of trying all choices for each `'*'`, track the **range** of possible open-paren counts: `lo` (fewest opens, treating stars as `')'` when possible) and `hi` (most opens, treating stars as `'('`). If `hi` ever drops below 0, there are too many `')'`. Clamp `lo` at 0 (we never need negative opens). The string is valid iff `lo == 0` at the end.

## Approach

1. `lo = hi = 0`.
2. For each char:
   - `'('`: `lo += 1`, `hi += 1`.
   - `')'`: `lo -= 1`, `hi -= 1`.
   - `'*'`: `lo -= 1`, `hi += 1`.
   - If `hi < 0`, return `False`. Set `lo = max(lo, 0)`.
3. Return `lo == 0`.

## Code

```python
# Dynamic Programming: O(n^2)
class Solution:
    def checkValidString(self, s: str) -> bool:
        dp = {(len(s), 0): True}  # key=(i, leftCount) -> isValid

        def dfs(i, left):
            if i == len(s) or left < 0:
                return left == 0
            if (i, left) in dp:
                return dp[(i, left)]

            if s[i] == "(":
                dp[(i, left)] = dfs(i + 1, left + 1)
            elif s[i] == ")":
                dp[(i, left)] = dfs(i + 1, left - 1)
            else:
                dp[(i, left)] = (
                    dfs(i + 1, left + 1) or dfs(i + 1, left - 1) or dfs(i + 1, left)
                )
            return dp[(i, left)]

        return dfs(0, 0)


# Greedy: O(n)
class Solution:
    def checkValidString(self, s: str) -> bool:
        leftMin, leftMax = 0, 0

        for c in s:
            if c == "(":
                leftMin, leftMax = leftMin + 1, leftMax + 1
            elif c == ")":
                leftMin, leftMax = leftMin - 1, leftMax - 1
            else:
                leftMin, leftMax = leftMin - 1, leftMax + 1
            if leftMax < 0:
                return False
            if leftMin < 0:  # required because -> s = ( * ) (
                leftMin = 0
        return leftMin == 0
```

## Complexity

- **Time:** `O(n)` — single pass.
- **Space:** `O(1)` — two counters.

## Other Approaches

- **Two stacks:** stack of `'('` indices and of `'*'` indices; match `')'` with `'('` first, then `'*'`; finally match leftover `'('` with later `'*'` — Time `O(n)`, Space `O(n)`.
- **DP / memoized DFS on `(i, open_count)`:** try all three meanings for `'*'` — Time `O(n^2)`, Space `O(n^2)`.

## Key Takeaway

When wildcards create many possibilities for a counter, track the feasible interval `[lo, hi]` instead of each possibility.

## C++

```cpp
class Solution {
public:
    bool checkValidString(string s) {
        int n = s.size();
    
        int balanced = 0;
        for(int i=0; i<n; i++) {
            if(s[i] == '(' || s[i] == '*') 
                balanced++;
            else 
                balanced--;

            if(balanced < 0) 
                return false;
        }

        if(balanced == 0) 
            return true;

        balanced = 0;
        for(int i=n-1; i>=0; i--) {
            if(s[i] == ')' || s[i] == '*') 
                balanced++;
            else 
                balanced--;

            if(balanced < 0) 
                return false;
        }

        return true;
    }
};
```
