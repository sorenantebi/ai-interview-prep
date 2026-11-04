---
topic: "Two Pointers"
difficulty: Easy
leetcode: https://leetcode.com/problems/remove-duplicates-from-sorted-array/
neetcode: https://neetcode.io/problems/remove-duplicates-from-sorted-array
---
# Remove Duplicates from Sorted Array - Solution

## Intuition

Because the array is sorted, equal values sit next to each other. A value is new exactly when it differs from the last unique value we kept. So we can keep a write pointer marking where the next unique value belongs and overwrite the array from the front as we scan.

## Approach

1. Set `k = 1`; the first element is always unique and already in place.
2. Scan `i` from `1` to `len(nums) - 1`.
3. If `nums[i] != nums[k - 1]`, it is a new unique value: write it to `nums[k]` and increment `k`.
4. After the scan, return `k`. The first `k` entries are the unique values in order.

## Code

```python
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        L = 1
        
        for R in range(1, len(nums)):
            if nums[R] != nums[R - 1]:
                nums[L] = nums[R]
                L += 1
        return L
```

## Complexity

- **Time:** `O(n)` — a single pass over the array.
- **Space:** `O(1)` — only two index variables are used; the array is modified in place.

## Other Approaches

- **Set + sort:** collect unique values with a set, sort them, and copy back — Time `O(n log n)` / Space `O(n)`; ignores the sorted property and uses extra memory.
- **Delete in place:** `del nums[i]` whenever a duplicate is found — Time `O(n^2)` / Space `O(1)`; each deletion shifts the remaining elements.

## C++

```cpp
int removeDuplicates(int* nums, int numsSize){
    int indx = 1;
    
    for(int i = 1; i < numsSize; i++){
        if(nums[i] != nums[i-1]){
            nums[indx] = nums[i];
            indx++;
        }
    }
    return indx;
}
```
