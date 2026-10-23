---
topic: "Two Pointers"
difficulty: Medium
leetcode: https://leetcode.com/problems/3sum/
neetcode: https://neetcode.io/problems/three-integer-sum
---
# 3Sum - Solution

**Question:** 3Sum - Question · **Difficulty:** Medium

## Intuition

Sort the array, then fix the smallest element `a = nums[i]` and solve Two Sum II on the suffix for target `-a` with two pointers. Sorting also makes duplicates adjacent, so skipping equal neighbors (for the fixed element and after each found pair) prevents duplicate triplets.

## Approach

1. Sort `nums`.
2. For each index `i`:
   - If `nums[i] > 0`, break: with a positive smallest value the sum can never reach 0.
   - Skip `i` if `nums[i] == nums[i - 1]`.
   - Set `l = i + 1`, `r = n - 1` and move them like Two Sum II.
   - On a hit, record the triplet, move `l` forward, and skip duplicates of `nums[l]`.
3. Return all recorded triplets.

## Code

```python
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        res = []
        nums.sort()

        for i, a in enumerate(nums):
            # Skip positive integers
            if a > 0:
                break

            if i > 0 and a == nums[i - 1]:
                continue

            l, r = i + 1, len(nums) - 1
            while l < r:
                threeSum = a + nums[l] + nums[r]
                if threeSum > 0:
                    r -= 1
                elif threeSum < 0:
                    l += 1
                else:
                    res.append([a, nums[l], nums[r]])
                    l += 1
                    r -= 1
                    while nums[l] == nums[l - 1] and l < r:
                        l += 1
                        
        return res
```

## Complexity

- **Time:** `O(n^2)` — `O(n log n)` sort plus an `O(n)` two-pointer scan for each `i`.
- **Space:** `O(1)` extra (or `O(n)` depending on the sort implementation), excluding the output.

## Other Approaches

- **Brute force with a set:** check all triples and dedupe via sorted tuples — Time `O(n^3)`, Space `O(k)` for results.
- **Hash set per fixed element:** for each `i`, run hash-based Two Sum on the rest — Time `O(n^2)`, Space `O(n)`.

## Key Takeaway

k-Sum reduces to "sort, fix one element, solve (k-1)-Sum", bottoming out at two pointers; skipping equal neighbors after sorting handles deduplication.
