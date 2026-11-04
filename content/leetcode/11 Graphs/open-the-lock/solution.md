---
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/open-the-lock/
neetcode: https://neetcode.io/problems/open-the-lock
---
# Open the Lock - Solution

## Intuition

Treat each of the 10,000 wheel states as a node in a graph. Two states are connected if one move turns a single wheel by one slot. Every move costs 1, so the minimum number of turns is the shortest path from `'0000'` to `target`, which breadth-first search finds. Dead ends are simply nodes we never enter.

## Approach

1. If `'0000'` is a dead end, return `-1` (the lock is stuck immediately). If `target` is `'0000'`, return `0`.
2. Put the dead ends into a set and use it as the initial `visited` set, so they are never expanded.
3. Run BFS from `'0000'`, processing one level at a time; each level is one move.
4. For each state, generate 8 neighbors: each of the 4 wheels turned up or down by one, with wraparound via modulo 10.
5. Skip neighbors already in `visited`; otherwise mark them visited and enqueue them.
6. Return the level count as soon as `target` is reached. If the queue empties, return `-1`.

## Code

```python
class Solution:
    def openLock(self, deadends: List[str], target: str) -> int:
        if "0000" in deadends:
            return -1

        def children(wheel):
            res = []
            for i in range(4):
                digit = str((int(wheel[i]) + 1) % 10)
                res.append(wheel[:i] + digit + wheel[i + 1 :])
                digit = str((int(wheel[i]) + 10 - 1) % 10)
                res.append(wheel[:i] + digit + wheel[i + 1 :])
            return res

        q = deque()
        visit = set(deadends)
        q.append(["0000", 0])  # [wheel, turns]
        while q:
            wheel, turns = q.popleft()
            if wheel == target:
                return turns
            for child in children(wheel):
                if child not in visit:
                    visit.add(child)
                    q.append([child, turns + 1])
        return -1
```

## Complexity

- **Time:** `O(10^4 * 4 * 2)` — there are at most 10,000 states and each generates 8 neighbors, so this is a constant bound.
- **Space:** `O(10^4)` — the visited set and queue hold at most all states.

## Other Approaches

- **Bidirectional BFS:** search from both `'0000'` and `target` and meet in the middle, shrinking the explored frontier — Time `O(10^4 * 8)` worst case / Space `O(10^4)`
- **A\* search:** BFS guided by a heuristic such as the sum of circular wheel distances to the target — Time `O(10^4 * 8 * log(10^4))` worst case / Space `O(10^4)`
