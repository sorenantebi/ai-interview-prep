---
topic: "Sliding Window"
difficulty: Hard
leetcode: https://leetcode.com/problems/sliding-window-maximum/
neetcode: https://neetcode.io/problems/sliding-window-maximum
---
# Sliding Window Maximum - Solution

**Question:** Sliding Window Maximum - Question · **Difficulty:** Hard

## Intuition

Keep a deque of indices whose values are in **decreasing** order. When a new element arrives, any smaller elements at the back can never be a future maximum (the new one is larger and lives longer), so pop them. The front of the deque is always the current window's maximum; pop it once it slides out of the window.

## Approach

1. Create an empty deque `dq` (stores indices) and result list `res`.
2. For each index `i`:
   - Pop from the back while `nums[dq[-1]] <= nums[i]`, then append `i`.
   - If `dq[0] <= i - k`, pop it from the front (out of window).
   - If `i >= k - 1`, append `nums[dq[0]]` to `res`.
3. Return `res`.

## Code

```python
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        output = []
        q = collections.deque()  # index
        l = r = 0
        # O(n) O(n)
        while r < len(nums):
            # pop smaller values from q
            while q and nums[q[-1]] < nums[r]:
                q.pop()
            q.append(r)

            # remove left val from window
            if l > q[0]:
                q.popleft()

            if (r + 1) >= k:
                output.append(nums[q[0]])
                l += 1
            r += 1

        return output
```

## Complexity

- **Time:** `O(n)` — each index is pushed and popped at most once.
- **Space:** `O(k)` — the deque holds at most `k` indices (output `O(n - k + 1)` not counted).

## Other Approaches

- **Max-heap with lazy deletion:** push `(-value, index)` and pop stale tops — Time `O(n log n)`, Space `O(n)`.
- **Brute force:** compute `max` of each window — Time `O(n * k)`, Space `O(1)` extra.

## Key Takeaway

A monotonic deque gives the max (or min) of every sliding window in amortized `O(1)`: drop dominated elements from the back, expired ones from the front.

## C++

```cpp
/*
    Given int array & sliding window size k, return max sliding window
    Ex. nums = [1,3,-1,-3,5,3,6,7] k = 3 -> [3,3,5,5,6,7]

    Sliding window deque, ensure monotonic decr, leftmost largest

    Time: O(n)
    Space: O(n)
*/

class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        deque<int> dq;
        vector<int> result;
        
        int i = 0;
        int j = 0;
        
        while (j < nums.size()) {
            while (!dq.empty() && nums[dq.back()] < nums[j]) {
                dq.pop_back();
            }
            dq.push_back(j);
            
            if (i > dq.front()) {
                dq.pop_front();
            }
            
            if (j + 1 >= k) {
                result.push_back(nums[dq.front()]);
                i++;
            }
            j++;
        }
        
        return result;
    }
};
```
