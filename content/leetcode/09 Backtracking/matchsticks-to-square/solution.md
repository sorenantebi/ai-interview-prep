---
topic: "Backtracking"
difficulty: Medium
leetcode: https://leetcode.com/problems/matchsticks-to-square/
neetcode: https://neetcode.io/problems/matchsticks-to-square
---
# Matchsticks to Square - Solution

## Intuition

The total length must be divisible by 4, and each side must equal `total / 4`. The problem is then to partition the sticks into four groups with equal sums. Placing long sticks first makes dead ends show up early, so the search prunes aggressively.

## Approach

1. Compute the sum. If it is not divisible by 4, return `false`. Let `side = sum // 4`.
2. Sort the sticks in descending order. If the longest exceeds `side`, return `false`.
3. Backtrack over sticks by index, trying to add the current stick to each of the four sides, provided the side does not overflow.
4. Skip a side whose current length equals one already tried for this stick (identical state, so it would lead to the same result).
5. If all sticks are placed, every side equals `side`, so return `true`.

## Code

```python
class Solution:
    def makesquare(self, matchsticks: List[int]) -> bool:
        length = sum(matchsticks) // 4
        sides = [0] * 4

        if sum(matchsticks) / 4 != length:
            return False
        matchsticks.sort(reverse=True)

        def backtrack(i):
            if i == len(matchsticks):
                return True

            for j in range(4):
                if sides[j] + matchsticks[i] <= length:
                    sides[j] += matchsticks[i]
                    if backtrack(i + 1):
                        return True
                    sides[j] -= matchsticks[i]
            return False

        return backtrack(0)
```

## Complexity

- **Time:** `O(4^n)` — each of the `n` sticks can go to one of four sides in the worst case; pruning reduces this considerably in practice.
- **Space:** `O(n)` — recursion depth is `n`, plus constant-size state for the sides.

## Other Approaches

- **Bitmask DP:** `dp[mask]` stores the leftover length in the current side after using the sticks in `mask`; a state is valid if some stick can be added without exceeding `side` — Time `O(n * 2^n)` / Space `O(2^n)`

## C++

```cpp
class Solution {
    int a,b,c,d;
    bool fun(vector<int>& matchsticks,int i){
        if(i==matchsticks.size()){
            if(a==0 && b==0 && c==0 && d==0) return true;
            else return false;
        }
        
        if(matchsticks[i]<=a){
            a-=matchsticks[i];
            if(fun(matchsticks,i+1)) return true;
            a+=matchsticks[i];
        }
        
        if(matchsticks[i]<=b){
            b-=matchsticks[i];
            if(fun(matchsticks,i+1)) return true;
            b+=matchsticks[i];
        }
        
        if(matchsticks[i]<=c){
            c-=matchsticks[i];
            if(fun(matchsticks,i+1)) return true;
            c+=matchsticks[i];
        }
        
        if(matchsticks[i]<=d){
            d-=matchsticks[i];
            if(fun(matchsticks,i+1)) return true;
            d+=matchsticks[i];
        }
		
        return false;
    }
public:
    bool makesquare(vector<int>& matchsticks) {
        if(matchsticks.size()<4) return false;
		int sum = accumulate(matchsticks.begin(), matchsticks.end(),0);
        if(sum % 4 != 0) return false;
		int sizeSum=sum/4;
        a=sizeSum,b=sizeSum,c=sizeSum,d=sizeSum;
		sort(matchsticks.rbegin(), matchsticks.rend());
		return fun(matchsticks,0);
    }
};
```
