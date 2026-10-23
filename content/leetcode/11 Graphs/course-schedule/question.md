---
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/course-schedule/
neetcode: https://neetcode.io/problems/course-schedule
---
# Course Schedule

**Topic:** Graphs · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/course-schedule/) · [NeetCode](https://neetcode.io/problems/course-schedule)

## Problem

There are `numCourses` courses labeled `0` to `numCourses - 1`. You are given `prerequisites`, where `prerequisites[i] = [a, b]` means course `b` must be completed before course `a`.

Return `true` if it is possible to finish all courses, otherwise return `false`. (This is impossible exactly when the prerequisites contain a cycle.)

## Examples

**Example 1**
```text
Input: numCourses = 2, prerequisites = [[1,0]]
Output: true
Explanation: Take course 0, then course 1.
```

**Example 2**
```text
Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
Output: false
Explanation: Each course requires the other.
```

## Constraints

- `1 <= numCourses <= 2000`
- `0 <= prerequisites.length <= 5000`
- `prerequisites[i].length == 2`, `0 <= a, b < numCourses`
- All pairs are unique
