---
topic: "Math & Geometry"
difficulty: Medium
leetcode: https://leetcode.com/problems/detect-squares/
neetcode: https://neetcode.io/problems/count-squares
---
# Detect Squares - Solution

**Question:** Detect Squares - Question · **Difficulty:** Medium

## Intuition

Fix the query point `(qx, qy)`. Any axis-aligned square through it has a diagonal corner `(x, y)` with `|x - qx| == |y - qy| != 0`, and the other two corners are then fixed at `(x, qy)` and `(qx, y)`. Store point counts in a hash map, try each stored point as the diagonal corner, and multiply the counts of the three corners.

## Approach

1. Keep `cnt`, a Counter of `(x, y) -> multiplicity`, and `pts`, a list of the distinct points added.
2. `add`: increment `cnt[(x, y)]`; if it is the first copy, also append to `pts`.
3. `count(qx, qy)`: for each distinct `(x, y)` in `pts`:
   - skip it unless `abs(x - qx) == abs(y - qy)` and `x != qx`, so that it is a diagonal corner of a square with positive area;
   - add `cnt[(x, y)] * cnt[(x, qy)] * cnt[(qx, y)]` to the result.
4. Return the sum.

## Code

```python
class DetectSquares:
    def __init__(self):
        self.ptsCount = defaultdict(int)
        self.pts = []

    def add(self, point: List[int]) -> None:
        self.ptsCount[tuple(point)] += 1
        self.pts.append(point)

    def count(self, point: List[int]) -> int:
        res = 0
        px, py = point
        for x, y in self.pts:
            if (abs(py - y) != abs(px - x)) or x == px or y == py:
                continue
            res += self.ptsCount[(x, py)] * self.ptsCount[(px, y)]
        return res
```

## Complexity

- **Time:** `add` is `O(1)`. `count` is `O(P)`, where `P` is the number of distinct points added so far.
- **Space:** `O(P)`: for the counter and the list of distinct points.

## Other Approaches

- **Iterate over side length:** for each `d` in `1..1000` and both directions, look up the three corners via `cnt`. Time `O(C)` per query where `C = 1000` is the coordinate range, Space `O(P)`.
- **Group by x-coordinate:** for each stored point sharing `qx`, the side length is fixed, so check the two candidate squares (left and right). Time `O(points on the same column)` per query, Space `O(P)`.

## Key Takeaway

For geometry counting, fix one point and enumerate a single free parameter (here the diagonal corner); the other points are then determined. Multiply hash-map counts to account for duplicates.

## C++

```cpp
/*
    Given stream of points, add new points, return count of squares

    Find diagonals, if exists then forms a square, loop thru all points

    Time: O(1) add O(n^2) count -> n = number of points
    Space: O(n)
*/

class DetectSquares {
public:
    DetectSquares() {
        
    }
    
    void add(vector<int> point) {
        points[point[0]][point[1]]++;
    }
    
    int count(vector<int> point) {
        int x1 = point[0];
        int y1 = point[1];
        
        int result = 0;
        
        for (auto x = points.begin(); x != points.end(); x++) {
            unordered_map<int, int> yPoints = x->second;
            for (auto y = yPoints.begin(); y != yPoints.end(); y++) {
                int x3 = x->first;
                int y3 = y->first;
                
                // skip points on same x-axis or y-axis
                if (abs(x3 - x1) == 0 || abs(x3 - x1) != abs(y3 - y1)) {
                    continue;
                }
                
                result += points[x3][y3] * points[x1][y3] * points[x3][y1];
            }
        }
        
        return result;
    }
private:
    // {x -> {y -> count}}
    unordered_map<int, unordered_map<int, int>> points;
};

/**
 * Your DetectSquares object will be instantiated and called as such:
 * DetectSquares* obj = new DetectSquares();
 * obj->add(point);
 * int param_2 = obj->count(point);
 */
```
