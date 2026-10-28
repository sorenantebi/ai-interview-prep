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

## C++

```cpp
/*
    Given array of tasks & cooldown b/w same tasks, return least # of units of time
    Ex. tasks = ["A","A","A","B","B","B"] n = 2 -> 8 (A->B->idle->A->B->idle->A->B)

    Key is to determine # of idles, greedy: always arrange task w/ most freq first
    3A, 2B, 1C -> A??A??A -> AB?AB?A -> ABCAB#A, since A most freq, needs most idles

    Time: O(n)
    Space: O(1)
*/
/*
class Solution {
public:
    int leastInterval(vector<char>& tasks, int n) {
        vector<int> counter(26);
        
        int maxCount = 0;
        int maxCountFrequency = 0;
        
        for (int i = 0; i < tasks.size(); i++) {
            counter[tasks[i] - 'A']++;
            int currCount = counter[tasks[i] - 'A'];
            
            if (maxCount == currCount) {
                maxCountFrequency++;
            } else if (maxCount < currCount) {
                maxCount = currCount;
                maxCountFrequency = 1;
            }
        }
        
        int partCount = maxCount - 1;
        int partLength = n - (maxCountFrequency - 1);
        int emptySlots = partCount * partLength;
        int availableTasks = tasks.size() - maxCount * maxCountFrequency;
        int idles = max(0, emptySlots - availableTasks);
        
        return tasks.size() + idles;
    }
};
*/

// Time O(n * cooldown)
class Solution {
public:
    int leastInterval(vector<char>& tasks, int n) {
        priority_queue<int> pq;
        queue<vector<int>> q;
        vector<int> counter(26);

        for (int i = 0; i < tasks.size(); ++i)
            ++counter[tasks[i] - 'A'];
        for (int i = 0; i < 26; ++i){
            if (counter[i])
                pq.push(counter[i]);
        }

        int time = 0;
        while (!q.empty() || !pq.empty()){
            ++time;
            if (!pq.empty()){
                if (pq.top() - 1)
                    q.push({pq.top() - 1, time + n});
                pq.pop();
            }
            if (!q.empty() && q.front()[1] == time){
                pq.push(q.front()[0]);
                q.pop();
            }
        }
        return time;
    }
};
```
