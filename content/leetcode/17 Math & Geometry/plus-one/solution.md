---
topic: "Math & Geometry"
difficulty: Easy
leetcode: https://leetcode.com/problems/plus-one/
neetcode: https://neetcode.io/problems/plus-one
---
# Plus One - Solution

**Question:** Plus One - Question · **Difficulty:** Easy

## Intuition

Add from the least significant digit, as in long addition. A digit less than 9 can be incremented, and we are done. A 9 becomes 0 and the carry moves one place left. A carry only survives past the front of the array if every digit was 9, in which case the answer is `1` followed by zeros.

## Approach

1. Iterate `i` from the last index down to `0`.
2. If `digits[i] < 9`, increment it and return `digits`.
3. Otherwise set `digits[i] = 0` and keep going, since the carry continues.
4. If the loop finishes, every digit was 9: return `[1] + digits`.

## Code

```python
class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        one = 1
        i = 0
        digits = digits[::-1]

        while one:
            if i < len(digits):
                if digits[i] == 9:
                    digits[i] = 0
                else:
                    digits[i] += 1
                    one = 0
            else:
                digits.append(one)
                one = 0
            i += 1
        return digits[::-1]
```

## Complexity

- **Time:** `O(n)`: in the worst case (all 9s) every digit is visited once.
- **Space:** `O(1)` extra, since the input is modified in place. Only the all-9s case allocates a new array of size `n + 1`.

## Other Approaches

- **Convert to int and back:** `int("".join(map(str, digits))) + 1`, then split it back into digits. This works in Python thanks to big integers but misses the point of the problem. Time `O(n)`, Space `O(n)`.

## Key Takeaway

For digit-array arithmetic, walk from the least significant end and carry. Often you can stop as soon as the carry disappears.

## C++

```cpp
/*
    Given large int as an array, add 1 (consider carry)
    Ex. digits = [1,2,3] -> [1,2,4]

    From right to left, keep carrying until digit < 9, add 1

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    vector<int> plusOne(vector<int>& digits) {
        for (int i = digits.size() - 1; i >= 0; i--) {
            if (digits[i] < 9) {
                digits[i]++;
                return digits;
            }
            digits[i] = 0;
        }
        
        digits[0] = 1;
        digits.push_back(0);
        return digits;
    }
};
```
