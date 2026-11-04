---
topic: "Sliding Window"
difficulty: Easy
leetcode: https://leetcode.com/problems/contains-duplicate-ii/
neetcode: https://neetcode.io/problems/contains-duplicate-ii
---
# Contains Duplicate II - Solution

## Intuition

Two equal values are close enough exactly when the later one sees the earlier one within the last `k` positions. Keeping a window of the most recent `k` elements in a set lets us check for a duplicate in constant time as we scan.

## Approach

1. Maintain a set `window` holding the values of the last at most `k` elements.
2. For each index `i`, if `nums[i]` is already in `window`, return `True`.
3. Add `nums[i]` to `window`.
4. If the window now has more than `k` elements, remove `nums[i - k]`.
5. If the scan finishes without a hit, return `False`.

## Code

```python
class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        window = set()
        L = 0

        for R in range(len(nums)):
            if R - L > k:
                window.remove(nums[L])
                L += 1
            if nums[R] in window:
                return True
            window.add(nums[R])
        return False
```

## Complexity

- **Time:** `O(n)` — each element is added and removed at most once, with `O(1)` average set operations.
- **Space:** `O(min(n, k))` — the window never holds more than `k` values.

## Other Approaches

- **Hash map of last index:** store each value's most recent index and check `i - last[num] <= k` — Time `O(n)` / Space `O(n)`
- **Brute force:** compare each element with the next `k` elements — Time `O(n·k)` / Space `O(1)`

## C++

```cpp
class Solution {
public:
    bool containsNearbyDuplicate(vector<int>& nums, int k) {
        unordered_map<int,int> number_map;
        for (int i = 0; i < nums.size(); ++i) {
            int num = nums[i];
            if (number_map.find(num) != number_map.end() && i - number_map[num] <= k) {
                return true;
            }else {
                number_map[num] = i;
            }
        }
        return false;
    }
};
```
