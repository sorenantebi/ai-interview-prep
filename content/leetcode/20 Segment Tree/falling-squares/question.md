---
topic: "Segment Tree"
difficulty: Hard
leetcode: https://leetcode.com/problems/falling-squares/
---
# Falling Squares

**Topic:** Segment Tree · **Difficulty:** Hard

## Problem

Squares are dropped one at a time onto the X-axis of a 2D plane. You are given a 2D integer array `positions`, where `positions[i] = [left_i, sideLength_i]` describes the `i`-th square: its side length is `sideLength_i`, and its left edge is aligned with X-coordinate `left_i`.

Each square starts above every square that has already landed and falls in the negative Y direction until it lands on the top side of another square or on the X-axis. A square that only touches the left or right side of another square does not count as landing on it. Once a square lands, it stays fixed and cannot move.

After each drop, record the height of the tallest stack of squares so far.

Return an integer array `ans` where `ans[i]` is that height after dropping the `i`-th square.

## Examples

**Example 1**
```text
Input: positions = [[1,2],[2,3],[6,1]]
Output: [2,5,5]
```
After the first drop, the tallest stack is square 1 with height 2. After the second drop, the tallest stack is squares 1 and 2 with height 5. After the third drop, the tallest stack is still squares 1 and 2 with height 5.

**Example 2**
```text
Input: positions = [[100,100],[200,100]]
Output: [100,100]
```
After the first drop, the tallest stack is square 1 with height 100. After the second drop, the tallest stack is either square 1 or square 2, both with height 100. Square 2 only brushes the right side of square 1, which does not count as landing on it.

## Constraints

- `1 <= positions.length <= 1000`
- `1 <= left_i <= 10^8`
- `1 <= sideLength_i <= 10^6`
