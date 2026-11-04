---
video: https://www.youtube.com/watch?v=cEW05ofxhn0
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/course-schedule-iv/
neetcode: https://neetcode.io/problems/course-schedule-iv
---
# Course Schedule IV

**Topic:** Graphs · **Difficulty:** Medium

## Problem

There are `numCourses` courses labeled from `0` to `numCourses - 1`. You are given an array `prerequisites` where `prerequisites[i] = [ai, bi]` means you must take course `ai` before course `bi`.

Prerequisites can be indirect: if course `a` is a prerequisite of course `b`, and `b` is a prerequisite of course `c`, then `a` is also a prerequisite of `c`.

You are also given an array `queries` where `queries[j] = [uj, vj]`. For each query, determine whether course `uj` is a prerequisite (direct or indirect) of course `vj`.

Return a boolean array `answer`, where `answer[j]` is the result of the `j`th query.

## Examples

**Example 1**
```text
Input: numCourses = 2, prerequisites = [[1,0]], queries = [[0,1],[1,0]]
Output: [false,true]
```
Course 0 is not a prerequisite of course 1, but course 1 is a prerequisite of course 0.

**Example 2**
```text
Input: numCourses = 2, prerequisites = [], queries = [[1,0],[0,1]]
Output: [false,false]
```
There are no prerequisites, so every course is independent.

**Example 3**
```text
Input: numCourses = 3, prerequisites = [[1,2],[1,0],[2,0]], queries = [[1,0],[1,2]]
Output: [true,true]
```

## Constraints

- `2 <= numCourses <= 100`
- `0 <= prerequisites.length <= (numCourses * (numCourses - 1) / 2)`
- `prerequisites[i].length == 2`
- `0 <= ai, bi <= numCourses - 1`
- `ai != bi`
- All the pairs `[ai, bi]` are unique.
- The prerequisites graph has no cycles.
- `1 <= queries.length <= 10^4`
- `0 <= ui, vi <= numCourses - 1`
- `ui != vi`
