---
topic: "Arrays & Hashing"
difficulty: Easy
leetcode: https://leetcode.com/problems/remove-element/
neetcode: https://neetcode.io/problems/remove-element
---
# Remove Element - Solution

## Intuition

Since the order of the kept elements does not matter and only the first `k` positions are checked, we do not need to physically delete anything. We just need to compact all values different from `val` to the front of the array and count them.

## Approach

1. Keep a write pointer `k` starting at `0`; it marks where the next kept element goes.
2. Scan the array from left to right with a read pointer.
3. If the current element is not equal to `val`, write it to `nums[k]` and increment `k`.
4. Elements equal to `val` are skipped, so they get overwritten or left beyond index `k`.
5. After the scan, return `k`.

## Code

```python
class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        k = 0
        for i in range(len(nums)):
            if nums[i] != val:
                nums[k] = nums[i]
                k += 1
        return k

# Optimized solution with the same time and space complexity
class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        # Avoid unessary copy operations in a previous solution, when k == i and nums[i] != val 
        # by swapping nums[i] and the last element of the array (nums[n])
        n = len(nums)
        i = 0

        while i < n:
            if nums[i] == val:
                nums[i], nums[n - 1] = nums[n - 1], nums[i]
                n -= 1  # decrement the length of the array by discarding the last element
            else:
                i += 1
        
        return n
```

## Complexity

- **Time:** `O(n)` — each element is visited exactly once.
- **Space:** `O(1)` — the array is modified in-place using only a single extra pointer.

## Other Approaches

- **Two pointers from both ends:** swap an element equal to `val` with the last unprocessed element and shrink the array end; does fewer writes when `val` is rare — Time `O(n)` / Space `O(1)`
- **Build a new list:** filter into a new list and copy it back; simple but violates the in-place spirit — Time `O(n)` / Space `O(n)`

## C++

```cpp
class Solution {
public:
    int removeElement(vector<int>& nums, int val) {
        int n=nums.size();
        int count=0;
        for(int i=0;i<n;i++)
        {
            if(nums[i]!=val)
            {
                swap(nums[i],nums[count]);
                count++;
            }
        }
        
        return count;
    }
};
```
