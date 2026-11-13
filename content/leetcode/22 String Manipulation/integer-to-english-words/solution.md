---
topic: "String Manipulation"
difficulty: Hard
leetcode: https://leetcode.com/problems/integer-to-english-words/
---
# Integer to English Words - Solution

## Intuition

English reads numbers in groups of three digits, each followed by a scale word (Thousand, Million, Billion). If we can convert any number below 1000 to words, we only need to split `num` into 3-digit chunks and attach the right scale word to each non-zero chunk.

## Approach

1. Handle `num == 0` directly by returning `"Zero"`.
2. Build lookup lists for 1-19, the tens (20, 30, ..., 90), and the scales (`""`, `"Thousand"`, `"Million"`, `"Billion"`).
3. Write a helper that converts a number in `[1, 999]` to words: hundreds digit plus `"Hundred"`, then the remainder, using the 1-19 list if it is below 20, otherwise tens word followed by the ones word.
4. Repeatedly take `num % 1000` as the lowest chunk. If it is non-zero, convert it, append its scale word, and prepend it to the result.
5. Divide `num` by 1000 and advance the scale index until `num` is 0.
6. Join all collected words with single spaces.

## Code

```python
from typing import List, Optional

class Solution:
    def numberToWords(self, num: int) -> str:
        if num == 0:
            return "Zero"

        below_20 = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven",
                    "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen",
                    "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen",
                    "Nineteen"]
        tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty",
                "Seventy", "Eighty", "Ninety"]
        scales = ["", "Thousand", "Million", "Billion"]

        def three_digits(n: int) -> List[str]:
            words = []
            if n >= 100:
                words.append(below_20[n // 100])
                words.append("Hundred")
                n %= 100
            if n >= 20:
                words.append(tens[n // 10])
                n %= 10
            if n > 0:
                words.append(below_20[n])
            return words

        result = []
        scale = 0
        while num > 0:
            chunk = num % 1000
            if chunk:
                # Chunks are produced lowest first, so prepend
                words = three_digits(chunk)
                if scales[scale]:
                    words.append(scales[scale])
                result = words + result
            num //= 1000
            scale += 1

        return " ".join(result)
```

## Complexity

- **Time:** `O(1)` — `num` is at most `2^31 - 1`, so there are at most 4 chunks and each is processed in constant time (in general `O(d)` for `d` digits).
- **Space:** `O(1)` — the lookup tables and the output have bounded size.

## Other Approaches

- **Recursive divide by magnitude:** recursively convert `num` by dividing by 1e9, 1e6, 1e3, 100 and handling the remainder, joining pieces with spaces — Time `O(1)` / Space `O(1)` (recursion depth is bounded)
- **Descending value-word table:** iterate over a list of `(value, word)` pairs from 1e9 down to 1, greedily emitting the quotient's words and the word itself — Time `O(1)` / Space `O(1)`
