---
topic: "Heap / Priority Queue"
difficulty: Medium
leetcode: https://leetcode.com/problems/kth-largest-element-in-an-array/
neetcode: https://neetcode.io/problems/kth-largest-element-in-an-array
---
# Kth Largest Element In An Array - Solution

**Question:** Kth Largest Element In An Array - Question · **Difficulty:** Medium

## Intuition

Only the `k` largest values matter. Maintain a **min-heap of size `k`** while scanning: after processing all elements, the heap holds exactly the `k` largest, and its root is the smallest of them — the `k`-th largest overall.

## Approach

1. Heapify the first `k` elements into a min-heap.
2. For every remaining element, if it is larger than the heap root, replace the root with it (`heapreplace`).
3. Return the heap root.

## Code

```python
# Solution: Sorting
# Time Complexity:
#   - Best Case: O(n*log(k))
#   - Average Case: O(n*log(k))
#   - Worst Case:O(n*log(k))
# Extra Space Complexity: O(k)
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        heapify(nums)
        while len(nums) > k:
            heappop(nums)
        return nums[0]

# Solution: Sorting
# Time Complexity:
#   - Best Case: O(n)
#   - Average Case: O(n*log(n))
#   - Worst Case:O(n*log(n))
# Extra Space Complexity: O(n)
class Solution1:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        nums.sort()
        return nums[len(nums) - k]


# Solution: QuickSelect
# Time Complexity: O(n)
# Extra Space Complexity: O(n)
class Solution2:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        pivot = random.choice(nums)
        left = [num for num in nums if num > pivot]
        mid = [num for num in nums if num == pivot]
        right = [num for num in nums if num < pivot]

        length_left = len(left)
        length_right = len(right)
        length_mid = len(mid)
        if k <= length_left:
            return self.findKthLargest(left, k)
        elif k > length_left + length_mid:
            return self.findKthLargest(right, k - length_mid - length_left)
        else:
            return mid[0]
```

## Complexity

- **Time:** `O(n log k)` — each element triggers at most one `O(log k)` heap operation.
- **Space:** `O(k)` — the heap.

## Other Approaches

- **Quickselect (Hoare / Lomuto partition with random pivot):** partition around a pivot and recurse into the side containing index `n - k` — Time `O(n)` average / `O(n^2)` worst, Space `O(1)` extra.
- **Sort:** `sorted(nums)[-k]` — Time `O(n log n)`, Space `O(n)`.

## Key Takeaway

k-th largest = root of a size-`k` min-heap (`O(n log k)`); mention quickselect for `O(n)` average if the interviewer pushes for better.

## C++

```cpp
/*
    Given array and int k, return kth largest element in array
    Ex. nums = [3,2,1,5,6,4], k = 2 -> 5

    Quickselect, partition until pivot = k, left side all > k

    Time: O(n) -> optimized from O(n log k) min heap solution
    Space: O(1)
*/

// class Solution {
// public:
//     int findKthLargest(vector<int>& nums, int k) {
//         priority_queue<int, vector<int>, greater<int>> pq;
//         for (int i = 0; i < nums.size(); i++) {
//             pq.push(nums[i]);
//             if (pq.size() > k) {
//                 pq.pop();
//             }
//         }
//         return pq.top();
//     }
// };

/*
class Solution {
public:
    int findKthLargest(vector<int>& nums, int k) {
        int low = 0;
        int high = nums.size() - 1;
        int pivotIndex = nums.size();
        
        while (pivotIndex != k - 1) {
            pivotIndex = partition(nums, low, high);
            if (pivotIndex < k - 1) {
                low = pivotIndex + 1;
            } else {
                high = pivotIndex - 1;
            }
        }
        
        return nums[k - 1];
    }
private:
    int partition(vector<int>& nums, int low, int high) {
        int pivot = nums[low];
        
        int i = low + 1;
        int j = high;
        
        while (i <= j) {
            if (nums[i] < pivot && pivot < nums[j]) {
                swap(nums[i], nums[j]);
                i++;
                j--;
            }
            if (nums[i] >= pivot) {
                i++;
            }
            if (pivot >= nums[j]) {
                j--;
            }
        }
        
        swap(nums[low], nums[j]);
        return j;
    }
};
*/

// Video's QuickSelect implementation
// class Solution {
// public:
//     int findKthLargest(vector<int>& nums, int k) {
//         int index = nums.size() - k;
//         return quickSelect(nums, index, 0, nums.size() - 1);
//     }
// private:
//     int quickSelect(vector<int>& nums, int k, int l, int r){
//         int pivot = nums[r];
//         int p_pos = l;
//         for (int i = l; i < r; ++i){
//             if (nums[i] <= pivot){
//                 swap(nums[i], nums[p_pos]);
//                 ++p_pos;
//             }
//         }
//         swap(nums[p_pos], nums[r]);
//         if (k < p_pos)
//             return quickSelect(nums, k, l, p_pos - 1);
//         if (k > p_pos)
//             return quickSelect(nums, k, p_pos + 1, r);
//         return nums[p_pos];
//     }
// };

// Solution that can pass current tests
class Solution {
public:
    int findKthLargest(vector<int>& nums, int k) {
        int pivot = nums[rand() % nums.size()];
        vector<int> left, mid, right;
        for (auto num: nums) {
            if (num > pivot) left.push_back(num);
            else if (num == pivot) mid.push_back(num);
            else right.push_back(num);
        }
        if (k <= left.size()) return findKthLargest(left, k);
        else if (k <= left.size() + mid.size()) return mid[0];
        else return findKthLargest(right, k - left.size() - mid.size());
    }
};
```
