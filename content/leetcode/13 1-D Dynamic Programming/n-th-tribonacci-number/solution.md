---
topic: "1-D Dynamic Programming"
difficulty: Easy
leetcode: https://leetcode.com/problems/n-th-tribonacci-number/
neetcode: https://neetcode.io/problems/n-th-tribonacci-number
---
# N-th Tribonacci Number - Solution

## Intuition

Each term depends only on the three terms immediately before it. There is no need to store the whole table: keeping a sliding window of the last three values is enough.

## Approach

1. Handle the base cases: return `0` for `n == 0`, and `1` for `n` equal to `1` or `2`.
2. Keep three variables `a, b, c` holding `T(i-3), T(i-2), T(i-1)`, initialised to `0, 1, 1`.
3. For each index from `3` to `n`, compute the next value as `a + b + c` and shift the window forward.
4. After the loop, `c` holds `T(n)`.

## Code

```python
class Solution:
    Memo = {}

    def tribonacci(self, n: int):
        if n in self.Memo:
            return self.Memo[n]
        if n == 0:
            return 0
        if n == 1:
            return 1
        if n == 2:
            return 1
        self.Memo[n] = (
            self.tribonacci(n - 1) + self.tribonacci(n - 2) + self.tribonacci(n - 3)
        )
        return self.Memo[n]
```

## Complexity

- **Time:** `O(n)` — one pass computing each term from `3` to `n` with constant work per step.
- **Space:** `O(1)` — only three rolling variables are stored.

## Other Approaches

- **Bottom-up DP array:** store `T(0..n)` in a list and fill it left to right — Time `O(n)` / Space `O(n)`
- **Memoized recursion:** top-down recursion with a cache on `n` — Time `O(n)` / Space `O(n)`
- **Matrix exponentiation:** raise the 3x3 Tribonacci transition matrix to the power `n` — Time `O(log n)` / Space `O(1)`

## C++

```cpp
// Time: O(n)
// Space: O(1)

class Solution {
public:
    int tribonacci(int n) {
        int t[] = {0, 1, 1};
        if (n < 3) {
            return t[n];
        }
        for (int i = 3; i <= n; i++) {
            int sum_t = t[0] + t[1] + t[2];
            t[0] = t[1];
            t[1] = t[2];
            t[2] = sum_t;
        }
        return t[2];
    }
};
```
