---
topic: "Linked List"
difficulty: Medium
leetcode: https://leetcode.com/problems/find-the-duplicate-number/
neetcode: https://neetcode.io/problems/find-duplicate-integer
---
# Find The Duplicate Number - Solution

**Question:** Find The Duplicate Number - Question · **Difficulty:** Medium

## Intuition

Treat the array as a linked list where index `i` points to index `nums[i]`. Index 0 is never a target (values are `>= 1`), so it is a safe start. Because two different indices point to the duplicate value, that value is the node where a cycle begins — so Floyd's cycle detection (Linked List Cycle II) finds it in `O(1)` space without modifying the array.

## Approach

1. Phase 1: `slow = nums[slow]`, `fast = nums[nums[fast]]` starting from index 0 until they meet inside the cycle.
2. Phase 2: start a second pointer `slow2` at 0; advance `slow` and `slow2` one step at a time.
3. The point where they meet is the entrance of the cycle, i.e. the duplicate value. Return it.

## Code

```python
class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        slow, fast = 0, 0
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break

        slow2 = 0
        while True:
            slow = nums[slow]
            slow2 = nums[slow2]
            if slow == slow2:
                return slow
```

## Complexity

- **Time:** `O(n)` — both phases take a linear number of steps.
- **Space:** `O(1)` — a few integer pointers; `nums` is untouched.

## Other Approaches

- **Hash set:** return the first value already seen — Time `O(n)`, Space `O(n)`.
- **Binary search on value:** for a candidate `mid`, count elements `<= mid`; if count `> mid` the duplicate is in `[1, mid]` — Time `O(n log n)`, Space `O(1)`.
- **Sort or negative marking:** both work but modify the array (forbidden by the constraints).

## Key Takeaway

When values are valid indices, an array can be viewed as a functional graph / linked list; "find the repeated value" becomes "find the cycle entrance" with Floyd's algorithm.
