---
topic: "Arrays & Hashing"
difficulty: Medium
leetcode: https://leetcode.com/problems/sort-colors/
neetcode: https://neetcode.io/problems/sort-colors
---
# Sort Colors - Solution

## Intuition

With only three distinct values, a full sort is unnecessary. We can partition the array into three regions (0s, 1s, 2s) in a single pass by keeping pointers at the boundaries. This is the Dutch National Flag algorithm.

## Approach

1. Keep `l` as the position where the next `0` goes, `r` as the position where the next `2` goes, and `i` as the current scan index.
2. While `i <= r`:
   - If `nums[i] == 0`, swap it with `nums[l]`, then advance both `l` and `i`.
   - If `nums[i] == 2`, swap it with `nums[r]` and decrement `r`. Do not advance `i`, since the swapped-in value has not been examined yet.
   - If `nums[i] == 1`, just advance `i`.
3. When `i` passes `r`, the array is sorted.

## Code

```python
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        low = 0
        high = len(nums) - 1
        mid = 0

        while mid <= high:
            if nums[mid] == 0:
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1
                mid += 1
            elif nums[mid] == 1:
                mid +=1
            else:
                nums[mid], nums[high] = nums[high], nums[mid]
                high -= 1
        return nums
```

## Complexity

- **Time:** `O(n)` — each element is examined once; every step advances `i` or shrinks `r`.
- **Space:** `O(1)` — only three pointers are used, and the array is modified in-place.

## Other Approaches

- **Counting sort:** count the 0s, 1s, and 2s, then overwrite the array in that order — Time `O(n)` (two passes) / Space `O(1)`
- **Built-in / comparison sort:** sort the array directly (disallowed here) — Time `O(n log n)` / Space `O(1)` to `O(n)` depending on the algorithm

## C++

```cpp
class Solution {
public:
    void sortColors(vector<int>& nums) {
        int p1=0,p2=nums.size()-1;
        for(int i=p1;i<=p2;i++)
        {
            if(nums[i]==0)
            {
                swap(nums[i],nums[p1]);
                p1++;
            }
            if(nums[i]==2)
            {
                swap(nums[i],nums[p2]);
                p2--;
                i--;
            }
        }
        
        
    }
};
```
