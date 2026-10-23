---
topic: "Linked List"
difficulty: Medium
leetcode: https://leetcode.com/problems/copy-list-with-random-pointer/
neetcode: https://neetcode.io/problems/copy-linked-list-with-random-pointer
---
# Copy List With Random Pointer

**Topic:** Linked List · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/copy-list-with-random-pointer/) · [NeetCode](https://neetcode.io/problems/copy-linked-list-with-random-pointer)

## Problem

A linked list of length `n` is given where every node has a `val`, a `next` pointer, and an extra `random` pointer that may point to any node in the list or be `null`. Build a **deep copy** of the list: `n` brand-new nodes such that for every original node, its copy has the same value, and the copy's `next` and `random` pointers point to the copies of the corresponding original targets. No pointer in the copy may reference an original node. Return the head of the copy.

(LeetCode serializes each node as `[val, random_index]`, where `random_index` is the index of the node `random` points to, or `null`.)

## Examples

**Example 1**
```text
Input: head = [[7,null],[13,0],[11,4],[10,2],[1,0]]
Output: [[7,null],[13,0],[11,4],[10,2],[1,0]]
```

**Example 2**
```text
Input: head = [[1,1],[2,1]]
Output: [[1,1],[2,1]]
```

**Example 3**
```text
Input: head = [[3,null],[3,0],[3,null]]
Output: [[3,null],[3,0],[3,null]]
```

## Constraints

- `0 <= n <= 1000`
- `-10^4 <= Node.val <= 10^4`
- `Node.random` is `null` or points to a node in the list
