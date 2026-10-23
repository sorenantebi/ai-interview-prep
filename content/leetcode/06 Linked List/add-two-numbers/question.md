---
topic: "Linked List"
difficulty: Medium
leetcode: https://leetcode.com/problems/add-two-numbers/
neetcode: https://neetcode.io/problems/add-two-numbers
---
# Add Two Numbers

**Topic:** Linked List · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/add-two-numbers/) · [NeetCode](https://neetcode.io/problems/add-two-numbers)

## Problem

Two non-negative integers are stored as non-empty linked lists, one digit per node, with the digits in **reverse order** (the head holds the ones digit). Add the two numbers and return their sum as a linked list in the same reversed-digit format. Apart from the number 0 itself, the inputs have no leading zeros.

## Examples

**Example 1**
```text
Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
Explanation: 342 + 465 = 807
```

**Example 2**
```text
Input: l1 = [0], l2 = [0]
Output: [0]
```

**Example 3**
```text
Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
Output: [8,9,9,9,0,0,0,1]
```

## Constraints

- The number of nodes in each list is in the range `[1, 100]`
- `0 <= Node.val <= 9`
- No leading zeros except for the number 0
