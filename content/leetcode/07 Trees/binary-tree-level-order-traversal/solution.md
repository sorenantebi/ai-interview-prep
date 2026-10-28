---
topic: "Trees"
difficulty: Medium
leetcode: https://leetcode.com/problems/binary-tree-level-order-traversal/
neetcode: https://neetcode.io/problems/level-order-traversal-of-binary-tree
---
# Binary Tree Level Order Traversal - Solution

**Question:** Binary Tree Level Order Traversal - Question · **Difficulty:** Medium

## Intuition

Breadth-first search naturally visits nodes level by level. If, at the start of each round, we record the queue's current length, exactly that many pops belong to the current level — the children they enqueue form the next level.

## Approach

1. If `root` is null, return `[]`; otherwise start a queue with `root`.
2. While the queue is non-empty, let `size = len(queue)`.
3. Pop `size` nodes, collecting their values into `level` and enqueueing their non-null children.
4. Append `level` to the result.
5. Return the result.

## Code

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None


class Solution:
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        res = []
        q = collections.deque()
        if root:
            q.append(root)

        while q:
            val = []

            for i in range(len(q)):
                node = q.popleft()
                val.append(node.val)
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            res.append(val)
        return res
```

## Complexity

- **Time:** `O(n)` — each node is enqueued and dequeued once.
- **Space:** `O(w)` — the queue holds at most one level (up to `n/2` nodes); output not counted.

## Other Approaches

- **DFS with depth index:** preorder DFS passing `depth`; append `node.val` to `res[depth]` (creating it when `depth == len(res)`) — Time `O(n)`, Space `O(h)`.

## Key Takeaway

The "`for _ in range(len(q))`" BFS loop is the standard way to process a tree (or grid/graph) one level at a time — reused in right side view, zigzag order, minimum depth, and shortest-path problems.

## C++

```cpp
/*
    Given root of binary tree, return level order traversal of its nodes (left to right)
    Ex. root = [3,9,20,null,null,15,7] -> [[3],[9,20],[15,7]]

    Standard BFS traversal, at each level, push left & right nodes if they exist to queue

    Time: O(n)
    Space: O(n)
*/

/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    vector<vector<int>> levelOrder(TreeNode* root) {
        vector<vector<int>> result;
        
        if (root == NULL) {
            return result;
        }
        
        queue<TreeNode*> q;
        q.push(root);
        
        while (!q.empty()) {
            int count = q.size();
            vector<int> curr;
            
            for (int i = 0; i < count; i++) {
                TreeNode* node = q.front();
                q.pop();
                
                curr.push_back(node->val);
                
                if (node->left != NULL) {
                    q.push(node->left);
                }
                if (node->right != NULL) {
                    q.push(node->right);
                }
            }
            
            result.push_back(curr);
        }
        
        return result;
    }
};
```
