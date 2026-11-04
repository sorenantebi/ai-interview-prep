---
topic: "Binary Search"
difficulty: Easy
leetcode: https://leetcode.com/problems/guess-number-higher-or-lower/
neetcode: https://neetcode.io/problems/guess-number-higher-or-lower
---
# Guess Number Higher or Lower - Solution

## Intuition

Each call to `guess` tells us which side of the current guess the answer lies on, so we can discard half of the remaining range every time. This is a standard binary search over `[1, n]`, where `guess` plays the role of the comparison.

## Approach

1. Set `lo = 1` and `hi = n`.
2. While `lo <= hi`, take the middle value `mid`.
3. Call `guess(mid)`:
   - `0`: `mid` is the pick, return it.
   - `-1`: the guess is too high, so set `hi = mid - 1`.
   - `1`: the guess is too low, so set `lo = mid + 1`.
4. The pick is guaranteed to be in range, so the loop always returns.

## Code

```python
class Solution:
    def guessNumber(self, n: int) -> int:
        # return a num btw 1,..,n
        
        low = 1
        high = n
        
        while True:
            mid = low + (high - low) // 2
            myGuess = guess(mid)
            if myGuess == 1:
                low = mid + 1
            elif myGuess == -1:
                high = mid - 1
            else:
                return mid
```

## Complexity

- **Time:** `O(log n)` — the search range is halved on every call to `guess`.
- **Space:** `O(1)` — only a few integer variables are used.

## Other Approaches

- **Linear scan:** call `guess` for `1, 2, ..., n` until it returns `0` — Time `O(n)` / Space `O(1)`
- **Ternary search:** split the range into three parts using two guesses per step — Time `O(log n)` (more calls than binary search) / Space `O(1)`

## C++

```cpp
class Solution {
public:
    int guessNumber(int n) {
        int low = 1;
        int high = n;
        
        while(true) {
            int mid = low + (high - low)/2;
            int myGuess = guess(mid);
            if(myGuess == 1)
                low = mid + 1;
            else if(myGuess == -1)
                high = mid - 1;
            else
                return mid;
        }
    }
};
```
