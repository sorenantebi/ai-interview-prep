---
video: https://www.youtube.com/watch?v=SS_IlBrocYQ
topic: "Math & Geometry"
difficulty: Easy
leetcode: https://leetcode.com/problems/insert-greatest-common-divisors-in-linked-list/
neetcode: https://neetcode.io/problems/insert-greatest-common-divisors-in-linked-list
---
# Insert Greatest Common Divisors in Linked List

**Topic:** Math & Geometry · **Difficulty:** Easy

## Problem

You are given the `head` of a singly linked list where each node holds an integer value.

Between every pair of adjacent nodes, insert a new node whose value is the greatest common divisor (GCD) of the two neighbouring nodes' values. The GCD of two numbers is the largest positive integer that divides both of them evenly.

Return the head of the linked list after all insertions.

## Examples

**Example 1**
```text
Input: head = [18,6,10,3]
Output: [18,6,6,2,10,1,3]
```
GCD(18, 6) = 6, GCD(6, 10) = 2, GCD(10, 3) = 1, and each result is inserted between its pair.

**Example 2**
```text
Input: head = [7]
Output: [7]
```
There are no adjacent pairs, so the list is unchanged.

## Constraints

- The number of nodes in the list is in the range `[1, 5000]`.
- `1 <= Node.val <= 1000`
