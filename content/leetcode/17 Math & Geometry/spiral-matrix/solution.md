---
topic: "Math & Geometry"
difficulty: Medium
leetcode: https://leetcode.com/problems/spiral-matrix/
neetcode: https://neetcode.io/problems/spiral-matrix
---
# Spiral Matrix - Solution

**Question:** Spiral Matrix - Question · **Difficulty:** Medium

## Intuition

Keep four boundaries: `top`, `bottom`, `left`, `right`. Walk each side of the current outer ring and move the matching boundary inward once that side is done. The difficult cases are a single leftover row or column. After the top row and right column have been taken, re-check the boundaries before walking back left or up, so no element is visited twice.

## Approach

1. Set `top, bottom = 0, m - 1` and `left, right = 0, n - 1`.
2. While `top <= bottom` and `left <= right`:
   - read the top row from `left` to `right`, then `top += 1`;
   - read the right column from `top` to `bottom`, then `right -= 1`;
   - if `top <= bottom`, read the bottom row from `right` to `left`, then `bottom -= 1`;
   - if `left <= right`, read the left column from `bottom` to `top`, then `left += 1`.
3. Return the collected list.

## Code

```python
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        res = []
        left, right = 0, len(matrix[0])
        top, bottom = 0, len(matrix)

        while left < right and top < bottom:
            # get every i in the top row
            for i in range(left, right):
                res.append(matrix[top][i])
            top += 1
            # get every i in the right col
            for i in range(top, bottom):
                res.append(matrix[i][right - 1])
            right -= 1
            if not (left < right and top < bottom):
                break
            # get every i in the bottom row
            for i in range(right - 1, left - 1, -1):
                res.append(matrix[bottom - 1][i])
            bottom -= 1
            # get every i in the left col
            for i in range(bottom - 1, top - 1, -1):
                res.append(matrix[i][left])
            left += 1

        return res
```

## Complexity

- **Time:** `O(m * n)`: each element is appended exactly once.
- **Space:** `O(1)` extra, not counting the output list.

## Other Approaches

- **Direction vector + visited marks:** step in direction `(dr, dc)` and turn right when the next cell is out of bounds or already visited. Time `O(m * n)`, Space `O(m * n)` for the visited grid (or `O(1)` if you overwrite the input with a sentinel).
- **Peel and rotate:** pop the first row, rotate the rest counter-clockwise (`list(zip(*matrix))[::-1]`), and repeat. Easy to write but `O(m * n * min(m, n))` time.

## Key Takeaway

Shrinking-boundary traversal handles spiral and layered matrix problems. After each pass, re-check `top <= bottom` and `left <= right` so a single row or column isn't read twice.

## C++

```cpp
/*
    Given a matrix, return all elements in spiral order

    Set up boundaries, go outside in CW: top->right->bottom->left

    Time: O(m x n)
    Space: O(m x n)
*/

class Solution {
public:
    vector<int> spiralOrder(vector<vector<int>>& matrix) {
        int left = 0;
        int top = 0;
        int right = matrix[0].size() - 1;
        int bottom = matrix.size() - 1;
        
        vector<int> result;
        
        while (top <= bottom && left <= right) {
            for (int j = left; j <= right; j++) {
                result.push_back(matrix[top][j]);
            }
            top++;
            
            for (int i = top; i <= bottom; i++) {
                result.push_back(matrix[i][right]);
            }
            right--;
            
            if (top <= bottom) {
                for (int j = right; j >= left; j--) {
                    result.push_back(matrix[bottom][j]);
                }
            }
            bottom--;
            
            if (left <= right) {
                for (int i = bottom; i >= top; i--) {
                    result.push_back(matrix[i][left]);
                }
            }
            left++;
        }
        
        return result;
    }
};
```
