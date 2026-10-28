---
topic: "Bit Manipulation"
difficulty: Easy
leetcode: https://leetcode.com/problems/counting-bits/
neetcode: https://neetcode.io/problems/counting-bits
---
# Counting Bits - Solution

**Question:** Counting Bits - Question · **Difficulty:** Easy

## Intuition

`i >> 1` is `i` with its last bit removed, and it is smaller than `i`, so its answer has already been computed. The bit count of `i` is therefore the count for `i >> 1` plus the bit that was dropped, `i & 1`. That gives a one-line DP recurrence.

## Approach

1. Create `ans = [0] * (n + 1)`.
2. For `i` from `1` to `n`: `ans[i] = ans[i >> 1] + (i & 1)`.
3. Return `ans`.

## Code

```python
class Solution:
    def countBits(self, n: int) -> List[int]:
        dp = [0] * (n + 1)
        offset = 1

        for i in range(1, n + 1):
            if offset * 2 == i:
                offset = i
            dp[i] = 1 + dp[i - offset]
        return dp

# Another dp solution
class Solution2:
    def countBits(self, n: int) -> List[int]:
        res = [0] * (n + 1)
        for i in range(1, n + 1):
            if i % 2 == 1:
                res[i] = res[i - 1] + 1
            else:
                res[i] = res[i // 2]
        return res
# This solution is based on the division of odd and even numbers. 
# I think it's easier to understand.
# This is my full solution, covering the details: https://leetcode.com/problems/counting-bits/solutions/4411054/odd-and-even-numbers-a-easier-to-understanding-way-of-dp/
```

## Complexity

- **Time:** `O(n)`: constant work per index.
- **Space:** `O(1)` extra, not counting the output array of size `n + 1`.

## Other Approaches

- **Lowest-set-bit DP:** `ans[i] = ans[i & (i - 1)] + 1`. Time `O(n)`, Space `O(1)` extra.
- **Popcount each number:** run Brian Kernighan's loop on every `i`. Time `O(n log n)`, Space `O(1)` extra.

## Key Takeaway

Bit DP: a number's answer often follows from a smaller number obtained by a shift (`i >> 1`) or by clearing a bit (`i & (i - 1)`). Look for such a recurrence before computing each value from scratch.

## C++

```cpp
/*
    Given int, return array: for each i, ans[i] is # of 1's
    Ex. n = 2 -> [0,1,1], 0 = 0 has 0, 1 = 1 has 1, 2 = 10 has 1

    x = 1001011101 = 605
    x'= 0100101110 = 302
    Differ by 1 bit, by removing LSB: f(x) = f(x / 2) + (x mod 2)

    Time: O(n)
    Space: O(1), the output array does not count towards space
*/

class Solution {
public:
    vector<int> countBits(int n) {
        vector<int> result(n + 1, 0);
        
        for (int i = 1; i <= n; i++) {
            //                 i / 2      i % 2
            result[i] = result[i >> 1] + (i & 1);
        }
        
        return result;
    }
};
```
