---
video: https://www.youtube.com/watch?v=Id_tqGdsZQI
topic: "Stack"
difficulty: Easy
leetcode: https://leetcode.com/problems/baseball-game/
neetcode: https://neetcode.io/problems/baseball-game
---
# Baseball Game

**Topic:** Stack · **Difficulty:** Easy

## Problem

You are keeping score for a baseball game with unusual rules. The record starts out empty.

You are given a list of strings `operations`, where each `operations[i]` is applied to the record in order and is one of the following:

- An integer `x`: record a new score of `x`.
- `"+"`: record a new score equal to the sum of the previous two scores.
- `"D"`: record a new score equal to double the previous score.
- `"C"`: invalidate the previous score, removing it from the record.

Return the sum of all scores on the record after applying all operations.

The test cases are generated such that the answer and all intermediate calculations fit in a 32-bit integer and that all operations are valid.

## Examples

**Example 1**
```text
Input: ops = ["5","2","C","D","+"]
Output: 30
```
Record evolves: [5] → [5, 2] → [5] → [5, 10] → [5, 10, 15]. The sum is 30.

**Example 2**
```text
Input: ops = ["5","-2","4","C","D","9","+","+"]
Output: 27
```
Record evolves: [5] → [5, -2] → [5, -2, 4] → [5, -2] → [5, -2, -4] → [5, -2, -4, 9] → [5, -2, -4, 9, 5] → [5, -2, -4, 9, 5, 14]. The sum is 27.

**Example 3**
```text
Input: ops = ["1","C"]
Output: 0
```
The record becomes [1] and then []. The sum of an empty record is 0.

## Constraints

- `1 <= operations.length <= 1000`
- `operations[i]` is `"C"`, `"D"`, `"+"`, or a string representing an integer in the range `[-3 * 10^4, 3 * 10^4]`.
- For operation `"+"`, there will always be at least two previous scores on the record.
- For operations `"C"` and `"D"`, there will always be at least one previous score on the record.
