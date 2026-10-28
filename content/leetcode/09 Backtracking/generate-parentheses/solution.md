---
topic: "Backtracking"
difficulty: Medium
leetcode: https://leetcode.com/problems/generate-parentheses/
neetcode: https://neetcode.io/problems/generate-parentheses
---
# Generate Parentheses - Solution

**Question:** Generate Parentheses - Question · **Difficulty:** Medium

## Intuition

Build the string one character at a time and only make moves that can still lead to a valid string: add `'('` while fewer than `n` have been used, and add `')'` only while it would close an open parenthesis (`close < open`). Every leaf of this pruned tree is a valid string, so no filtering is needed.

## Approach

1. `dfs(open, close)` with a shared `path` list.
2. If `len(path) == 2n`, record `"".join(path)`.
3. If `open < n`: append `'('`, recurse with `open + 1`, pop.
4. If `close < open`: append `')'`, recurse with `close + 1`, pop.

## Code

```python
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        stack = []
        res = []

        def backtrack(openN, closedN):
            if openN == closedN == n:
                res.append("".join(stack))
                return

            if openN < n:
                stack.append("(")
                backtrack(openN + 1, closedN)
                stack.pop()
            if closedN < openN:
                stack.append(")")
                backtrack(openN, closedN + 1)
                stack.pop()

        backtrack(0, 0)
        return res
```

## Complexity

- **Time:** `O(4^n / sqrt(n))` — the number of results is the `n`-th Catalan number, each built in `O(n)`.
- **Space:** `O(n)` — recursion depth and path (output excluded).

## Other Approaches

- **Brute force:** generate all `2^(2n)` strings and keep the valid ones — Time `O(n * 4^n)`, Space `O(n)`.
- **DP by closure number:** every valid string is `"(" + A + ")" + B` with `|A| + |B| = n - 1` pairs; combine smaller results — same output-bound complexity.

## Key Takeaway

Backtrack with constraints that keep every partial state valid (`open <= n`, `close <= open`) so you never generate invalid candidates.

## C++

```cpp
/*
    Given n pairs of parentheses, generate all combos of well-formed parentheses
    Ex. n = 3 -> ["((()))","(()())","(())()","()(())","()()()"], n = 1 -> ["()"]

    Backtracking, keep valid, favor trying opens, then try closes if still valid

    Time: O(2^n)
    Space: O(n)
*/

class Solution {
public:
    vector<string> generateParenthesis(int n) {
        vector<string> result;
        generate(n, 0, 0, "", result);
        return result;
    }
private:
    void generate(int n, int open, int close, string str, vector<string>& result) {
        if (open == n && close == n) {
            result.push_back(str);
            return;
        }
        if (open < n) {
            generate(n, open + 1, close, str + '(', result);
        }
        if (open > close) {
            generate(n, open, close + 1, str + ')', result);
        }
    }
};

/*
    Using a single stack without recursion

    Time: O(2^n)
    Space: O(n)
*/
class Solution {
public:
    vector<string> generateParenthesis(int n) {
        stack<vector<string>> stk;
        vector<string> result;
        stk.push({"(", "1", "0"}); // {string, left_count, right_count}

        while (!stk.empty()) {
            for (int i = 0; i < stk.size(); i++) {
                vector<string> item = stk.top();
                stk.pop();
                int left = stoi(item[1]), right = stoi(item[2]);
                if (left == n && right == n) {
                    result.push_back(item[0]);
                    continue;
                }
                if (left < n) {
                    stk.push({item[0] + "(", to_string(++left), to_string(right)});
                    left--; // reverse left count
                }
                if (left > right) {
                    stk.push({item[0] + ")", to_string(left), to_string(++right)});
                }
            }
        }
        return result;
    }
};
```
