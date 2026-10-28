---
topic: "Heap / Priority Queue"
difficulty: Hard
leetcode: https://leetcode.com/problems/find-median-from-data-stream/
neetcode: https://neetcode.io/problems/find-median-in-a-data-stream
---
# Find Median From Data Stream - Solution

**Question:** Find Median From Data Stream - Question · **Difficulty:** Hard

## Intuition

Split the numbers into a **lower half** and an **upper half**. If the lower half is a max-heap and the upper half a min-heap, the median only depends on their two roots. Keep every element of `low` `<=` every element of `high`, and keep the sizes balanced (`low` may have one extra), so the median is `low`'s root (odd count) or the average of both roots (even count).

## Approach

1. `low` is a max-heap (store negatives), `high` is a min-heap.
2. `addNum`: push `num` into `low`, then move `low`'s max into `high` — this keeps the ordering invariant.
3. If `high` now has more elements than `low`, move `high`'s min back into `low` — this keeps the size invariant.
4. `findMedian`: if `low` is larger, return its root; otherwise return the average of the two roots.

## Code

```python
class MedianFinder:
    def __init__(self):
        """
        initialize your data structure here.
        """
        # two heaps, large, small, minheap, maxheap
        # heaps should be equal size
        self.small, self.large = [], []  # maxHeap, minHeap (python default)

    def addNum(self, num: int) -> None:
        if self.large and num > self.large[0]:
            heapq.heappush(self.large, num)
        else:
            heapq.heappush(self.small, -1 * num)

        if len(self.small) > len(self.large) + 1:
            val = -1 * heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        if len(self.large) > len(self.small) + 1:
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -1 * val)

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -1 * self.small[0]
        elif len(self.large) > len(self.small):
            return self.large[0]
        return (-1 * self.small[0] + self.large[0]) / 2.0
```

## Complexity

- **Time:** `O(log n)` per `addNum` (a constant number of heap ops), `O(1)` per `findMedian`.
- **Space:** `O(n)` — all numbers are stored across the two heaps.

## Other Approaches

- **Sorted list with binary insertion:** `bisect.insort` then index the middle — Time `O(n)` per add, `O(1)` median, Space `O(n)`.
- **Counting buckets (follow-up for values in `[0, 100]`):** keep 101 counters and walk them to the middle — Time `O(1)` add, `O(100)` median, Space `O(1)`.

## Key Takeaway

Running median = two heaps (max-heap for the lower half, min-heap for the upper half) kept balanced; the median lives at the roots.

## C++

```cpp
/*
    Implement data structure that gets the median from a data stream

    Max heap of lower values & min heap of higher values, access to mids

    Time: O(log n) + O(1)
    Space: O(n)
*/

class MedianFinder {
public:
    MedianFinder() {
        
    }
    
    void addNum(int num) {
        if (lower.empty()) {
            lower.push(num);
            return;
        }
        
        if (lower.size() > higher.size()) {
            if (lower.top() > num) {
                higher.push(lower.top());
                lower.pop();
                lower.push(num);
            } else {
                higher.push(num);
            }
        } else {
            if (num > higher.top()) {
                lower.push(higher.top());
                higher.pop();
                higher.push(num);
            } else {
                lower.push(num);
            }
        }
    }
    
    double findMedian() {
        double result = 0.0;
        
        if (lower.size() == higher.size()) {
            result = lower.top() + (higher.top() - lower.top()) / 2.0;
        } else {
            if (lower.size() > higher.size()) {
                result = lower.top();
            } else {
                result = higher.top();
            }
        }
        
        return result;
    }
private:
    priority_queue<int> lower;
    priority_queue<int, vector<int>, greater<int>> higher;
};

/**
 * Your MedianFinder object will be instantiated and called as such:
 * MedianFinder* obj = new MedianFinder();
 * obj->addNum(num);
 * double param_2 = obj->findMedian();
 */
```
