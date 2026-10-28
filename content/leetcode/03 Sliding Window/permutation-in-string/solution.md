---
topic: "Sliding Window"
difficulty: Medium
leetcode: https://leetcode.com/problems/permutation-in-string/
neetcode: https://neetcode.io/problems/permutation-string
---
# Permutation In String - Solution

**Question:** Permutation In String - Question · **Difficulty:** Medium

## Intuition

A permutation of `s1` is any string with identical letter counts, so slide a window of fixed length `len(s1)` over `s2` and compare letter-count arrays. Instead of comparing all 26 counts each step, maintain `matches`: how many of the 26 letters currently have equal counts; the answer is found when `matches == 26`.

## Approach

1. If `len(s1) > len(s2)`, return `False`.
2. Build count arrays `c1` (for `s1`) and `c2` (for the first window of `s2`) and compute `matches`.
3. Slide the window one step at a time: add the new right char and remove the old left char, updating `matches` whenever a count becomes equal or stops being equal.
4. Return `True` as soon as `matches == 26`, otherwise `False`.

## Code

```python
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2):
            return False

        s1Count, s2Count = [0] * 26, [0] * 26
        for i in range(len(s1)):
            s1Count[ord(s1[i]) - ord("a")] += 1
            s2Count[ord(s2[i]) - ord("a")] += 1

        matches = 0
        for i in range(26):
            matches += 1 if s1Count[i] == s2Count[i] else 0

        l = 0
        for r in range(len(s1), len(s2)):
            if matches == 26:
                return True

            index = ord(s2[r]) - ord("a")
            s2Count[index] += 1
            if s1Count[index] == s2Count[index]:
                matches += 1
            elif s1Count[index] + 1 == s2Count[index]:
                matches -= 1

            index = ord(s2[l]) - ord("a")
            s2Count[index] -= 1
            if s1Count[index] == s2Count[index]:
                matches += 1
            elif s1Count[index] - 1 == s2Count[index]:
                matches -= 1
            l += 1
        return matches == 26
```

## Complexity

- **Time:** `O(n1 + n2)` — constant work per slide (plus a one-time 26-letter comparison).
- **Space:** `O(1)` — two fixed-size arrays of 26.

## Other Approaches

- **Compare count arrays each step:** slide the window and test `c1 == c2` directly — Time `O(26 * n2)`, Space `O(1)`; simpler and still linear.
- **Sort every window:** compare `sorted(window)` with `sorted(s1)` — Time `O(n2 * n1 log n1)`, Space `O(n1)`.

## Key Takeaway

"Anagram/permutation inside a string" = fixed-size sliding window with frequency counts; tracking the number of matching buckets makes each slide `O(1)`.

## C++

```cpp
/*
    Given 2 strings, return true if s2 contains permutation of s1
    Ex. s1 = "ab", s2 = "eidbaooo" -> true, s2 contains "ba"

    Sliding window, expand + count down char, contract + count up char

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    bool checkInclusion(string s1, string s2) {
        int m = s1.size();
        int n = s2.size();
        if (m > n) {
            return false;
        }
        
        vector<int> count(26);
        for (int i = 0; i < m; i++) {
            count[s1[i] - 'a']++;
            count[s2[i] - 'a']--;
        }
        if (isPermutation(count)) {
            return true;
        }
        
        for (int i = m; i < n; i++) {
            count[s2[i] - 'a']--;
            count[s2[i - m] - 'a']++;
            if (isPermutation(count)) {
                return true;
            }
        }
        
        return false;
    }
private:
    bool isPermutation(vector<int>& count) {
        for (int i = 0; i < 26; i++) {
            if (count[i] != 0) {
                return false;
            }
        }
        return true;
    }
};
```
