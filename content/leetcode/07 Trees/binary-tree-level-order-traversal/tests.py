import sys
import collections
from typing import List, Optional, Dict


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_list(vals):
    dummy = ListNode()
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_array(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def build_tree(vals):
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    q = collections.deque([root])
    i = 1
    while q and i < len(vals):
        node = q.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            q.append(node.right)
        i += 1
    return root


def tree_to_array(root):
    if not root:
        return []
    out = []
    q = collections.deque([root])
    while q:
        node = q.popleft()
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            q.append(node.left)
            q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict,
      "collections": collections}
exec(open("attempt.py").read(), ns)


def expected_level_order(root):
    res = []
    q = collections.deque([root] if root else [])
    while q:
        level = []
        for _ in range(len(q)):
            n = q.popleft()
            level.append(n.val)
            if n.left:
                q.append(n.left)
            if n.right:
                q.append(n.right)
        res.append(level)
    return res


# Large cases
big_complete = list(range(1, 2001))
big_skew_left = []
# left-skewed chain of 2000 nodes: [v, v, null, v, null, ...]
big_skew_left = [1]
for i in range(2, 2001):
    big_skew_left += [i, None]
big_skew_left = big_skew_left[:1] + [x for x in big_skew_left[1:]]
big_skew_right = [1]
for i in range(2, 2001):
    big_skew_right += [None, i]

cases = [
    ([3, 9, 20, None, None, 15, 7], [[3], [9, 20], [15, 7]]),
    ([1], [[1]]),
    ([], []),
    ([1, 2], [[1], [2]]),
    ([1, None, 2], [[1], [2]]),
    ([1, 2, 3, 4, None, None, 5], [[1], [2, 3], [4, 5]]),
    ([-1, -2, -3, -4, -5], [[-1], [-2, -3], [-4, -5]]),
    ([1, 1, 1, 1, 1, 1, 1], [[1], [1, 1], [1, 1, 1, 1]]),
    ([0, 0, None, 0, None, 0], [[0], [0], [0], [0]]),
    ([1, 2, 3, None, 4, 5, None], [[1], [2, 3], [4, 5]]),
    (big_complete, None),
    (big_skew_left, None),
    (big_skew_right, None),
]

passed = 0
total = len(cases)
for idx, (arr, exp) in enumerate(cases, 1):
    label = arr if len(arr) <= 30 else f"<{len(arr)} elements>"
    try:
        root = build_tree(arr)
        if exp is None:
            exp = expected_level_order(build_tree(arr))
        got = ns["Solution"]().levelOrder(root)
        if got == exp:
            passed += 1
            print(f"PASS case {idx}")
        else:
            es = exp if len(str(exp)) < 300 else f"<{len(exp)} levels>"
            gs = got if len(str(got)) < 300 else f"<{len(got)} levels>"
            print(f"FAIL case {idx}: input={label}, expected={es}, got={gs}")
    except Exception as e:
        print(f"FAIL case {idx}: input={label}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
