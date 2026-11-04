---
topic: "Binary Search"
difficulty: Easy
leetcode: https://leetcode.com/problems/search-insert-position/
neetcode: https://neetcode.io/problems/search-insert-position
---
# Search Insert Position - Solution

## Intuition

The insert position is the index of the first element that is greater than or equal to `target`. Because the array is sorted, this "first element satisfying a condition" can be found with binary search. If no element qualifies, the answer is `len(nums)`.

## Approach

1. Set `left = 0` and `right = len(nums)`, so the search range is the half-open interval `[left, right)`.
2. While `left < right`, compute `mid = (left + right) // 2`.
3. If `nums[mid] < target`, the answer lies to the right, so set `left = mid + 1`.
4. Otherwise `nums[mid] >= target`, so `mid` could be the answer; set `right = mid`.
5. When the loop ends, `left == right` is the first index with `nums[i] >= target` (or `len(nums)`). Return `left`.

## Code

```python
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        # O(log n) and O(1)
        
        
        low, high = 0, len(nums)
        while low<high:
            mid = low +(high - low) // 2
            if target > nums[mid]:
                low = mid + 1
            else:
                high = mid
        return low
```

## Complexity

- **Time:** `O(log n)` — the search range is halved on every iteration.
- **Space:** `O(1)` — only a few integer variables are used.

## Other Approaches

- **Linear scan:** return the first index whose value is `>= target`, or `len(nums)` — Time `O(n)` / Space `O(1)`
- **Built-in `bisect_left`:** `bisect.bisect_left(nums, target)` does the same binary search — Time `O(log n)` / Space `O(1)`

## C++

```cpp
/*
    Given a sorted array of distinct integers and a target value, return the index if the target is found. 
    If not, return the index where it would be if it were inserted in order.

    Ex.
    Input: nums = [1,3,5,6], target = 5
    Output: 2

    1.- Find the number in the middle of the vector.
    2.- Takes a part (first or second), depending on whether or not the target is greater than the middel.
    3.- Change the current left or right part.
    3.- Do this process until the left exceeds the right.

    Time: O(log n)
    Space: O(1)
*/

class Solution {
public:
    int searchInsert(vector<int>& nums, int target) {
        int left = 0;
        int right = nums.size() - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;

            if (nums[mid] < target)
                left = mid + 1;
            else
                right = mid - 1;
        }
        return left;
    }
};
```
