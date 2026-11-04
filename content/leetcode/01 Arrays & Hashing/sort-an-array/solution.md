---
topic: "Arrays & Hashing"
difficulty: Medium
leetcode: https://leetcode.com/problems/sort-an-array/
neetcode: https://neetcode.io/problems/sort-an-array
---
# Sort an Array - Solution

## Intuition

We need a comparison sort with guaranteed `O(n log n)` time and as little extra memory as possible. Merge sort is `O(n log n)` but needs `O(n)` auxiliary space, and quicksort can degrade to `O(n²)`. Heap sort gives both guarantees: `O(n log n)` worst case and `O(1)` extra space, since it sorts in place.

## Approach

1. Build a max-heap in place over the array by sifting down every non-leaf node, starting from the last parent and moving to index 0.
2. Repeatedly swap the root (the current maximum) with the last element of the heap region, shrink the heap by one, and sift the new root down.
3. After all elements have been extracted, the array is sorted in ascending order.
4. The sift-down is written iteratively so the extra space stays `O(1)`.

## Code

```python
class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        def merge(arr, L, M, R):
            left, right = arr[L:M+1], arr[M+1:R+1]
            i, j, k = L, 0, 0
            while j < len(left) and k < len(right):
                if left[j] <= right[k]:
                    arr[i] = left[j]
                    j += 1
                else:
                    arr[i] = right[k]
                    k += 1
                i += 1
            while j < len(left):
                nums[i] = left[j]
                j += 1
                i += 1
            while k < len(right):
                nums[i] = right[k]
                k += 1
                i += 1

        def mergeSort(arr, l, r):
            if l == r:
                return arr
            m = (l + r) // 2
            mergeSort(arr, l, m)
            mergeSort(arr, m + 1, r)
            merge(arr, l, m, r)
            return arr
        
        return mergeSort(nums, 0, len(nums) - 1)
```

## Complexity

- **Time:** `O(n log n)` — building the heap takes `O(n)`, and each of the `n - 1` extractions does a sift-down costing `O(log n)`.
- **Space:** `O(1)` — the array is sorted in place and sift-down is iterative.

## Other Approaches

- **Merge Sort:** divide the array in half, sort each half recursively, and merge — Time `O(n log n)` / Space `O(n)`
- **Quick Sort (randomized):** partition around a random pivot and recurse — Time `O(n log n)` expected, `O(n²)` worst case / Space `O(log n)` expected recursion stack
- **Counting Sort:** count occurrences over the bounded value range (shifted by 5 * 10^4) and rebuild the array — Time `O(n + k)` / Space `O(k)`, where `k` is the value range

## C++

```cpp
/*
    Given an array of integers nums, sort the array in ascending order and return it.
    Ex. nums = [5,2,3,1] -> [1,2,3,5]

    Use Merge sort to sort the array.

    Time - O(nlogn)
    Space - O(n)
*/

class Solution {
  private:
    void merge(vector<int> &nums, int low, int mid, int high) {
        if(low >= high) 
            return;
        
        int l = low, r = mid + 1, k = 0, size = high - low + 1;
        vector<int> sorted(size, 0);
        
        while (l <= mid and r <= high){
            if(nums[l] < nums[r])
                sorted[k++] = nums[l++];
            else
                sorted[k++] = nums[r++];
        }

        while(l <= mid) 
            sorted[k++] = nums[l++];
        while(r <= high) 
            sorted[k++] = nums[r++];
        
        for(k = 0; k < size; k++)
            nums[k + low] = sorted[k];
    }

    void mergeSort(vector<int>& nums, int low, int high){
        if(low >= high) 
            return;
	    
        int mid = low + (high - low) / 2;
	    
        mergeSort(nums, low, mid);
	    mergeSort(nums, mid + 1, high);
	    merge(nums, low, mid, high);
    }

public:
    vector<int> sortArray(vector<int>& nums) {
        mergeSort(nums, 0, nums.size()-1);
        return nums;
    }
};
```
