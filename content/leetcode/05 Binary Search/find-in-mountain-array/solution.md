---
topic: "Binary Search"
difficulty: Hard
leetcode: https://leetcode.com/problems/find-in-mountain-array/
neetcode: https://neetcode.io/problems/find-in-mountain-array
---
# Find in Mountain Array - Solution

## Intuition

A mountain array is an increasing run followed by a decreasing run, and each run is sorted. Once the peak is known, each side can be searched with ordinary binary search. With `n <= 10^4`, each binary search needs about 14 calls, so three searches stay well under the limit of 100 `get` calls.

## Approach

1. Binary search for the peak index: compare `get(mid)` with `get(mid + 1)`. If it is smaller, the peak is to the right; otherwise it is at `mid` or to the left.
2. Binary search the ascending part `[0, peak]` for `target`. If found, return that index, since it is the smallest possible.
3. Otherwise binary search the descending part `[peak + 1, n - 1]` (with reversed comparisons) for `target`.
4. If neither finds it, return `-1`.

## Code

```python
from typing import List, Optional

# class MountainArray:
#    def get(self, index: int) -> int: ...
#    def length(self) -> int: ...

class Solution:
    def findInMountainArray(self, target: int, mountain_arr: 'MountainArray') -> int:
        n = mountain_arr.length()

        lo, hi = 0, n - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if mountain_arr.get(mid) < mountain_arr.get(mid + 1):
                lo = mid + 1
            else:
                hi = mid
        peak = lo

        lo, hi = 0, peak
        while lo <= hi:
            mid = (lo + hi) // 2
            val = mountain_arr.get(mid)
            if val == target:
                return mid
            if val < target:
                lo = mid + 1
            else:
                hi = mid - 1

        lo, hi = peak + 1, n - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            val = mountain_arr.get(mid)
            if val == target:
                return mid
            if val > target:
                lo = mid + 1
            else:
                hi = mid - 1

        return -1
```

## Complexity

- **Time:** `O(log n)` — three binary searches, each halving its range.
- **Space:** `O(1)` — only a few index variables.

## Other Approaches

- **Cache `get` results:** same three searches but memoize calls to avoid repeated queries — Time `O(log n)` / Space `O(log n)`
- **Linear scan:** read every element and track the first match — Time `O(n)` / Space `O(1)` (exceeds the 100-call limit)

## C++

```cpp
/**
 * 
 *  Algorithm:
 *      -  The algorithm's goal is to find the minimum index at which the value "target",
 *         exist within a "MountainArray".
 *      -  It employs a binary search approach, dividing the array into ascending and 
 *         descending halves. Additionally, it identifies the peak index to determine the
 *         transition from ascending to descending.
 * 
 *  Time  Complexity: O(log n) 
 *  Space Complexity: O(1)
 * 
 */

/**
 * // This is the MountainArray's API interface.
 * // You should not implement it, or speculate about its implementation
 * class MountainArray {
 *   public:
 *     int get(int index);
 *     int length();
 * };
 */

class Solution {
public:
    int binarySearch(int& begin, int& end, const int& target, MountainArray &mountainArr)
    {
        while (begin <= end)
        {
            int mid = begin + (end-begin)/2;
            int mid_number = mountainArr.get(mid);

            if(mid_number == target)
            {
                return mid;
            }
            else if (mid_number > target)
            {
                end = --mid;
            }
            else
            {
                begin = ++mid;
            }
        }
        return -1;
    }

    int reverseBinarySearch(int& begin, int& end, const int& target, MountainArray &mountainArr)
    {
        while (begin <= end)
        {
            int mid = begin + (end-begin)/2;
            int mid_number = mountainArr.get(mid);

            if(mid_number == target)
            {
                return mid;
            }
            else if (mid_number > target)
            {
                begin = ++mid;
            }
            else
            {
                end = --mid;
            }
        }
        return -1;
    }

    int findPeakElement(int& begin, int& end, MountainArray &mountainArr)
    {
        while (begin < end)
        {
            int mid = begin + (end-begin)/2;
            if(mountainArr.get(mid) < mountainArr.get(mid+1))
            {
                begin = ++mid;
            }
            else
            {
                end = --mid;
            }
        }
        return begin;
    }

    int findInMountainArray(int target, MountainArray &mountainArr) {
        ios_base::sync_with_stdio(false);
        cin.tie(NULL);

        int begin = 0; 
        int end = mountainArr.length()-1;
        int minimum_index = 0;

        int peak_index = findPeakElement(begin, end, mountainArr);

        begin = 0; 
        end = peak_index;   
        minimum_index = binarySearch(begin, end, target, mountainArr);

        if(minimum_index != -1) return minimum_index;
        
        begin = peak_index;
        end = mountainArr.length()-1;
        minimum_index = reverseBinarySearch(begin, end, target, mountainArr);

        return minimum_index;
    }
};
```
