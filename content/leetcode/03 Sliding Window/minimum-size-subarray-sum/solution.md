---
topic: "Sliding Window"
difficulty: Medium
leetcode: https://leetcode.com/problems/minimum-size-subarray-sum/
neetcode: https://neetcode.io/problems/minimum-size-subarray-sum
---
# Minimum Size Subarray Sum - Solution

## Intuition

Because every number is positive, extending a window to the right always increases its sum, and shrinking it from the left always decreases it. That monotonic behavior lets us use a variable-size sliding window: grow until the sum is big enough, then shrink as much as possible while it still qualifies.

## Approach

1. Keep two pointers `left` and `right` and a running `window_sum`, starting at zero.
2. Move `right` across the array, adding `nums[right]` to `window_sum`.
3. While `window_sum >= target`, record `right - left + 1` as a candidate answer, subtract `nums[left]`, and advance `left`.
4. After the loop, return the best length found, or `0` if no window ever reached `target`.

## Code

```python
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        res = float('inf')
        l, total = 0, 0

        for r in range(len(nums)):
            total += nums[r]
            while total >= target:
                res = min(res, r - l + 1)
                total -= nums[l]
                l += 1
        return res if res != float('inf') else 0
```

## Complexity

- **Time:** `O(n)` — each index is added once by `right` and removed at most once by `left`.
- **Space:** `O(1)` — only a few scalar variables are used.

## Other Approaches

- **Prefix sums + binary search:** build a prefix-sum array (strictly increasing since values are positive) and, for each start index, binary search for the earliest end with sum `>= target` — Time `O(n log n)` / Space `O(n)`
- **Brute force:** check the sum of every subarray, breaking early once it reaches `target` — Time `O(n^2)` / Space `O(1)`

## C++

```cpp
/* Given an array of positive integers nums and a positive integer target, 
return the minimal length of a contiguous subarray [numsl, numsl+1, ..., numsr-1, numsr] 
of which the sum is greater than or equal to target. 
If there is no such subarray, return 0 instead.
Ex.: target = 7, nums = [2,3,1,2,4,3] -> 2 
     target = 4, nums = [1,4,4] -> 1     
Sliding window (with two pointer). Keep adding elements to the SL. When Sum => target or SP points to end of the vector resize the SW. */

class Solution{    
    public:    
        int minSubArrayLen(int target, vector<int>& nums){            
            int min;            
            int fp, sp;            
            int sum;            
            fp = 0;            
            sp = 1;            
            sum = nums[0];            
            min = nums.size() + 1;            
            while(fp != sp){                
                if(Sum >= target){                    
                    min = min(sp - fp, min);                    
                    sum = Sìsum - nums[fp];                    
                    fp++;                    
                }
                else{                        
                    if(sp < nums.size()){                         
                        sum = sum + nums[sp];
                        sp++;                            
                    }
                    else{                            
                        fp++;                            
                    }                    
                }                  
            }            
            return min;
        }    
};
```
