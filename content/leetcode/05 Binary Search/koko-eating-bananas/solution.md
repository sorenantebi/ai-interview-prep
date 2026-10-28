---
topic: "Binary Search"
difficulty: Medium
leetcode: https://leetcode.com/problems/koko-eating-bananas/
neetcode: https://neetcode.io/problems/eating-bananas
---
# Koko Eating Bananas - Solution

**Question:** Koko Eating Bananas - Question · **Difficulty:** Medium

## Intuition

If Koko can finish at speed `k`, she can also finish at any faster speed, so feasibility is monotone in `k`. Binary search the smallest feasible `k` in `[1, max(piles)]`, where checking a speed costs one pass: hours needed = `sum(ceil(p / k))`.

## Approach

1. Search `lo = 1`, `hi = max(piles)` (eating the largest pile in one hour always works since `h >= n`).
2. While `lo < hi`: `mid = (lo + hi) // 2`; compute `hours = sum((p + mid - 1) // mid)`.
3. If `hours <= h`, `mid` works — try slower: `hi = mid`; else `lo = mid + 1`.
4. Return `lo`.

## Code

```python
class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        l, r = 1, max(piles)
        res = r

        while l <= r:
            k = (l + r) // 2

            totalTime = 0
            for p in piles:
                totalTime += math.ceil(float(p) / k)
            if totalTime <= h:
                res = k
                r = k - 1
            else:
                l = k + 1
        return res
```

## Complexity

- **Time:** `O(n log M)` where `M = max(piles)` — `log M` feasibility checks, each `O(n)`.
- **Space:** `O(1)`.

## Other Approaches

- **Linear search on speed:** try `k = 1, 2, …` until feasible — Time `O(n · M)`, Space `O(1)`.

## Key Takeaway

"Minimize a value such that a monotone feasibility check passes" → binary search on the answer space with an O(n) check.

## C++

```cpp
/*
    Given array of banana piles, guards are gone for h hours
    Return min int k such that can eat all banans within h
    Ex. piles = [3,6,7,11] h = 8 -> 4 (1@3, 2@6, 2@7, 3@11)

    Binary search, for each k count hours needed, store min

    Time: O(n x log m) -> n = # of piles, m = max # in a pile
    Space: O(1)
*/

class Solution {
public:
    int minEatingSpeed(vector<int>& piles, int h) {
        int n = piles.size();
        
        int low = 1;
        int high = 0;
        for (int i = 0; i < n; i++) {
            high = max(high, piles[i]);
        }
        
        int result = high;
        
        while (low <= high) {
            int k = low + (high - low) / 2;
            long int hours = 0;
            for (int i = 0; i < n; i++) {
                hours += ceil((double) piles[i] / k);
            }
            if (hours <= h) {
                result = min(result, k);
                high = k - 1;
            } else {
                low = k + 1;
            }
        }
        
        return result;
    }
};
```
