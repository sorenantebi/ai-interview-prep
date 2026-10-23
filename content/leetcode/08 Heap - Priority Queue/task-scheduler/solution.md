---
topic: "Heap / Priority Queue"
difficulty: Medium
leetcode: https://leetcode.com/problems/task-scheduler/
neetcode: https://neetcode.io/problems/task-scheduling
---
# Task Scheduler - Solution

**Question:** Task Scheduler - Question · **Difficulty:** Medium

## Intuition

Greedily, at every time step we should run the available task with the **most remaining copies** — the most frequent task is what forces idles, so working it down first minimizes them. A max-heap gives the most frequent ready task; a queue holds tasks that are cooling down along with the time they become available again.

## Approach

1. Count each label and push the counts (negated) into a max-heap.
2. Advance `time` one unit per iteration while the heap or cooldown queue is non-empty.
3. If the heap has a task, pop it, decrement its count, and if copies remain, enqueue `(remaining, time + n)`.
4. If the front of the queue becomes available at `time`, push it back onto the heap.
5. Optimization: if the heap is empty, jump `time` directly to the next availability time instead of stepping through idles.

## Code

```python
class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        count = Counter(tasks)
        maxHeap = [-cnt for cnt in count.values()]
        heapq.heapify(maxHeap)

        time = 0
        q = deque()  # pairs of [-cnt, idleTime]
        while maxHeap or q:
            time += 1

            if not maxHeap:
                time = q[0][1]
            else:
                cnt = 1 + heapq.heappop(maxHeap)
                if cnt:
                    q.append([cnt, time + n])
            if q and q[0][1] == time:
                heapq.heappush(maxHeap, q.popleft()[0])
        return time


# Greedy algorithm
class Solution(object):
    def leastInterval(self, tasks: List[str], n: int) -> int:
        counter = collections.Counter(tasks)
        max_count = max(counter.values())
        min_time = (max_count - 1) * (n + 1) + \
                    sum(map(lambda count: count == max_count, counter.values()))
    
        return max(min_time, len(tasks))
```

## Complexity

- **Time:** `O(T * log 26) = O(T)` — each of the `T` tasks is popped/pushed once on a heap of at most 26 labels; idle stretches are skipped in `O(1)`.
- **Space:** `O(26) = O(1)` — heap and queue hold at most one entry per label.

## Other Approaches

- **Math formula:** with `maxf` = highest frequency and `cnt` = number of labels having it, answer = `max(len(tasks), (maxf - 1) * (n + 1) + cnt)` — Time `O(T)`, Space `O(1)`.

## Key Takeaway

Scheduling with cooldowns = max-heap of "ready" items plus a FIFO queue of "cooling" items stamped with their release time; the frame-counting formula is the fast closed form.
