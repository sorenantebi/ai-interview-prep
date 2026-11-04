---
video: https://www.youtube.com/watch?v=VymjPQUXjL8
topic: "Arrays & Hashing"
difficulty: Easy
leetcode: https://leetcode.com/problems/design-hashset/
neetcode: https://neetcode.io/problems/design-hashset
---
# Design HashSet

**Topic:** Arrays & Hashing · **Difficulty:** Easy

## Problem

Design a HashSet without using any built-in hash table libraries.

Implement the `MyHashSet` class:

- `void add(key)` inserts the value `key` into the HashSet.
- `bool contains(key)` returns whether the value `key` exists in the HashSet.
- `void remove(key)` removes the value `key` from the HashSet. If `key` does not exist in the HashSet, do nothing.

## Examples

**Example 1**
```text
Input:
["MyHashSet", "add", "add", "contains", "contains", "add", "contains", "remove", "contains"]
[[], [1], [2], [1], [3], [2], [2], [2], [2]]
Output:
[null, null, null, true, false, null, true, null, false]
```

Explanation:
```text
MyHashSet myHashSet = new MyHashSet();
myHashSet.add(1);      // set = [1]
myHashSet.add(2);      // set = [1, 2]
myHashSet.contains(1); // return True
myHashSet.contains(3); // return False, (not found)
myHashSet.add(2);      // set = [1, 2]
myHashSet.contains(2); // return True
myHashSet.remove(2);   // set = [1]
myHashSet.contains(2); // return False, (already removed)
```

## Constraints

- `0 <= key <= 10^6`
- At most `10^4` calls will be made to `add`, `remove`, and `contains`.
