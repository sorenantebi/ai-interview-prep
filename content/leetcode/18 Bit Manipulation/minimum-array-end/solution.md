---
topic: "Bit Manipulation"
difficulty: Medium
leetcode: https://leetcode.com/problems/minimum-array-end/
neetcode: https://neetcode.io/problems/minimum-array-end
---
# Minimum Array End - Solution

## Intuition

For the AND of all elements to equal `x`, every element must contain all the set bits of `x`. The bits where `x` is 0 are free, and at least one element must have a 0 in each of those positions (the AND must clear them). To keep the last element as small as possible, the elements should be `x` with different values placed in the free (zero) bit positions, counting upward. The first element uses all zeros there, which is `x` itself. The `n`-th element uses the binary representation of `n - 1` spread into those free positions. Since `n - 1` is used from the first element onward and element 0 has all free bits zero, the AND over the free positions stays 0, so the AND equals `x`.

## Approach

1. Let `k = n - 1`, the index of the last element, whose free bits encode `k`.
2. Start with `result = x`.
3. Walk through the bit positions from lowest to highest. Whenever `x` has a 0 at the current position, take the next lowest unused bit of `k` and place it there.
4. Stop when all bits of `k` have been placed. Return `result`.

## Code

```python
from typing import List, Optional

class Solution:
    def minEnd(self, n: int, x: int) -> int:
        k = n - 1
        result = x
        pos = 1
        while k:
            # only zero bits of x are free to hold bits of k
            if not (x & pos):
                if k & 1:
                    result |= pos
                k >>= 1
            pos <<= 1
        return result
```

## Complexity

- **Time:** `O(log n + log x)` — each loop iteration advances one bit position, and we stop after all bits of `n - 1` are placed, which needs at most about `log n + log x` positions.
- **Space:** `O(1)` — only a few integer variables.

## Other Approaches

- **Brute force simulation:** repeatedly take the next number greater than the previous one that is a superset of `x`'s bits (`prev = (prev + 1) | x`), `n - 1` times — Time `O(n)` / Space `O(1)`
- **Bit-deposit with a scan of `k`:** iterate over bits of `k` and insert each into the next zero bit of `x` — Time `O(log n + log x)` / Space `O(1)`
