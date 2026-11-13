---
topic: "String Manipulation"
difficulty: Medium
leetcode: https://leetcode.com/problems/compare-version-numbers/
---
# Compare Version Numbers - Solution

## Intuition

Each version is a list of integers. Compare them position by position, and pad the shorter one with zeros. Converting each revision with `int()` handles leading zeros automatically.

## Approach

1. Split both strings on `'.'`.
2. Iterate `i` from `0` to `max(len(a), len(b)) - 1`.
3. At each index, take the revision as an integer, or `0` if the index is past the end of that list.
4. If the values differ, return `-1` or `1` accordingly.
5. If all positions are equal, return `0`.

## Code

```python
from typing import List, Optional

class Solution:
    def compareVersion(self, version1: str, version2: str) -> int:
        a = version1.split('.')
        b = version2.split('.')
        for i in range(max(len(a), len(b))):
            x = int(a[i]) if i < len(a) else 0
            y = int(b[i]) if i < len(b) else 0
            if x < y:
                return -1
            if x > y:
                return 1
        return 0
```

## Complexity

- **Time:** `O(n + m)` — each string is split and scanned once, where `n` and `m` are the lengths of the two strings.
- **Space:** `O(n + m)` — the split lists hold all revisions.

## Other Approaches

- **Two pointers without splitting:** parse each revision digit by digit in place, accumulating its value until a `'.'` or the end of the string — Time `O(n + m)` / Space `O(1)`
