---
topic: "Heap / Priority Queue"
difficulty: Hard
leetcode: https://leetcode.com/problems/find-median-from-data-stream/
neetcode: https://neetcode.io/problems/find-median-in-a-data-stream
---
# Find Median From Data Stream

**Topic:** Heap / Priority Queue · **Difficulty:** Hard · [LeetCode](https://leetcode.com/problems/find-median-from-data-stream/) · [NeetCode](https://neetcode.io/problems/find-median-in-a-data-stream)

## Problem

The median of a sorted list of integers is its middle element when the length is odd, and the average of the two middle elements when the length is even (e.g. median of `[2,3,4]` is `3`, median of `[2,3]` is `2.5`).

Design a `MedianFinder` that receives integers one at a time and can report the median of everything received so far:

- `MedianFinder()` creates an empty structure.
- `void addNum(int num)` adds `num` to the data.
- `double findMedian()` returns the current median. Answers within `10^-5` of the true value are accepted.

`findMedian` is only called when at least one number has been added.

## Examples

**Example 1**
```text
Input:  ["MedianFinder","addNum","addNum","findMedian","addNum","findMedian"]
        [[],[1],[2],[],[3],[]]
Output: [null,null,null,1.5,null,2.0]
```

**Example 2**
```text
Input:  ["MedianFinder","addNum","findMedian","addNum","findMedian"]
        [[],[-1],[],[-2],[]]
Output: [null,null,-1.0,null,-1.5]
```

## Constraints

- `-10^5 <= num <= 10^5`
- At most `5 * 10^4` total calls to `addNum` and `findMedian`
- Follow-up: what if all numbers are in `[0, 100]`? What if 99% of them are?
