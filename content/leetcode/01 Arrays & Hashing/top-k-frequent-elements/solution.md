---
topic: "Arrays & Hashing"
difficulty: Medium
leetcode: https://leetcode.com/problems/top-k-frequent-elements/
neetcode: https://neetcode.io/problems/top-k-elements-in-list
---
# Top K Frequent Elements - Solution

**Question:** Top K Frequent Elements - Question · **Difficulty:** Medium

## Intuition

A frequency can be at most `n`, so we can bucket values by their count: `buckets[f]` lists every value that appears exactly `f` times. Walking the buckets from the highest frequency downward yields the most frequent values first, avoiding any comparison sort.

## Approach

1. Count occurrences of each value with a hash map.
2. Create `n + 1` empty buckets and put each value into `buckets[count]`.
3. Iterate frequencies from `n` down to `1`, collecting values until `k` have been gathered.
4. Return the collected values.

## Code

```python
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count = {}
        freq = [[] for i in range(len(nums) + 1)]

        for n in nums:
            count[n] = 1 + count.get(n, 0)
        for n, c in count.items():
            freq[c].append(n)

        res = []
        for i in range(len(freq) - 1, 0, -1):
            res += freq[i]
            if len(res) == k:
                return res
                

        # O(n)
```

## Complexity

- **Time:** `O(n)` — counting and bucketing are linear, and the bucket scan touches at most `n + 1` buckets.
- **Space:** `O(n)` — the counter and the buckets.

## Other Approaches

- **Min-heap of size `k`:** push `(freq, value)` and pop when the heap exceeds `k` (or `heapq.nlargest`) — Time `O(n log k)`, Space `O(n)`.
- **Sort by frequency:** sort distinct values by count descending — Time `O(n log n)`, Space `O(n)`.
- **Quickselect on frequencies:** Time `O(n)` average, Space `O(n)`.

## Key Takeaway

When the key you sort by is bounded by `n` (like a frequency), bucket sort gives linear time; otherwise a size-`k` heap is the go-to for "top k".
