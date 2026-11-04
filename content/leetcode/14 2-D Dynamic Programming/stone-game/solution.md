---
topic: "2-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/stone-game/
neetcode: https://neetcode.io/problems/stone-game
---
# Stone Game - Solution

## Intuition

Define `dp[l][r]` as the maximum lead (current player's stones minus the opponent's) the player to move can achieve on the sub-row `piles[l..r]`. Alice wins if her lead on the full row is positive.

## Approach

1. Let `dp[l][r]` be the best score difference for the player to move on `piles[l..r]`.
2. Base case: `dp[i][i] = piles[i]`.
3. Transition: taking the left pile gives `piles[l] - dp[l+1][r]`, taking the right gives `piles[r] - dp[l][r-1]`. Take the maximum.
4. Fill by increasing interval length.
5. Return `dp[0][n-1] > 0`.

## Code

```python
from typing import List, Optional

class Solution:
    def stoneGame(self, piles: List[int]) -> bool:
        n = len(piles)
        dp = [[0] * n for _ in range(n)]
        for i in range(n):
            dp[i][i] = piles[i]
        for length in range(2, n + 1):
            for l in range(n - length + 1):
                r = l + length - 1
                # the opponent's best lead on the remainder is subtracted
                dp[l][r] = max(piles[l] - dp[l + 1][r], piles[r] - dp[l][r - 1])
        return dp[0][n - 1] > 0
```

## Complexity

- **Time:** `O(n^2)` — each of the `O(n^2)` intervals is computed in constant time.
- **Space:** `O(n^2)` — the DP table.

## Other Approaches

- **Return true:** with an even number of piles and an odd total, Alice can always force a win by choosing all odd-indexed or all even-indexed piles, whichever sums higher — Time `O(1)` / Space `O(1)`
- **1-D DP:** roll the table into a single array indexed by `l` — Time `O(n^2)` / Space `O(n)`
- **Top-down memoization:** recursion on `(l, r)` with caching — Time `O(n^2)` / Space `O(n^2)`

## C++

```cpp
/*
  Alice and Bob play a game with piles of stones. There are an even number of piles arranged 
  in a row, and each pile has a positive integer number of stones piles[i].

  The objective of the game is to end with the most stones. The total number of stones across 
  all the piles is odd, so there are no ties.

  Alice and Bob take turns, with Alice starting first. Each turn, a player takes the entire pile 
  of stones either from the beginning or from the end of the row. This continues until there are 
  no more piles left, at which point the person with the most stones wins.

  Assuming Alice and Bob play optimally, return true if Alice wins the game, or false if Bob wins.
	
  Ex: Input: piles = [5,3,4,5]
  Output: true
  Explanation: 
  Alice starts first, and can only take the first 5 or the last 5.
  Say she takes the first 5, so that the row becomes [3, 4, 5].
  If Bob takes 3, then the board is [4, 5], and Alice takes 5 to win with 10 points.
  If Bob takes the last 5, then the board is [3, 4], and Alice takes 4 to win with 9 points.
  This demonstrated that taking the first 5 was a winning move for Alice, so we return true.

  Space: O(n/2)
  Time : O(1)
*/


class Solution {
public:
    bool stoneGame(vector<int>& piles) {
        int alice = 0, bob = 0, size = piles.size();
        for(int i = 0 ; i < size/2; i++) {
            alice = alice + max( piles[i], piles[size - 1- i] );
            bob = bob + min( piles[i], piles[size - 1- i] );
        }
        if(alice > bob)  
            return true;
        return false;
    }
};
```
