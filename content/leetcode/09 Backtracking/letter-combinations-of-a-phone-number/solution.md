---
topic: "Backtracking"
difficulty: Medium
leetcode: https://leetcode.com/problems/letter-combinations-of-a-phone-number/
neetcode: https://neetcode.io/problems/combinations-of-a-phone-number
---
# Letter Combinations of a Phone Number - Solution

**Question:** Letter Combinations of a Phone Number - Question · **Difficulty:** Medium

## Intuition

Each digit is an independent choice among 3–4 letters, so the answers are the leaves of a tree with one level per digit. Backtracking picks a letter for the current digit, recurses to the next digit, and undoes the choice.

## Approach

1. If `digits` is empty, return `[]`.
2. Map each digit to its letters.
3. `dfs(i)`: if `i == len(digits)`, record `"".join(path)`.
4. Otherwise for each letter of `digits[i]`: append it, recurse with `i + 1`, pop.

## Code

```python
class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        res = []
        digitToChar = {
            "2": "abc",
            "3": "def",
            "4": "ghi",
            "5": "jkl",
            "6": "mno",
            "7": "qprs",
            "8": "tuv",
            "9": "wxyz",
        }

        def backtrack(i, curStr):
            if len(curStr) == len(digits):
                res.append(curStr)
                return
            for c in digitToChar[digits[i]]:
                backtrack(i + 1, curStr + c)

        if digits:
            backtrack(0, "")

        return res
```

## Complexity

- **Time:** `O(n * 4^n)` — up to `4^n` strings, each joined in `O(n)`.
- **Space:** `O(n)` — recursion depth and path (output excluded).

## Other Approaches

- **Iterative BFS-style expansion:** start with `[""]` and for each digit replace the list with every prefix extended by each letter — same Time, Space output-sized.
- **Cartesian product:** `["".join(p) for p in itertools.product(*(keypad[d] for d in digits))]` — same complexity.

## Key Takeaway

When each position has an independent set of options, the answer is a Cartesian product — backtracking with one recursion level per position generates it cleanly.

## C++

```cpp
/*
    Given cell phone pad, return all possible letter combos that the number could represent
    Ex. digits = "23" -> ["ad","ae","af","bd","be","bf","cd","ce","cf"]

    Hash map all digits to letters, add 1 letter at a time for each digit, then backtrack undo

    Time: O(n x 4^n)
    Space: O(n x 4^n)
*/

class Solution {
public:
    vector<string> letterCombinations(string digits) {
        if (digits.empty()) {
            return {};
        }
        
        unordered_map<char, string> m = {
            {'2', "abc"},
            {'3', "def"},
            {'4', "ghi"},
            {'5', "jkl"},
            {'6', "mno"},
            {'7', "pqrs"},
            {'8', "tuv"},
            {'9', "wxyz"}
        };
        string curr = "";
        vector<string> result;
        
        dfs(digits, 0, m, curr, result);
        return result;
    }
private:
    void dfs(string digits, int index, unordered_map<char, string>& m, string& curr, vector<string>& result) {
        if (index == digits.size()) {
            result.push_back(curr);
            return;
        }
        string str = m[digits[index]];
        for (int i = 0; i < str.size(); i++) {
            curr.push_back(str[i]);
            dfs(digits, index + 1, m, curr, result);
            curr.pop_back();
        }
    }
};
```
