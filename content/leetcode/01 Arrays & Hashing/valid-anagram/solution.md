---
topic: "Arrays & Hashing"
difficulty: Easy
leetcode: https://leetcode.com/problems/valid-anagram/
neetcode: https://neetcode.io/problems/is-anagram
---
# Valid Anagram - Solution

**Question:** Valid Anagram - Question · **Difficulty:** Easy

## Intuition

Two strings are anagrams exactly when their character frequency tables are equal. With only 26 lowercase letters, a fixed-size count array is enough: increment for characters of `s`, decrement for characters of `t`, and check everything returns to zero.

## Approach

1. If the lengths differ, return `False` immediately.
2. Create a count array of 26 zeros.
3. For each position `i`, increment the count of `s[i]` and decrement the count of `t[i]`.
4. Return `True` only if every count is zero.

## Code

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        countS, countT = {}, {}

        for i in range(len(s)):
            countS[s[i]] = 1 + countS.get(s[i], 0)
            countT[t[i]] = 1 + countT.get(t[i], 0)
        return countS == countT

    
    # easier solution
    #return True if sorted(s) == sorted(t) else False
```

## Complexity

- **Time:** `O(n)` — one pass over both strings plus a 26-entry check.
- **Space:** `O(1)` — the count array has fixed size 26.

## Other Approaches

- **Sorting:** `sorted(s) == sorted(t)` — Time `O(n log n)`, Space `O(n)`.
- **Hash map / `Counter`:** `Counter(s) == Counter(t)`; also handles Unicode (the follow-up) — Time `O(n)`, Space `O(k)` for `k` distinct characters.

## Key Takeaway

Anagram checks reduce to comparing frequency counts; use a fixed array for small alphabets and a hash map for arbitrary characters.
