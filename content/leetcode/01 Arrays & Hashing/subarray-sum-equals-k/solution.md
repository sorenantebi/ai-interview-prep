---
topic: "Arrays & Hashing"
difficulty: Medium
leetcode: https://leetcode.com/problems/subarray-sum-equals-k/
neetcode: https://neetcode.io/problems/subarray-sum-equals-k
---
# Subarray Sum Equals K - Solution

## Intuition

The sum of the subarray `nums[i..j]` equals `prefix[j] - prefix[i-1]`. So a subarray ending at `j` has sum `k` exactly when some earlier prefix sum equals `prefix[j] - k`. Counting how often each prefix sum has occurred lets us find all such subarrays in one lookup. Because values can be negative, a sliding window does not work, but a hash map does.

## Approach

1. Keep a running prefix sum `total` and a hash map `seen` counting prefix sums so far, initialized with `{0: 1}` (the empty prefix).
2. For each number, add it to `total`.
3. Add `seen[total - k]` to the answer: each earlier prefix with that value marks the start of a subarray summing to `k`.
4. Increment `seen[total]` and continue.
5. Return the answer.

## Code

```python
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        count = 0
        sum = 0
        dic = {}
        dic[0] = 1
        for i in range(len(nums)):
            sum += nums[i]
            if sum-k in dic:
                count += dic[sum-k]
            dic[sum] = dic.get(sum, 0)+1
        return count

# Time Complexity :
#     O(N) -> Where N is the size of the array and we are iterating over the array once

# Space Complexity:
#     O(N) -> Creating a hashmap/dictionary
```

## Complexity

- **Time:** `O(n)` — one pass with `O(1)` average hash map operations.
- **Space:** `O(n)` — the map may hold up to `n + 1` distinct prefix sums.

## Other Approaches

- **Brute force:** check every start/end pair, with a running sum per start — Time `O(n^2)` / Space `O(1)`
- **Prefix sum array with nested loop:** precompute prefixes and compare all pairs — Time `O(n^2)` / Space `O(n)`

## C++

```cpp
class Solution {
public:
    int subarraySum(vector<int>& nums, int target) {
        int i=0,j=0,count=0,n=size(nums),sum=0;
        unordered_map<int,int>mp;
        while(j<n){
           sum+=nums[j];
           if(sum==target)count++;
           if(mp.find(sum-target)!=mp.end())count+=mp[sum-target];
           mp[sum]++;
           j++;
       } 
       return count;
    }
};
```
