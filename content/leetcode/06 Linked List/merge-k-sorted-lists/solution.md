---
topic: "Linked List"
difficulty: Hard
leetcode: https://leetcode.com/problems/merge-k-sorted-lists/
neetcode: https://neetcode.io/problems/merge-k-sorted-linked-lists
---
# Merge K Sorted Lists - Solution

**Question:** Merge K Sorted Lists - Question · **Difficulty:** Hard

## Intuition

At every step the next output node is the smallest among the current heads of the `k` lists. A min-heap holding at most one node per list gives that minimum in `O(log k)`. Python's `heapq` cannot compare `ListNode`s, so we push `(val, index, node)` tuples with the list index as a tie-breaker.

## Approach

1. Push `(head.val, i, head)` for each non-empty list into a min-heap.
2. Pop the smallest tuple, append its node to the result tail.
3. If that node has a `next`, push `(next.val, i, next)`.
4. Repeat until the heap is empty; return `dummy.next`.

## Code

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        if not lists or len(lists) == 0:
            return None

        while len(lists) > 1:
            mergedLists = []
            for i in range(0, len(lists), 2):
                l1 = lists[i]
                l2 = lists[i + 1] if (i + 1) < len(lists) else None
                mergedLists.append(self.mergeList(l1, l2))
            lists = mergedLists
        return lists[0]

    def mergeList(self, l1, l2):
        dummy = ListNode()
        tail = dummy

        while l1 and l2:
            if l1.val < l2.val:
                tail.next = l1
                l1 = l1.next
            else:
                tail.next = l2
                l2 = l2.next
            tail = tail.next
        if l1:
            tail.next = l1
        if l2:
            tail.next = l2
        return dummy.next
```

## Complexity

- **Time:** `O(N log k)` — `N` total nodes, each pushed/popped once on a heap of size `<= k`.
- **Space:** `O(k)` — the heap; nodes are re-linked in place.

## Other Approaches

- **Divide and conquer:** merge lists in pairs (like merge sort), halving the count each round — Time `O(N log k)`, Space `O(1)` iterative (`O(log k)` recursive).
- **Merge one by one:** fold `mergeTwoLists` across the array — Time `O(N k)`, Space `O(1)`.
- **Collect all values and sort:** Time `O(N log N)`, Space `O(N)`.

## Key Takeaway

"k-way merge" → min-heap of the k frontier elements. In Python, add a unique tie-breaker to heap tuples when the payload is not comparable.

## C++

```cpp
/*
    Given array of k sorted linked-lists, merge all into 1 sorted list
    Ex. lists = [[1,4,5],[1,3,4],[2,6]] -> [1,1,2,3,4,4,5,6]

    Min heap -> optimize space w/ divide-and-conquer, merge 2 each time

    Time: O(n log k)
    Space: O(n) -> O(1)
*/

/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */

// class Solution {
// public:
//     ListNode* mergeKLists(vector<ListNode*>& lists) {
//         priority_queue<int, vector<int>, greater<int>> pq;
//         for (int i = 0; i < lists.size(); i++) {
//             ListNode* node = lists[i];
//             while (node != NULL) {
//                 pq.push(node->val);
//                 node = node->next;
//             }
//         }
//         if (pq.empty()) {
//             return NULL;
//         }
//         ListNode* node = new ListNode(pq.top());
//         pq.pop();
//         ListNode* head = node;
//         while (!pq.empty()) {
//             node->next = new ListNode(pq.top());
//             pq.pop();
//             node = node->next;
//         }
//         return head;
//     }
// };

class Solution {
public:
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        int n = lists.size();
        if (n == 0) {
            return NULL;
        }
        
        while (n > 1) {
            for (int i = 0; i < n / 2; i++) {
                lists[i] = mergeTwoLists(lists[i], lists[n - i - 1]);
            }
            n = (n + 1) / 2;
        }
        
        return lists.front();
    }
private:
    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
        if (list1 == NULL && list2 == NULL) {
            return NULL;
        }
        if (list1 == NULL) {
            return list2;
        }
        if (list2 == NULL) {
            return list1;
        }
        
        ListNode* head = NULL;
        if (list1->val <= list2->val) {
            head = list1;
            list1 = list1->next;
        } else {
            head = list2;
            list2 = list2->next;
        }
        ListNode* curr = head;
        
        while (list1 != NULL && list2 != NULL) {
            if (list1->val <= list2->val) {
                curr->next = list1;
                list1 = list1->next;
            } else {
                curr->next = list2;
                list2 = list2->next;
            }
            curr = curr->next;
        }
        
        if (list1 == NULL) {
            curr->next = list2;
        } else {
            curr->next = list1;
        }
        
        return head;
    }
};
```
