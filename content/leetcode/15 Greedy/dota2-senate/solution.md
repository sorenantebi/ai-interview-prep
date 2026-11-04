---
topic: "Greedy"
difficulty: Medium
leetcode: https://leetcode.com/problems/dota2-senate/
neetcode: https://neetcode.io/problems/dota2-senate
---
# Dota2 Senate - Solution

## Intuition

Each senator's best move is to ban the next opposing senator who would otherwise act soonest, since that opponent is the one who can hurt their party first. Simulating this only needs the positions of the senators of each party, because the earlier of two opposing senators always wins the confrontation.

## Approach

1. Store the indices of all `R` senators in one queue and all `D` senators in another.
2. Repeatedly compare the fronts of both queues. The senator with the smaller index acts first and bans the other.
3. Pop both fronts. The winner is re-queued with index `i + n`, meaning they act again in the next round, after everyone currently in the round.
4. When one queue becomes empty, the other party wins.

## Code

```python
from typing import List, Optional
from collections import deque

class Solution:
    def predictPartyVictory(self, senate: str) -> str:
        n = len(senate)
        radiant, dire = deque(), deque()
        for i, c in enumerate(senate):
            if c == 'R':
                radiant.append(i)
            else:
                dire.append(i)

        while radiant and dire:
            r, d = radiant.popleft(), dire.popleft()
            # the earlier senator bans the other and acts again next round
            if r < d:
                radiant.append(r + n)
            else:
                dire.append(d + n)

        return "Radiant" if radiant else "Dire"
```

## Complexity

- **Time:** `O(n)` — each iteration removes one senator permanently, so there are at most `n` iterations with `O(1)` queue operations.
- **Space:** `O(n)` — the two queues hold all senators.

## Other Approaches

- **Ban counters with a circular simulation:** Loop over the string tracking pending bans for each party and mark banned senators — Time `O(n^2)` worst case / Space `O(n)`
- **Single queue:** Keep one queue of senators with counts of pending bans per party — Time `O(n)` / Space `O(n)`
