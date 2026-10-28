---
topic: "Binary Search"
difficulty: Hard
leetcode: https://leetcode.com/problems/median-of-two-sorted-arrays/
neetcode: https://neetcode.io/problems/median-of-two-sorted-arrays
---
# Median of Two Sorted Arrays - Solution

**Question:** Median of Two Sorted Arrays - Question · **Difficulty:** Hard

## Intuition

The median splits the merged array into a left half and a right half of (almost) equal size. If we take `i` elements from `nums1` and `j = half - i` from `nums2` for the left half, the partition is correct exactly when `A[i-1] <= B[j]` and `B[j-1] <= A[i]`. Since `i` determines `j`, we binary search `i` over the shorter array.

## Approach

1. Let `A` be the shorter array (swap if needed), `total = m + n`, `half = (total + 1) // 2`.
2. Binary search `i` in `[0, len(A)]`; set `j = half - i`.
3. Read the four boundary values, using `-inf`/`+inf` when an index is out of range: `Aleft = A[i-1]`, `Aright = A[i]`, `Bleft = B[j-1]`, `Bright = B[j]`.
4. If `Aleft <= Bright` and `Bleft <= Aright`, the partition is valid: return `max(Aleft, Bleft)` for odd `total`, else the average of `max(Aleft, Bleft)` and `min(Aright, Bright)`.
5. If `Aleft > Bright`, take fewer from `A` (`hi = i - 1`); otherwise take more (`lo = i + 1`).

## Code

```python
# Time: log(min(n, m))


class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        A, B = nums1, nums2
        total = len(nums1) + len(nums2)
        half = total // 2

        if len(B) < len(A):
            A, B = B, A

        l, r = 0, len(A) - 1
        while True:
            i = (l + r) // 2  # A
            j = half - i - 2  # B

            Aleft = A[i] if i >= 0 else float("-infinity")
            Aright = A[i + 1] if (i + 1) < len(A) else float("infinity")
            Bleft = B[j] if j >= 0 else float("-infinity")
            Bright = B[j + 1] if (j + 1) < len(B) else float("infinity")

            # partition is correct
            if Aleft <= Bright and Bleft <= Aright:
                # odd
                if total % 2:
                    return min(Aright, Bright)
                # even
                return (max(Aleft, Bleft) + min(Aright, Bright)) / 2
            elif Aleft > Bright:
                r = i - 1
            else:
                l = i + 1
```

## Complexity

- **Time:** `O(log(min(m, n)))` — binary search over the shorter array only.
- **Space:** `O(1)`.

## Other Approaches

- **Merge then pick:** two-pointer merge up to the middle index — Time `O(m + n)`, Space `O(1)` if you only track the last two values.
- **k-th smallest by elimination:** recursively discard `k/2` elements from one array — Time `O(log(m + n))`, Space `O(log(m + n))` recursion.

## Key Takeaway

Binary search a partition, not a value: choose how many elements come from the shorter array and validate with the cross-boundary conditions, padding edges with ±infinity.

## C++

```cpp
/*
    Given 2 sorted arrays of size m & n, return the median of these arrays
    Ex. nums1 = [1,3] nums2 = [2] -> 2, nums1 = [1,2] nums2 = [3,4] -> 2.5

    Binary search, partition each array until partitions are correct, get median
    [1,2,3,4,5]
    |  a|b    |
    [1,2,3,4,5,6,7,8]    -->    a <= d ? yes, c <= b ? no, so need to fix
    |      c|d      |

    Time: O(log min(m, n))
    Space: O(1)
*/

class Solution {
public:
    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        int m = nums1.size();
        int n = nums2.size();
        
        if (m > n) {
            return findMedianSortedArrays(nums2, nums1);
        }
        
        int total = m + n;
        
        int low = 0;
        int high = m;
        
        double result = 0.0;
        
        while (low <= high) {
            // nums1
            int i = low + (high - low) / 2;
            // nums2
            int j = (total + 1) / 2 - i;
            
            int left1 = (i > 0) ? nums1[i - 1] : INT_MIN;
            int right1 = (i < m) ? nums1[i] : INT_MAX;
            int left2 = (j > 0) ? nums2[j - 1] : INT_MIN;
            int right2 = (j < n) ? nums2[j] : INT_MAX;
            
            // partition is correct
            if (left1 <= right2 && left2 <= right1) {
                // even
                if (total % 2 == 0) {
                    result = (max(left1, left2) + min(right1, right2)) / 2.0;
                // odd
                } else {
                    result = max(left1, left2);
                }
                break;
            } else if (left1 > right2) {
                high = i - 1;
            } else {
                low = i + 1;
            }
        }
        
        return result;
    }
};
```
