---
topic: "Sliding Window"
difficulty: Medium
leetcode: https://leetcode.com/problems/longest-substring-without-repeating-characters/
neetcode: https://neetcode.io/problems/longest-substring-without-duplicates
---
# Longest Substring Without Repeating Characters - Solution

**Question:** Longest Substring Without Repeating Characters - Question · **Difficulty:** Medium

## Intuition

Maintain a window `[l, r]` with all-distinct characters. When the new character `s[r]` already appears inside the window, the window must start just after that earlier occurrence. Storing each character's last index lets the left edge jump directly there instead of shrinking one step at a time.

## Approach

1. Keep a dict `last` of char -> most recent index, `l = 0`, `best = 0`.
2. For each `r, c`:
   - If `c` is in `last` and `last[c] >= l`, set `l = last[c] + 1`.
   - Record `last[c] = r`.
   - Update `best = max(best, r - l + 1)`.
3. Return `best`.

## Code

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        charSet = set()
        l = 0
        res = 0

        for r in range(len(s)):
            while s[r] in charSet:
                charSet.remove(s[l])
                l += 1
            charSet.add(s[r])
            res = max(res, r - l + 1)
        return res
```

## Complexity

- **Time:** `O(n)` — each character is processed once.
- **Space:** `O(min(n, m))` — `m` is the alphabet size stored in the map.

## Other Approaches

- **Set-based window:** shrink from the left, removing chars until `s[r]` is no longer in the set — Time `O(n)` (each char added/removed once), Space `O(m)`.
- **Brute force:** check every substring for uniqueness — Time `O(n^3)` (or `O(n^2)` with early stop), Space `O(m)`.

## Key Takeaway

Variable-size sliding window: expand right every step, and move left only as far as needed to restore the invariant. The `last[c] >= l` guard (see "abba") is the classic bug to avoid.
