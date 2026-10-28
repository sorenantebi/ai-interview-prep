---
topic: "Backtracking"
difficulty: Hard
leetcode: https://leetcode.com/problems/n-queens/
neetcode: https://neetcode.io/problems/n-queens
---
# N Queens - Solution

**Question:** N Queens - Question · **Difficulty:** Hard

## Intuition

Exactly one queen goes in each row, so place queens row by row and only choose a column that is not attacked. A square `(r, c)` is attacked if its column, its diagonal (`r - c` constant), or its anti-diagonal (`r + c` constant) already has a queen — three sets give `O(1)` checks, and backtracking removes the queen when a branch is done.

## Approach

1. Keep sets `cols`, `diag` (`r - c`), `anti` (`r + c`) and an array `queen_col[r]`.
2. `dfs(r)`: if `r == n`, convert `queen_col` into board strings and record them.
3. For each column `c`: skip if `c`, `r - c`, or `r + c` is taken; otherwise add to all three sets, set `queen_col[r] = c`, recurse on `r + 1`, then remove from the sets.

## Code

```python
class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        col = set()
        posDiag = set()  # (r + c)
        negDiag = set()  # (r - c)

        res = []
        board = [["."] * n for i in range(n)]

        def backtrack(r):
            if r == n:
                copy = ["".join(row) for row in board]
                res.append(copy)
                return

            for c in range(n):
                if c in col or (r + c) in posDiag or (r - c) in negDiag:
                    continue

                col.add(c)
                posDiag.add(r + c)
                negDiag.add(r - c)
                board[r][c] = "Q"

                backtrack(r + 1)

                col.remove(c)
                posDiag.remove(r + c)
                negDiag.remove(r - c)
                board[r][c] = "."

        backtrack(0)
        return res
```

## Complexity

- **Time:** `O(n!)` — row `r` has at most `n - r` free columns; building each board adds `O(n^2)` per solution.
- **Space:** `O(n)` — sets, column array, and recursion depth (output excluded).

## Other Approaches

- **Validate by scanning the board:** for each candidate square, scan its column and diagonals on a char grid — Time `O(n! * n)`, Space `O(n^2)`.
- **Bitmasks:** represent `cols`, `diag`, `anti` as integers and iterate available bits — same asymptotic bound, much faster constants.

## Key Takeaway

For N-Queens, index diagonals by `r - c` and anti-diagonals by `r + c`; place one queen per row and backtrack with three "occupied" sets.

## C++

```cpp
/*
    N-Queens: place n queens such that no 2 queens atk each other, return all soln's

    Place queens per row, try all possibilities & validate for further rows, backtrack

    Time: O(n!)
    Space: O(n^2)
*/

class Solution {
private:
    unordered_set<int> cols;     //for Columns
    unordered_set<int> negDiag;  //for negative diagnals R-C
    unordered_set<int> posDiag;  //for positive diagnals R+C
    
    void backtrack(int n, int row, vector<vector<string>>& res, vector<string>& board){
        if(row==n){
            res.push_back(board);
            return ; 
        }
        
        for(int col = 0; col < n; col++){   //Shifting through each col
            if( cols.find(col) != cols.end() or //if queen alread placed in this col
                negDiag.find(row - col) != negDiag.end() or //if queen in negDiag
                posDiag.find(row + col) != posDiag.end()    //if queen in posDiag
              )
                continue;
            
            cols.insert(col);
            negDiag.insert(row - col);
            posDiag.insert(row + col);
            board[row][col] = 'Q';
            
            backtrack(n, row +1, res, board);
            
            cols.erase(col);
            negDiag.erase(row - col);
            posDiag.erase(row + col);
            board[row][col] = '.';
        }
    }
   
public:
    vector<vector<string>> solveNQueens(int n) {
        vector<vector<string>> res;
        vector<string> board(n, string(n,'.'));
        backtrack(n, 0, res, board);
        return res;
    }
};
```
