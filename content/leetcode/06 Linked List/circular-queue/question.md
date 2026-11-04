---
video: https://www.youtube.com/watch?v=aBbsfn863oA
topic: "Linked List"
difficulty: Medium
leetcode: https://leetcode.com/problems/design-circular-queue/
neetcode: https://neetcode.io/problems/design-circular-queue
---
# Design Circular Queue

**Topic:** Linked List · **Difficulty:** Medium

## Problem

Design a circular queue, a linear data structure that follows the FIFO (First In First Out) principle and whose last position is connected back to the first, forming a ring. It is also known as a "Ring Buffer".

The advantage of a circular queue is that it reuses freed space at the front. In an ordinary queue, once it fills up no more elements can be inserted even if earlier slots have been vacated; a circular queue can store new values in those slots.

Implement the `MyCircularQueue` class:

- `MyCircularQueue(k)` Initializes the queue with a capacity of `k`.
- `int Front()` Returns the front item of the queue, or `-1` if the queue is empty.
- `int Rear()` Returns the last item of the queue, or `-1` if the queue is empty.
- `boolean enQueue(int value)` Inserts an element into the queue. Returns `true` if the operation succeeds.
- `boolean deQueue()` Deletes an element from the queue. Returns `true` if the operation succeeds.
- `boolean isEmpty()` Returns whether the queue is empty.
- `boolean isFull()` Returns whether the queue is full.

You must solve the problem without using the built-in queue data structure of your programming language.

## Examples

**Example 1**
```text
Input
["MyCircularQueue", "enQueue", "enQueue", "enQueue", "enQueue", "Rear", "isFull", "deQueue", "enQueue", "Rear"]
[[3], [1], [2], [3], [4], [], [], [], [4], []]
Output
[null, true, true, true, false, 3, true, true, true, 4]
```

Explanation:
```text
MyCircularQueue myCircularQueue = new MyCircularQueue(3);
myCircularQueue.enQueue(1); // return True
myCircularQueue.enQueue(2); // return True
myCircularQueue.enQueue(3); // return True
myCircularQueue.enQueue(4); // return False
myCircularQueue.Rear();     // return 3
myCircularQueue.isFull();   // return True
myCircularQueue.deQueue();  // return True
myCircularQueue.enQueue(4); // return True
myCircularQueue.Rear();     // return 4
```

## Constraints

- `1 <= k <= 1000`
- `0 <= value <= 1000`
- At most `3000` calls will be made to `enQueue`, `deQueue`, `Front`, `Rear`, `isEmpty`, and `isFull`.
