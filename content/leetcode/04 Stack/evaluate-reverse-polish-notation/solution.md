---
topic: "Stack"
difficulty: Medium
leetcode: https://leetcode.com/problems/evaluate-reverse-polish-notation/
neetcode: https://neetcode.io/problems/evaluate-reverse-polish-notation
---
# Evaluate Reverse Polish Notation - Solution

**Question:** Evaluate Reverse Polish Notation - Question · **Difficulty:** Medium

## Intuition

In postfix notation every operator applies to the two values produced most recently, which is exactly what a stack of operands provides. Push numbers; on an operator, pop two, combine, and push the result back.

## Approach

1. Iterate over `tokens` with an empty stack.
2. If the token is an operator, pop `b` (right operand) then `a` (left operand), compute `a op b`, and push it.
3. For `/`, use `int(a / b)` so the result truncates toward zero (Python's `//` floors instead).
4. Otherwise push `int(token)`.
5. The single remaining stack value is the answer.

## Code

```python
class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []
        for c in tokens:
            if c == "+":
                stack.append(stack.pop() + stack.pop())
            elif c == "-":
                a, b = stack.pop(), stack.pop()
                stack.append(b - a)
            elif c == "*":
                stack.append(stack.pop() * stack.pop())
            elif c == "/":
                a, b = stack.pop(), stack.pop()
                stack.append(int(float(b) / a))
            else:
                stack.append(int(c))
        return stack[0]
```

## Complexity

- **Time:** `O(n)` — each token is processed once with O(1) work.
- **Space:** `O(n)` — the operand stack can hold up to about half the tokens.

## Other Approaches

- **Recursion from the end:** read the last token; if it is an operator, recursively evaluate its right then left sub-expression — Time `O(n)`, Space `O(n)` recursion stack.

## Key Takeaway

Postfix evaluation = operand stack. Watch the operand order (`a - b`, `a / b` with `b` popped first) and Python's floor division vs. truncation.
