---
topic: "Arrays & Hashing"
difficulty: Medium
leetcode: https://leetcode.com/problems/longest-consecutive-sequence/
neetcode: https://neetcode.io/problems/longest-consecutive-sequence
---
# Longest Consecutive Sequence - Solution

**Question:** Longest Consecutive Sequence - Question · **Difficulty:** Medium

## Intuition

Put all values in a hash set. A number `x` starts a sequence only if `x - 1` is not in the set; from each such start we count upward while `x + 1, x + 2, ...` exist. Every number is visited by at most one upward walk, so the total work is linear.

## Approach

1. Build `num_set = set(nums)`.
2. For each `x` in `num_set`, skip it if `x - 1` is in the set (it is not a sequence start).
3. Otherwise walk `y = x` upward while `y + 1` is in the set, counting the length.
4. Track and return the maximum length (0 for an empty input).

## Code

```python
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        numSet = set(nums)
        longest = 0

        for n in numSet:
            # check if its the start of a sequence
            if (n - 1) not in numSet:
                length = 1
                while (n + length) in numSet:
                    length += 1
                longest = max(length, longest)
        return longest
```

## Complexity

- **Time:** `O(n)` — each element is part of exactly one upward walk, and set lookups are `O(1)` average.
- **Space:** `O(n)` — the hash set.

## Other Approaches

- **Sort and scan:** sort, skip duplicates, and count runs of `+1` steps — Time `O(n log n)`, Space `O(1)` to `O(n)`.
- **Union-Find:** union `x` with `x + 1` when both exist and take the largest component — Time `~O(n)`, Space `O(n)`.

## Key Takeaway

Only start expanding from the beginning of a sequence (`x - 1` absent); this "start-only" check turns a naive quadratic scan into linear time.

## C++

```cpp
/*
    Given unsorted array, return length of longest consecutive sequence
    Ex. nums = [100,4,200,1,3,2] -> 4, longest is [1,2,3,4]

    Store in hash set, only check for longer seq if it's the beginning

    Time: O(n)
    Space: O(n)
*/


class Solution {
public:
    int longestConsecutive(vector<int>& nums) {
        unordered_set<int>s(nums.begin(), nums.end());
        int longest = 0;
        for(auto &n: s){
            //if this is the start of the sequence
            if(!s.count(n - 1)){
                int length = 1; 
                while(s.count(n + length))
                    ++length;
                longest = max(longest, length);
            } 

        }
        return longest;
    }
};
```
