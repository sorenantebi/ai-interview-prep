---
topic: "Trees"
difficulty: Easy
leetcode: https://leetcode.com/problems/maximum-depth-of-binary-tree/
neetcode: https://neetcode.io/problems/depth-of-binary-tree
---
# Maximum Depth of Binary Tree - Solution

**Question:** Maximum Depth of Binary Tree - Question · **Difficulty:** Easy

## Intuition

The depth of a tree is `1 + max(depth(left), depth(right))`. Instead of recursing (which can hit Python's recursion limit on a 10^4-node chain), a level-order BFS counts how many levels exist — that count is the depth.

## Approach

1. If `root` is null, return `0`.
2. Put `root` in a queue and set `depth = 0`.
3. While the queue is non-empty: process exactly the nodes currently in it (one level), enqueue their children, and increment `depth`.
4. Return `depth`.

## Code

```python
# RECURSIVE DFS
class Solution:
    def maxDepth(self, root: TreeNode) -> int:
        if not root:
            return 0

        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))


# ITERATIVE DFS
class Solution:
    def maxDepth(self, root: TreeNode) -> int:
        stack = [[root, 1]]
        res = 0

        while stack:
            node, depth = stack.pop()

            if node:
                res = max(res, depth)
                stack.append([node.left, depth + 1])
                stack.append([node.right, depth + 1])
        return res


# BFS
class Solution:
    def maxDepth(self, root: TreeNode) -> int:
        q = deque()
        if root:
            q.append(root)

        level = 0

        while q:

            for i in range(len(q)):
                node = q.popleft()
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            level += 1
        return level
```

## Complexity

- **Time:** `O(n)` — each node is enqueued and dequeued once.
- **Space:** `O(w)` — the queue holds at most one level (`w` = max width, up to `n/2`).

## Other Approaches

- **Recursive DFS:** `return 1 + max(maxDepth(left), maxDepth(right))` — Time `O(n)`, Space `O(h)` (may overflow Python's default recursion limit on very deep trees).
- **Iterative DFS with `(node, depth)` stack:** track the max depth seen — Time `O(n)`, Space `O(h)`.

## Key Takeaway

"Height/depth" is the canonical post-order recursion; BFS level counting is the iterative alternative that avoids recursion-depth issues.

## C++

```cpp
/*
    Given root of binary tree, return max depth (# nodes along longest path from root to leaf)

    At every node, max depth is the max depth between its left & right children + 1

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
    int maxDepth(TreeNode* root) {
        // return maxDepthRecur(root);          // recursive DFS - preorder - easiest    
        // return maxDepthStkInorder(root);     // iterative DFS - inorder 
        return maxDepthStkPreorder(root);    // iterative DFS - preorder - easier
        // return maxDepthQueueLevelorder(root);   // iterative BFS - levelorder - easy
    }

    int maxDepthQueueLevelorder(TreeNode* root) {
        if (root == NULL) return 0;

        queue<TreeNode*> q;
        int ans = 0, depth = 0;
        q.push(root);

        while (!q.empty()) 
        {            
            int s = q.size();
            for(int i = 0; i < s; i++) 
            {
                root = q.front();
                q.pop();
                
                if (root->left) q.push(root->left);
                if (root->right) q.push(root->right);
            }
            depth += 1;
            ans = max(ans, depth);
        }
        return ans;
    }


    int maxDepthStkPreorder(TreeNode* root) {
        if (root == NULL) return 0;

        stack<pair<TreeNode*, int>> s;
        int ans = 1, depth = 1;
        s.push({root, depth});
        while (!s.empty()) 
        {
            root = s.top().first;
            depth = s.top().second;

            ans = max(ans, depth);
            s.pop();
            if (root->left) s.push({root->left, depth + 1});
            if (root->right) s.push({root->right, depth + 1});
        }
        return ans;
    }

    int maxDepthStkInorder(TreeNode* root) {
        stack<pair<TreeNode*, int>> s;
        int ans = 0, depth = 0;

        while (root || !s.empty())
        {
            while (root != NULL)
            {
                s.push(make_pair(root, ++depth));
                root = root->left;
            }

            root = s.top().first; 
            ans = max(ans, depth);
            
            depth = s.top().second;
            s.pop();
            
            root = root->right;
        }
        return ans;
    }

    int maxDepthRecur(TreeNode* root) {
        // recursive DFS
        if (root == NULL) return 0;

        // we should inc. the depth by 1 here
        // and check for max in left and right subtrees 

        return 1 + max(maxDepthRecur(root->left), maxDepthRecur(root->right));
    }
};
```
