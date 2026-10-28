---
topic: "C++ Basics"
difficulty: Medium
---
# Hand-Rolled Singly Linked List - Solution

## Intuition

Each node lives in its own heap allocation and knows only its successor. Appending in O(1) needs a `tail` pointer. Reversing is a matter of flipping each `next` to point backwards: hold `prev` (the already-reversed part) and `cur`, save `cur->next` before overwriting it, then step forward. Freeing has the same trap: once a node is deleted you can't read its `next`, so save it first.

## Approach

1. `buildList`: `head = tail = nullptr`; for each value `Node* node = new Node{v, nullptr}`; link it after `tail` (or make it `head`), move `tail`.
2. `reverseList`: `prev = nullptr; while (cur) { next = cur->next; cur->next = prev; prev = cur; cur = next; } return prev;`
3. `freeList`: `while (head) { Node* next = head->next; delete head; head = next; ++count; }`
4. The input array is temporary: `new int[n]`, then `delete[]` once the list is built.

## Code

```cpp
#include <iostream>

struct Node {
    int value;
    Node* next;
};

Node* buildList(const int* values, int n) {
    Node* head = nullptr;
    Node* tail = nullptr;
    for (int i = 0; i < n; ++i) {
        Node* node = new Node{values[i], nullptr};
        if (tail) tail->next = node;
        else head = node;
        tail = node;
    }
    return head;
}

void printList(const Node* head) {
    for (const Node* p = head; p; p = p->next) std::cout << p->value << (p->next ? ' ' : '\n');
}

Node* reverseList(Node* head) {
    Node* prev = nullptr;
    while (head) {
        Node* next = head->next;
        head->next = prev;
        prev = head;
        head = next;
    }
    return prev;
}

int freeList(Node* head) {
    int count = 0;
    while (head) {
        Node* next = head->next;
        delete head;
        head = next;
        ++count;
    }
    return count;
}

int main() {
    int n;
    std::cin >> n;
    int* values = new int[n];
    for (int i = 0; i < n; ++i) std::cin >> values[i];
    Node* head = buildList(values, n);
    delete[] values;

    printList(head);
    head = reverseList(head);
    printList(head);
    std::cout << "freed " << freeList(head) << '\n';
    return 0;
}
```

## Complexity

- Time: O(n) for each operation.
- Space: O(n) nodes; O(1) extra for reversing and freeing.

## Interview follow-ups

- Why must `printList` take `const Node*`, and could it take `const Node* const`?
- Write `reverseList` recursively. What is its stack depth, and why is that a problem for long lists?
- Find the middle node in one pass; detect a cycle (Floyd's fast/slow pointers).
- How would `std::unique_ptr<Node> next` remove the manual `freeList`, and what problem does its recursive destructor cause on a very long list?
- Why are linked lists usually slower than `std::vector` in practice, even for insert-heavy workloads? (Cache misses, one allocation per node.)
