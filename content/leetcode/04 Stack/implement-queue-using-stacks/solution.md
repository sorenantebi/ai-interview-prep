---
topic: "Stack"
difficulty: Easy
leetcode: https://leetcode.com/problems/implement-queue-using-stacks/
neetcode: https://neetcode.io/problems/implement-queue-using-stacks
---
# Implement Queue using Stacks - Solution

## Intuition

A stack reverses order: popping everything from one stack into another flips it, so the oldest element ends up on top. If we do that transfer only when needed and keep the flipped elements until they run out, each element moves at most once, which gives amortized O(1).

## Approach

1. Keep two stacks: `in_stack` receives all pushes, `out_stack` serves pops and peeks.
2. `push(x)`: append `x` to `in_stack`.
3. For `pop` and `peek`, if `out_stack` is empty, move every element from `in_stack` to `out_stack` (popping from one, pushing to the other). The front of the queue is now on top of `out_stack`.
4. `pop` pops from `out_stack`; `peek` reads its top.
5. `empty` is true only when both stacks are empty.

## Code

```python
class MyQueue:
    
    def __init__(self):
        self.append_stack = []
        self.inverted_stack = []

    def push(self, x: int) -> None:
        self.append_stack.append(x)

    def pop(self) -> int:
        if not self.inverted_stack:
            while self.append_stack:
                self.inverted_stack.append(self.append_stack.pop())
        return self.inverted_stack.pop()

    def peek(self) -> int:
        if not self.inverted_stack:
            while self.append_stack:
                self.inverted_stack.append(self.append_stack.pop())
        return self.inverted_stack[-1]

    def empty(self) -> bool:
        return not (self.append_stack or self.inverted_stack)
```

## Complexity

- **Time:** `O(1)` amortized per operation — each element is moved from `in_stack` to `out_stack` at most once, so n operations cost O(n) in total (a single `pop`/`peek` can take O(n)).
- **Space:** `O(n)` — all elements are stored across the two stacks.

## Other Approaches

- **Costly push (transfer on every push):** move everything to a helper stack, add the new element, then move it all back so the front is always on top — Time: O(n) push, O(1) pop/peek / Space: O(n)
- **Costly pop (single transfer each time):** push in O(1), and on every pop/peek move all elements to the second stack and back — Time: O(1) push, O(n) pop/peek / Space: O(n)
