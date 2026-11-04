---
topic: "Bit Manipulation"
difficulty: Easy
leetcode: https://leetcode.com/problems/add-binary/
neetcode: https://neetcode.io/problems/add-binary
---
# Add Binary - Solution

## Intuition

Binary addition works exactly like grade-school decimal addition: go from the least significant digit to the most significant, add the two digits plus the carry, write down the low bit, and carry the high bit. The strings can be far longer than a machine word, so we simulate the addition digit by digit instead of converting to integers.

## Approach

1. Set two pointers `i` and `j` at the last characters of `a` and `b`, and `carry = 0`.
2. While either pointer is still in range or a carry remains:
   - Start `total` with `carry`.
   - Add the digit of `a` at `i` if `i >= 0`, and the digit of `b` at `j` if `j >= 0`, moving each pointer left.
   - Append `total % 2` to the result and set `carry = total // 2`.
3. The digits were produced least significant first, so reverse them and join into a string.

## Code

```python
class Solution:
    def addBinary(self, a: str, b: str) -> str:
        res = ""
        carry = 0

        a, b = a[::-1], b[::-1]
        for i in range(max(len(a), len(b))):
            bitA = ord(a[i]) - ord('0') if i < len(a) else 0
            bitB = ord(b[i]) - ord('0') if i < len(b) else 0

            total = bitA + bitB + carry
            char = str(total % 2)
            res = char + res
            carry = total // 2

        if carry:
            res = "1" + res

        return res
```

## Complexity

- **Time:** `O(max(n, m))` — each digit of the longer string is visited once.
- **Space:** `O(max(n, m))` — the result holds up to `max(n, m) + 1` digits.

## Other Approaches

- **Built-in conversion:** `bin(int(a, 2) + int(b, 2))[2:]` — short, but relies on big-integer arithmetic; Time `O(n + m)` in practice / Space `O(max(n, m))`
- **Bitwise XOR/AND loop:** convert to integers, then repeat `sum = x ^ y`, `carry = (x & y) << 1` until carry is zero — Time `O((n + m)^2)` worst case with big integers / Space `O(max(n, m))`

## C++

```cpp
class Solution {
public:
    string addBinary(string a, string b) {
        string res;
        int maxLen = a.size() > b.size() ? a.size() : b.size();
        unsigned int carry = 0;

        for(int i = 0; i < maxLen; i++)
        {
            unsigned int bitA = i < a.size() ? a[a.size() - i - 1] - '0' : 0;
            unsigned int bitB = i < b.size() ? b[b.size() - i - 1] - '0' : 0;

            unsigned int total = bitA + bitB + carry;
            char sum = '0' + total % 2;
            carry = total / 2;

            // Add to the beginning of the string
            res.insert(0, 1, sum);
        }

        if(carry)
        {
            res.insert(0, 1, '1');
        }

        return res;
    }
};
```
