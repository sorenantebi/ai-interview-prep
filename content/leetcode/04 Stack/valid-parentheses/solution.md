---
topic: "Stack"
difficulty: Easy
leetcode: https://leetcode.com/problems/valid-parentheses/
neetcode: https://neetcode.io/problems/validate-parentheses
---
# Valid Parentheses - Solution

**Question:** Valid Parentheses - Question · **Difficulty:** Easy

## Intuition

The bracket that must be closed next is always the most recently opened one that is still unmatched, so a stack of open brackets models the nesting exactly. Each closing bracket must match the top of the stack.

## Approach

1. Map each closing bracket to its opening partner.
2. Scan the string: push opening brackets onto the stack.
3. For a closing bracket, if the stack is empty or its top is not the matching opener, return `False`; otherwise pop.
4. At the end the string is valid only if the stack is empty (no unclosed openers).

## Code

```python
class Solution:
    def isValid(self, s: str) -> bool:
        bracketMap = {")": "(", "]": "[", "}": "{"}
        stack = []

        for c in s:
            if c not in bracketMap:
                stack.append(c)
                continue
            if not stack or stack[-1] != bracketMap[c]:
                return False
            stack.pop()

        return not stack
```

## Complexity

- **Time:** `O(n)` — single pass, O(1) work per character.
- **Space:** `O(n)` — the stack can hold every character in the worst case (e.g. all openers).

## Other Approaches

- **Repeated replacement:** keep deleting `"()"`, `"[]"`, `"{}"` substrings until nothing changes; valid iff the string becomes empty — Time `O(n^2)`, Space `O(n)`.

## Key Takeaway

Matching nested pairs = stack. Check for an empty stack both when popping and at the very end.

## C++

```cpp
/*
    Given s w/ '(, ), {, }, [, ]', determine if valid
    Ex. s = "()[]{}" -> true, s = "(]" -> false

    Stack of opens, check for matching closes & validity

    Time: O(n)
    Space: O(n)
*/

class Solution {
public:
    bool isValid(string s) {
        stack<char> open;
        unordered_map<char, char> parens = {
            {')', '('},
            {']', '['},
            {'}', '{'},
        };
        
        for (const auto& c : s) {
            if (parens.find(c) != parens.end()) {
                // if input starts with a closing bracket.
                if (open.empty()) {
                    return false;
                }

                if (open.top() != parens[c]) {
                    return false;
                }

                open.pop();
            } else {
                open.push(c);
            }
        }
        
        return open.empty();
    }
};
```
