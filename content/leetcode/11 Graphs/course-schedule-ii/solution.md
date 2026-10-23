---
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/course-schedule-ii/
neetcode: https://neetcode.io/problems/course-schedule-ii
---
# Course Schedule II - Solution

**Question:** Course Schedule II - Question · **Difficulty:** Medium

## Intuition

A valid course order is exactly a **topological sort** of the prerequisite graph. Kahn's algorithm produces one directly: a course can be scheduled once all of its prerequisites have been scheduled (in-degree drops to 0). If the order ends up shorter than `numCourses`, a cycle blocked some courses.

## Approach

1. Build edges `b -> a` and in-degrees from the prerequisite pairs.
2. Start a queue with every course of in-degree 0.
3. Pop a course, append it to `order`, decrement the in-degree of its dependents and enqueue those that hit 0.
4. Return `order` if it contains all courses, else `[]`.

## Code

```python
class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        prereq = {c: [] for c in range(numCourses)}
        for crs, pre in prerequisites:
            prereq[crs].append(pre)

        output = []
        visit, cycle = set(), set()

        def dfs(crs):
            if crs in cycle:
                return False
            if crs in visit:
                return True

            cycle.add(crs)
            for pre in prereq[crs]:
                if dfs(pre) == False:
                    return False
            cycle.remove(crs)
            visit.add(crs)
            output.append(crs)
            return True

        for c in range(numCourses):
            if dfs(c) == False:
                return []
        return output
```

## Complexity

- **Time:** `O(V + E)` — every course and prerequisite edge is handled once.
- **Space:** `O(V + E)` — adjacency list, in-degrees, queue, and output.

## Other Approaches

- **DFS post-order:** run DFS with cycle detection (visiting/visited states), append each course after all its dependents finish, then reverse (or build edges `a -> b` and append in post-order directly) — Time `O(V + E)`, Space `O(V + E)`.

## Key Takeaway

Kahn's algorithm gives both the topological order and cycle detection in one pass: if not every node is output, there is a cycle.
