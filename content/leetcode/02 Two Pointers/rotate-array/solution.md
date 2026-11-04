---
topic: "Two Pointers"
difficulty: Medium
leetcode: https://leetcode.com/problems/rotate-array/
neetcode: https://neetcode.io/problems/rotate-array
---
# Rotate Array - Solution

## Intuition

Rotating right by `k` moves the last `k` elements to the front while keeping the relative order within both the front part and the back part. Reversing the whole array puts the last `k` elements at the front, but in reversed order. Reversing each of the two blocks afterwards restores their internal order. Each reversal is a two-pointer swap, so the whole thing is done in place.

## Approach

1. Reduce `k` with `k %= n`, since rotating by `n` leaves the array unchanged.
2. Reverse the entire array.
3. Reverse the first `k` elements.
4. Reverse the remaining `n - k` elements.

## Code

```python
class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        k = k % len(nums)
        l, r = 0, len(nums) - 1
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l, r = l + 1, r - 1
            
        l, r = 0, k - 1
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l, r = l + 1, r - 1
            
        l, r = k, len(nums) - 1
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l, r = l + 1, r - 1
```

## Complexity

- **Time:** `O(n)` — each element is swapped a constant number of times across the three reversals.
- **Space:** `O(1)` — only a few index variables are used; the array is modified in place.

## Other Approaches

- **Extra array:** place `nums[i]` at index `(i + k) % n` in a new array, then copy it back — Time `O(n)` / Space `O(n)`
- **Slicing:** `nums[:] = nums[-k:] + nums[:-k]` after `k %= n` — Time `O(n)` / Space `O(n)`
- **Cyclic replacements:** move each element to its destination and follow the cycle, using `gcd(n, k)` cycles — Time `O(n)` / Space `O(1)`
- **Brute force:** rotate by one step `k` times — Time `O(n·k)` / Space `O(1)`

## C++

```cpp
/*
    Given an array, rotate the array to the right by k steps, where k is non-negative.
    Ex. 
    Input: nums = [1,2,3,4,5,6,7], k = 3 
    Output: [5,6,7,1,2,3,4]

    1.- To avoid problems with the size of the vector we use the remainder of a division.
    2.- Reverse the entire vector.
    3.- Reverse the parts you want to obtain the result.

    Time: O(1)
    Space: O(1)
*/

class Solution {
public:
    void rotate(vector<int>& nums, int k) {
        k %= nums.size();
        reverse(nums.begin(), nums.end());
        reverse(nums.begin(), nums.begin() + k);
        reverse(nums.begin() + k, nums.end());
    }
};
```
