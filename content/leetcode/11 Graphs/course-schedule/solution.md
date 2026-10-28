---
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/course-schedule/
neetcode: https://neetcode.io/problems/course-schedule
---
# Course Schedule - Solution

**Question:** Course Schedule - Question · **Difficulty:** Medium

## Intuition

Courses and prerequisites form a directed graph; all courses can be finished iff the graph has no cycle, i.e. a topological order exists. **Kahn's algorithm** builds that order by repeatedly taking courses with no remaining prerequisites (in-degree 0). If some courses are never freed, they sit on or behind a cycle.

## Approach

1. Build an adjacency list `b -> a` for each pair `[a, b]` and compute each course's in-degree.
2. Enqueue all courses with in-degree 0.
3. Pop a course, count it as taken, and decrement the in-degree of each dependent course; enqueue any that reach 0.
4. Return `taken == numCourses`.

## Code

```python
class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # dfs
        preMap = {i: [] for i in range(numCourses)}

        # map each course to : prereq list
        for crs, pre in prerequisites:
            preMap[crs].append(pre)

        visiting = set()

        def dfs(crs):
            if crs in visiting:
                return False
            if preMap[crs] == []:
                return True

            visiting.add(crs)
            for pre in preMap[crs]:
                if not dfs(pre):
                    return False
            visiting.remove(crs)
            preMap[crs] = []
            return True

        for c in range(numCourses):
            if not dfs(c):
                return False
        return True
```

## Complexity

- **Time:** `O(V + E)` — each course and each prerequisite edge is processed once.
- **Space:** `O(V + E)` — adjacency list, in-degree array, and queue.

## Other Approaches

- **DFS with three colors (unvisited / visiting / done):** a back edge to a "visiting" node means a cycle — Time `O(V + E)`, Space `O(V + E)` (recursion stack up to `V`).

## Key Takeaway

"Can all tasks with dependencies be completed?" = cycle detection in a directed graph; Kahn's BFS topological sort answers it by checking whether every node gets processed.

## C++

```cpp
/*
    Courses & prerequisites, return true if can finish all courses
    Ex. numCourses = 2, prerequisites = [[1,0]] -> true

    All courses can be completed if there's no cycle (visit already visited)

    Time: O(V + E)
    Space: O(V + E)
*/

class Solution {
public:
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
        // map each course to prereq list
        unordered_map<int, vector<int>> m;
        for (int i = 0; i < prerequisites.size(); i++) {
            m[prerequisites[i][0]].push_back(prerequisites[i][1]);
        }
        // all courses along current DFS path
        unordered_set<int> visited;
        
        for (int course = 0; course < numCourses; course++) {
            if (!dfs(course, m, visited)) {
                return false;
            }
        }
        return true;
    }
private:
    bool dfs(int course, unordered_map<int, vector<int>>& m, unordered_set<int>& visited) {
        if (visited.find(course) != visited.end()) {
            return false;
        }
        if (m[course].empty()) {
            return true;
        }
        visited.insert(course);
        for (int i = 0; i < m[course].size(); i++) {
            int nextCourse = m[course][i];
            if (!dfs(nextCourse, m, visited)) {
                return false;
            }
        }
        m[course].clear();
        visited.erase(course);
        return true;
    }
};
```
