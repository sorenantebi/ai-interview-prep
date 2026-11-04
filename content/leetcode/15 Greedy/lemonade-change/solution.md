---
topic: "Greedy"
difficulty: Easy
leetcode: https://leetcode.com/problems/lemonade-change/
neetcode: https://neetcode.io/problems/lemonade-change
---
# Lemonade Change - Solution

## Intuition

Only the counts of $5 and $10 bills in hand matter, since $20 bills are never given back as change. The only real choice comes up when a customer pays $20: change of $15 can be made as $10 + $5 or as three $5 bills. $5 bills are more flexible (they can serve both $10 and $20 payers), so prefer spending the $10 bill first and keep $5 bills.

## Approach

1. Keep counters `fives` and `tens`, both starting at 0.
2. For a $5 bill: increment `fives`.
3. For a $10 bill: a $5 is needed as change. If `fives == 0`, return `False`; otherwise decrement `fives` and increment `tens`.
4. For a $20 bill: prefer giving one $10 and one $5 if possible; otherwise give three $5 bills. If neither is possible, return `False`.
5. If the whole queue is processed, return `True`.

## Code

```python
from typing import List, Optional

class Solution:
    def lemonadeChange(self, bills: List[int]) -> bool:
        fives = tens = 0
        for bill in bills:
            if bill == 5:
                fives += 1
            elif bill == 10:
                if fives == 0:
                    return False
                fives -= 1
                tens += 1
            else:
                # Prefer using a $10 so that scarcer-in-use $5 bills are kept
                if tens > 0 and fives > 0:
                    tens -= 1
                    fives -= 1
                elif fives >= 3:
                    fives -= 3
                else:
                    return False
        return True
```

## Complexity

- **Time:** `O(n)` — a single pass over the bills with constant work per customer.
- **Space:** `O(1)` — only two counters are stored.

## Other Approaches

- **Hash map of bill counts:** store counts for each denomination in a dictionary and apply the same greedy rule — Time `O(n)` / Space `O(1)`
