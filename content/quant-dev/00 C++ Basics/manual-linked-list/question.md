---
topic: "C++ Basics"
difficulty: Medium
---
# Hand-Rolled Singly Linked List

**Topic:** C++ Basics · **Difficulty:** Medium

## Problem

Write a complete program (including `main`) that manages a singly linked list by hand with `new` and `delete`:

```cpp
struct Node {
    int value;
    Node* next;
};

Node* buildList(const int* values, int n);  // appends in order (keep a tail pointer), returns head
void printList(const Node* head);           // values separated by single spaces, then a newline
Node* reverseList(Node* head);              // reverses the links in place, returns the new head
int freeList(Node* head);                   // deletes every node, returns how many were deleted
```

The program reads `n` and then `n` integers. It builds the list, prints it, reverses it, prints it again, frees it and finally prints `freed <count>`.

## Examples

**Example 1**
```text
Input:
4
1 2 3 4
Output:
1 2 3 4
4 3 2 1
freed 4
```

**Example 2**
```text
Input:
1
5
Output:
5
5
freed 1
```

## Constraints

- `1 <= n <= 10^5`
- No `std::list` / `std::forward_list` / `std::vector` for the list itself, and no recursion in `reverseList` (a 10^5-long recursion may overflow the stack).
- Reverse by re-pointing `next` pointers; don't copy values into a new list.
