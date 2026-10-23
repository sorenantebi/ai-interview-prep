---
topic: "Stack"
difficulty: Medium
leetcode: https://leetcode.com/problems/daily-temperatures/
neetcode: https://neetcode.io/problems/daily-temperatures
---
# Daily Temperatures - Solution

**Question:** Daily Temperatures - Question · **Difficulty:** Medium

## Intuition

This is a "next greater element" problem. Keep a stack of days still waiting for a warmer day; their temperatures are non-increasing from bottom to top. When a warmer day arrives, it resolves every waiting day on top of the stack that is colder.

## Approach

1. Initialize `answer` with zeros and an empty stack of indices.
2. For each day `i`, while the stack is non-empty and `temperatures[i] > temperatures[stack[-1]]`, pop index `j` and set `answer[j] = i - j`.
3. Push `i`.
4. Indices left on the stack never see a warmer day and keep `0`.

## Code

```python
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        res = [0] * len(temperatures)
        stack = []  # pair: [temp, index]

        for i, t in enumerate(temperatures):
            while stack and t > stack[-1][0]:
                stackT, stackInd = stack.pop()
                res[stackInd] = i - stackInd
            stack.append((t, i))
        return res
```

## Complexity

- **Time:** `O(n)` — each index is pushed and popped at most once.
- **Space:** `O(n)` — the stack (plus the output array).

## Other Approaches

- **Brute force:** for each day scan forward for the first warmer day — Time `O(n^2)`, Space `O(1)` extra.
- **Backward scan with jumps:** iterate from the right and jump using already-computed `answer[j]` values to skip colder days — Time `O(n)` amortized, Space `O(1)` extra.

## Key Takeaway

"Next greater/smaller element" → monotonic stack of indices; resolve elements at pop time.
