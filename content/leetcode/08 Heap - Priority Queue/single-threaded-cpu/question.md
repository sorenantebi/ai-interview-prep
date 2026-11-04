---
video: https://www.youtube.com/watch?v=RR1n-d4oYqE
topic: "Heap - Priority Queue"
difficulty: Medium
leetcode: https://leetcode.com/problems/single-threaded-cpu/
neetcode: https://neetcode.io/problems/single-threaded-cpu
---
# Single-Threaded CPU

**Topic:** Heap - Priority Queue · **Difficulty:** Medium

## Problem

You are given `n` tasks labeled from `0` to `n - 1`, represented by a 2D integer array `tasks`, where `tasks[i] = [enqueueTime_i, processingTime_i]` means that the `i`-th task becomes available at `enqueueTime_i` and takes `processingTime_i` units of time to complete.

A single-threaded CPU can process at most one task at a time and behaves as follows:

- If the CPU is idle and no tasks are available, it stays idle.
- If the CPU is idle and there are available tasks, it picks the one with the shortest processing time. If several tasks share the shortest processing time, it picks the one with the smallest index.
- Once a task is started, the CPU processes it to completion without stopping.
- The CPU can finish a task and start a new one instantly.

Return the order in which the CPU will process the tasks.

## Examples

**Example 1**
```text
Input: tasks = [[1,2],[2,4],[3,2],[4,1]]
Output: [0,2,3,1]
```
At time 1 the idle CPU starts task 0 and finishes at time 3. Tasks 1 and 2 are available, and task 2 is shorter, so it runs until time 5. Task 3 (available since time 4) is shortest, runs until time 6, then task 1 runs until time 10.

**Example 2**
```text
Input: tasks = [[7,10],[7,12],[7,5],[7,4],[7,2]]
Output: [4,3,2,0,1]
```
All tasks become available at time 7. They are processed in increasing order of processing time: 2, 4, 5, 10, 12, which correspond to tasks 4, 3, 2, 0, 1.

## Constraints

- `1 <= tasks.length <= 10^5`
- `tasks[i] = [enqueueTime_i, processingTime_i]`
- `1 <= enqueueTime_i, processingTime_i <= 10^9`
