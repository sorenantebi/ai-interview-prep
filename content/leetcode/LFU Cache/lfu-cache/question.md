---
topic: "LFU Cache"
difficulty: Hard
leetcode: https://leetcode.com/problems/lfu-cache/
neetcode: https://neetcode.io/problems/lfu-cache
---
# LFU Cache

**Topic:** LFU Cache · **Difficulty:** Hard

## Problem

Build a cache with a fixed size that removes the **least frequently used** (LFU) entry when it runs out of space. Implement the `LFUCache` class:

- `LFUCache(int capacity)` creates an empty cache that can hold up to `capacity` entries.
- `int get(int key)` returns the value stored for `key`, or `-1` if `key` is not in the cache.
- `void put(int key, int value)` sets the value for `key`. If `key` is already present, its value is replaced. If `key` is new and the cache is full, first remove one entry to free space, then insert the new key.

**Choosing which entry to remove:** pick the key with the smallest use count. If more than one key has that smallest count, remove the one that was used longest ago (the least recently used among them).

**Counting uses:** every key has a use counter. A newly inserted key starts at `1`, since the `put` that inserted it counts as one use. Each `get` or `put` on a key that is already in the cache increases its counter by `1`. When a key is removed, its counter is lost.

Both `get` and `put` must run in **O(1)** average time.

## Examples

**Example 1**
```text
Input:
["LFUCache", "put", "put", "get", "put", "get", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [3], [4, 4], [1], [3], [4]]
Output:
[null, null, null, 1, null, -1, 3, null, -1, 3, 4]

Explanation:
put(1,1), put(2,2)      -> counts: 1→1, 2→1
get(1) = 1              -> counts: 1→2, 2→1
put(3,3)                -> full; key 2 has the lowest count, so it is removed. counts: 1→2, 3→1
get(2) = -1
get(3) = 3              -> counts: 1→2, 3→2
put(4,4)                -> full; keys 1 and 3 are tied at 2, and key 1 was used longest ago, so it is removed
get(1) = -1
get(3) = 3              -> 3→3
get(4) = 4              -> 4→2
```

**Example 2**
```text
Input:
["LFUCache", "put", "get", "put", "get", "get"]
[[1], [1, 10], [1], [2, 20], [1], [2]]
Output:
[null, null, 10, null, -1, 20]

Explanation: The capacity is 1, so inserting key 2 removes key 1, even though key 1 has a higher count.
```

**Example 3**
```text
Input:
["LFUCache", "put", "put", "put", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1, 5], [3, 3], [2], [1], [3]]
Output:
[null, null, null, null, null, -1, 5, 3]

Explanation: put(1,5) changes key 1's value and raises its count to 2. When key 3 is inserted, key 2 (count 1) is removed.
```

## Constraints

- `1 <= capacity <= 10^4`
- `0 <= key <= 10^5`
- `0 <= value <= 10^9`
- At most `2 * 10^5` calls in total are made to `get` and `put`.
