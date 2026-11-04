---
topic: "Stack"
difficulty: Medium
leetcode: https://leetcode.com/problems/decode-string/
neetcode: https://neetcode.io/problems/decode-string
---
# Decode String - Solution

## Intuition

Brackets can nest, so the innermost group must be fully decoded before the group that contains it can be repeated. That last-opened, first-closed order is what a stack handles. When we meet `[`, we save the work in progress and start fresh; when we meet `]`, we finish the current group and merge it back into the saved one.

## Approach

1. Keep `cur` (the string being built at the current depth) and `num` (the repeat count being read).
2. Scan the characters of `s`:
   - Digit: extend `num` (counts can have several digits).
   - `[`: push `(cur, num)` onto the stack, then reset `cur = ""` and `num = 0`.
   - `]`: pop `(prev, k)` and set `cur = prev + cur * k`.
   - Letter: append it to `cur`.
3. After the scan, `cur` is the decoded string.

## Code

```python
class Solution:
    def decodeString(self, s: str) -> str:
        stack = []

        for char in s:
            if char is not "]":
                stack.append(char)
            else:
                sub_str = ""
                while stack[-1] is not "[":
                    sub_str = stack.pop() + sub_str
                stack.pop()

                multiplier = ""
                while stack and stack[-1].isdigit():
                    multiplier = stack.pop() + multiplier

                stack.append(int(multiplier) * sub_str)

        return "".join(stack)
```

## Complexity

- **Time:** `O(n + L)` — each input character is processed once, and building the output costs time proportional to the decoded length `L` (at most `10^5`), though intermediate concatenations across nesting levels can copy strings repeatedly.
- **Space:** `O(n + L)` — the stack holds partial strings for each open bracket, bounded by the input length and the output size.

## Other Approaches

- **Two stacks (counts and strings):** same idea with separate stacks for numbers and partial strings — Time `O(n + L)` / Space `O(n + L)`
- **Recursion:** a recursive-descent parser that decodes a bracket group and returns the string and next index — Time `O(n + L)` / Space `O(n + L)` including call stack depth

## C++

```cpp
class Solution {
public:
    string decodeString(string s) {
        stack<string> stack;
        string result;

        for (int i = 0; i < s.length(); i++) {
            if (s[i] != ']') {
                stack.push(string(1, s[i]));
            } else {
                string substr;
                while (!stack.empty() && stack.top() != "[") {
                    substr = stack.top() + substr;
                    stack.pop();
                }
                stack.pop();

                string k;
                while (!stack.empty() && isdigit(stack.top()[0])) {
                    k = stack.top() + k;
                    stack.pop();
                }
                int kInt = stoi(k);

                string temp;
                for (int j = 0; j < kInt; j++) {
                    temp += substr;
                }
                stack.push(temp);
            }
        }

        while (!stack.empty()) {
            result = stack.top() + result;
            stack.pop();
        }

        return result;
    }
};
```
