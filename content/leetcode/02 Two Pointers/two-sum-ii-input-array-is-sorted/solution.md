---
topic: "Two Pointers"
difficulty: Medium
leetcode: https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/
neetcode: https://neetcode.io/problems/two-integer-sum-ii
---
# Two Sum II Input Array Is Sorted - Solution

**Question:** Two Sum II Input Array Is Sorted - Question · **Difficulty:** Medium

## Intuition

With a sorted array, start one pointer at each end. If their sum is too large, the only way to shrink it is to move the right pointer left; if too small, move the left pointer right. Each move safely discards a value that cannot be part of the answer.

## Approach

1. Set `l = 0`, `r = len(numbers) - 1`.
2. While `l < r`, compute `s = numbers[l] + numbers[r]`:
   - If `s == target`, return `[l + 1, r + 1]`.
   - If `s > target`, decrement `r`; otherwise increment `l`.

## Code

```python
class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        l, r = 0, len(numbers) - 1

        while l < r:
            curSum = numbers[l] + numbers[r]

            if curSum > target:
                r -= 1
            elif curSum < target:
                l += 1
            else:
                return [l + 1, r + 1]
```

## Complexity

- **Time:** `O(n)` — pointers move toward each other, at most `n` steps total.
- **Space:** `O(1)` — two indices.

## Other Approaches

- **Binary search per element:** for each `i`, binary search `target - numbers[i]` in the suffix — Time `O(n log n)`, Space `O(1)`.
- **Hash map (Two Sum I):** Time `O(n)`, Space `O(n)` — ignores the sorted property and breaks the constant-space requirement.

## Key Takeaway

Sorted input plus a pair-sum target means opposite-end two pointers: the comparison with the target tells you exactly which pointer to move.

## C++

```cpp
/*
    Given a 1-indexed sorted int array & target:
    Return indices (added by 1) of 2 nums that add to target

    2 pointers, outside in, iterate i/j if sum is too low/high

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    vector<int> twoSum(vector<int>& numbers, int target) {
        int i = 0;
        int j = numbers.size() - 1;
        
        vector<int> result;
        
        while (i < j) {
            int sum = numbers[i] + numbers[j];
            if (sum < target) {
                i++;
            } else if (sum > target) {
                j--;
            } else {
                result.push_back(i + 1);
                result.push_back(j + 1);
                break;
            }
        }
        
        return result;
    }
};
```
