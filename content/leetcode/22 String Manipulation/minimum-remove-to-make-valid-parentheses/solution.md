---
topic: "String Manipulation"
difficulty: Medium
leetcode: https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses/
---
# Minimum Remove to Make Valid Parentheses - Solution

## Intuition

A parenthesis is invalid in exactly two cases: a `')'` with no earlier unmatched `'('`, or a `'('` that never gets closed. A stack of indices of open parentheses finds both kinds in a single pass, and anything flagged is simply dropped.

## Approach

1. Convert `s` to a list of characters so individual positions can be blanked out.
2. Scan left to right, keeping a stack of indices of unmatched `'('`.
3. On `'('`, push its index.
4. On `')'`, pop if the stack is non-empty (it matches an open parenthesis). Otherwise this `')'` is unmatched, so mark it for removal.
5. After the scan, every index left on the stack is an unmatched `'('`; mark those for removal too.
6. Join the characters that were not marked.

## Code

```python
from typing import List, Optional

class Solution:
    def minRemoveToMakeValid(self, s: str) -> str:
        chars = list(s)
        stack = []
        for i, c in enumerate(chars):
            if c == '(':
                stack.append(i)
            elif c == ')':
                if stack:
                    stack.pop()
                else:
                    chars[i] = ''  # unmatched closing parenthesis
        for i in stack:
            chars[i] = ''  # unmatched opening parenthesis
        return ''.join(chars)
```

## Complexity

- **Time:** `O(n)` — one pass over the string, a second pass over the stack (at most `n` items), and one join.
- **Space:** `O(n)` — the character list and the stack.

## Other Approaches

- **Two-pass without a stack:** a left-to-right pass drops surplus `')'` using an open counter, then a right-to-left pass drops surplus `'('` — Time `O(n)` / Space `O(n)`.
- **Brute force:** try removing every subset of parentheses and keep the longest valid result — Time `O(2^n · n)` / Space `O(n)`.

## C++

```cpp
/*
* [1249] Minimum Remove to Make Valid Parentheses *

Given a string s of '(' , ')' and lowercase English characters.

Your task is to remove the minimum number of parentheses ( '(' or ')', in any positions ) so that the resulting parentheses string is valid and return any valid string.

Formally, a parentheses string is valid if and only if:

    It is the empty string, contains only lowercase characters, or
    It can be written as AB (A concatenated with B), where A and B are valid strings, or
    It can be written as (A), where A is a valid string.

Example 1:

Input: s = "lee(t(c)o)de)"
Output: "lee(t(c)o)de"
Explanation: "lee(t(co)de)" , "lee(t(c)ode)" would also be accepted.

Time: O(n)
Space: O(n)

Runtime: 14 ms, faster than 98.14% of C++ online submissions for Minimum Remove to Make Valid Parentheses.
Memory Usage: 14.2 MB, less than 10.57% of C++ online submissions for Minimum Remove to Make Valid Parentheses.
*/



class Solution {
public:
    string minRemoveToMakeValid(string s) {
        stack<pair<char,int>> st;
        
        for (int i = 0; i < s.size(); i++) {
            if (s[i] == '(') {
                st.push(make_pair(s[i], i));
            } else if (s[i] == ')') {
                if (!st.empty() and st.top().first == '(') {
                    st.pop();                
                } else {
                    st.push(make_pair(')', i));
                }
            }
        }

        while (!st.empty()) {
            s.erase(s.begin() + st.top().second);
            st.pop();
        }

        return s;
    }
};
```
