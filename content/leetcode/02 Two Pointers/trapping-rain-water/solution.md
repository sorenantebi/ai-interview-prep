---
topic: "Two Pointers"
difficulty: Hard
leetcode: https://leetcode.com/problems/trapping-rain-water/
neetcode: https://neetcode.io/problems/trapping-rain-water
---
# Trapping Rain Water - Solution

**Question:** Trapping Rain Water - Question · **Difficulty:** Hard

## Intuition

Water above a bar depends on the smaller of the tallest bars to its left and right. With two pointers, track `leftMax` and `rightMax`. Whichever side has the smaller max is the bottleneck: the opposite side is already known to have something at least as tall, so the water at the smaller side's pointer is fully determined and can be added immediately.

## Approach

1. Set `l = 0`, `r = n - 1`, `leftMax = height[l]`, `rightMax = height[r]`, `water = 0`.
2. While `l < r`:
   - If `leftMax < rightMax`: move `l` right, update `leftMax = max(leftMax, height[l])`, add `leftMax - height[l]`.
   - Else: move `r` left, update `rightMax`, add `rightMax - height[r]`.
3. Return `water`.

## Code

```python
class Solution:
    def trap(self, height: List[int]) -> int:
        if not height:
            return 0

        l, r = 0, len(height) - 1
        leftMax, rightMax = height[l], height[r]
        res = 0
        while l < r:
            if leftMax < rightMax:
                l += 1
                leftMax = max(leftMax, height[l])
                res += leftMax - height[l]
            else:
                r -= 1
                rightMax = max(rightMax, height[r])
                res += rightMax - height[r]
        return res
```

## Complexity

- **Time:** `O(n)` — each index is visited once.
- **Space:** `O(1)` — only a few running values.

## Other Approaches

- **Prefix/suffix max arrays:** precompute `maxLeft[i]` and `maxRight[i]`, sum `min(...) - height[i]` — Time `O(n)`, Space `O(n)`.
- **Monotonic stack:** pop shorter bars and fill horizontal layers between boundaries — Time `O(n)`, Space `O(n)`.

## Key Takeaway

When an answer depends on `min(leftMax, rightMax)`, process from the side with the smaller max: that side's value is final, which turns an `O(n)`-space solution into `O(1)`.

## C++

```cpp
/*
    Given elevation map array, compute trapped water
    Ex. height = [0,1,0,2,1,0,1,3,2,1,2,1] -> 6

    2 pointers, outside in, track max left/right
    For lower max, curr only dependent on that one
    Compute height of these, iterate lower one

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    int trap(vector<int>& height) {
        int i = 0;
        int j = height.size() - 1;
        
        int maxLeft = height[i];
        int maxRight = height[j];
        
        int result = 0;
        
        while (i < j) {
            if (maxLeft <= maxRight) {
                i++;
                maxLeft = max(maxLeft, height[i]);
                result += maxLeft - height[i];
            } else {
                j--;
                maxRight = max(maxRight, height[j]);
                result += maxRight - height[j];
            }
        }
        
        return result;
    }
};
```
