---
topic: "Two Pointers"
difficulty: Easy
leetcode: https://leetcode.com/problems/merge-sorted-array/
neetcode: https://neetcode.io/problems/merge-sorted-array
---
# Merge Sorted Array - Solution

## Intuition

Merging from the front would overwrite elements of `nums1` that have not been consumed yet. The free space, however, sits at the back of `nums1`. If we fill the array from the back, placing the largest remaining element each time, the write position never overtakes unread elements of `nums1`.

## Approach

1. Set pointers `i = m - 1` (last valid element of `nums1`), `j = n - 1` (last element of `nums2`), and `k = m + n - 1` (write position).
2. While `j >= 0`, compare `nums1[i]` and `nums2[j]` (if `i >= 0`):
   - If `i >= 0` and `nums1[i] > nums2[j]`, write `nums1[i]` to `nums1[k]` and decrement `i`.
   - Otherwise write `nums2[j]` to `nums1[k]` and decrement `j`.
3. Decrement `k` after each write.
4. When `j < 0`, all of `nums2` has been placed. Any remaining elements of `nums1` are already in their correct positions.

## Code

```python
class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        while m > 0 and n > 0:
            if nums1[m-1] >= nums2[n-1]:
                nums1[m+n-1] = nums1[m-1]
                m -= 1
            else:
                nums1[m+n-1] = nums2[n-1]
                n -= 1
        if n > 0:
            nums1[:n] = nums2[:n]
```

## Complexity

- **Time:** `O(m + n)` — each iteration places one element, and there are at most `m + n` placements.
- **Space:** `O(1)` — the merge is done in place with three pointers.

## Other Approaches

- **Copy and sort:** Copy `nums2` into the tail of `nums1` and call `sort()` — Time `O((m + n) log(m + n))` / Space `O(1)` to `O(m + n)` depending on the sort.
- **Forward merge with extra array:** Copy the first `m` elements of `nums1`, then merge forward into `nums1` — Time `O(m + n)` / Space `O(m)`.

## C++

```cpp
class Solution {
public:
    void merge(vector<int>& nums1, int m, vector<int>& nums2, int n) {
        int j=0;
        int i=0;
        if(n==0) return;
        if(m==0)
        {  
         for(int i = 0; i < n; i++){
                nums1[i] = nums2[i];
            } return;
        } 
        while(i<m)
        {
            if(nums1[i]>nums2[j])
            {
                swap(nums1[i],nums2[j]);
                sort(nums2.begin(),nums2.end());
            }
            i++;
        }
        j=0;
        while(i<m+n)
        {
            nums1[i] = nums2[j];
            j++;
            i++;
        }
        
    }
};
```
