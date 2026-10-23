---
topic: "Arrays & Hashing"
difficulty: Medium
leetcode: https://leetcode.com/problems/group-anagrams/
neetcode: https://neetcode.io/problems/anagram-groups
---
# Group Anagrams - Solution

**Question:** Group Anagrams - Question · **Difficulty:** Medium

## Intuition

All anagrams share the same letter-frequency signature. If we compute a canonical key for each word (a 26-length count tuple, or the sorted word) and bucket words by that key in a hash map, each bucket is one anagram group.

## Approach

1. Create a `defaultdict(list)` called `groups`.
2. For each word, build a 26-entry count array of its letters and convert it to a tuple (hashable key).
3. Append the word to `groups[key]`.
4. Return the list of bucket values.

## Code

```python
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = {}

        # Iterate over strings
        for s in strs: # O(m)
            count = {}

            # Count frequency of each character
            for char in s: # O(n)
                count[char] = count.get(char, 0) + 1

            # Convert count Dict to List, sort it, and then convert to Tuple (we cannot use dicts or lists as keys in a hashmap)
            tup = tuple(sorted(count.items())) # O(1) because there is limited amount of possible keys in the alphabet -> O(26) + O(26*log26) + O(26)

            if tup in groups:
                groups[tup].append(s)
            else:
                groups[tup] = [s] 
            
        return list(groups.values())
    
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        ans = collections.defaultdict(list)

        for s in strs:
            count = [0] * 26
            for c in s:
                count[ord(c) - ord("a")] += 1
            ans[tuple(count)].append(s)
        return list(ans.values())
```

## Complexity

- **Time:** `O(n · k)` — `n` words of max length `k`, each counted in `O(k)` (plus `O(26)` to build the key).
- **Space:** `O(n · k)` — the map stores every word plus one key per group.

## Other Approaches

- **Sorted-string key:** use `"".join(sorted(word))` as the key — Time `O(n · k log k)`, Space `O(n · k)`.

## Key Takeaway

Grouping by an equivalence relation = hash map from a canonical form to a list; for anagrams the canonical form is the sorted word or its letter-count tuple.
