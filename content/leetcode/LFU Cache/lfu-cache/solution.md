---
topic: "LFU Cache"
difficulty: Hard
leetcode: https://leetcode.com/problems/lfu-cache/
neetcode: https://neetcode.io/problems/lfu-cache
---
# LFU Cache - Solution

## Intuition

To remove an entry, we need the lowest use count first, then the least recent key within that count. Group keys into buckets by use count. Inside each bucket, keep the keys in recency order. An `OrderedDict` handles this well: it supports O(1) removal of any key, O(1) appends at the end, and O(1) pops from the front (the oldest key).

We also track `min_freq`, the lowest count that currently has any keys, so we know which bucket to remove from without scanning. `min_freq` only changes in two ways:
- When a key moves out of the `min_freq` bucket and that bucket becomes empty, `min_freq` goes up by exactly 1, because the key moved into bucket `min_freq + 1`.
- When a new key is inserted, `min_freq` resets to 1.

## Approach

1. Store `key -> value` and `key -> freq` in two dicts. Store `freq -> OrderedDict` of keys, with the least recent key at the front.
2. **touch(key):** remove the key from its current bucket and add it to the end of bucket `freq + 1`. If the old bucket was the `min_freq` bucket and is now empty, increase `min_freq` by 1.
3. **get:** if the key is missing, return `-1`. Otherwise, call touch and return the value.
4. **put:**
   - If the key exists, update its value and call touch.
   - If the key is new and the cache is full, pop the first key from bucket `min_freq` and delete its records.
   - Insert the new key with count 1 at the end of bucket 1, and set `min_freq = 1`.

## Code

```python
from typing import List, Optional
from collections import defaultdict, OrderedDict

class LFUCache:

	def __init__(self, capacity: int):
		self.cap = capacity
		self.vals = {}
		self.freq = {}
		self.buckets = defaultdict(OrderedDict)  # freq -> keys in LRU order (oldest first)
		self.min_freq = 0

	def _touch(self, key: int) -> None:
		f = self.freq[key]
		del self.buckets[f][key]
		if not self.buckets[f]:
			del self.buckets[f]
			if self.min_freq == f:
				self.min_freq += 1  # key just moved to f + 1, so that's the new minimum
		self.freq[key] = f + 1
		self.buckets[f + 1][key] = None

	def get(self, key: int) -> int:
		if key not in self.vals:
			return -1
		self._touch(key)
		return self.vals[key]

	def put(self, key: int, value: int) -> None:
		if key in self.vals:
			self.vals[key] = value
			self._touch(key)
			return
		if len(self.vals) == self.cap:
			evict, _ = self.buckets[self.min_freq].popitem(last=False)  # LRU within lowest freq
			if not self.buckets[self.min_freq]:
				del self.buckets[self.min_freq]
			del self.vals[evict]
			del self.freq[evict]
		self.vals[key] = value
		self.freq[key] = 1
		self.buckets[1][key] = None
		self.min_freq = 1
```

## Complexity

- **Time:** `O(1)` average per `get` / `put`. Each call does a fixed number of dict and `OrderedDict` operations, and none of them scan the data.
- **Space:** `O(capacity)`. Each stored key appears once in `vals`, once in `freq`, and in exactly one bucket.

## Other Approaches

- **Doubly linked list per frequency (manual):** same idea, but you write the nodes and per-bucket linked lists yourself instead of using `OrderedDict`. This is useful in languages that lack an ordered hash map. — Time `O(1)` / Space `O(capacity)`
- **Min-heap of (freq, last_used_tick, key) with lazy deletion:** push a new tuple on every use and skip outdated tuples when removing an entry. Simpler, but it doesn't meet the O(1) requirement. — Time `O(log n)` amortized / Space `O(n + ops)`
- **Linear scan on eviction:** store the count and last-use time for each key, and scan all keys to find the one to remove. — Time `O(capacity)` per eviction / Space `O(capacity)`
