---
topic: "Heap / Priority Queue"
difficulty: Medium
leetcode: https://leetcode.com/problems/task-scheduler/
neetcode: https://neetcode.io/problems/task-scheduling
---
# Task Scheduler

**Topic:** Heap / Priority Queue · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/task-scheduler/) · [NeetCode](https://neetcode.io/problems/task-scheduling)

## Problem

You are given a list of CPU tasks `tasks`, each labeled by an uppercase letter `'A'`–`'Z'`, and a non-negative integer `n`. Each time unit the CPU can either run exactly one task or stay idle. Tasks can be executed in any order, but two runs of the **same** label must be separated by at least `n` time units (i.e. at least `n` other units — tasks or idles — in between).

Return the minimum number of time units needed to finish all tasks.

## Examples

**Example 1**
```text
Input: tasks = ["A","A","A","B","B","B"], n = 2
Output: 8
Explanation: A -> B -> idle -> A -> B -> idle -> A -> B
```

**Example 2**
```text
Input: tasks = ["A","C","A","B","D","B"], n = 1
Output: 6
Explanation: A -> B -> C -> D -> A -> B, no idles needed
```

**Example 3**
```text
Input: tasks = ["A","A","A","B","B","B"], n = 3
Output: 10
Explanation: A -> B -> idle -> idle -> A -> B -> idle -> idle -> A -> B
```

## Constraints

- `1 <= tasks.length <= 10^4`
- `tasks[i]` is an uppercase English letter
- `0 <= n <= 100`
