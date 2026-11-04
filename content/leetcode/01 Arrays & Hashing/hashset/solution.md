---
topic: "Arrays & Hashing"
difficulty: Easy
leetcode: https://leetcode.com/problems/design-hashset/
neetcode: https://neetcode.io/problems/design-hashset
---
# Design HashSet - Solution

## Intuition

Keys are bounded by `10^6`, but only up to `10^4` operations occur, so a full direct-address table is wasteful. A hash table with separate chaining uses space proportional to the number of stored keys: hash each key into a fixed number of buckets, and keep a small list in each bucket to handle collisions.

## Approach

1. Allocate a fixed number of buckets (a prime, such as `1009`), each an empty list.
2. Hash a key with `key % size` to pick its bucket.
3. `add`: if the key is not already in its bucket, append it.
4. `contains`: check whether the key is in its bucket.
5. `remove`: if the key is in its bucket, remove it.

## Code

```python
class MyHashSet:

    def __init__(self):
        self.hashset = []

    def add(self, key: int) -> None:
        if not self.contains(key):
            self.hashset.append(key)

    def remove(self, key: int) -> None:
        if self.contains(key):
            self.hashset.remove(key)

    def contains(self, key: int) -> bool:
        return True if key in self.hashset else False


# Your MyHashSet object will be instantiated and called as such:
# obj = MyHashSet()
# obj.add(key)
# obj.remove(key)
# param_3 = obj.contains(key)
```

## Complexity

- **Time:** `O(n / b)` per operation on average — keys spread across `b` buckets, so each bucket holds about `n / b` keys; with at most `10^4` keys and `1009` buckets this is roughly constant.
- **Space:** `O(n + b)` — `n` stored keys plus `b` bucket lists.

## Other Approaches

- **Boolean array (direct addressing):** a list of `10^6 + 1` booleans indexed by key — Time `O(1)` per operation / Space `O(10^6)`
- **Bitset:** pack membership into bits of an integer array — Time `O(1)` per operation / Space `O(10^6 / 8)` bytes
- **Binary search tree buckets:** use a BST per bucket to avoid long chains — Time `O(log(n / b))` average / Space `O(n + b)`

## C++

```cpp
// Time: O(n)
// Space: O(n)

class MyHashSet {
public:
    void add(int key) {
        if (!contains(key)) {
            hashSet.push_back(key);
        }
    }

    void remove(int key) {
        auto k = find(hashSet.begin(), hashSet.end(), key);
        if (k != hashSet.end()) {
            hashSet.erase(k);
        }
    }

    bool contains(int key) {
        return (find(hashSet.begin(), hashSet.end(), key) != hashSet.end());
    }

private:
    vector<int> hashSet;
};
```
