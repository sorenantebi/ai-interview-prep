---
topic: "Linked List"
difficulty: Medium
leetcode: https://leetcode.com/problems/copy-list-with-random-pointer/
neetcode: https://neetcode.io/problems/copy-linked-list-with-random-pointer
---
# Copy List With Random Pointer - Solution

**Question:** Copy List With Random Pointer - Question · **Difficulty:** Medium

## Intuition

The difficulty is that a `random` pointer may point to a node whose copy has not been created yet. Splitting the work into two passes solves it: first create a copy of every node and record `original → copy` in a hash map, then wire up `next` and `random` by looking the targets up in the map.

## Approach

1. Initialize `old_to_new = {None: None}` so `null` pointers map to `None` without special cases.
2. Pass 1: for every original node, create `Node(cur.val)` and store it in the map.
3. Pass 2: for every original node, set `copy.next = old_to_new[cur.next]` and `copy.random = old_to_new[cur.random]`.
4. Return `old_to_new[head]`.

## Code

```python
"""
# Definition for a Node.
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random
"""


class Solution:
    def copyRandomList(self, head: "Node") -> "Node":
        oldToCopy = {None: None}

        cur = head
        while cur:
            copy = Node(cur.val)
            oldToCopy[cur] = copy
            cur = cur.next
        cur = head
        while cur:
            copy = oldToCopy[cur]
            copy.next = oldToCopy[cur.next]
            copy.random = oldToCopy[cur.random]
            cur = cur.next
        return oldToCopy[head]
```

## Complexity

- **Time:** `O(n)` — two linear passes with `O(1)` dict operations.
- **Space:** `O(n)` — the hash map (excluding the `n` output nodes themselves).

## Other Approaches

- **Interleaving (O(1) extra space):** insert each copy right after its original (`A → A' → B → B'`), set `A'.random = A.random.next`, then unweave the two lists — Time `O(n)`, Space `O(1)` extra.
- **Recursive DFS with memo:** `clone(node)` creates the copy, memoizes it, then recursively clones `next` and `random` — Time `O(n)`, Space `O(n)` (recursion stack can be deep).

## Key Takeaway

For cloning any pointer-based structure (lists with random pointers, graphs), map original nodes to copies first, then connect edges via the map.

## C++

```cpp
/*
    Given linked list w/ also a random pointer, construct deep copy

    Hash map {old -> new}, O(n) space
    Optimize interweave old and new nodes, O(1) space
    A -> A' -> B -> B' -> C -> C', A'.random = A.random.next

    Time: O(n)
    Space: O(n) -> can optimize to O(1)
*/

/*
// Definition for a Node.
class Node {
public:
    int val;
    Node* next;
    Node* random;
    
    Node(int _val) {
        val = _val;
        next = NULL;
        random = NULL;
    }
};
*/

// class Solution {
// public:
//     Node* copyRandomList(Node* head) {
//         if (head == NULL) {
//             return NULL;
//         }
//         Node* oldNode = head;
//         Node* newNode = new Node(oldNode->val);
//         visited[oldNode] = newNode;
//         while (oldNode != NULL) {
//             newNode->next = getClonedNode(oldNode->next);
//             newNode->random = getClonedNode(oldNode->random);
//             oldNode = oldNode->next;
//             newNode = newNode->next;
//         }
//         return visited[head];
//     }
// private:
//     unordered_map<Node*, Node*> visited;
//     Node* getClonedNode(Node* node) {
//         if (node == NULL) {
//             return NULL;
//         }
//         if (visited.find(node) != visited.end()) {
//             return visited[node];
//         }
//         visited[node] = new Node(node->val);
//         return visited[node];
//     }
// };
/*
class Solution {
public:
    Node* copyRandomList(Node* head) {
        if (head == NULL) {
            return NULL;
        }
        
        Node* ptr = head;
        while (ptr != NULL) {
            Node* newNode = new Node(ptr->val);
            newNode->next = ptr->next;
            ptr->next = newNode;
            ptr = newNode->next;
        }
        ptr = head;
        
        while (ptr != NULL) {
            if (ptr->random == NULL) {
                ptr->next->random == NULL;
            } else {
                ptr->next->random = ptr->random->next;
            }
            ptr = ptr->next->next;
        }
        
        Node* oldPtr = head;
        Node* newPtr = head->next;
        Node* oldHead = head->next;
        
        while (oldPtr != NULL) {
            oldPtr->next = oldPtr->next->next;
            if (newPtr->next == NULL) {
                newPtr->next = NULL;
            } else {
                newPtr->next = newPtr->next->next;
            }
            oldPtr = oldPtr->next;
            newPtr = newPtr->next;
        }
        
        return oldHead;
    }
};
*/

// class Solution {
// public:
//     Node* copyRandomList(Node* head) {
//         unordered_map<Node*, Node*> nodes;
//         Node* h = head;
        
//         while (h){
//             nodes[h] = new Node(h->val);
//             h = h->next;
//         }
//         h = head;
//         while (h){
//             Node* newNode = nodes[h];
//             newNode->next = nodes[h->next];
//             newNode->random = nodes[h->random];
//             h = h->next;
//         }
//         return nodes[head];
//     }
// };

class Solution {
public:
    Node* copyRandomList(Node* head) {
        unordered_map<Node*, Node*> nodes;
        Node* curr = head;
        
        while (curr != NULL) {
            nodes[curr] = new Node(curr->val);
            curr = curr->next;
        }

        curr = head;
        while (curr != NULL) {
            nodes[curr]->next = nodes[curr->next];
            nodes[curr]->random = nodes[curr->random];
            curr = curr->next;
        }
        return nodes[head];
    }   
};
```
