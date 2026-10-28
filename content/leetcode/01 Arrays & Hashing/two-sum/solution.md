---
topic: "Arrays & Hashing"
difficulty: Easy
leetcode: https://leetcode.com/problems/two-sum/
neetcode: https://neetcode.io/problems/two-integer-sum
---
# Two Sum - Solution

**Question:** Two Sum - Question · **Difficulty:** Easy

## Intuition

For each number `x`, the partner we need is `target - x`. If we store every value we have already passed together with its index in a hash map, we can check in `O(1)` whether the partner appeared earlier, turning the quadratic pair search into one pass.

## Approach

1. Create an empty dict `index_of` mapping value to index.
2. Iterate over `nums` with index `i` and value `x`.
3. Compute `need = target - x`; if `need` is in `index_of`, return `[index_of[need], i]`.
4. Otherwise store `index_of[x] = i` and continue.

## Code

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        prevMap = {}  # val -> index

        for i, n in enumerate(nums):
            diff = target - n
            if diff in prevMap:
                return [prevMap[diff], i]
            prevMap[n] = i
```

## Complexity

- **Time:** `O(n)` — single pass with `O(1)` average hash lookups.
- **Space:** `O(n)` — the dict can store up to `n` entries.

## Other Approaches

- **Brute force:** check every pair `(i, j)` — Time `O(n^2)`, Space `O(1)`.
- **Sort + two pointers:** sort `(value, index)` pairs and move pointers inward — Time `O(n log n)`, Space `O(n)`.

## Key Takeaway

"Find a complement" problems become one-pass with a hash map from value to index; check for the complement before inserting the current element.

## C++

```cpp
/*
    Given int array & target, return indices of 2 nums that add to target
    Ex. nums = [2,7,11,15] & target = 9 -> [0,1], 2 + 7 = 9

    At each num, calculate complement, if exists in hash map then return

    Time: O(n)
    Space: O(n)
*/

class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        int n = nums.size();
        unordered_map<int, int> mp; // val -> index

        for (int i = 0; i < n; i++) {
            int complement = target - nums[i];
            if (mp.find(complement) != mp.end()) {
                return {mp[complement], i};
            }
            mp.insert({nums[i], i});
        }
        return {};
    }
};
```
