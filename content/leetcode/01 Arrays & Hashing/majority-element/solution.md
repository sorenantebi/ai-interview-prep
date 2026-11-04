---
topic: "Arrays & Hashing"
difficulty: Easy
leetcode: https://leetcode.com/problems/majority-element/
neetcode: https://neetcode.io/problems/majority-element
---
# Majority Element - Solution

## Intuition

The majority element appears more than half the time, so it outnumbers all other elements combined. If we pair off each occurrence of it with a different element, it still has occurrences left over. This is the idea behind the Boyer-Moore voting algorithm: keep a candidate and a counter, and let differing elements cancel each other out.

## Approach

1. Initialize `candidate` to nothing and `count` to `0`.
2. For each number `num` in `nums`:
   - If `count == 0`, set `candidate = num`.
   - If `num == candidate`, increment `count`; otherwise decrement it.
3. Since a majority element is guaranteed to exist, return `candidate`.

## Code

```python
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        res, count = 0, 0

        for n in nums:
            if count == 0:
                res = n
            count += (1 if n == res else -1)
            
        return res
```

## Complexity

- **Time:** `O(n)` — a single pass over the array.
- **Space:** `O(1)` — only a candidate and a counter are stored.

## Other Approaches

- **Hash map counting:** count occurrences of each value and return the one with count > n/2 — Time `O(n)` / Space `O(n)`
- **Sorting:** after sorting, the element at index `n // 2` is the majority — Time `O(n log n)` / Space `O(1)` or `O(n)` depending on the sort
- **Bit counting:** for each of the 32 bit positions, the majority element's bit is the one set in more than half the numbers — Time `O(32n)` / Space `O(1)`

## C++

```cpp
/*
Given an array nums of size n, return the majority element.

The majority element is the element that appears more than ⌊n / 2⌋ times. You may assume that the majority element always exists in the array.
*/

class Solution {
public:
    int majorityElement(vector<int>& nums) {
        int count = 0;
        int res = 0;

        for (const int& num: nums) {
            if (count == 0) {
                res = num;
            } 
            count += (num == res) ? 1 : -1;
        }

        return res;
    }
};
```
