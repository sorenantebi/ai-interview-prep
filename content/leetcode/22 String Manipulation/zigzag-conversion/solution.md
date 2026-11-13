---
topic: "String Manipulation"
difficulty: Medium
leetcode: https://leetcode.com/problems/zigzag-conversion/
---
# Zigzag Conversion - Solution

## Intuition

We never need to build the 2D grid. Each character belongs to exactly one row, and the row index simply bounces between `0` and `numRows - 1` as we walk through the string. If we append each character to the buffer of its row and join the buffers at the end, we get the answer.

## Approach

1. If `numRows == 1` or `numRows >= len(s)`, the zigzag does not change the string, so return `s`.
2. Create one list per row.
3. Keep a current row index `row` and a direction `step` (`+1` going down, `-1` going up).
4. For each character, append it to `rows[row]`, then flip the direction when `row` reaches `0` or `numRows - 1`, and move `row += step`.
5. Concatenate all rows in order.

## Code

```python
class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1 or numRows >= len(s):
            return s

        res = [""] * numRows

        index = 0
        step = 1
        for c in s:
            res[index] += c
            if index == 0:
                step = 1
            elif index == numRows - 1:
                step = -1
            index += step

        return "".join(res)
```

## Complexity

- **Time:** `O(n)` — each character is visited and appended exactly once, then joined once.
- **Space:** `O(n)` — the row buffers together hold all `n` characters (excluding the output string).

## Other Approaches

- **Index jumping by cycle length:** for each row, step through the string with cycle length `2 * (numRows - 1)`, adding the extra diagonal character for middle rows — Time `O(n)` / Space `O(1)` extra (besides the output).
- **Explicit 2D grid simulation:** fill a `numRows x numCols` matrix following the zigzag, then read it row by row — Time `O(n * numRows)` / Space `O(n * numRows)`.

## C++

```cpp
/*
    For each row the next chracter is at index 2 * (n -1) and 
    For middle rows there will be extra characters
    Time: O(n)
    Space: O(1)
*/
class Solution {
public:
    string convert(string s, int n) {
        // Edge case
        if(n == 1) return s;
        // Other cases
        // Take string to store answer
        string ans = "";
        // We are going to traverse each row
        for(int row = 0; row < n ; row++){
            // for each row the next chracter is at index 2 *  (n -1) 
            int increment = 2 *  (n -1);
            // For first and last rows 
            for(int i = row; i < s.length(); i+= increment){
                ans += s[i];
                // For middle rows there will be extra characters
                if(row > 0 && row < n-1 && i+increment - 2 * row < s.length()){
                    ans += s[i+increment - 2 * row];
                }
            }
        }
        return ans;
    }
};
```
