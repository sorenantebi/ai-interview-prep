---
topic: "Trees"
difficulty: Hard
leetcode: https://leetcode.com/problems/serialize-and-deserialize-binary-tree/
neetcode: https://neetcode.io/problems/serialize-and-deserialize-binary-tree
---
# Serialize And Deserialize Binary Tree - Solution

**Question:** Serialize And Deserialize Binary Tree - Question · **Difficulty:** Hard

## Intuition

A traversal alone is ambiguous, but a traversal that also records **null children** pins down the structure exactly. Level-order (BFS) with `"N"` markers is easy to encode and decode iteratively — each non-null node consumes the next two tokens as its left and right children — and it avoids recursion-depth problems on very deep trees.

## Approach

1. **Serialize:** BFS from the root; append each node's value (or `"N"` for null) and enqueue both children of every non-null node. Join tokens with commas.
2. **Deserialize:** split on commas; if the first token is `"N"`, return null.
3. Create the root from token 0 and put it in a queue; keep an index `i = 1`.
4. For each dequeued node, read token `i` as its left child and `i+1` as its right child (skipping `"N"`), enqueue any created children, and advance `i` by 2.
5. Return the root.

## Code

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None


class Codec:
    def serialize(self, root):
        res = []

        def dfs(node):
            if not node:
                res.append("N")
                return
            res.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(res)

    def deserialize(self, data):
        vals = data.split(",")

        def dfs():
            val = vals.pop(0)
            if val == "N":
                return None
            node = TreeNode(val=int(val))
            node.left = dfs()
            node.right = dfs()
            return node

        return dfs()
```

## Complexity

- **Time:** `O(n)` — each node (and each null child) is emitted and parsed once.
- **Space:** `O(n)` — the output string/token list and the BFS queue.

## Other Approaches

- **Preorder DFS with null markers:** serialize `val, left, right` recursively; deserialize by consuming tokens with an iterator in the same order — Time `O(n)`, Space `O(n)` (recursion depth `O(h)`, so deep trees need a higher recursion limit).
- **Preorder + inorder arrays:** only works with unique values and needs two traversals — Time `O(n)`, Space `O(n)`.

## Key Takeaway

Include null markers and any traversal becomes a lossless encoding; decode by replaying the same traversal order. BFS-based codecs stay iterative and are safe for deep trees.
