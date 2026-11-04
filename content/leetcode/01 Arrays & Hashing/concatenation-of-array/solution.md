---
topic: "Arrays & Hashing"
difficulty: Easy
leetcode: https://leetcode.com/problems/concatenation-of-array/
neetcode: https://neetcode.io/problems/concatenation-of-array
---
# Concatenation of Array - Solution

## Intuition

The answer is just `nums` laid out twice in a row. Element `i` of the result comes from `nums[i % n]`, so we only need to copy the input into both halves of a new array.

## Approach

1. Let `n = len(nums)`.
2. Create `ans` with `2n` slots.
3. For each index `i` in `0..n-1`, set `ans[i] = nums[i]` and `ans[i + n] = nums[i]`.
4. Return `ans`.

## Code

```python
class Solution:
    def getConcatenation(self, nums: List[int]) -> List[int]:
        ans = []
        for i in range(2):
            for n in nums:
                ans.append(n)
        return ans
```

## Complexity

- **Time:** `O(n)` — each element is written exactly twice.
- **Space:** `O(n)` — the output array has `2n` elements (no extra space beyond the output).

## Other Approaches

- **List concatenation:** `return nums + nums` — Time `O(n)` / Space `O(n)`
- **Append loop:** copy `nums` into `ans`, then append each element again in a second pass — Time `O(n)` / Space `O(n)`

## C++

```cpp
class Solution{    
    public:    
        vector<int> getConcatenation(vector<int>& nums){            
            vector<int> ans;            
            int len;            
            len = nums.size();            
            for(int i = 0; i < 2 * len; i++){                
                ans.push_back(nums[i % len]);                
            }
            return ans;            
        }
};
```
