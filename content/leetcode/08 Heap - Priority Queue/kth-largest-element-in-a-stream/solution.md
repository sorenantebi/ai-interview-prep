---
topic: "Heap / Priority Queue"
difficulty: Easy
leetcode: https://leetcode.com/problems/kth-largest-element-in-a-stream/
neetcode: https://neetcode.io/problems/kth-largest-integer-in-a-stream
---
# Kth Largest Element In a Stream - Solution

**Question:** Kth Largest Element In a Stream - Question · **Difficulty:** Easy

## Intuition

We only ever need the `k` largest values; everything smaller can never become the answer again. Keep those `k` values in a **min-heap of size `k`** — its root is exactly the `k`-th largest, and new values only need to be compared against that root.

## Approach

1. In `__init__`, heapify `nums` and pop the smallest element until the heap has at most `k` elements.
2. In `add`, push `val`; if the heap now has more than `k` elements, pop the minimum.
3. Return `heap[0]`, the smallest of the `k` largest values.

## Code

```python
class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        # minHeap w/ K largest integers
        self.minHeap, self.k = nums, k
        heapq.heapify(self.minHeap)
        while len(self.minHeap) > k:
            heapq.heappop(self.minHeap)

    def add(self, val: int) -> int:
        heapq.heappush(self.minHeap, val)
        if len(self.minHeap) > self.k:
            heapq.heappop(self.minHeap)
        return self.minHeap[0]
```

## Complexity

- **Time:** `O(n log n)` for construction (heapify `O(n)` plus up to `n - k` pops), `O(log k)` per `add`.
- **Space:** `O(k)` — the heap never holds more than `k + 1` elements after construction.

## Other Approaches

- **Sorted list:** keep all values sorted and insert with `bisect.insort`, then read index `-k` — Time `O(n)` per add (shifting), Space `O(n)`.
- **Re-sort on every add:** Time `O(n log n)` per add, Space `O(n)`.

## Key Takeaway

"k-th largest" in a stream = min-heap capped at size `k`; the root is the answer. Mirror it (max-heap of size `k`) for "k-th smallest".

## C++

```cpp
/*
    Design a class to find the kth largest element in a stream

    Min heap & maintain only k elements, top will always be kth largest
    Ex. nums = [6,2,3,1,7], k = 3 -> [1,2,3,6,7] -> [3,6,7]

    Time: O(n log n + m log k) -> n = length of nums, m = add calls
    Space: O(n)
*/

class KthLargest {
public:
    KthLargest(int k, vector<int>& nums) {
        this->k = k;
        for (int i = 0; i < nums.size(); i++) {
            pq.push(nums[i]);
        }
        while (pq.size() > this->k) {
            pq.pop();
        }
    }
    
    int add(int val) {
        pq.push(val);
        if (pq.size() > k) {
            pq.pop();
        }
        return pq.top();
    }
private:
    int k;
    priority_queue<int, vector<int>, greater<int>> pq;
};

/**
 * Your KthLargest object will be instantiated and called as such:
 * KthLargest* obj = new KthLargest(k, nums);
 * int param_1 = obj->add(val);
 */
```
