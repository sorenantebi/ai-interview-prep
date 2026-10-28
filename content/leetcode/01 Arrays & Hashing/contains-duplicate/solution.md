---
topic: "Arrays & Hashing"
difficulty: Easy
leetcode: https://leetcode.com/problems/contains-duplicate/
neetcode: https://neetcode.io/problems/duplicate-integer
---
# Contains Duplicate - Solution

**Question:** Contains Duplicate - Question · **Difficulty:** Easy

## Intuition

A duplicate exists exactly when we encounter a value we have already seen. A hash set gives `O(1)` average membership checks, so a single pass that remembers seen values answers the question and can stop early at the first repeat.

## Approach

1. Create an empty set `seen`.
2. Walk through `nums`; if the current value is already in `seen`, return `True`.
3. Otherwise add it to `seen`.
4. If the loop finishes, all values are distinct: return `False`.

## Code

```python
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        hashset = set()

        for n in nums:
            if n in hashset:
                return True
            hashset.add(n)
        return False
```

## Complexity

- **Time:** `O(n)` — one pass with `O(1)` average set operations.
- **Space:** `O(n)` — the set may hold every element.

## Other Approaches

- **Sort then compare neighbours:** duplicates become adjacent after sorting — Time `O(n log n)`, Space `O(1)` to `O(n)` depending on the sort.
- **Length comparison:** `len(set(nums)) != len(nums)` — Time `O(n)`, Space `O(n)` (no early exit).

## Key Takeaway

"Have I seen this before?" is the canonical hash-set question; trade `O(n)` memory for linear time instead of sorting.

## C++

```cpp
/*
    Given int array, return true if any value appears at least twice
    Ex. nums = [1,2,3,1] -> true, nums = [1,2,3,4] -> false

    If the number has been seen previously, then it has a duplicate. Otherwise, insert it into the hash set.

    Time: O(n)
    Space: O(n)
*/

class Solution {
public:
    bool containsDuplicate(vector<int>& nums) {
        unordered_set<int> s;
        
        for (int i = 0; i < nums.size(); i++) {
            if (s.find(nums[i]) != s.end()) {
                return true;
            }
            s.insert(nums[i]);
        }
        
        return false;
    }
};
```
