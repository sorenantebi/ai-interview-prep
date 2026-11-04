---
topic: "Arrays & Hashing"
difficulty: Hard
leetcode: https://leetcode.com/problems/first-missing-positive/
neetcode: https://neetcode.io/problems/first-missing-positive
---
# First Missing Positive - Solution

## Intuition

For an array of length `n`, the answer must lie in `[1, n + 1]`. If all of `1..n` are present, the answer is `n + 1`; otherwise it is some missing value in `1..n`. So the array itself can serve as a hash set: value `v` belongs at index `v - 1`.

## Approach

1. For each index `i`, while `nums[i]` is in `[1, n]` and is not already at its correct position (`nums[nums[i] - 1] != nums[i]`), swap it into place.
2. Scan the array from left to right; the first index `i` where `nums[i] != i + 1` gives the answer `i + 1`.
3. If every position is correct, return `n + 1`.

## Code

```python
class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        A = nums
        for i in range(len(A)):
            if A[i] < 0:
                A[i] = 0
            
        for i in range(len(A)):
            val = abs(A[i])
            if 1 <= val <= len(A):
                if A[val - 1] > 0:
                    A[val - 1] *= -1
                elif A[val - 1] == 0:
                    A[val - 1] = -1 * (len(A) + 1)
        
        for i in range( 1, len(A)+ 1):
            if A[i -1] >= 0:
                return i
        
        return len(A) + 1
        
    def firstMissingPositive_2(self, nums: List[int]) -> int:
        new = set(nums)
        i = 1
        while i in new:
            i += 1
        return i
```

## Complexity

- **Time:** `O(n)` — each swap places at least one value in its final position, so there are at most `n` swaps in total.
- **Space:** `O(1)` — the array is rearranged in place.

## Other Approaches

- **Hash set:** store all values and test `1, 2, 3, ...` until one is missing — Time `O(n)` / Space `O(n)`
- **Sorting:** sort, then scan for the first gap among positives — Time `O(n log n)` / Space `O(1)` or `O(n)` depending on the sort
- **Sign marking:** replace out-of-range values with `n + 1`, then negate `nums[abs(v) - 1]` to mark presence — Time `O(n)` / Space `O(1)`

## C++

```cpp
class Solution {
public:
    int firstMissingPositive(vector<int>& nums) {
        for(int i=0; i<nums.size(); i++){
            if(i+1==nums[i]) continue;
            int x = nums[i];
            while(x>=1 && x<=nums.size() && x!=nums[x-1]){
                swap(x, nums[x-1]);
            }
        }
        for(int i=0; i<nums.size(); i++){
            if(i+1!=nums[i])    return i+1;
        }
        return nums.size()+1;
    }
};
```
