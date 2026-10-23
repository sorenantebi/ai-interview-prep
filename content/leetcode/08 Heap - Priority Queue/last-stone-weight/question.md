---
topic: "Heap / Priority Queue"
difficulty: Easy
leetcode: https://leetcode.com/problems/last-stone-weight/
neetcode: https://neetcode.io/problems/last-stone-weight
---
# Last Stone Weight

**Topic:** Heap / Priority Queue · **Difficulty:** Easy · [LeetCode](https://leetcode.com/problems/last-stone-weight/) · [NeetCode](https://neetcode.io/problems/last-stone-weight)

## Problem

You have a list of stones, each with a positive integer weight `stones[i]`. Repeatedly play the following round: pick the two heaviest stones, with weights `x <= y`, and smash them together.

- If `x == y`, both stones are destroyed.
- If `x != y`, the stone of weight `x` is destroyed and the other stone's weight becomes `y - x`.

The game stops when at most one stone is left. Return the weight of the remaining stone, or `0` if no stones remain.

## Examples

**Example 1**
```text
Input: stones = [2,7,4,1,8,1]
Output: 1
Explanation: 8,7 -> 1; 4,2 -> 2; 2,1 -> 1; 1,1 -> 0; one stone of weight 1 remains
```

**Example 2**
```text
Input: stones = [1]
Output: 1
```

**Example 3**
```text
Input: stones = [3,3]
Output: 0
```

## Constraints

- `1 <= stones.length <= 30`
- `1 <= stones[i] <= 1000`
