---
video: https://www.youtube.com/watch?v=LN7KjRszjk4
topic: "Stack"
difficulty: Medium
leetcode: https://leetcode.com/problems/asteroid-collision/
neetcode: https://neetcode.io/problems/asteroid-collision
---
# Asteroid Collision

**Topic:** Stack · **Difficulty:** Medium

## Problem

You are given an integer array `asteroids` describing asteroids in a row. The position of each asteroid in the array is its relative position in space.

The absolute value of each element is the asteroid's size, and the sign is its direction: positive means moving right, negative means moving left. All asteroids move at the same speed.

Determine the state of the row after all collisions have happened. When two asteroids meet, the smaller one explodes. If both have the same size, both explode. Two asteroids moving in the same direction never meet.

Return the array of asteroids that remain.

## Examples

**Example 1**
```text
Input: asteroids = [5,10,-5]
Output: [5,10]
```
The 10 and -5 collide, and 10 survives. The 5 and 10 never collide.

**Example 2**
```text
Input: asteroids = [8,-8]
Output: []
```
The 8 and -8 collide and both explode.

**Example 3**
```text
Input: asteroids = [10,2,-5]
Output: [10]
```
The 2 and -5 collide and -5 survives. Then 10 and -5 collide and 10 survives.

**Example 4**
```text
Input: asteroids = [3,5,-6,2,-1,4]
Output: [-6,2,4]
```
The -6 destroys 3 and 5 and keeps moving left. On the other side, 2 destroys -1. Since 2 and 4 both move right, they never collide.

## Constraints

- `2 <= asteroids.length <= 10^4`
- `-1000 <= asteroids[i] <= 1000`
- `asteroids[i] != 0`
