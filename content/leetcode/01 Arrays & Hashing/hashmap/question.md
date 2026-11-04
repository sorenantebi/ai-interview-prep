---
video: https://www.youtube.com/watch?v=cNWsgbKwwoU
topic: "Arrays & Hashing"
difficulty: Easy
leetcode: https://leetcode.com/problems/design-hashmap/
neetcode: https://neetcode.io/problems/design-hashmap
---
# Design HashMap

**Topic:** Arrays & Hashing · **Difficulty:** Easy

## Problem

Design a hash map without using any built-in hash table libraries.

Implement the `MyHashMap` class:

- `MyHashMap()` initializes the object with an empty map.
- `void put(int key, int value)` inserts a `(key, value)` pair into the map. If the key already exists, update its value.
- `int get(int key)` returns the value mapped to `key`, or `-1` if the map contains no mapping for the key.
- `void remove(int key)` removes the key and its value if the map contains the mapping for the key.

## Examples

**Example 1**
```text
Input
["MyHashMap", "put", "put", "get", "get", "put", "get", "remove", "get"]
[[], [1, 1], [2, 2], [1], [3], [2, 1], [2], [2], [2]]
Output
[null, null, null, 1, -1, null, 1, null, -1]
```

Explanation:
```text
MyHashMap myHashMap = new MyHashMap();
myHashMap.put(1, 1); // The map is now [[1,1]]
myHashMap.put(2, 2); // The map is now [[1,1], [2,2]]
myHashMap.get(1);    // return 1
myHashMap.get(3);    // return -1 (not found)
myHashMap.put(2, 1); // The map is now [[1,1], [2,1]] (update existing value)
myHashMap.get(2);    // return 1
myHashMap.remove(2); // The map is now [[1,1]]
myHashMap.get(2);    // return -1 (not found)
```

## Constraints

- `0 <= key, value <= 10^6`
- At most `10^4` calls will be made to `put`, `get`, and `remove`.
