---
topic: "Linked List"
difficulty: Medium
leetcode: https://leetcode.com/problems/design-circular-queue/
neetcode: https://neetcode.io/problems/design-circular-queue
---
# Design Circular Queue - Solution

## Intuition

Store the elements in a fixed-size array and treat it as a ring. Keep the index of the front element and the current size; the rear index can be derived from them. Moving an index forward with modulo `k` wraps it from the last slot back to the first, so freed slots at the front are reused automatically.

## Approach

1. Allocate an array of length `k`, set `head = 0` and `size = 0`.
2. `enQueue`: if full, return `false`. Otherwise write the value at `(head + size) % k`, increment `size`, return `true`.
3. `deQueue`: if empty, return `false`. Otherwise advance `head = (head + 1) % k`, decrement `size`, return `true`.
4. `Front`: return `-1` if empty, else `data[head]`.
5. `Rear`: return `-1` if empty, else `data[(head + size - 1) % k]`.
6. `isEmpty` is `size == 0`; `isFull` is `size == k`.

Tracking `size` explicitly avoids the classic ambiguity where `head == tail` could mean either empty or full.

## Code

```python
class Node:
    def __init__(self, val: int):
        self.val = val
        self.next = None


class MyCircularQueue:

    def __init__(self, k: int):
        self.head = self.tail = None
        self.capacity = k
        self.size = 0


    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False

        node = Node(value)
        if self.size == 0:
            self.head = self.tail = node
        else:
            self.tail.next = self.tail = node

        self.size += 1

        return True


    def deQueue(self) -> bool:
        if self.isEmpty():
            return False

        self.head = self.head.next
        self.size -= 1

        return True


    def Front(self) -> int:
        return -1 if self.isEmpty() else self.head.val


    def Rear(self) -> int:
        return -1 if self.isEmpty() else self.tail.val


    def isEmpty(self) -> bool:
        return self.size == 0


    def isFull(self) -> bool:
        return self.capacity == self.size
```

## Complexity

- **Time:** `O(1)` — every operation is a constant number of index and array operations.
- **Space:** `O(k)` — a single array of capacity `k`.

## Other Approaches

- **Array with head and tail pointers:** keep two indices and allocate `k + 1` slots (or a flag) to distinguish empty from full — Time `O(1)` per op / Space `O(k)`
- **Singly linked list with head and tail:** allocate nodes on enqueue and track a count to enforce capacity `k` — Time `O(1)` per op / Space `O(k)`
