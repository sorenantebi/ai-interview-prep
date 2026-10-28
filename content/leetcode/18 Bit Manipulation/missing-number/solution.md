---
topic: "Bit Manipulation"
difficulty: Easy
leetcode: https://leetcode.com/problems/missing-number/
neetcode: https://neetcode.io/problems/missing-number
---
# Missing Number - Solution

**Question:** Missing Number - Question · **Difficulty:** Easy

## Intuition

XOR every index `0..n` together with every value in `nums`. Each number that is present appears twice (once as an index or `n`, once as a value) and cancels out, leaving only the missing number. This avoids the overflow concern that the sum formula has in fixed-width languages.

## Approach

1. Start with `res = n`, because the indices only cover `0..n-1`.
2. For each `i, num`: `res ^= i ^ num`.
3. Return `res`.

## Code

```python
class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        res = len(nums)

        for i in range(len(nums)):
            res += i - nums[i]
        return res
```

## Complexity

- **Time:** `O(n)`: one pass.
- **Space:** `O(1)`.

## Other Approaches

- **Gauss sum:** `n * (n + 1) // 2 - sum(nums)`. Time `O(n)`, Space `O(1)`. It could overflow with fixed-width integers; this is safe in Python.
- **Hash set or sort:** check each `0..n` against a set, or sort and look for the first `nums[i] != i`. Time `O(n)` / `O(n log n)`, Space `O(n)` / `O(1)`.

## Key Takeaway

Find the missing element by XOR-ing the expected set with the actual set, so that everything present cancels out. The sum difference does the same job when overflow isn't a concern.

## C++

```cpp
/*
    Given array in range [0, n], return missing
    Ex. nums = [3,0,1] -> 2, nums = [0,1] -> 2

    Use the fact that XOR is its own inverse
    Ex. [0,1,3,4]
    Missing = 4^(0^0)^(1^1)^(2^3)^(3^4)
            = (4^4)^(0^0)^(1^1)^(3^3)^2
            = 0^0^0^0^2 = 2

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    int missingNumber(vector<int>& nums) {
        int n = nums.size();
        int result = n;
        for (int i = 0; i < n; i++) {
            result ^= i ^ nums[i];
        }
        return result;
    }
};
```
