---
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/course-schedule-ii/
neetcode: https://neetcode.io/problems/course-schedule-ii
---
# Course Schedule II

**Topic:** Graphs · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/course-schedule-ii/) · [NeetCode](https://neetcode.io/problems/course-schedule-ii)

## Problem

There are `numCourses` courses labeled `0` to `numCourses - 1`, and `prerequisites[i] = [a, b]` means course `b` must be taken before course `a`.

Return an ordering of all courses that satisfies every prerequisite. If several valid orderings exist, return **any** of them. If no valid ordering exists (the prerequisites contain a cycle), return an empty list.

## Examples

**Example 1**
```text
Input: numCourses = 2, prerequisites = [[1,0]]
Output: [0,1]
```

**Example 2**
```text
Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
Output: [0,1,2,3]
Explanation: [0,2,1,3] is also valid.
```

**Example 3**
```text
Input: numCourses = 1, prerequisites = []
Output: [0]
```

## Constraints

- `1 <= numCourses <= 2000`
- `0 <= prerequisites.length <= numCourses * (numCourses - 1)`
- `prerequisites[i].length == 2`, `0 <= a, b < numCourses`, `a != b`
- All pairs are distinct
