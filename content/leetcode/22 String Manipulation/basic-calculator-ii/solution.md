---
topic: "String Manipulation"
difficulty: Medium
leetcode: https://leetcode.com/problems/basic-calculator-ii/
---
# Basic Calculator II - Solution

## Intuition

Multiplication and division bind tighter than addition and subtraction. If we handle `*` and `/` immediately against the most recent term, then the final answer is just the sum of all terms. A stack of pending terms (or a single running "last term" variable) captures this.

## Approach

1. Scan the string left to right, building the current number `num` from consecutive digits.
2. Keep `op`, the operator that preceded `num` (initially `'+'`).
3. When reaching a non-digit, non-space character, or the end of the string, apply `op` to `num`:
   - `+`: add `num` to the running total as a new term (`last = num`).
   - `-`: new term `last = -num`.
   - `*`: `last = last * num`.
   - `/`: `last = int(last / num)`, truncating toward zero.
4. Whenever a new `+` or `-` term begins, first add the previous `last` to the total.
5. Update `op` to the current character and reset `num`.
6. At the end, return `total + last`.

## Code

```python
from typing import List, Optional

class Solution:
    def calculate(self, s: str) -> int:
        total = 0
        last = 0
        num = 0
        op = '+'
        n = len(s)
        for i, ch in enumerate(s):
            if ch.isdigit():
                num = num * 10 + int(ch)
            if (not ch.isdigit() and ch != ' ') or i == n - 1:
                if op == '+':
                    total += last
                    last = num
                elif op == '-':
                    total += last
                    last = -num
                elif op == '*':
                    last *= num
                else:
                    # truncate toward zero, not floor
                    last = abs(last) // num * (1 if last >= 0 else -1)
                op = ch
                num = 0
        return total + last
```

## Complexity

- **Time:** `O(n)` — a single pass over the string.
- **Space:** `O(1)` — only a few integer variables are kept.

## Other Approaches

- **Stack of terms:** push `num`/`-num` for `+`/`-`, pop and combine for `*`/`/`, then sum the stack — Time `O(n)` / Space `O(n)`
- **Two-stack (shunting-yard) evaluation:** separate operand and operator stacks with precedence handling, generalizes to parentheses — Time `O(n)` / Space `O(n)`
