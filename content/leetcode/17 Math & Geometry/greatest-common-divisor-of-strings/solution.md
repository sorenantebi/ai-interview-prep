---
topic: "Math & Geometry"
difficulty: Easy
leetcode: https://leetcode.com/problems/greatest-common-divisor-of-strings/
neetcode: https://neetcode.io/problems/greatest-common-divisor-of-strings
---
# Greatest Common Divisor of Strings - Solution

## Intuition

If a common divisor string `x` exists, then both strings are built from repeats of `x`, so `str1 + str2` must equal `str2 + str1` (both are just `x` repeated). Conversely, if the two concatenations differ, no common divisor exists. When they match, the answer's length must be the GCD of the two lengths, and the answer is the prefix of that length.

## Approach

1. If `str1 + str2 != str2 + str1`, return `""`.
2. Compute `g = gcd(len(str1), len(str2))`.
3. Return the first `g` characters of `str1`.

## Code

```python
from typing import List, Optional
from math import gcd

class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        # Commutativity of concatenation holds only if both are powers of one string
        if str1 + str2 != str2 + str1:
            return ""
        return str1[:gcd(len(str1), len(str2))]
```

## Complexity

- **Time:** `O(n + m)` — the concatenation comparison scans both strings; the GCD takes `O(log(min(n, m)))`.
- **Space:** `O(n + m)` — the two concatenated strings (plus the output slice).

## Other Approaches

- **Brute force over prefix lengths:** try each prefix length that divides both lengths, from longest to shortest, and check that it repeats to form both strings — Time `O(min(n, m) * (n + m))` / Space `O(min(n, m))`
- **Euclidean algorithm on strings:** if `str1` starts with `str2`, recurse on `(str1[len(str2):], str2)`, swapping as needed, until one is empty — Time `O(n + m)` per step, `O(n + m)` overall amortized by string slicing cost bounds / Space `O(n + m)`

## C++

```cpp
/**
 *  Time Complexity: O(n^2) 
 *  Space Complexity: O(1)
 */

class Solution {
public:
    string gcdOfStrings(string str1, string str2) {
        string shortest, longest;
        
        if(str1.length() < str2.length()){
            shortest = str1;
            longest = str2;
        }
        else{
            shortest = str2;
            longest = str1;
        }

        string solution = "";   
        ushort shortest_length = shortest.length();
        ushort longest_length = longest.length();

        for(ushort i = shortest_length; i > 0; --i)
        {   
            if (longest_length % i != 0 || shortest_length % i != 0) continue;

            for(ushort j = 0; j < longest_length; ++j)
            {
                ushort first_pointer = j % i;
                ushort second_pointer = j % shortest_length;

                if(shortest[first_pointer] != longest[j] || shortest[second_pointer] != longest[j])
                {
                    solution = "";
                    break;
                }

                if(first_pointer == j) solution += longest[j];
            }
            
            if(solution != "") return solution;
        }

        return "";
    }
};
```
