---
topic: "Heap - Priority Queue"
difficulty: Medium
leetcode: https://leetcode.com/problems/single-threaded-cpu/
neetcode: https://neetcode.io/problems/single-threaded-cpu
---
# Single-Threaded CPU - Solution

## Intuition

The CPU always wants the shortest available task, with ties broken by index, which is exactly what a min-heap keyed on `(processingTime, index)` gives us. The only trick is to know which tasks are available at the current time, so we sort tasks by enqueue time and feed them into the heap as the clock advances.

## Approach

1. Build a list of `(enqueueTime, processingTime, index)` and sort it by enqueue time.
2. Keep a clock `time`, a pointer `i` into the sorted list, and a min-heap of `(processingTime, index)`.
3. While tasks remain unprocessed or the heap is non-empty:
   - If the heap is empty, jump `time` forward to the next task's enqueue time (the CPU is idle).
   - Push every task with `enqueueTime <= time` into the heap.
   - Pop the heap's top, append its index to the result, and add its processing time to `time`.
4. Return the result.

## Code

```python
class Solution:
    def getOrder(self, tasks: List[List[int]]) -> List[int]:
        tasks = sorted([(t[0], t[1], i) for i, t in enumerate(tasks)])
        result, heap = [], []
        cur_task_index = 0
        cur_time = tasks[0][0]
        
        while len(result) < len(tasks):
            while (cur_task_index < len(tasks)) and (tasks[cur_task_index][0] <= cur_time):
                heapq.heappush(heap, (tasks[cur_task_index][1], tasks[cur_task_index][2]))
                cur_task_index += 1
            if heap:
                time_difference, original_index = heapq.heappop(heap)
                cur_time += time_difference
                result.append(original_index)
            elif cur_task_index < len(tasks):
                cur_time = tasks[cur_task_index][0]
                
        return result
```

## Complexity

- **Time:** `O(n log n)` — sorting plus `n` pushes and `n` pops on a heap of size at most `n`.
- **Space:** `O(n)` — the sorted list, the heap, and the result.

## Other Approaches

- **Brute force scan:** at each step, scan all tasks for the available one with the smallest `(processingTime, index)` — Time `O(n^2)` / Space `O(n)`
- **Sorted indices with heap (no tuple copy):** sort only indices by enqueue time and use the heap the same way — Time `O(n log n)` / Space `O(n)`
