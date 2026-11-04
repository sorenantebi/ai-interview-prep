---
topic: "Backtracking"
difficulty: Hard
leetcode: https://leetcode.com/problems/n-queens-ii/
neetcode: https://neetcode.io/problems/n-queens-ii
---
# N-Queens II - Solution

## Intuition

Every row must contain exactly one queen, so we can place queens row by row and only choose the column. A placement is safe if no earlier queen shares its column or either diagonal. Cells on the same diagonal share `row - col`, and cells on the same anti-diagonal share `row + col`, so three sets let us check safety in O(1).

## Approach

1. Keep three sets: occupied columns, occupied diagonals (`row - col`), and occupied anti-diagonals (`row + col`).
2. Recurse over `row` from `0` to `n - 1`.
3. For each column in the current row, skip it if the column or either diagonal is taken.
4. Otherwise add the placement to the sets, recurse into `row + 1`, then remove it (backtrack).
5. When `row == n`, all queens are placed, so count one solution.
6. Return the total count.

## Code

```python
class Solution:
    def totalNQueens(self, n: int) -> int:
        answer = 0

        cols = set()
        posdiag = set()
        negdiag = set()

        def backtrack(i):
            if i == n:
                nonlocal answer
                answer += 1
                return
            
            for j in range(n):
                if j in cols or (i+j) in posdiag or (i-j) in negdiag:
                    continue

                cols.add(j)
                posdiag.add(i+j)
                negdiag.add(i-j)

                backtrack(i+1)
                
                cols.remove(j)
                posdiag.remove(i+j)
                negdiag.remove(i-j)
        
        backtrack(0)
        return answer
```

## Complexity

- **Time:** `O(n!)` — the first row has `n` choices, and each later row has fewer safe columns, so the search tree is bounded by roughly `n!` nodes.
- **Space:** `O(n)` — recursion depth is `n` and the three sets hold at most `n` entries each.

## Other Approaches

- **Bitmask backtracking:** represent columns and both diagonals as integers and pick free positions with bit operations — Time `O(n!)` / Space `O(n)`
- **Brute force with board validation:** place queens on every combination of cells and validate each board — Time `O(n^n · n)` or worse / Space `O(n)`

## C++

```cpp
class Solution {
public:
    int queen[9];
    bool check(int &r,int &c,int n){
        for(int i=0;i<r;i++){
            // here we have to check from before rows any queen(queen[i]) is placed to attk the cur level queen;
            int pre_row=i; // previous row
            int pre_col=queen[i]; // previous col is stored in queen[i]
            // checking for col collison as rows cant be && and for diagonal attk
            if(pre_col==c or abs(r-pre_row)==abs(c-pre_col)) return false;
        }
        return true;
    }
    int bt(int level,int n){
        // base conditon
        
        if(level==n) return 1;
        // return 1 as u made a board and placing queens from 0 to n-1 so u came out of board
        
        int ans=0;
        // exploring choices and computation
        for(int col=0;col<n;col++){
            if(check(level,col,n)){
                // check
                queen[level]=col;
                // move
                ans+=bt(level+1,n);
                queen[level]=-1;
            }
        }
        // return count of ways to place queen from this row to n-1/ last row
        return ans;
    }
    int totalNQueens(int n) {
        memset(queen,-1,sizeof(queen));
        return bt(0,n);
    }
};
```
