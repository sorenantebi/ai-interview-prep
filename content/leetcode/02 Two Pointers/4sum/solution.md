---
topic: "Two Pointers"
difficulty: Medium
leetcode: https://leetcode.com/problems/4sum/
neetcode: https://neetcode.io/problems/4sum
---
# 4Sum - Solution

## Intuition

Sorting the array lets us reduce the problem step by step: fix the two smallest numbers with nested loops, then find the remaining two with a two-pointer sweep, exactly as in 3Sum. Sorting also puts equal values next to each other, so duplicates are easy to skip.

## Approach

1. Sort `nums`.
2. Loop `i` over the first element. Skip it if it equals the previous value (to avoid duplicate quadruplets).
3. Loop `j` over the second element, starting at `i + 1`, with the same duplicate skip.
4. Set `left = j + 1` and `right = n - 1`, and compute the sum of the four values.
   - If the sum is smaller than `target`, move `left` right.
   - If it is larger, move `right` left.
   - If it matches, record the quadruplet, move both pointers, and skip over repeated values on both sides.
5. Return all recorded quadruplets.

## Code

```python
class Solution:
    def fourSum(self, nums, target):
        def findNsum(l, r, target, N, result, results):
            if r-l+1 < N or N < 2 or target < nums[l]*N or target > nums[r]*N:  
                return
            if N == 2: 
                while l < r:
                    s = nums[l] + nums[r]
                    if s == target:
                        results.append(result + [nums[l], nums[r]])
                        l += 1
                        while l < r and nums[l] == nums[l-1]:
                            l += 1
                    elif s < target:
                        l += 1
                    else:
                        r -= 1
            else:
                for i in range(l, r+1):
                    if i == l or (i > l and nums[i-1] != nums[i]):
                        findNsum(i+1, r, target-nums[i], N-1, result+[nums[i]], results)

        nums.sort()
        results = []
        findNsum(0, len(nums)-1, target, 4, [], results)
        return results
```

## Complexity

- **Time:** `O(n^3)` — two nested loops fix the first two numbers, and each two-pointer sweep is `O(n)`; sorting adds only `O(n log n)`.
- **Space:** `O(1)` — extra space beyond the output and the sort is constant.

## Other Approaches

- **Brute force:** check every combination of four indices and dedupe with a set — Time `O(n^4)` / Space `O(k)` for the set of results.
- **Hash map of pair sums:** store pair sums and look up the complement, deduping the results — Time `O(n^2)` average (but can degrade with many duplicate combinations) / Space `O(n^2)`.
- **Generalized k-Sum recursion:** recurse down to 2Sum with two pointers — Time `O(n^(k-1))` / Space `O(k)` recursion depth.

## C++

```cpp
// Time Complexity = O(n^3)
// Space Complexity = O(n)

class Solution {
public:
    vector<vector<int>> fourSum(vector<int>& nums, int target) {
        sort(nums.begin(), nums.end());

        vector<vector<int> > res;
        int n = nums.size();

        for (int i = 0; i < n; i++) {
            if (i > 0 && nums[i] == nums[i - 1])
                continue;
            for (int j = i + 1; j < n; j++) {
                if (j > (i + 1) && nums[j] == nums[j - 1])
                    continue;
                int l = j + 1, r = n - 1;
                while (l < r) {
                    long sm = (long)nums[i] + (long)nums[j] + (long)nums[l] + (long)nums[r];
                    if (sm == target) {
                        res.push_back(vector<int>{nums[i], nums[j], nums[l], nums[r]});
                        l += 1;
                        while (l < r && nums[l] == nums[l - 1])
                            l += 1;
                    }
                    else if (sm > target)
                        r -= 1;
                    else
                        l += 1;
                }
            }
        }
        return res;
    }
};
```
