import sys
from typing import List, Optional, Dict
from collections import defaultdict


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


def list_to_array(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


def build_tree(vals):
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    q = [root]
    i = 1
    while q and i < len(vals):
        node = q.pop(0)
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
    q = [root]
    while q:
        node = q.pop(0)
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            q.append(node.left)
            q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional,
      "Dict": Dict, "defaultdict": defaultdict}
exec(open("attempt.py").read(), ns)

# Large inputs
big_judge = 777
big_trust = [[i, big_judge] for i in range(1, 1001) if i != big_judge]
for i in range(1, 1001):
    nxt = i % 1000 + 1
    if i != big_judge and nxt != big_judge:
        big_trust.append([i, nxt])

big_nojudge = [[i, 777] for i in range(1, 1001) if i != 777] + [[777, 1]]

cases = [
    (2, [[1, 2]], 2),
    (3, [[1, 3], [2, 3]], 3),
    (3, [[1, 3], [2, 3], [3, 1]], -1),
    (1, [], 1),
    (2, [], -1),
    (3, [[1, 2], [2, 3]], -1),
    (4, [[1, 3], [1, 4], [2, 3], [3, 4]], -1),
    (4, [[1, 4], [2, 4], [3, 4]], 4),
    (3, [[1, 2], [2, 1]], -1),
    (4, [[2, 1], [3, 1], [4, 1], [2, 3], [3, 4]], 1),
    (3, [[1, 3]], -1),
    (1000, big_judge and big_trust, 777),
    (1000, big_nojudge, -1),
]

passed = 0
total = len(cases)
for idx, (n, trust, expected) in enumerate(cases, 1):
    try:
        sol = ns["Solution"]()
        got = sol.findJudge(n, [list(p) for p in trust])
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            shown = trust if len(trust) < 20 else f"<{len(trust)} pairs>"
            print(f"FAIL case {idx}: input=(n={n}, trust={shown}), expected={expected}, got={got}")
    except Exception as e:
        shown = trust if len(trust) < 20 else f"<{len(trust)} pairs>"
        print(f"FAIL case {idx}: input=(n={n}, trust={shown}), error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
